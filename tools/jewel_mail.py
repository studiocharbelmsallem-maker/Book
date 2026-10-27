import json,sys,urllib.parse as U,html
B='https://studiocharbelmsallem-maker.github.io/Book/'
M=B+'acts/mail/jewel/'; V='?v=5'
F=json.load(open('/home/claude/acts/jewel_fixed.json'))
INK='#1E1C18';INK2='#4A4740';MUTE='#8A8478';GOLD='#9A7B2E';CH='#F7F4EC';HAIR='#E6DCC4'
G="font-family:'EB Garamond',Georgia,'Times New Roman',serif;"; A="font-family:Archivo,Helvetica,Arial,sans-serif;"
LAB=A+f"font-size:10px;letter-spacing:2.6px;text-transform:uppercase;color:{GOLD};"
def btn(href,txt,solid):
    st=(f"background:{GOLD};color:#FFFFFF;" if solid else f"background:#FFFFFF;color:{INK};border:1px solid {GOLD};")
    return f'<a href="{href}" style="display:block;padding:14px 0;{A}font-size:10px;font-weight:bold;letter-spacing:2.6px;text-transform:uppercase;text-decoration:none;text-align:center;{st}">{txt}</a>'
def mail(house,slug,greet,r=None):
    r=r or 'em-'+slug; H=html.escape(house)
    def wa(n,t): return 'https://wa.me/96191729713?text='+U.quote(f'Hello Charbel, {house} here. We choose Act {n} · {t}.')
    imgs={1:('act1.jpg',300),2:('act2n.jpg',267),3:('act3.jpg',300)}
    acts=''
    for i,(a,n) in enumerate(zip(F['acts'],['I','II','III']),1):
        f,h=imgs[i]
        sw=''.join(f'<td height="6" bgcolor="{c}" style="font-size:0;line-height:0">&nbsp;</td>' for c in a['sw'])
        acts+=(f'<tr><td style="padding:0 0 34px"><table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0"><tr>'
          f'<td width="200" valign="top"><a href="{wa(n,a["title"])}"><img src="{M}{f}{V}" width="200" height="{h}" alt="Act {n}, {a["title"]}" style="display:block;border:0;width:200px;height:auto"></a></td>'
          f'<td width="24">&nbsp;</td><td valign="top">'
          f'<div style="{LAB}font-size:9px">Act {n} · {a["kind"]}</div>'
          f'<div style="{G}font-size:28px;line-height:1.06;color:{INK};padding:8px 0 4px">{a["title"]}</div>'
          f'<div style="{G}font-style:italic;font-size:13px;color:{MUTE};padding-bottom:10px">{a["for"].capitalize()}</div>'
          f'<div style="{G}font-style:italic;font-size:16px;line-height:1.42;color:{INK2}">{a["line"]}</div>'
          f'<table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0" style="margin:14px 0 12px"><tr>{sw}</tr></table>'
          f'<div style="{G}font-size:14px;line-height:1.5;color:{INK2}"><span style="{LAB}font-size:8px">The concept</span>&nbsp; {a["concept"]}</div>'
          f'<table role="presentation" width="170" cellpadding="0" cellspacing="0" border="0" style="margin-top:16px"><tr><td>{btn(wa(n,a["title"]),"This one &rarr;",False)}</td></tr></table>'
          f'</td></tr></table></td></tr>')
    cal='https://calendly.com/studiocharbelmsallem/concept-call-10-min?a1='+U.quote_plus(f'{house} · Concept call')+f'&utm_source=mail&utm_campaign={slug}&utm_content=inline'
    return f'''<div style="{G}font-size:17px;line-height:1.55;color:{INK}">Dear {html.escape(greet)},<br><br>As promised, a first look made only for {H}: three ways your next campaign could feel. Choose the act that speaks to you, and the other seven frames follow within 48 hours.<br><br></div>
<table role="presentation" width="600" cellpadding="0" cellspacing="0" border="0" style="width:100%;max-width:600px;border-collapse:collapse;background:#FFFFFF;border:1px solid {HAIR}">
<tr><td style="padding:22px 32px 0">
 <table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0" style="border-bottom:1px solid {HAIR}"><tr><td style="padding-bottom:14px;{G}font-size:14px;letter-spacing:3.4px;text-transform:uppercase;color:{INK}">Charbel Msallem<span style="color:{GOLD}">&nbsp;&nbsp;|&nbsp;&nbsp;</span><span style="{A}font-size:9px;letter-spacing:2.2px;color:{GOLD}">Fashion photographer &amp; film director</span></td></tr></table>
</td></tr>
<tr><td style="padding:30px 32px 6px">
 <div style="{LAB}">For {H} · three acts</div>
 <div style="{G}font-size:44px;line-height:1.04;color:{INK};padding:12px 0 16px">{H},<br>in <i style="color:{GOLD}">three</i> acts.</div>
 <table role="presentation" width="120" cellpadding="0" cellspacing="0" border="0"><tr><td height="1" bgcolor="{GOLD}" style="font-size:0;line-height:0">&nbsp;</td></tr></table>
 <div style="{G}font-style:italic;font-size:18px;line-height:1.45;color:{INK2};padding:16px 0 26px">{F["line"]}</div>
 <img src="{M}cover.jpg{V}" width="360" height="480" alt="{H}, the first frame" style="display:block;border:0;width:100%;max-width:360px;height:auto">
</td></tr>
<tr><td style="padding:34px 32px 8px">
 <div style="{LAB}padding-bottom:14px">Two films · fifteen seconds each</div>
 <table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0"><tr>
  <td width="169" valign="bottom"><a href="{B}films/jw15-skin-play.mp4"><img src="{M}film1.gif{V}" width="169" height="300" alt="Film one, plays with sound" style="display:block;border:0;width:169px;height:300px"></a></td>
  <td width="8" style="font-size:0">&nbsp;</td>
  <td valign="bottom"><a href="{B}films/jw15-coast-play.mp4"><img src="{M}film2.gif{V}" width="359" height="202" alt="Film two, plays with sound" style="display:block;border:0;width:100%;max-width:359px;height:auto"></a></td>
 </tr><tr>
  <td style="{LAB}font-size:9px;padding-top:9px">&#9654;&nbsp; Sound on · 15 s</td><td></td>
  <td style="{LAB}font-size:9px;padding-top:9px">&#9654;&nbsp; Sound on · 15 s</td>
 </tr></table>
</td></tr>
<tr><td style="padding:26px 32px 0">
 <table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0" style="border-bottom:1px solid {HAIR};margin-bottom:26px"><tr><td style="{LAB}padding-bottom:12px">Choose the act</td><td align="right" style="{A}font-size:9px;letter-spacing:2.2px;text-transform:uppercase;color:{MUTE};padding-bottom:12px">Frame 01 of 08 · each</td></tr></table>
 <table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0">{acts}</table>
</td></tr>
<tr><td bgcolor="{CH}" style="background:{CH};padding:30px 32px 32px">
 <div style="{G}font-size:26px;line-height:1.22;color:{INK};padding-bottom:20px">Pick one. The other <i style="color:{GOLD}">seven</i> frames arrive within 48 hours, made only for {H}.</div>
 <table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0"><tr>
  <td width="49%">{btn(cal,"Reserve 10 minutes &rarr;",True)}</td><td width="2%">&nbsp;</td>
  <td width="49%">{btn(B+"jewellery.html?r="+r,"The jewellery book &rarr;",False)}</td>
 </tr></table>
</td></tr>
<tr><td style="padding:20px 32px 22px;border-top:1px solid {HAIR}">
 <div style="{G}font-size:15px;line-height:1.5;color:{INK}">Warm regards,<br><span style="letter-spacing:3px;text-transform:uppercase;font-size:13px">Charbel Msallem</span> <span style="color:{MUTE}">· Fashion Director</span></div>
 <div style="{A}font-size:10px;letter-spacing:1.4px;color:{MUTE};padding-top:8px">CHARBEL MSALLEM STUDIOS · +961 91 729 713 · studiocharbelmsallem@gmail.com · @charbelmsallemstudios</div>
</td></tr></table>'''
if __name__=='__main__':
    house,slug,greet,out=sys.argv[1:5]
    open(out,'w').write(mail(house,slug,greet,'test' if 'test' in out else None))
