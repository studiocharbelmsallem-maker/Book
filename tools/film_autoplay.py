"""Six-city pages: films play by themselves, muted, when they come on screen.
Replaces the tap-to-play tile with autoplay plus a Sound on button (same markup as the jewellery pages).
Usage: film_autoplay.py <input index.html> <output index.html>"""
import re,sys
def fix(s):
    def rep(m):
        t=m.group(0); city=re.search(r'data-ev="(\w+) film"',t).group(1)
        src=re.search(r'src="([^"]+)"',t).group(1); poster=re.search(r'poster="([^"]+)"',t).group(1)
        return (f'<figure><video data-city="{city}" src="{src}" poster="{poster}" muted loop playsinline preload="metadata"></video>'
                f'<button class="snd" type="button">Sound on</button></figure>')
    s,n=re.subn(r'<video controls playsinline preload="none"[^>]*></video>',rep,s)
    if n and '.pair>figure' not in s:
        s=s.replace('</style>','.pair:has(>figure){grid-template-columns:0.8fr 0.5625fr;align-items:start}.pair>figure{margin:0}.pair>figure video{aspect-ratio:9/16;width:100%;height:auto;object-fit:cover;background:#1a1815;cursor:pointer}\n</style>',1)
    return s,n
if __name__=='__main__':
    s,n=fix(open(sys.argv[1],encoding='utf-8').read()); open(sys.argv[2],'w',encoding='utf-8').write(s); print(n)
