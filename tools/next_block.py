"""The 'Next' section above the six cities: the two soonest dates, on every couture page.
Run once over acts/ to refresh; couture_gen.py calls apply() on new pages."""
import re,sys,glob,html,urllib.parse
CSS='<style id="next-css">.nxf{position:relative;margin:0 0 14px}.nxi{display:block;width:100%;aspect-ratio:4/5;object-fit:cover;object-position:50% 40%}.nxc{position:absolute;right:8px;bottom:6px;font-size:9px;letter-spacing:.02em;color:#fff;opacity:.6}.nxgap{height:56px}</style>'
def cal(H,slug,city):
    n=urllib.parse.quote_plus(f"{H} · {city} shoot")
    return f'https://cal.com/charbelmsallem/concept-call?notes={n}&amp;utm_source=acts&amp;utm_campaign={slug}&amp;utm_content={city.lower()}'
def tile(img,credit,when,city,tag,txt,H,slug):
    c=f'<div class="nxc">{credit}</div>' if credit else ''
    return f'''    <div class="city nx">
      <div class="nxf"><img class="nxi" src="../couture/{img}" alt="">{c}</div>
      <div class="n">{when}</div>
      <h2>{city}</h2>
      <div class="tag">{tag}</div>
      <div class="concept">{txt}</div>
      <a class="btn" data-ev="{city} chosen" href="{cal(H,slug,city)}" target="_blank" rel="noopener">Reserve {city} →</a>
    </div>
'''
def block(H,slug):
    return '  <div class="head" id="next"><span class="lab">Next</span><span class="lab">November · December</span></div>\n  <div class="grid cities">\n'+tile('istanbul-2.jpg?v=1','','Bridal Week · 24–27 November','Izmir','Where it is shot live','I am in Izmir for Bridal Week. A few collections photographed and filmed on site, stills and film delivered as one.',H,slug)+tile('egypt.jpg?v=2','Photo: Richard Mortel, CC BY 2.0, adapted','Two days · 9–10 December','Egypt','Where it is remembered','The Grand Egyptian Museum and Abdeen Palace. A few collections photographed and filmed in rooms that have outlived every season.',H,slug)+'  </div>\n  <div class="nxgap"></div>\n'
def apply(s,H,slug):
    if 'id="next"' in s: return s
    a=s.find('    <div class="city izmir">')
    if a>=0:
        e=s.index('  </div>\n</div></section>',a); s=s[:a]+s[e:]
    h='  <div class="head"><span class="lab">Choose the city</span>'
    if h not in s: raise SystemExit('no anchor in '+slug)
    return s.replace(h,block(H,slug)+h,1).replace('</head>',CSS+'</head>',1)
if __name__=='__main__':
    n=0
    for f in sorted(glob.glob('acts/*/index.html')):
        s=open(f,encoding='utf-8').read()
        if '<div class="grid cities">' not in s: continue
        slug=f.split('/')[1]
        m=re.search(r'<title>(.*?), in six cities',s)
        H='Six cities' if slug=='six-cities' else html.unescape(m.group(1))
        t=apply(s,H,slug)
        if t!=s: open(f,'w',encoding='utf-8').write(t); n+=1
    print(n,'pages')
