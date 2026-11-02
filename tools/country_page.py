#!/usr/bin/env python3
"""Phase 2 web page: one mood board per country, the country mail's structure.

    python3 tools/country_page.py          -> acts/mood/<country>/index.html (all six)

The house name and tracking arrive in the address:
    /acts/mood/paris/?h=TSKAFF&r=em-tskaff
"This one" opens WhatsApp with the choice typed in. Same page for every house:
only the name changes.
"""
import html, json, pathlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from country_mail import COUNTRIES, ROMAN, WA, V

ROOT = pathlib.Path(__file__).resolve().parent.parent
ORDER = ["beirut", "paris", "milano", "istanbul", "dubai", "barcelona"]
CAL = "https://calendly.com/studiocharbelmsallem/concept-call-10-min"
E = html.escape

CSS = """:root{--bg:#F7F4EC;--ink:#1E1C18;--ink2:#4A4740;--mute:#8A8478;--gold:#9A7B2E;--hair:#E6DCC4}
*{box-sizing:border-box;margin:0;padding:0}html{-webkit-text-size-adjust:100%}
body{background:var(--bg);color:var(--ink);font-family:'EB Garamond',Georgia,'Times New Roman',serif;-webkit-font-smoothing:antialiased}
a{color:inherit;text-decoration:none}
.sheet{max-width:760px;margin:0 auto;background:#fff;min-height:100vh}
.top{padding:20px 32px 14px;border-bottom:1px solid var(--hair);margin:0;font-size:14px;letter-spacing:.24em;text-transform:uppercase}
.top span{font-family:Archivo,Helvetica,Arial,sans-serif;font-size:9px;letter-spacing:.24em;color:var(--gold);white-space:nowrap}
.k{font-family:Archivo,Helvetica,Arial,sans-serif;font-size:10px;letter-spacing:.26em;text-transform:uppercase;color:var(--gold)}
.head{padding:34px 32px 8px}
h1{font-weight:400;font-size:clamp(40px,8vw,56px);line-height:1.04;padding:12px 0 16px}h1 i{color:var(--gold)}
.rule{width:120px;height:1px;background:var(--gold)}
.lead{font-style:italic;font-size:20px;line-height:1.45;color:var(--ink2);padding-top:16px}
.films{padding:28px 32px 6px}.films .row{display:grid;gap:8px;grid-template-columns:repeat(2,1fr);padding-top:14px}.films .row.one{grid-template-columns:minmax(0,340px)}
figure video{display:block;width:100%;aspect-ratio:9/16;background:#000}figcaption{padding-top:9px;font-family:Archivo,Helvetica,Arial,sans-serif;font-size:9px;letter-spacing:.24em;text-transform:uppercase;color:var(--gold)}
.mood{padding:30px 32px 6px}.mh{display:flex;justify-content:space-between;gap:12px;padding-bottom:12px;border-bottom:1px solid var(--hair);margin-bottom:28px}.mh b{font-weight:400;font-family:Archivo,Helvetica,Arial,sans-serif;font-size:9px;letter-spacing:.22em;text-transform:uppercase;color:var(--mute)}
.act{display:grid;grid-template-columns:260px 1fr;gap:26px;padding-bottom:40px}
.act img{display:block;width:100%;height:auto}
.act .k{font-size:9px}h2{font-weight:400;font-size:30px;line-height:1.08;padding:8px 0 4px}
.sub{font-style:italic;font-size:14px;color:var(--mute);padding-bottom:10px}.line{font-style:italic;font-size:18px;line-height:1.42;color:var(--ink2)}
.strip{display:grid;grid-template-columns:repeat(4,1fr);height:6px;margin:14px 0 12px}
.why{font-size:16px;line-height:1.5;color:var(--ink2)}.why span{font-family:Archivo,Helvetica,Arial,sans-serif;font-size:8px;letter-spacing:.24em;text-transform:uppercase;color:var(--gold)}
.btn{display:inline-block;margin-top:16px;padding:14px 34px;border:1px solid var(--gold);font-family:Archivo,Helvetica,Arial,sans-serif;font-size:10px;font-weight:700;letter-spacing:.26em;text-transform:uppercase;text-align:center}
.close{background:var(--bg);padding:32px}.close p{font-size:27px;line-height:1.22;padding-bottom:20px}.close i{color:var(--gold)}
.two{display:grid;grid-template-columns:1fr 1fr;gap:10px}.two .btn{margin:0;padding:14px 8px}.two .fill{background:var(--gold);border-color:var(--gold);color:#fff}
.other{padding:26px 32px;border-top:1px solid var(--hair)}.other div{display:flex;flex-wrap:wrap;gap:8px 18px;padding-top:12px;font-size:18px}.other a{border-bottom:1px solid var(--hair)}
.sig{padding:20px 32px 28px;border-top:1px solid var(--hair);font-size:16px;line-height:1.5}.sig small{display:block;padding-top:8px;font-family:Archivo,Helvetica,Arial,sans-serif;font-size:10px;letter-spacing:.12em;color:var(--mute);line-height:1.6}
@media(max-width:600px){.top,.head,.films,.mood,.other,.sig{padding-left:16px;padding-right:16px}.close{padding:28px 16px}.act{grid-template-columns:1fr;gap:16px}.top span{display:block;padding-top:6px}}
"""


def film(f):
    p, m, label, dur = f
    name = m[6:-4]
    return (f'<figure><video controls playsinline preload="none" poster="../../../films/poster-{name}.jpg?v=2" '
            f'src="../../../{m}" data-ev="{E(label)} film"></video>'
            f'<figcaption>&#9654;&nbsp; {E(label)} · {E(dur)}</figcaption></figure>')


def act(key, c, i, a):
    img, register, name, sub, line, colors, concept = a
    strip = "".join(f'<i style="background:{x}"></i>' for x in colors)
    return f'''<article class="act"><a href="#" data-pick="{ROMAN[i]} · {E(name)}"><img src="../../mail/{key}/{img}?v={V}" alt="{E(register)}, {E(name)}" loading="lazy"></a><div>
<div class="k">{ROMAN[i]} · {E(register)}</div><h2>{E(name)}</h2><div class="sub">{E(sub)}</div><div class="line">{E(line)}</div>
<div class="strip">{strip}</div><div class="why"><span>Why it works</span>&nbsp; {E(concept)}</div>
<a class="btn" href="#" data-pick="{ROMAN[i]} · {E(name)}">This one &rarr;</a></div></article>'''


def page(key):
    c = COUNTRIES[key]
    city = c["city"]
    n = len(c["films"])
    films = ""
    if n:
        films = (f'<section class="films"><div class="k">{"Two films" if n == 2 else "The film"} · {city}</div>'
                 f'<div class="row{" one" if n == 1 else ""}">{"".join(film(f) for f in c["films"])}</div></section>')
    acts = "".join(act(key, c, i, a) for i, a in enumerate(c["acts"]))
    others = "".join(f'<a data-city="{k}" href="../{k}/">{COUNTRIES[k]["city"]}</a>' for k in ORDER if k != key)
    cfg = json.dumps({"city": city, "wa": WA, "cal": CAL})
    return f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="robots" content="noindex,nofollow"><title>{city}, {E(c["tagline"])} · Charbel Msallem</title>
<meta property="og:title" content="{city}, {E(c["tagline"])}"><meta property="og:description" content="{E(c["italic"])}"><meta property="og:image" content="https://studiocharbelmsallem-maker.github.io/Book/acts/mail/{key}/{c["acts"][0][0]}">
<script>
(function(){{var q=new URLSearchParams(location.search),r=(q.get('r')||'').toLowerCase(),internal=false;
try{{if(/^(test|charbel)/.test(r)){{localStorage.setItem('cms-internal','1');}}internal=localStorage.getItem('cms-internal')==='1';}}catch(e){{internal=/^(test|charbel)/.test(r);}}
window.clarity=window.clarity||function(){{(window.clarity.q=window.clarity.q||[]).push(arguments)}};
if(internal)return;var c=document.createElement('script');c.async=1;c.src='https://www.clarity.ms/tag/z0n2deh343';document.head.appendChild(c);}})();
</script>
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=EB+Garamond:ital,wght@0,400;1,400&family=Archivo:wght@400;700&display=swap" rel="stylesheet">
<style>{CSS}</style></head><body><main class="sheet">
<div class="top">Charbel Msallem <span>&nbsp;|&nbsp; Fashion Photographer &amp; Film Director</span></div>
<header class="head"><div class="k"><span data-for>For you</span> · {c["chapter"]} · {city}</div>
<h1>{city},<br><i>{E(c["tagline"])}</i>.</h1><div class="rule"></div><p class="lead">{E(c["italic"])}</p></header>
{films}<section class="mood"><div class="mh"><div class="k">Choose the register</div><b>The mood board</b></div>{acts}</section>
<section class="close"><p><span class="k" style="display:block;padding-bottom:12px">Architect your campaign</span>Pick one. The first frames follow within <i>48 hours</i>, every pixel choreographed, made only for <span data-house>you</span>.</p>
<div class="two"><a class="btn fill" data-cal href="{CAL}">Reserve 10 minutes &rarr;</a><a class="btn" data-home href="https://charbelmsallem.net/">The {city} chapter &rarr;</a></div></section>
<section class="other"><span class="k">Another city</span><div>{others}</div></section>
<footer class="sig"><i>Let's create magic together.</i><br><br>Warm regards,<br>Charbel Msallem · Fashion Photographer &amp; Film Director
<small>CHARBEL MSALLEM STUDIOS · +961 3 729713 · info@charbelmsallem.net · studiocharbelmsallem@gmail.com · @charbelmsallemstudios</small></footer>
</main><script>
(function(){{var C={cfg},q=new URLSearchParams(location.search),h=(q.get('h')||'').slice(0,60),
r=(q.get('r')||'').replace(/[^a-zA-Z0-9_-]/g,'').slice(0,40),keep=(h?'h='+encodeURIComponent(h)+'&':'')+(r?'r='+r:'');
function ev(n){{try{{window.clarity('event',n);}}catch(e){{}}}}
try{{window.clarity('set','ref',r||'direct');window.clarity('set','edition','mood-'+C.city.toLowerCase());if(r){{window.clarity('identify',r);}}}}catch(e){{}}
ev('Mood Open');ev(C.city+' mood');
if(h){{document.querySelector('[data-for]').textContent='For '+h;document.querySelector('[data-house]').textContent=h;document.title=h+', '+document.title;}}
document.querySelectorAll('[data-pick]').forEach(function(a){{var p=a.getAttribute('data-pick'),
t='Hello Charbel, '+(h?h+' here. ':'')+'For '+C.city+' we choose '+p+'.';
a.href='https://wa.me/'+C.wa+'?text='+encodeURIComponent(t);a.target='_blank';a.rel='noopener';
a.addEventListener('click',function(){{ev(C.city+' · '+p+' chosen');}});}});
var cal=document.querySelector('[data-cal]');cal.href=C.cal+'?a1='+encodeURIComponent((h?h+' · ':'')+C.city+' concept call')+'&utm_source=mood&utm_campaign='+(r||'direct');
document.querySelector('[data-home]').href='https://charbelmsallem.net/?r='+(r||'mood-'+C.city.toLowerCase())+'#chapters';
document.querySelectorAll('[data-city]').forEach(function(a){{if(keep)a.href+='?'+keep;}});
document.querySelectorAll('video').forEach(function(v){{v.addEventListener('play',function(){{ev(v.getAttribute('data-ev'));}});}});
}})();
</script></body></html>
'''


if __name__ == "__main__":
    for key in ORDER:
        out = ROOT / "acts" / "mood" / key
        out.mkdir(parents=True, exist_ok=True)
        (out / "index.html").write_text(page(key), encoding="utf-8")
        print(out)
