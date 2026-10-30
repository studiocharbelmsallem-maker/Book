"""Switch the Book from GitHub Pages to charbelmsallem.net. Run from the repo root, only AFTER the DNS points at GitHub.

Steps, in order:
 1. DNS (where charbelmsallem.net is managed; today it points at WordPress.com, 192.0.78.24/25):
      A     @    185.199.108.153 / 185.199.109.153 / 185.199.110.153 / 185.199.111.153
      CNAME www  studiocharbelmsallem-maker.github.io
 2. python tools/move_domain.py        (rewrites every absolute link, writes CNAME)
 3. python tools/seo.py https://charbelmsallem.net/
 4. commit + push, then GitHub > Book > Settings > Pages: confirm the domain, tick "Enforce HTTPS".
 5. Search Console: add charbelmsallem.net, submit https://charbelmsallem.net/sitemap.xml.
Links already sent on github.io/Book/... keep working: GitHub redirects them to the domain.
"""
import os

OLD = "https://studiocharbelmsallem-maker.github.io/Book/"
NEW = "https://charbelmsallem.net/"

n = 0
for dp, dn, fn in os.walk("."):
    if ".git" in dp:
        continue
    for f in fn:
        if not f.endswith((".html", ".xml", ".txt", ".py")) or f == "move_domain.py":
            continue
        p = os.path.join(dp, f)
        s = open(p, encoding="utf-8").read()
        if OLD in s:
            open(p, "w", encoding="utf-8", newline="").write(s.replace(OLD, NEW))
            n += 1
open("CNAME", "w").write("charbelmsallem.net\n")
assert not any(OLD in open(os.path.join(dp, f), encoding="utf-8", errors="ignore").read()
               for dp, _, fn in os.walk(".") if ".git" not in dp
               for f in fn if f.endswith((".html", ".xml", ".txt")))
print(f"rewrote {n} files, CNAME set")
