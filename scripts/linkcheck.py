"""Check every internal href in public/ resolves to a real file."""
import os
import re
import sys
from urllib.parse import urlparse, unquote

ROOT = sys.argv[1] if len(sys.argv) > 1 else "public"

# Derive the site base URL from Hugo config so this check never silently turns
# into a no-op after a domain change. If baseURL is a root domain, BASE_PATH is
# empty; if it is a project sub-path, BASE_PATH holds that prefix.
REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONFIG_PATH = os.path.join(REPO_ROOT, "config", "_default", "hugo.toml")
FALLBACK_BASE = "https://blog.woodsat.com"


def read_base_url(path):
    try:
        with open(path, encoding="utf-8") as fh:
            for line in fh:
                m = re.match(r"""\s*baseURL\s*=\s*["']([^"']+)["']""", line)
                if m:
                    return m.group(1).rstrip("/")
    except OSError:
        pass
    return FALLBACK_BASE


BASE = read_base_url(CONFIG_PATH)
BASE_PATH = urlparse(BASE).path.rstrip("/")

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
            elif BASE_PATH and raw.startswith(BASE_PATH):
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

print("base URL:", BASE)
print("internal links checked:", checked)
print("broken targets:", len(broken))
for t in sorted(broken):
    srcs = sorted(broken[t])
    print("  BROKEN %s   <- %d page(s), e.g. %s" % (t, len(srcs), srcs[0]))
print("external hosts referenced:", ", ".join(sorted(external)) or "(none)")
sys.exit(1 if broken else 0)
