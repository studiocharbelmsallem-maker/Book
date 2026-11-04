"""Six-city pages: films play by themselves, muted, when they come on screen.
Replaces the tap-to-play tile with autoplay plus a Sound on button (same markup as the jewellery pages).
Usage: film_autoplay.py <input index.html> <output index.html>"""
import re,sys
JS="""<script>
document.querySelectorAll('.pair>figure').forEach(function(f){var v=f.querySelector('video');
function open(e){e.preventDefault();e.stopPropagation();document.querySelectorAll('video').forEach(function(o){if(o!==v){o.muted=true;}});
v.muted=false;v.controls=true;v.currentTime=0;var p=v.play();if(p&&p.catch)p.catch(function(){});
if(v.webkitEnterFullscreen&&!v.requestFullscreen){v.webkitEnterFullscreen();}else if(v.requestFullscreen){v.requestFullscreen().catch(function(){if(v.webkitEnterFullscreen)v.webkitEnterFullscreen();});}
cmsEv((v.dataset.city||'Film')+' full screen');}
function close(){v.muted=true;v.controls=false;var p=v.play();if(p&&p.catch)p.catch(function(){});}
v.addEventListener('click',function(e){if(!v.controls)open(e);});f.querySelector('.wch').addEventListener('click',open);
v.addEventListener('webkitendfullscreen',close);document.addEventListener('fullscreenchange',function(){if(!document.fullscreenElement&&v.controls)close();});});
</script>
"""
def fix(s):
    def rep(m):
        t=m.group(0); city=re.search(r'data-ev="(\w+) film"',t).group(1)
        src=re.search(r'src="([^"]+)"',t).group(1); poster=re.search(r'poster="([^"]+)"',t).group(1)
        return (f'<figure><video data-city="{city}" src="{src}" poster="{poster}" muted loop playsinline preload="metadata"></video>'
                f'<button class="wch" type="button">▶ Watch</button></figure>')
    s,n=re.subn(r'<video controls playsinline preload="none"[^>]*></video>',rep,s)
    if n and '.pair>figure' not in s:
        s=s.replace('</style>','.pair:has(>figure){grid-template-columns:0.8fr 0.5625fr;align-items:start}.pair>figure{margin:0}.pair>figure{position:relative}.pair>figure video{aspect-ratio:9/16;width:100%;height:auto;object-fit:cover;background:#1a1815;cursor:pointer}.pair>figure video:fullscreen{object-fit:contain;background:#000}.wch{position:absolute;right:8px;bottom:8px;font-family:Archivo,sans-serif;font-size:9px;letter-spacing:.2em;text-transform:uppercase;color:#EDE9E0;background:rgba(19,17,14,.6);border:1px solid rgba(237,233,224,.55);padding:7px 9px;cursor:pointer}\n</style>',1)
        s=s.replace('else{v.pause();}','else if(!document.fullscreenElement&&!v.webkitDisplayingFullscreen){v.pause();}',1)
        i=s.rindex('<!--cms-bar-->') if '<!--cms-bar-->' in s else s.rindex('</body>')
        s=s[:i]+JS+s[i:]
    return s,n
if __name__=='__main__':
    s,n=fix(open(sys.argv[1],encoding='utf-8').read()); open(sys.argv[2],'w',encoding='utf-8').write(s); print(n)
