"""Mail 1, short version: six city tiles (2 x 3), one line and one button each.
Preview only until Charbel approves it. Usage: python3 couture_mail_short.py "House" slug "Greeting" out.html"""
import sys,os,urllib.parse as U,html
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from couture_gen import CITIES
from jewel_mail import B,INK,INK2,MUTE,GOLD,CH,HAIR,G,A,LAB,btn
from couture_mail import M,V,RATIO

def tile(n,city,img,date,tag,house,r):
    wa=f'https://charbelmsallem.net/acts/mood/{img}/?h={U.quote(house)}&amp;r={r}'
    rt=RATIO[img]; bw,bh=260,300
    fw,fh=(bw,round(bw/rt)) if rt>bw/bh else (round(bh*rt),bh)
    return (f'<td width="264" valign="top" style="width:264px;padding-bottom:26px">'
      f'<a href="{wa}"><table role="presentation" width="264" cellpadding="0" cellspacing="0" border="0"><tr>'
      f'<td width="264" height="{bh}" align="center" valign="middle" bgcolor="{CH}" style="background:{CH};width:264px;height:{bh}px">'
      f'<img src="{M}{img}.gif{V}" width="{fw}" height="{fh}" alt="{city}" style="display:block;border:0;width:{fw}px;height:{fh}px;margin:0 auto"></td></tr></table></a>'
      f'<table role="presentation" cellpadding="0" cellspacing="0" border="0" style="margin-top:14px"><tr>'
      f'<td valign="baseline" style="{G}font-style:italic;font-size:18px;color:{GOLD};padding-right:10px">{n}</td>'
      f'<td valign="baseline" style="{G}font-size:24px;line-height:1;color:{INK}">{city}</td></tr></table>'
      f'<div style="{A}font-size:8px;letter-spacing:2px;text-transform:uppercase;color:{MUTE};padding:7px 0 3px">{date}</div>'
      f'<div style="{G}font-style:italic;font-size:15px;color:{INK2};padding-bottom:12px">{tag}</div>'
      f'<table role="presentation" width="150" cellpadding="0" cellspacing="0" border="0"><tr><td>{btn(wa,"This city &rarr;",False)}</td></tr></table>'
      f'</td>')

def mail(house,slug,greet,r=None):
    r=r or 'em-'+slug; H=html.escape(house)
    t=[tile(n,city,img,date,tag,house,r) for n,city,img,date,tag,txt,pos in CITIES]
    rows=''.join(f'<tr>{t[i]}<td width="8" style="font-size:0">&nbsp;</td>{t[i+1]}</tr>' for i in range(0,6,2))
    cal='https://cal.com/charbelmsallem/concept-call?notes='+U.quote_plus(f'{house} · Concept call')+f'&utm_source=mail&utm_campaign={slug}&utm_content=short'
    return f'''<div style="{G}font-size:17px;line-height:1.55;color:{INK}">Dear {html.escape(greet)},<br><br>Six cities where the next {H} collection could be filmed. Tap the one that speaks to you, and the concept follows within the week.<br><br></div>
<table role="presentation" width="600" cellpadding="0" cellspacing="0" border="0" style="width:100%;max-width:600px;border-collapse:collapse;background:#FFFFFF;border:1px solid {HAIR}">
<tr><td style="padding:22px 32px 0">
 <table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0" style="border-bottom:1px solid {HAIR}"><tr><td style="padding-bottom:14px;{G}font-size:14px;letter-spacing:3.4px;text-transform:uppercase;color:{INK}"><span style="{G}font-size:14px;letter-spacing:3.4px;text-transform:uppercase;color:{INK}">Charbel Msallem</span><span style="color:{GOLD}">&nbsp;&nbsp;|&nbsp;&nbsp;</span><span style="{A}font-size:9px;letter-spacing:2.2px;color:{GOLD}">Fashion photographer &amp; film director</span></td></tr></table>
</td></tr>
<tr><td style="padding:28px 32px 4px">
 <div style="{LAB}">For {H} · the season 2027</div>
 <div style="{G}font-size:40px;line-height:1.04;color:{INK};padding:12px 0 14px">{H},<br>in <i style="color:{GOLD}">six</i> cities.</div>
 <table role="presentation" width="120" cellpadding="0" cellspacing="0" border="0"><tr><td height="1" bgcolor="{GOLD}" style="font-size:0;line-height:0">&nbsp;</td></tr></table>
</td></tr>
<tr><td style="padding:26px 32px 6px">
 <table role="presentation" width="536" cellpadding="0" cellspacing="0" border="0" style="width:100%;max-width:536px">{rows}</table>
</td></tr>
<tr><td bgcolor="{CH}" style="background:{CH};padding:26px 32px 28px">
 <div style="{G}font-size:22px;line-height:1.25;color:{INK};padding-bottom:18px">Choose a city. Eight frames, the light and the <i style="color:{GOLD}">film</i>, made only for {H}.</div>
 <table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0"><tr>
  <td width="49%">{btn(cal,"Reserve 10 minutes &rarr;",True)}</td><td width="2%">&nbsp;</td>
  <td width="49%">{btn(B+"?r="+r,"The couture book &rarr;",False)}</td>
 </tr></table>
</td></tr>
<tr><td style="padding:20px 32px 22px;border-top:1px solid {HAIR}">
 <div style="{G}font-size:15px;line-height:1.5;color:{INK}">Warm regards,<br><span style="letter-spacing:3px;text-transform:uppercase;font-size:13px">Charbel Msallem</span> <span style="color:{MUTE}">· Fashion Photographer &amp; Film Director</span></div>
 <div style="{A}font-size:10px;letter-spacing:1.4px;color:{MUTE};padding-top:8px">CHARBEL MSALLEM STUDIOS · +961 3 729713 · info@charbelmsallem.net · @charbelmsallemstudios</div>
 <div style="{G}font-style:italic;font-size:13px;color:{MUTE};padding-top:12px">If this isn't for you, one word back and I won't write again.</div>
</td></tr></table>'''

def row(n,city,img,date,tag,house,r,slug):
    wa=f'https://charbelmsallem.net/acts/mood/{img}/?h={U.quote(house)}&amp;r={r}'
    rt=RATIO[img]; bw,bh=196,250
    fw,fh=(bw,round(bw/rt)) if rt>bw/bh else (round(bh*rt),bh)
    return (f'<tr><td style="padding:22px 0;border-top:1px solid {HAIR}">'
      f'<table role="presentation" width="536" cellpadding="0" cellspacing="0" border="0" style="width:100%;max-width:536px"><tr>'
      f'<td width="196" height="{bh}" align="center" valign="middle" bgcolor="{CH}" style="background:{CH};width:196px;height:{bh}px"><a href="{wa}"><img src="{M}{img}.jpg{V}" width="{fw}" height="{fh}" alt="{city}, photograph" style="display:block;border:0;width:{fw}px;height:{fh}px;margin:0 auto"></a></td>'
      f'<td width="6" style="font-size:0">&nbsp;</td>'
      f'<td width="140" height="{bh}" valign="middle" bgcolor="{CH}" style="background:{CH};width:140px;height:{bh}px"><a href="{wa}"><img src="{M}film-{img}.jpg{V}" width="140" height="250" alt="{city}, film" style="display:block;border:0;width:140px;height:250px"></a></td>'
      f'<td width="20" style="font-size:0">&nbsp;</td>'
      f'<td valign="middle">'
      f'<div style="{G}font-style:italic;font-size:17px;color:{GOLD}">{n}</div>'
      f'<div style="{G}font-size:26px;line-height:1.05;color:{INK};padding-top:2px">{city}</div>'
      f'<div style="{A}font-size:8px;letter-spacing:2px;text-transform:uppercase;color:{MUTE};padding:9px 0 4px">{date}</div>'
      f'<div style="{G}font-style:italic;font-size:15px;line-height:1.35;color:{INK2};padding-bottom:16px">{tag}</div>'
      f'<table role="presentation" width="150" cellpadding="0" cellspacing="0" border="0"><tr><td>{btn(wa,"This city &rarr;",False)}</td></tr></table>'
      f'</td></tr>'
      f'<tr><td align="center" style="{A}font-size:8px;letter-spacing:2px;text-transform:uppercase;color:{MUTE};padding-top:8px">Photograph</td><td></td>'
      f'<td align="center" style="{LAB}font-size:8px;letter-spacing:2px;padding-top:8px">&#9654;&nbsp; Film</td><td></td><td></td></tr></table>'
      f'</td></tr>')

def mail_rows(house,slug,greet,r=None):
    r=r or 'em-'+slug
    rows=''.join(row(n,city,img,date,tag,house,r,slug) for n,city,img,date,tag,txt,pos in CITIES)
    out=mail(house,slug,greet,r)
    a=out.index('<tr><td style="padding:26px 32px 6px">'); b=out.index('<tr><td bgcolor=')
    return out[:a]+f'<tr><td style="padding:22px 32px 10px"><table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0">{rows}</table></td></tr>\n'+out[b:]

if __name__=='__main__':
    house,slug,greet,out=sys.argv[1:5]
    open(out,'w').write(mail(house,slug,greet,'test' if 'test' in out else None))
