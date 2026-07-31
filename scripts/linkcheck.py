"""Check every internal href in public/ resolves to a real file."""
import os
import re
import sys
from urllib.parse import urlparse, unquote

ROOT = sys.argv[1] if len(sys.argv) > 1 else "public"
BASE = "https://diecasting.github.io/Woodsat.github.io"
BASE_PATH = "/Woodsat.github.io"

href_re = re.compile(r'href=(?:"([^"]*)"|\'([^\']*)\'|([^\s>]+))')

broken = {}
checked = 0
external = set()

for dirpath, _dirs, files in os.walk(ROOT):
    for fn in files:
        if not fn.endswith(".html"):
            continue
        path = os.path.join(dirpath, fn)
        try:
            html = open(path, encoding="utf-8").read()
        except Exception:
            continue
        for m in href_re.finditer(html):
            raw = m.group(1) or m.group(2) or m.group(3) or ""
            raw = raw.strip()
            if not raw or raw.startswith(("#", "mailto:", "tel:", "javascript:", "data:")):
                continue
            if raw.startswith(BASE):
                target = raw[len(BASE):]
            elif raw.startswith(("http://", "https://")):
                external.add(urlparse(raw).netloc)
                continue
            elif raw.startswith(BASE_PATH):
                target = raw[len(BASE_PATH):]
            elif raw.startswith("/"):
                target = raw
            else:
                continue

            target = unquote(target.split("#")[0].split("?")[0])
            if not target:
                target = "/"
            checked += 1
            rel = target.lstrip("/")
            candidates = [
                os.path.join(ROOT, rel),
                os.path.join(ROOT, rel, "index.html"),
            ]
            if not any(os.path.isfile(c) for c in candidates):
                broken.setdefault(target, set()).add(os.path.relpath(path, ROOT))

print("internal links checked:", checked)
print("broken targets:", len(broken))
for t in sorted(broken):
    srcs = sorted(broken[t])
    print("  BROKEN %s   <- %d page(s), e.g. %s" % (t, len(srcs), srcs[0]))
print("external hosts referenced:", ", ".join(sorted(external)) or "(none)")
sys.exit(1 if broken else 0)
