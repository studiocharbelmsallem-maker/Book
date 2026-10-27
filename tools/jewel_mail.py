import json,sys,urllib.parse as U,html
B='https://studiocharbelmsallem-maker.github.io/Book/'
M=B+'acts/mail/jewel/'
F=json.load(open('/home/claude/acts/jewel_fixed.json'))
G="font-family:Georgia,'EB Garamond',serif;"; A="font-family:Helvetica,Arial,sans-serif;"
LAB=A+"font-size:10px;letter-spacing:3px;text-transform:uppercase;"
def mail(house,slug,greet,r=None):
    r=r or 'em-'+slug; H=html.escape(house)
    def wa(n,t): return 'https://wa.me/96191729713?text='+U.quote(f'Hello Charbel, {house} here. We choose Act {n} · {t}.')
    cols=''
    for i,(a,n) in enumerate(zip(F['acts'],['I','II','III']),1):
        sw=''.join(f'<td height="7" bgcolor="{c}" style="font-size:0;line-height:0">&nbsp;</td>' for c in a['sw'])
        cols+=(f'<div style="display:inline-block;vertical-align:top;width:100%;max-width:172px;margin:0 2px 26px;text-align:left;font-size:16px">'
          f'<a href="{wa(n,a["title"])}"><img src="{M}act{i}.jpg" width="172" height="258" alt="{a["title"]}" style="display:block;border:0;width:100%;max-width:172px;height:auto"></a>'
          f'<div style="{G}font-style:italic;font-size:12px;line-height:1.3;color:#8B7027;padding-top:12px;min-height:32px">Act {n} · {a["kind"]} · {a["for"]}</div>'
          f'<div style="{G}font-size:23px;line-height:1.1;color:#201F1C;padding:6px 0 8px">{a["title"]}</div>'
          f'<div style="{G}font-style:italic;font-size:13.5px;line-height:1.4;color:#4A4842;min-height:57px">{a["line"]}</div>'
          f'<div style="{G}font-size:12px;line-height:1.45;color:#4A4842;padding-top:10px;min-height:122px"><span style="{A}font-size:8px;letter-spacing:2px;text-transform:uppercase;color:#8B7027">The concept.</span> {a["concept"]}</div>'
          f'<table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0" style="margin:12px 0 10px"><tr>{sw}</tr></table>'
          f'<table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0"><tr><td align="center" style="border:1px solid #8B7027;background:#ffffff">'
          f'<a href="{wa(n,a["title"])}" style="display:block;padding:10px 0;{A}font-size:10px;font-weight:bold;letter-spacing:3px;text-transform:uppercase;color:#201F1C;text-decoration:none">This one →</a></td></tr></table></div>')
    cal='https://calendly.com/studiocharbelmsallem/concept-call-10-min?a1='+U.quote_plus(f'{house} · Concept call')+f'&utm_source=mail&utm_campaign={slug}&utm_content=inline'
    return f'''<div style="{G}font-size:16px;line-height:1.5;color:#201F1C">Dear {html.escape(greet)},<br><br>As promised, a first look made only for {H}: three ways your next campaign could feel. Choose the act that speaks to you and the other seven frames follow within 48 hours.<br><br></div>
<table role="presentation" width="600" cellpadding="0" cellspacing="0" border="0" style="width:100%;max-width:600px;border-collapse:collapse">
<tr><td bgcolor="#13110E" style="background:#13110E;padding:24px 30px 34px">
 <table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0"><tr><td style="{LAB}color:#C9A85C">Charbel Msallem</td><td align="right" style="{LAB}color:#C9A85C">For {H}</td></tr></table>
 <table role="presentation" cellpadding="0" cellspacing="0" border="0" align="center" style="margin:26px auto 0"><tr><td style="border:1px solid #5E5137;padding:7px"><img src="{M}cover.jpg" width="250" height="333" alt="{H}" style="display:block;border:0;width:250px;height:333px"></td></tr></table>
 <div style="text-align:center;padding-top:26px"><div style="{LAB}color:#C9A85C">Three acts · one is already yours</div>
 <div style="{G}font-size:42px;line-height:1.08;color:#EDE9E0;padding:12px 0 10px">{H},<br>in <i style="color:#C9A85C">three</i> acts.</div>
 <div style="{G}font-style:italic;font-size:17px;color:#C9C4B8">{F["line"]}</div>
 <div style="{LAB}color:#C9A85C;padding:30px 0 14px">Two films · fifteen seconds each</div></div>
 <div style="font-size:0;text-align:center"><div style="display:inline-block;vertical-align:bottom;width:169px;margin:0 4px 8px"><a href="{B}films/jw15-skin-play.mp4"><img src="{M}film1.gif" width="169" height="300" alt="Film, 15 seconds, sound on" style="display:block;border:0;width:169px;height:300px"></a></div><div style="display:inline-block;vertical-align:bottom;width:100%;max-width:363px;margin:0 0 8px"><a href="{B}films/jw15-coast-play.mp4"><img src="{M}film2.gif" width="363" height="204" alt="Film, 15 seconds, sound on" style="display:block;border:0;width:100%;max-width:363px;height:auto"></a></div></div>
</td></tr>
<tr><td bgcolor="#F3F2EE" style="background:#F3F2EE;padding:28px 30px 4px">
 <table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0" style="border-bottom:1px solid #DAD8D1;margin-bottom:22px"><tr><td style="{LAB}color:#8B7027;padding-bottom:12px">Choose the act</td><td align="right" style="{LAB}color:#8B7027;padding-bottom:12px">Frame 01 of 08 · each</td></tr></table>
 <div style="font-size:0;text-align:center">{cols}</div>
</td></tr>
<tr><td bgcolor="#F3F2EE" style="background:#F3F2EE;padding:6px 30px 30px">
 <div style="{G}font-size:24px;line-height:1.25;color:#201F1C;padding-bottom:16px">Pick one. The other <i style="color:#8B7027">seven frames</i> arrive within 48 hours, made only for {H}.</div>
 <table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0"><tr>
  <td width="49%" bgcolor="#201F1C" align="center" style="background:#201F1C"><a href="{cal}" style="display:block;padding:15px 0;{A}font-size:10px;font-weight:bold;letter-spacing:3px;text-transform:uppercase;color:#F3F2EE;text-decoration:none">Reserve 10 minutes →</a></td>
  <td width="2%">&nbsp;</td>
  <td width="49%" align="center" style="border:1px solid #8B7027;background:#ffffff"><a href="{B}jewellery.html?r={r}" style="display:block;padding:14px 0;{A}font-size:10px;font-weight:bold;letter-spacing:3px;text-transform:uppercase;color:#201F1C;text-decoration:none">The jewellery book →</a></td>
 </tr></table>
 <div style="padding-top:22px;{G}font-size:14px;color:#8B8A83"><b style="{A}font-size:10px;letter-spacing:3px;text-transform:uppercase;color:#201F1C">Charbel Msallem</b> · Fashion Director<br>+961 91 729 713 · <span style="color:#8B7027">studiocharbelmsallem@gmail.com</span></div>
</td></tr></table>'''
if __name__=='__main__':
    house,slug,greet,out=sys.argv[1:5]
    open(out,'w').write(mail(house,slug,greet,'test' if 'test' in out else None))
