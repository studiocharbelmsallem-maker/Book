import json,sys,urllib.parse,os
CITIES=[
 ("I","Beirut","beirut","November – December","Where the light is learned","Archive rooms, one window, no fill. The city that taught the region scale, and the light every collection is first judged by.","25% center"),
 ("II","Paris","paris","Couture Week · 21–29 January","Where it is judged","Haussmann interiors, a courtyard show, an editor with forty collections open on her desk. Shot to survive her.","center 30%"),
 ("III","Milano","milano","23 February – 1 March","Where it is sold","Palazzo windows and frescoed rooms. Imagery that holds on a linesheet, in a showroom and above a runway, without a reshoot.","center"),
 ("IV","Istanbul","istanbul","12–19 January","Where it crosses","Ottoman staircases and Byzantine stone. A collection directed to read in two markets at once, from Riyadh to Milan.","center"),
 ("V","Dubai","dubai","March","Where it is wanted","Open desert, open water, no wall to bounce the light. Crystal and tulle read by the sun alone.","center"),
 ("VI","Barcelona","barcelona","14–18 April","Where it breathes","Modernist stone at Mediterranean noon, Gothic shadow at night. Couture with air around it.","center 30%"),
]
def page(d):
    H=d['house']; slug=d['slug']
    tiles=''
    for n,city,img,date,tag,txt,pos in CITIES:
        wa='https://wa.me/96191729713?text='+urllib.parse.quote(f"Hello Charbel, {H} here. We choose {city} · {date}.")
        tiles+=f'''    <div class="city">
      <div class="ph" style="background-image:url(../couture/{img}.jpg);background-position:{pos}"></div>
      <div class="n">{n} · {date}</div>
      <h2>{city}</h2>
      <div class="tag">{tag}</div>
      <div class="concept">{txt}</div>
      <a class="btn" data-ev="{city} chosen" href="{wa}" target="_blank" rel="noopener">This city →</a>
    </div>
'''
    cal='https://calendly.com/studiocharbelmsallem/concept-call-10-min?a1='+urllib.parse.quote_plus(f"{H} · Concept call")+f'&amp;utm_source=acts&amp;utm_campaign={slug}&amp;utm_content=page'
    t=open(os.path.join(os.path.dirname(__file__),'couture_tpl.html')).read()
    for k,v in {'{{HOUSE}}':H,'{{SLUG}}':slug,'{{LINE}}':d['line'],'{{TILES}}':tiles,'{{CAL}}':cal}.items(): t=t.replace(k,v)
    return t
if __name__=='__main__':
    d=json.loads(sys.argv[1]); out=sys.argv[2]
    os.makedirs(out,exist_ok=True); open(os.path.join(out,'index.html'),'w').write(page(d)); print('ok',out)
