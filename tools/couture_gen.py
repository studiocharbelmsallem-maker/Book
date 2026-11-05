import json,sys,urllib.parse,os
CITIES=[
 ("I","Beirut","beirut","November – December","Where the light is learned","Customised to every campaign. Elegance emerges from the machinery; every crystal catches the light of reinvention.","25% center"),
 ("II","Paris","paris","Couture Week · 21–29 January","Where it is judged","A museum, not a studio. Precision in structure, softness in motion.","center 30%"),
 ("III","Milano","milano","23 February – 1 March","Where it is sold","Palazzo windows and frescoed rooms. Imagery that holds on a linesheet, in a showroom and above a runway, without a reshoot.","center"),
 ("IV","Istanbul","istanbul","12–19 January","Where it crosses","Vintage moods, modern lens, eternity in a single frame. Every frame whispers secrets from another time.","center"),
 ("V","Dubai","dubai","March","Where it is wanted","Open desert, open water, no wall to bounce the light. Crystal and tulle read by the sun alone.","center"),
 ("VI","Barcelona","barcelona","14–18 April","Where it breathes","Modernist stone at Mediterranean noon, Gothic shadow at night. Couture with air around it.","center 30%"),
]
BOOK='/home/claude/book'

def _with_bar(s):
    """Every client page carries the sticky WhatsApp / Book a call bar (tools/cms_bar.html)."""
    import os as _o
    b=open(_o.path.join(_o.path.dirname(_o.path.abspath(__file__)),'cms_bar.html'),encoding='utf-8').read().strip()+'\n'
    i=s.rindex('</body>'); return s[:i]+b+s[i:]

FILMS={'beirut':'beirut-couture','istanbul':'istanbul','paris':'paris-couture','milano':'milano','dubai':'dubai-16','barcelona':'barcelona-16'}
def media(img,city):
    f=FILMS[img]
    assert os.path.exists(f'{BOOK}/films/{f}.mp4'),f
    return f'<div class="pair"><img class="ph" src="../couture/{img}.jpg?v=2" alt=""><video controls playsinline preload="none" poster="../../films/poster-{f}.jpg?v=2" src="../../films/{f}.mp4" data-ev="{city} film"></video></div>'
def page(d):
    H=d['house']; slug=d['slug']
    tiles=''
    for n,city,img,date,tag,txt,pos in CITIES:
        wa=f"../mood/{img}/?h={urllib.parse.quote(H)}&amp;r=act-{slug}"
        tiles+=f'''    <div class="city">
      {media(img,city)}
      <div class="n">{n} · {date}</div>
      <h2>{city}</h2>
      <div class="tag">{tag}</div>
      <div class="concept">{txt}</div>
      <a class="btn" data-ev="{city} chosen" href="{wa}">This city →</a>
    </div>
'''
    cal='https://cal.com/charbelmsallem/concept-call?notes='+urllib.parse.quote_plus(f"{H} · Concept call")+f'&amp;utm_source=acts&amp;utm_campaign={slug}&amp;utm_content=page'
    t=open(os.path.join(os.path.dirname(__file__),'couture_tpl.html')).read()
    for k,v in {'{{HOUSE}}':H.replace('&','&amp;'),'{{SLUG}}':slug,'{{LINE}}':d['line'],'{{TILES}}':tiles,'{{CAL}}':cal}.items(): t=t.replace(k,v)
    import next_block
    return next_block.apply(t,H,slug)
if __name__=='__main__':
    d=json.loads(sys.argv[1]); out=sys.argv[2]
    os.makedirs(out,exist_ok=True); open(os.path.join(out,'index.html'),'w').write(__import__('film_autoplay').fix(_with_bar(page(d)))[0]); print('ok',out)
