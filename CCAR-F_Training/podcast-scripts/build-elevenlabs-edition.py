"""Build the ElevenLabs edition of the CCAR-F podcast from the reading-edition chapters.

Rewrites technical identifiers, acronyms, symbols and numbers into spoken form, keeps paragraph
breaks as natural pauses (no SSML, so it works on every ElevenLabs model), passes [beat] topic
markers through for the recorder to turn into real silence, keeps ## headings as unspoken
structure lines, and writes:
  elevenlabs/ccar-f-exam-podcast.epub   one book, one Studio chapter per exam domain (h1 headings)
  elevenlabs/chapter-N-*.txt            the same text per chapter, for pasting or TXT import
Refuses to write anything if a technical-looking token survives without a spoken form.
Usage: python build-elevenlabs-edition.py
"""
import html
import pathlib
import re
import sys
import uuid
import zipfile
from datetime import datetime, timezone

HERE = pathlib.Path(__file__).parent
OUT = HERE / "elevenlabs"
CHAPTERS = sorted(HERE.glob("chapter-[1-5]-*.md"))

# Exact spoken forms for identifiers that the generic rules would say badly. Checked first, longest first.
SPOKEN = {
    "CLAUDE.md": "Claude dot M D", "SKILL.md": "skill dot M D", "AGENTS.md": "agents dot M D",
    ".mcp.json": "dot M C P dot Jason", ".claude.json": "dot Claude dot Jason", "settings.json": "settings dot Jason",
    "settings.local.json": "settings dot local dot Jason", ".claude": "dot Claude", "~/.claude": "tilde slash dot Claude",
    "CCAR-F": "C C A R F", "CCA-F": "C C A F", "CI/CD": "C I C D", "JSON-RPC": "Jason R P C", "JSON": "Jason", "json": "Jason",
    "YAML": "yamel", "SQL": "sequel", "OAuth": "oh auth", "GitHub": "GitHub", "GitLab": "GitLab", "Pearson VUE": "Pearson view",
    "stdin": "standard in", "stdout": "standard out", "stderr": "standard error", "claude -p": "claude dash P",
    "-p": "dash P", "@import": "at import", "$ARGUMENTS": "dollar arguments", "I/O": "I O", "A/B": "A B",
    "tool_choice": "tool choice", "stop_reason": "stop reason", "end_turn": "end turn", "tool_use": "tool use",
    "tool_result": "tool result", "max_tokens": "max tokens", "pause_turn": "pause turn", "isError": "is error",
    "PreToolUse": "pre tool use", "PostToolUse": "post tool use", "UserPromptSubmit": "user prompt submit",
    "SubagentStop": "subagent stop", "SessionStart": "session start", "e.g.": "for example", "i.e.": "that is",
    "etc.": "and so on", "vs.": "versus", "vs": "versus",
}
# Acronyms said as a word rather than letter by letter.
SAY_AS_WORD = {"CLAUDE": "Claude", "SKILL": "skill", "AGENTS": "agents", "README": "read me", "TODO": "to do", "JSON": "Jason", "YAML": "yamel", "SQL": "sequel", "NASA": "NASA", "SaaS": "sass", "RAM": "ram", "GIF": "gif", "REST": "rest", "CRUD": "crud", "WASM": "wasm"}
EXT = {"md": "M D", "json": "Jason", "py": "pie", "ts": "T S", "tsx": "T S X", "js": "J S", "jsx": "J S X", "sh": "S H",
       "yml": "yamel", "yaml": "yamel", "tf": "T F", "env": "env", "txt": "text", "csv": "C S V", "toml": "tom-el", "pls": "P L S"}
ONES = "zero one two three four five six seven eight nine ten eleven twelve thirteen fourteen fifteen sixteen seventeen eighteen nineteen".split()
TENS = "_ _ twenty thirty forty fifty sixty seventy eighty ninety".split()


def num_words(n: int) -> str:
    if n < 20:
        return ONES[n]
    if n < 100:
        return TENS[n // 10] + ("" if n % 10 == 0 else "-" + ONES[n % 10])
    if n < 1000:
        rest = n % 100
        return ONES[n // 100] + " hundred" + ("" if rest == 0 else " and " + num_words(rest))
    if n < 1_000_000:
        rest = n % 1000
        return num_words(n // 1000) + " thousand" + ("" if rest == 0 else (" and " if rest < 100 else " ") + num_words(rest))
    return " ".join(ONES[int(d)] for d in str(n))


def letters(tok: str) -> str:
    return " ".join(tok)


def speak_identifier(tok: str) -> str:
    """Generic spoken form for a technical token not in SPOKEN."""
    t = tok
    if t.startswith("_"):
        return "underscore " + speak_identifier(t.lstrip("_"))
    if t.startswith("--"):
        return "dash dash " + speak_identifier(t[2:])
    if t.endswith("()"):
        return speak_identifier(t[:-2])
    if "/" in t or (("." in t) and re.search(r"\.[A-Za-z]{1,5}$", t)):
        parts = re.split(r"(/|\.)", t)
        out = []
        for i, p in enumerate(parts):
            if p == "/":
                out.append("slash")
            elif p == ".":
                out.append("dot")
            elif p == "~":
                out.append("tilde")
            elif p == "**":
                out.append("double star")
            elif p == "*":
                out.append("star")
            elif p:
                is_ext = i == len(parts) - 1 and i > 0 and parts[i - 1] == "."
                out.append(EXT.get(p.lower(), p) if is_ext else speak_identifier(p) if re.search(r"[_A-Z*]", p) else p.replace("-", " "))
        return " ".join(out)
    t = t.replace("*", " star ")
    if re.fullmatch(r"[A-Z][A-Za-z]*[A-Z][A-Za-z]*s?", t) and t.upper() == t.rstrip("s").upper() + ("S" if t.endswith("s") else ""):
        pass
    if re.fullmatch(r"[A-Z]{2,6}s?", t):
        base, plural = (t[:-1], "s") if t.endswith("s") and t[:-1].isupper() else (t, "")
        return SAY_AS_WORD.get(base, letters(base)) + plural
    t = re.sub(r"([a-z0-9])([A-Z])", r"\1 \2", t)          # camelCase -> camel Case
    t = re.sub(r"([A-Z]+)([A-Z][a-z])", r"\1 \2", t)        # HTTPServer -> HTTP Server
    words = [w for w in re.split(r"[_\-\s]+", t) if w]
    out = []
    for w in words:
        if re.fullmatch(r"[A-Z]{2,6}", w):
            out.append(SAY_AS_WORD.get(w, letters(w)))
        elif w.isdigit():
            out.append(num_words(int(w)))
        elif re.fullmatch(r"[A-Za-z]+\d+", w):                # v2 -> v two
            head, digits = re.match(r"([A-Za-z]+)(\d+)", w).groups()
            out.append(head.lower() + " " + num_words(int(digits)))
        else:
            out.append(w.lower() if not w[0].isupper() or len(w) > 1 else w)
    return " ".join(out)


TECH_TOKEN = re.compile(
    r"(?<![\w])(?:--[A-Za-z][\w-]*|[~.@$]?[\w*][\w.*/~\-]*[\w*]\(\)|[~.@$]?[\w*]+(?:[./][\w*\-]+)+|"
    r"_[A-Za-z]\w*|[A-Za-z]+_[\w]+|[a-z]+[A-Z][A-Za-z]+|[A-Z][a-z]+[A-Z][A-Za-z]+|[A-Z]{2,}[a-z]?s?)(?![\w])")


MONTHS = "January February March April May June July August September October November December".split()
ORD = {1: "first", 2: "second", 3: "third", 5: "fifth", 8: "eighth", 9: "ninth", 12: "twelfth", 20: "twentieth", 30: "thirtieth"}


def ordinal(n: int) -> str:
    if n in ORD:
        return ORD[n]
    if n > 20 and n % 10 in ORD:
        return TENS[n // 10] + "-" + ORD[n % 10]
    return num_words(n) + "th"


def dated_identifier(m) -> str:
    """compact_20260112 -> 'compact, version dated January twelfth, twenty twenty-six'"""
    name, y, mo, d = m.group(1), int(m.group(2)), int(m.group(3)), int(m.group(4))
    if not (1 <= mo <= 12 and 1 <= d <= 31):
        return m.group(0)
    year = num_words(y // 100) + " " + (num_words(y % 100) if y % 100 >= 10 else "oh " + num_words(y % 100))
    return f"{speak_identifier(name)}, version dated {MONTHS[mo - 1]} {ordinal(d)}, {year}"


def mixed_alnum(m) -> str:
    """P1 -> 'P one', sha256 -> 'S H A two five six', v2 -> 'v two'."""
    head, digits = m.group(1), m.group(2)
    head_s = letters(head.upper()) if (head.isupper() or len(head) <= 3) and head.lower() not in ("v",) else head
    if head.lower() == "v":
        head_s = "v"
    dig_s = " ".join(ONES[int(d)] for d in digits) if len(digits) >= 3 else num_words(int(digits))
    return head_s + " " + dig_s


def spoken(text: str) -> str:
    text = re.sub(r"\b([A-Za-z][\w-]*?)[_-](20\d{2})(\d{2})(\d{2})\b", dated_identifier, text)
    text = text.replace("`", "")
    # Question IDs help readers cross-reference the trainer but are noise to a listener.
    text = re.sub(r"\b[Pp]ractice question D[1-5]-\d{2,3}\b", "A practice question", text)
    text = re.sub(r"\s*\bD[1-5]-\d{2,3}\b", "", text)
    text = re.sub(r"(?<![\w.])\./", "dot slash ", text)                          # ./CLAUDE.md
    text = re.sub(r"(?<![\w/.])/([a-z][\w-]*)", lambda m: "slash " + m.group(1).replace("-", " "), text)  # /memory
    text = re.sub(r"\$(\d+)\b", lambda m: "dollar " + num_words(int(m.group(1))), text)          # $0, $1
    text = re.sub(r"\$([A-Za-z]\w*)", lambda m: "dollar " + (m.group(1).lower() if m.group(1).isupper() else m.group(1)), text)
    text = re.sub(r"(?<![\w.])@(?=[A-Za-z])", "at ", text)                                  # @docs, @claude
    text = re.sub(r"\.?\{([\w\s,]+)\}", lambda m: (" dot " if m.group(0).startswith(".") else " ") + " or ".join(x.strip() for x in m.group(1).split(",")), text)  # .{ts,tsx}
    text = re.sub(r"\b([A-Za-z]\w*?)=(\w+)", r"\1 equals \2", text)             # continue=True
    text = re.sub(r"\b([A-Za-z]+)_(?!\w)", r"\1 underscore", text)                # async_ , continue_
    text = re.sub(r"\b([A-Za-z]+)\+([A-Za-z]+)\b", r"\1 plus \2", text)           # Shift+Tab
    text = re.sub(r"\b([A-Za-z]{1,4})(\d+)\b", mixed_alnum, text)                 # P1, sha256, v2
    for k in sorted(SPOKEN, key=len, reverse=True):
        text = re.sub(r"(?<![\w.\-/~@$])" + re.escape(k) + r"(?![\w\-])", lambda m, v=SPOKEN[k]: v, text)
    text = re.sub(r"(\d+(?:\.\d+)?)\s?%", lambda m: m.group(1) + " percent", text)
    text = TECH_TOKEN.sub(lambda m: speak_identifier(m.group(0)), text)
    text = re.sub(r"\b(\d+)\.(\d+)\b", lambda m: num_words(int(m.group(1))) + " point " + " ".join(num_words(int(d)) for d in m.group(2)), text)
    text = re.sub(r"\b\d{1,6}\b", lambda m: num_words(int(m.group(0))), text)
    text = re.sub(r"/(?=[\s.,;:!?\"')]|$)", " slash", text)                      # agents/  (trailing folder slash)
    text = re.sub(r"\s?\*+", " star", text)                                       # kubectl*, git diff *
    text = text.replace("&", " and ").replace("→", " to ").replace("~", " tilde ").replace("+", " plus ")
    text = re.sub(r"\(([^()]*)\)", r", \1,", text)          # parentheses read badly: fold into commas
    text = re.sub(r"\s+,", ",", re.sub(r",\s*,", ",", text))
    return re.sub(r"[ \t]{2,}", " ", text).strip()


BEAT = "[beat]"
LEFTOVER = re.compile(r"[_/\\*`#<>{}\[\]|^=@$~]|\d|--|\b[a-z]+[A-Z]\w*|\b[A-Z]{2,}\b")


def parse(md: str):
    title, parts, cur = None, [], None
    for block in re.split(r"\n\s*\n", md.strip()):
        b = block.strip()
        if b.startswith("# "):
            title = b[2:].strip()
        elif b.startswith("## "):
            cur = {"heading": b[3:].strip(), "paras": []}
            parts.append(cur)
        elif b:
            if cur is None:
                cur = {"heading": None, "paras": []}
                parts.append(cur)
            cur["paras"].append(" ".join(line.strip() for line in b.splitlines()))
    return title, parts


def main():
    if len(CHAPTERS) != 5:
        print(f"REFUSED: expected 5 chapter files, found {len(CHAPTERS)}: {[c.name for c in CHAPTERS]}")
        sys.exit(1)
    books, problems = [], []
    for path in CHAPTERS:
        title, parts = parse(path.read_text(encoding="utf-8"))
        s_title = spoken(title or path.stem)
        # [beat] marks a topic change; the recorder turns it into real silence, so it is passed through unspoken.
        s_parts = [{"heading": spoken(p["heading"]) if p["heading"] else None, "raw_heading": p["heading"],
                    "paras": [x if x == BEAT else spoken(x) for x in p["paras"]]} for p in parts]
        for chunk in [s_title] + [p["heading"] or "" for p in s_parts] + [x for p in s_parts for x in p["paras"] if x != BEAT]:
            for m in LEFTOVER.finditer(chunk):
                ctx = chunk[max(0, m.start() - 30): m.end() + 30].replace("\n", " ")
                problems.append(f"{path.name}: unspoken {m.group(0)!r} in ...{ctx}...")
        books.append((path, s_title, s_parts))
    if problems:
        uniq = sorted(set(problems))
        print(f"REFUSED: {len(uniq)} fragments have no spoken form. First 40:\n  " + "\n  ".join(uniq[:40]))
        sys.exit(1)

    OUT.mkdir(exist_ok=True)
    total_chars = 0
    for path, s_title, s_parts in books:
        # Headings are structure, not speech: each section of the spoken edition opens with its own spoken heading.
        # The recorder splits parts on "## Part ..." lines and never reads a "## " line aloud.
        lines = [s_title, ""]
        for p in s_parts:
            if p["raw_heading"]:
                lines += ["## " + p["raw_heading"], ""]
            for para in p["paras"]:
                lines += [para, ""]
        txt = "\n".join(lines).strip() + "\n"
        (OUT / (path.stem + ".txt")).write_text(txt, encoding="utf-8")
        total_chars += len(txt)
        print(f"{path.stem}.txt  {len(txt.split()):,} words  {len(txt):,} characters")

    write_epub(books)
    print(f"ccar-f-exam-podcast.epub  5 chapters  {total_chars:,} characters in total")


def xhtml(title: str, body: str) -> str:
    return ('<?xml version="1.0" encoding="utf-8"?>\n<!DOCTYPE html>\n'
            '<html xmlns="http://www.w3.org/1999/xhtml" xmlns:epub="http://www.idpf.org/2007/ops" lang="en" xml:lang="en">\n'
            f"<head><meta charset=\"utf-8\"/><title>{html.escape(title)}</title></head>\n<body>\n{body}\n</body>\n</html>\n")


def write_epub(books):
    book_title = "CCAR-F Exam Prep Podcast"
    ident = "urn:uuid:" + str(uuid.uuid5(uuid.NAMESPACE_URL, "ccar-f-exam-podcast"))
    modified = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    items, spine, nav = [], [], []
    files = {}
    for i, (path, s_title, s_parts) in enumerate(books, 1):
        body = [f"<h1>{html.escape(s_title)}</h1>"]
        for p in s_parts:
            if p["heading"]:
                body.append(f"<h2>{html.escape(p['heading'])}</h2>")
            body += [f"<p>{html.escape(x)}</p>" for x in p["paras"] if x != BEAT]
        name = f"chapter-{i}.xhtml"
        files["OEBPS/" + name] = xhtml(s_title, "\n".join(body))
        items.append(f'<item id="ch{i}" href="{name}" media-type="application/xhtml+xml"/>')
        spine.append(f'<itemref idref="ch{i}"/>')
        nav.append(f'<li><a href="{name}">{html.escape(s_title)}</a></li>')
    files["OEBPS/nav.xhtml"] = xhtml("Contents", '<nav epub:type="toc" id="toc"><h1>Contents</h1><ol>' + "".join(nav) + "</ol></nav>")
    files["OEBPS/content.opf"] = (
        '<?xml version="1.0" encoding="utf-8"?>\n'
        '<package xmlns="http://www.idpf.org/2007/opf" version="3.0" unique-identifier="bookid">\n'
        '<metadata xmlns:dc="http://purl.org/dc/elements/1.1/">\n'
        f'<dc:identifier id="bookid">{ident}</dc:identifier>\n<dc:title>{book_title}</dc:title>\n'
        '<dc:creator>Matthew Varone</dc:creator>\n<dc:language>en</dc:language>\n'
        f'<meta property="dcterms:modified">{modified}</meta>\n</metadata>\n'
        '<manifest>\n<item id="nav" href="nav.xhtml" media-type="application/xhtml+xml" properties="nav"/>\n'
        + "\n".join(items) + "\n</manifest>\n<spine>\n" + "\n".join(spine) + "\n</spine>\n</package>\n")
    container = ('<?xml version="1.0" encoding="utf-8"?>\n'
                 '<container version="1.0" xmlns="urn:oasis:names:tc:opendocument:xmlns:container">\n'
                 '<rootfiles><rootfile full-path="OEBPS/content.opf" media-type="application/oebps-package+xml"/></rootfiles>\n</container>\n')
    with zipfile.ZipFile(OUT / "ccar-f-exam-podcast.epub", "w") as z:
        z.writestr(zipfile.ZipInfo("mimetype"), "application/epub+zip", compress_type=zipfile.ZIP_STORED)
        z.writestr("META-INF/container.xml", container, compress_type=zipfile.ZIP_DEFLATED)
        for n, content in files.items():
            z.writestr(n, content, compress_type=zipfile.ZIP_DEFLATED)


if __name__ == "__main__":
    main()
