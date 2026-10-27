import sys,urllib.parse as U,html
sys.path.insert(0,'/home/claude/acts')
from couture_gen import CITIES
from jewel_mail import B,INK,INK2,MUTE,GOLD,CH,HAIR,G,A,LAB,btn
M=B+'acts/mail/couture/'; V='?v=4'
COVER='saab-cover.jpg'
RATIO={'beirut':440/551,'paris':262/466,'milano':355/473,'istanbul':264/331,'dubai':440/584,'barcelona':440/552}
LINE='Every collection has a film inside it. Six cities to find it.'
PH={'beirut':250,'paris':356,'milano':266,'istanbul':251,'dubai':265,'barcelona':251}
def mail(house,slug,greet,r=None):
    r=r or 'em-'+slug; H=html.escape(house); page=f'{B}acts/{slug}/?r={r}'
    rows=''
    for n,city,img,date,tag,txt,pos in CITIES:
        wa='https://wa.me/96191729713?text='+U.quote(f'Hello Charbel, {house} here. We choose {city} · {date}.')
        rt=RATIO[img]; fw,fh=(236,round(236/rt)) if rt>236/312 else (round(312*rt),312); tw=512
        rows+=(f'<tr><td style="padding:30px 0 34px;border-top:1px solid {HAIR}">'
          f'<table role="presentation" cellpadding="0" cellspacing="0" border="0"><tr><td valign="baseline" style="{G}font-style:italic;font-size:26px;color:{GOLD};padding-right:14px">{n}</td>'
          f'<td valign="baseline" style="{G}font-size:32px;line-height:1;color:{INK}">{city}</td></tr></table>'
          f'<div style="{A}font-size:9px;letter-spacing:2.2px;text-transform:uppercase;color:{MUTE};padding:10px 0 4px">{date}</div>'
          f'<div style="{G}font-style:italic;font-size:17px;color:{INK2};padding-bottom:16px">{tag}</div>'
          f'<table role="presentation" width="536" cellpadding="0" cellspacing="0" border="0" style="width:100%;max-width:536px"><tr>'
          f'<td width="264" height="340" align="center" valign="middle" bgcolor="{CH}" style="background:{CH};width:264px;height:340px"><img src="{M}{img}.jpg{V}" width="{fw}" height="{fh}" alt="{city}, photograph" style="display:block;border:0;width:{fw}px;height:{fh}px;margin:0 auto"></td>'
          f'<td width="8" style="font-size:0">&nbsp;</td>'
          f'<td width="264" height="340" align="center" valign="middle" bgcolor="{CH}" style="background:{CH};width:264px;height:340px"><a href="{page}"><img src="{M}{img}.gif{V}" width="175" height="312" alt="{city}, film" style="display:block;border:0;width:175px;height:312px;margin:0 auto"></a></td></tr>'
          f'<tr><td align="center" style="{A}font-size:8px;letter-spacing:2px;text-transform:uppercase;color:{MUTE};padding-top:9px">Photograph</td><td></td>'
          f'<td align="center" style="{LAB}font-size:8px;letter-spacing:2px;padding-top:9px">&#9654;&nbsp; Film</td></tr></table>'
          f'<div style="{G}font-size:15px;line-height:1.55;color:{INK2};padding-top:16px;max-width:470px">{txt}</div>'
          f'<table role="presentation" width="170" cellpadding="0" cellspacing="0" border="0" style="margin-top:18px"><tr><td>{btn(wa,"This city &rarr;",False)}</td></tr></table>'
          f'</td></tr>')
    cal='https://calendly.com/studiocharbelmsallem/concept-call-10-min?a1='+U.quote_plus(f'{house} · Concept call')+f'&utm_source=mail&utm_campaign={slug}&utm_content=inline'
    return f'''<div style="{G}font-size:17px;line-height:1.55;color:{INK}">Dear {html.escape(greet)},<br><br>A short follow-up. Rather than describe it, I prepared a first look made only for {H}: six cities where your next collection could be filmed. Choose the one that speaks to you, and the concept follows within 48 hours.<br><br></div>
<table role="presentation" width="600" cellpadding="0" cellspacing="0" border="0" style="width:100%;max-width:600px;border-collapse:collapse;background:#FFFFFF;border:1px solid {HAIR}">
<tr><td style="padding:22px 32px 0">
 <table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0" style="border-bottom:1px solid {HAIR}"><tr><td style="padding-bottom:14px;{G}font-size:14px;letter-spacing:3.4px;text-transform:uppercase;color:{INK}">Charbel Msallem<span style="color:{GOLD}">&nbsp;&nbsp;|&nbsp;&nbsp;</span><span style="{A}font-size:9px;letter-spacing:2.2px;color:{GOLD}">Fashion photographer &amp; film director</span></td></tr></table>
</td></tr>
<tr><td style="padding:30px 32px 6px">
 <div style="{LAB}">For {H} · the season 2027</div>
 <div style="{G}font-size:44px;line-height:1.04;color:{INK};padding:12px 0 16px">{H},<br>in <i style="color:{GOLD}">six</i> cities.</div>
 <table role="presentation" width="120" cellpadding="0" cellspacing="0" border="0"><tr><td height="1" bgcolor="{GOLD}" style="font-size:0;line-height:0">&nbsp;</td></tr></table>
 <div style="{G}font-style:italic;font-size:18px;line-height:1.45;color:{INK2};padding:16px 0 26px">{LINE}</div>
 <img src="{M}{COVER}{V}" width="536" height="357" alt="{H}, the first frame" style="display:block;border:0;width:100%;max-width:536px;height:auto">
</td></tr>
<tr><td style="padding:34px 32px 0">
 <table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0" style="margin-bottom:0"><tr><td style="{LAB}padding-bottom:12px">Choose the city</td><td align="right" style="{A}font-size:9px;letter-spacing:2.2px;text-transform:uppercase;color:{MUTE};padding-bottom:12px">Photo · film · the light</td></tr></table>
 <table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0">{rows}</table>
</td></tr>
<tr><td bgcolor="{CH}" style="background:{CH};padding:30px 32px 32px">
 <div style="{G}font-size:26px;line-height:1.22;color:{INK};padding-bottom:20px">Choose a city. The concept for {H} follows within 48 hours: eight frames, the light and the <i style="color:{GOLD}">film</i>, made only for you.</div>
 <table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0"><tr>
  <td width="49%">{btn(cal,"Reserve 10 minutes &rarr;",True)}</td><td width="2%">&nbsp;</td>
  <td width="49%">{btn(B+"?r="+r,"The couture book &rarr;",False)}</td>
 </tr></table>
</td></tr>
<tr><td style="padding:20px 32px 22px;border-top:1px solid {HAIR}">
 <div style="{G}font-size:15px;line-height:1.5;color:{INK}">Warm regards,<br><span style="letter-spacing:3px;text-transform:uppercase;font-size:13px">Charbel Msallem</span> <span style="color:{MUTE}">· Fashion Director</span></div>
 <div style="{A}font-size:10px;letter-spacing:1.4px;color:{MUTE};padding-top:8px">CHARBEL MSALLEM STUDIOS · +961 91 729 713 · studiocharbelmsallem@gmail.com · @charbelmsallemstudios</div>
</td></tr></table>'''
if __name__=='__main__':
    house,slug,greet,out=sys.argv[1:5]
    open(out,'w').write(mail(house,slug,greet,'test' if 'test' in out else None))
