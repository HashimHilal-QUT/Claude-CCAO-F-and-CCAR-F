"""Generate podcast audio for one chapter with ElevenLabs, one MP3 per part.

Resumable: each request's text is hashed, and a chunk whose file already exists is never paid for twice.
Stops cleanly at the monthly character cap instead of retrying into it.

Usage (run with the ElevenLabs connector's Python, which already has the SDK):
    python generate-audio.py 4 --dry-run     # plan and cost, no API calls
    python generate-audio.py 4               # generate chapter 4
"""
import argparse
import hashlib
import json
import os
import pathlib
import re
import subprocess
import sys
import time

HERE = pathlib.Path(__file__).parent
SRC_DIR = HERE / "elevenlabs"
OUT_DIR = HERE / "audio"

VOICE_ID = "Cz0K1kOv9tD8l0b5Qu53"  # Jon - Relaxed, Deep and Approachable
MODEL_ID = "eleven_multilingual_v2"  # Jon is fine-tuned for this model; 10,000 chars per request
OUTPUT_FORMAT = "mp3_44100_128"      # highest the Starter plan allows; smaller copies can be derived later
TARGET_CHARS = 5000                  # soft size of one request
HARD_CHARS = 9500                    # never send more than this in one request
CONTEXT_CHARS = 400                  # neighbouring text sent for smooth joins, not billed
PART_RE = re.compile(r"^Part [a-z\- ]+:", re.IGNORECASE)           # legacy edition
PART_HEADING_RE = re.compile(r"^## Part [a-z\- ]+:", re.IGNORECASE)  # spoken edition
BEAT_SECONDS = 1.3                   # silence at every [beat] topic change
RETRYABLE = {429, 500, 502, 503, 504}


def api_key():
    key = os.environ.get("ELEVENLABS_API_KEY")
    if key:
        return key
    # Fall back to the connector's own entry, so the key lives in one place only.
    cfg = json.loads((pathlib.Path.home() / ".claude.json").read_text(encoding="utf-8"))
    return cfg["mcpServers"]["elevenlabs"]["env"]["ELEVENLABS_API_KEY"]


def split_parts(text):
    lines = text.splitlines()
    if not any(PART_HEADING_RE.match(l) for l in lines):     # legacy edition: spoken "Part one:" lines, no ## markers
        parts, title, buf = [], "Introduction", []
        for line in lines:
            if PART_RE.match(line) and buf:
                parts.append((title, "\n".join(buf).strip()))
                title, buf = line.rstrip("."), []
            buf.append(line)
        parts.append((title, "\n".join(buf).strip()))
        return parts
    # Spoken edition: "## Part ..." starts a part; every "## " line is structure and is never read aloud.
    parts, title, buf = [], "Introduction", []
    for line in lines:
        if PART_HEADING_RE.match(line) and any(l.strip() for l in buf):
            parts.append((title, "\n".join(buf).strip()))
            title, buf = line[3:].strip(), []
            continue
        if line.startswith("## "):
            if PART_HEADING_RE.match(line):
                title = line[3:].strip()
            continue
        buf.append(line)
    parts.append((title, "\n".join(buf).strip()))
    return parts


def split_segments(part_text):
    """Topics separated by [beat] lines. Each topic is recorded on its own and followed by real silence."""
    segs = re.split(r"^\s*\[beat\]\s*$", part_text, flags=re.M)
    return [split_chunks(s) for s in segs if s.strip()]


def split_chunks(part_text):
    paras = [p.strip() for p in re.split(r"\n\s*\n", part_text) if p.strip()]
    pieces = []
    for p in paras:
        if len(p) <= HARD_CHARS:
            pieces.append(p)
            continue
        cur = ""
        for s in re.split(r"(?<=[.!?])\s+", p):
            if cur and len(cur) + len(s) + 1 > TARGET_CHARS:
                pieces.append(cur)
                cur = s
            else:
                cur = f"{cur} {s}".strip()
        pieces.append(cur)
    chunks, cur = [], ""
    for p in pieces:
        if cur and len(cur) + len(p) + 2 > TARGET_CHARS:
            chunks.append(cur)
            cur = p
        else:
            cur = f"{cur}\n\n{p}".strip()
    if cur:
        chunks.append(cur)
    return chunks


def slug(s, n=40):
    return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")[:n].rstrip("-")


def plan(chapter):
    src = next(SRC_DIR.glob(f"chapter-{chapter}-*.txt"))
    out = OUT_DIR / src.stem
    items = []
    for i, (title, body) in enumerate(split_parts(src.read_text(encoding="utf-8"))):
        flat = []                                    # (text, beat_after)
        for seg in split_segments(body):
            flat += [(c, k == len(seg) - 1) for k, c in enumerate(seg)]
        part_file = out / f"part-{i:02d}-{slug(title)}.mp3"
        entries = []
        for j, (c, beat_after) in enumerate(flat):
            h = hashlib.sha256(f"{VOICE_ID}|{MODEL_ID}|{OUTPUT_FORMAT}|{c}".encode()).hexdigest()[:12]
            entries.append({"text": c, "file": out / "chunks" / f"p{i:02d}-c{j:02d}-{h}.mp3",
                            "beat_after": beat_after and j + 1 < len(flat),
                            "prev": flat[j - 1][0][-CONTEXT_CHARS:] if j else None,
                            "next": flat[j + 1][0][:CONTEXT_CHARS] if j + 1 < len(flat) else None})
        items.append({"index": i, "title": title, "file": part_file, "chunks": entries})
    return src, out, items


def join(part):
    # Re-encode through ffmpeg's concat filter: real silence at every [beat], and clean joins with no
    # timestamp overlaps (the old byte-copy join produced non-monotonic timestamps at each seam).
    inputs, chain = [], []
    for c in part["chunks"]:
        inputs += ["-i", str(c["file"])]
        chain.append(f"[{len(chain)}:a]")
        if c["beat_after"]:
            inputs += ["-f", "lavfi", "-t", str(BEAT_SECONDS), "-i", "anullsrc=r=44100:cl=mono"]
            chain.append(f"[{len(chain)}:a]")
    tmp = part["file"].with_suffix(".tmp.mp3")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", *inputs,
                    "-filter_complex", "".join(chain) + f"concat=n={len(chain)}:v=0:a=1[a]", "-map", "[a]",
                    "-c:a", "libmp3lame", "-b:a", "128k", "-ar", "44100", "-ac", "1", str(tmp)], check=True)
    tmp.replace(part["file"])  # a part file only ever appears whole, so the page build never copies half of one


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("chapter", type=int, choices=range(1, 6))
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--allow-partial", action="store_true",
                    help="start even if the allowance may run out mid-chapter; the plan's hard cap stops it and a rerun resumes")
    args = ap.parse_args()

    src, out, items = plan(args.chapter)
    pending = [c for p in items for c in p["chunks"] if not c["file"].exists()]
    need = sum(len(c["text"]) for c in pending)
    total = sum(len(c["text"]) for p in items for c in p["chunks"])
    print(f"{src.name}: {len(items)} parts, {sum(len(p['chunks']) for p in items)} requests, "
          f"{total:,} chars; still to generate {len(pending)} requests, {need:,} chars")
    for p in items:
        print(f"  {p['file'].name:<60} {len(p['chunks'])} req  {sum(len(c['text']) for c in p['chunks']):>6,} chars")
    if args.dry_run or not pending:
        return

    os.environ.setdefault("SSL_CERT_FILE", str(pathlib.Path.home() / ".certs" / "ca-bundle-with-zscaler.pem"))
    from elevenlabs.client import ElevenLabs
    from elevenlabs.core.api_error import ApiError

    client = ElevenLabs(api_key=api_key())
    sub = client.user.subscription.get()
    left = sub.character_limit - sub.character_count
    print(f"allowance: {sub.character_count:,} of {sub.character_limit:,} used, {left:,} left")
    if need > left and not args.allow_partial:
        sys.exit(f"STOP: needs {need:,} chars but only {left:,} left this month. Nothing generated.")
    if left <= 0:
        sys.exit("STOP: no allowance left this month. Nothing generated.")

    (out / "chunks").mkdir(parents=True, exist_ok=True)
    for p in items:
        for c in p["chunks"]:
            if c["file"].exists():
                continue
            for attempt in range(4):
                try:
                    audio = client.text_to_speech.convert(
                        voice_id=VOICE_ID, model_id=MODEL_ID, output_format=OUTPUT_FORMAT, text=c["text"],
                        previous_text=c["prev"], next_text=c["next"])
                    tmp = c["file"].with_suffix(".partial")
                    with open(tmp, "wb") as f:
                        for b in audio:
                            f.write(b)
                    tmp.replace(c["file"])  # only a complete download counts as done
                    print(f"  done {c['file'].name} ({len(c['text']):,} chars)")
                    break
                except ApiError as e:
                    if e.status_code in RETRYABLE and attempt < 3:
                        time.sleep((5, 20, 60)[attempt])
                        continue
                    sys.exit(f"STOP on {c['file'].name}: HTTP {e.status_code} {e.body}. "
                             "Finished chunks are kept; rerun to resume.")
        join(p)
        print(f"PART {p['file'].name}")
    print("chapter complete")


if __name__ == "__main__":
    main()
