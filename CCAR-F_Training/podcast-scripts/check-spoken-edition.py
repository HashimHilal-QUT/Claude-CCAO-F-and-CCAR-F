"""Gate the spoken rewrite before any audio is paid for.

For each chapter, compares spoken/chapter-N/*.md (the rewrite, one file per ## section) with the
original chapter-N-*.md section by section, and refuses unless:
  - the sections and their ## headings match the original exactly, in order;
  - every number, quoted phrase and technical identifier in an original section is still in the rewrite;
  - lengths sit in the agreed band, no topic stretch between [beat] markers is too long,
    and no leftover markup (bullets, bold, code fences, tables) remains.
A model saying it kept everything is a claim; this script is the evidence.
Usage: python check-spoken-edition.py [chapter ...]     (default: all five)
"""
import pathlib
import re
import sys

HERE = pathlib.Path(__file__).parent
BAND = (0.95, 1.50)           # agreed 1.05-1.35, with tolerance for short sections
SEG_WARN, SEG_MAX = 2200, 9000


def sections(md):
    out, cur = [], None
    for line in md.splitlines():
        if line.startswith("## "):
            cur = [line.strip(), []]
            out.append(cur)
        elif cur is not None:
            cur[1].append(line)
    return [(h, "\n".join(b).strip()) for h, b in out]


def must_keep(text):
    """Tokens a rewrite may not lose: numbers, quoted phrases, and code-like identifiers."""
    keep = set()
    keep |= set(re.findall(r"\b\d[\d,.]*\b", text))
    keep |= {q.strip().lower() for q in re.findall(r"[\"“]([^\"”\n]{3,80})[\"”]", text)}
    keep |= set(re.findall(r"`([^`\n]+)`", text))
    keep |= set(re.findall(r"(?<![\w-])(?:--?[a-z][\w-]+|[A-Za-z]+_[\w_]+|[a-z]+[A-Z]\w*|[\w.-]+\.(?:md|json|py|sh|yml|yaml|ts|txt)|/[a-z][\w-]+)(?![\w-])", text))
    return {k for k in keep if k.strip(".,")}


CONTRACTIONS = {"what's": "what is", "it's": "it is", "that's": "that is", "there's": "there is", "here's": "here is",
                "let's": "let us", "don't": "do not", "doesn't": "does not", "didn't": "did not", "isn't": "is not",
                "aren't": "are not", "wasn't": "was not", "can't": "cannot", "won't": "will not", "you're": "you are",
                "they're": "they are", "we're": "we are", "i'm": "i am", "i'll": "i will", "you'll": "you will",
                "it'll": "it will", "you've": "you have", "we've": "we have", "shouldn't": "should not", "couldn't": "could not"}


def norm(s):
    """For quoted phrases: case, curly quotes, contractions and punctuation do not count as a change."""
    s = s.lower().replace("’", "'").replace("‘", "'")
    s = re.sub(r"\b(" + "|".join(re.escape(k) for k in CONTRACTIONS) + r")\b", lambda m: CONTRACTIONS[m.group(1)], s)
    return " ".join(re.sub(r"[^\w\s]", " ", s).split())


def present(token, text, low):
    t = token.strip(".,")
    if t.replace(",", "").replace(".", "").isdigit():
        return re.search(r"(?<![\d.,])" + re.escape(t) + r"(?![\d])", text) is not None
    if t.lower() in low:
        return True
    return " " in t and norm(t) in norm(text)     # a quoted phrase, allowing contractions and punctuation


def check(n):
    problems, notes = [], []
    orig_path = next(HERE.glob(f"chapter-{n}-*.md"))
    orig = sections(orig_path.read_text(encoding="utf-8"))
    files = sorted((HERE / "spoken" / f"chapter-{n}").glob("*.md"))
    if len(files) != len(orig):
        return [f"ch{n}: {len(files)} section files, original has {len(orig)} sections"], notes
    total_o = total_n = 0
    for (oh, ob), f in zip(orig, files):
        new = f.read_text(encoding="utf-8").strip()
        first, _, nb = new.partition("\n")
        if first.strip() != oh:
            problems.append(f"ch{n} {f.name}: heading {first.strip()!r} != original {oh!r}")
            continue
        nb = nb.strip()
        low = nb.lower()
        lost = sorted(t for t in must_keep(ob) if not present(t, nb, low))
        if lost:
            problems.append(f"ch{n} {f.name}: {len(lost)} lost: {lost[:12]}")
        ratio = len(nb) / max(1, len(ob))
        total_o += len(ob); total_n += len(nb)
        if not BAND[0] <= ratio <= BAND[1]:
            problems.append(f"ch{n} {f.name}: length ratio {ratio:.2f} outside {BAND}")
        for i, seg in enumerate(re.split(r"^\s*\[beat\]\s*$", nb, flags=re.M)):
            if len(seg) > SEG_MAX:
                problems.append(f"ch{n} {f.name}: topic {i} is {len(seg)} chars (max {SEG_MAX})")
            elif len(seg) > SEG_WARN:
                notes.append(f"ch{n} {f.name}: topic {i} is {len(seg)} chars")
        # Backticked spans are spoken identifiers (glob patterns contain "**"), so they are not markup.
        if re.search(r"^\s*([-*•]|\d+\.)\s|\*\*|^```|^\|", re.sub(r"`[^`\n]+`", "", nb), flags=re.M):
            problems.append(f"ch{n} {f.name}: leftover markup (bullets, bold, code fence or table)")
        if "[beat]" not in nb and len(nb) > 2500:
            problems.append(f"ch{n} {f.name}: no [beat] markers in a {len(nb)}-char section")
    notes.append(f"ch{n}: {len(files)} sections, {total_o:,} -> {total_n:,} chars ({total_n / max(1, total_o):.2f}x)")
    return problems, notes


def main():
    chapters = [int(a) for a in sys.argv[1:]] or [1, 2, 3, 4, 5]
    all_problems = []
    for n in chapters:
        p, notes = check(n)
        all_problems += p
        for x in notes:
            print("  note:", x)
    if all_problems:
        print("REFUSED:\n  " + "\n  ".join(all_problems))
        sys.exit(1)
    print(f"PASS: chapters {chapters}")


if __name__ == "__main__":
    main()
