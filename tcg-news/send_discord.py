"""Post a markdown briefing to a Discord webhook.

Usage: DISCORD_WEBHOOK_URL=... python3 send_discord.py briefing.md [--dry-run]
"""
import json, os, re, sys, time, urllib.error, urllib.request

LIMIT = 1900  # Discord allows 2000 chars per message
SUPPRESS_EMBEDS = 1 << 2


def to_discord(md):
    out, lines = [], md.splitlines()
    sep = lambda l: bool(re.fullmatch(r"\|?(\s*:?-+:?\s*\|)+\s*:?-*:?\s*", l.strip()))
    for i, line in enumerate(lines):
        s = line.strip()
        if s.startswith("|"):  # Discord can't render tables: turn rows into bullets
            cells = [c.strip() for c in s.strip("|").split("|")]
            if sep(s) or (i + 1 < len(lines) and sep(lines[i + 1])):
                continue  # separator row, or the header row above it
            out.append("• " + " · ".join(c for c in cells if c))
        elif s.startswith("#### "):
            out.append("**" + s[5:] + "**")
        else:
            out.append(line)
    return re.sub(r"\n{3,}", "\n\n", "\n".join(out)).strip()


def chunks(text):
    # Split at section headings first, then pack lines under the limit.
    parts, buf = [], ""
    for line in text.split("\n"):
        while len(line) > LIMIT:
            parts.append(line[:LIMIT]); line = line[LIMIT:]
        starts_section = line.startswith("## ")
        if buf and (len(buf) + len(line) + 1 > LIMIT or (starts_section and len(buf) > LIMIT // 2)):
            parts.append(buf.rstrip()); buf = ""
        buf += line + "\n"
    if buf.strip():
        parts.append(buf.rstrip())
    return parts


def post(url, content):
    body = json.dumps({"content": content, "flags": SUPPRESS_EMBEDS,
                       "allowed_mentions": {"parse": []}}).encode()
    for attempt in range(3):
        req = urllib.request.Request(url, data=body, headers={
            "Content-Type": "application/json", "User-Agent": "tcg-daily-briefing"})
        try:
            urllib.request.urlopen(req, timeout=30)
            return
        except urllib.error.HTTPError as e:
            if e.code == 429 and attempt < 2:
                time.sleep(float(json.loads(e.read() or b"{}").get("retry_after", 2)) + 0.5)
                continue
            raise


def main():
    path, dry = sys.argv[1], "--dry-run" in sys.argv
    parts = chunks(to_discord(open(path, encoding="utf-8").read()))
    if dry:
        for i, p in enumerate(parts, 1):
            print(f"--- message {i}/{len(parts)} ({len(p)} chars) ---\n{p}\n")
        return
    url = os.environ["DISCORD_WEBHOOK_URL"]
    for p in parts:
        post(url, p)
        time.sleep(1)
    print(f"sent {len(parts)} messages")


if __name__ == "__main__":
    main()
