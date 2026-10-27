import re,sys,json,os,urllib.parse,shutil
from PIL import Image
BOOK='/home/claude/book'
src=open(f'{BOOK}/acts/rutana/index.html').read()
ROMAN=['I','II','III']
def build(d):
    H=d['house'];slug=d['slug'];dirn=d['dir']
    s=src
    # head/title
    s=s.replace('Rutana, in three acts',f'{H}, in three acts').replace("Three directions for Rutana's next campaign.",f"Three directions for {H}'s next campaign.")
    s=s.replace('acts/rutana/cover.jpg',f'acts/{dirn}/cover.jpg').replace("'acts-rutana'",f"'acts-{dirn}'")
    s=s.replace('<span class="lab">For Rutana</span>',f'<span class="lab">For {H}</span>')
    s=s.replace('<h1>Rutana,<br>',f'<h1>{H},<br>')
    s=s.replace('<p>Gold that remembers. A jewel that hides. Colour that answers back.</p>',f"<p>{d['line']}</p>")
    s=s.replace('made only for Rutana.</div>',f'made only for {H}.</div>')
    s=s.replace('a1=Rutana+%C2%B7+Concept+call',  'a1='+urllib.parse.quote_plus(f'{H} · Concept call')).replace('utm_campaign=rutanajewelry',f'utm_campaign={slug}')
    s=s.replace('jewellery.html?r=acts-rutanajewelry',f'jewellery.html?r=acts-{slug}')
    s=s.replace('role="img" aria-label="Jewellery campaign in a red box with falling snow, photographed by Charbel Msallem"','role="img" aria-label="Jewellery campaign photographed by Charbel Msallem"')
    parts=s.split('    <div class="act">')
    head=parts[0]; tail=parts[-1][parts[-1].index('  </div>\n</div></section>'):]
    acts=''
    for k,a in enumerate(d['acts']):
        wa='https://wa.me/96191729713?text='+urllib.parse.quote(f"Hello Charbel, {H} here. We choose Act {ROMAN[k]} · {a['title']}.")
        sw=''.join(f'<i style="background:{c}"></i>' for c in a['sw'])
        acts+=f'''    <div class="act">
      <div class="ph" style="background-image:url(act{k+1}.jpg?v=1)"></div>
      <div class="n">Act {ROMAN[k]} · {a['kind']} · {a['for']}</div>
      <h2>{a['title']}</h2>
      <div class="line">{a['line']}</div>
      <div class="concept"><b>The concept.</b> {a['concept']}</div>
      <div class="sw">{sw}</div>
      <a class="btn" data-ev="Act {ROMAN[k]} chosen" href="{wa}" target="_blank" rel="noopener">This one →</a>
    </div>
'''
    s=head+acts+tail
    out=f'{BOOK}/acts/{dirn}'; os.makedirs(out,exist_ok=True)
    open(f'{out}/index.html','w').write(s)
    for name,srcimg in [('cover',d['cover'])]+[(f'act{k+1}',a['img']) for k,a in enumerate(d['acts'])]:
        im=Image.open(srcimg).convert('RGB')
        if im.width>900: im=im.resize((900,round(900*im.height/im.width)),Image.LANCZOS)
        im.save(f'{out}/{name}.jpg',quality=88)
    print('built',out)
if __name__=='__main__':
    build(json.load(open(sys.argv[1])))
