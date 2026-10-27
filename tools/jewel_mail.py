import json,sys,urllib.parse as U,html
B='https://studiocharbelmsallem-maker.github.io/Book/'
M=B+'acts/mail/jewel/'
F=json.load(open('/home/claude/acts/jewel_fixed.json'))
def mail(house,slug,greet,r=None):
    r=r or 'em-'+slug; H=html.escape(house)
    G="font-family:Georgia,'EB Garamond',serif;"; A="font-family:Helvetica,Arial,sans-serif;"
    lab=A+"font-size:10px;letter-spacing:3px;text-transform:uppercase;"
    def wa(n,t): return 'https://wa.me/96191729713?text='+U.quote(f'Hello Charbel, {house} here. We choose Act {n} · {t}.')
    def film(i,src):
        return (f'<td width="150" valign="middle" align="center"><a href="{B}films/{src}" style="text-decoration:none">'
                f'<img src="{M}film{i}.jpg" width="150" height="267" alt="Film, 15 seconds" style="display:block;border:0;width:150px;height:267px"></a>'
                f'<div style="{lab}color:#C9A85C;padding-top:8px">Film · 15 s</div></td>')
    acts=''
    hs={1:540,2:481,3:540}
    for i,(a,n) in enumerate(zip(F['acts'],['I','II','III']),1):
        sw=''.join(f'<td height="8" bgcolor="{c}" style="font-size:0;line-height:0">&nbsp;</td>' for c in a['sw'])
        acts+=(f'<tr><td style="padding:0 0 30px"><table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0"><tr>'
          f'<td width="200" valign="top"><a href="{wa(n,a["title"])}"><img src="{M}act{i}.jpg" width="200" height="{round(200*hs[i]/360)}" alt="{a["title"]}" style="display:block;border:0;width:200px;height:auto"></a></td>'
          f'<td width="22">&nbsp;</td><td valign="top">'
          f'<div style="{G}font-style:italic;font-size:14px;color:#8B7027">Act {n} · {a["kind"]} · {a["for"]}</div>'
          f'<div style="{G}font-size:28px;line-height:1.1;color:#201F1C;padding:6px 0 8px">{a["title"]}</div>'
          f'<div style="{G}font-style:italic;font-size:15px;line-height:1.4;color:#4A4842">{a["line"]}</div>'
          f'<table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0" style="margin:12px 0"><tr>{sw}</tr></table>'
          f'<div style="{G}font-size:13.5px;line-height:1.45;color:#4A4842"><span style="{lab}font-size:9px;color:#8B7027">The concept.</span> {a["concept"]}</div>'
          f'<table role="presentation" cellpadding="0" cellspacing="0" border="0" style="margin-top:14px"><tr><td style="border:1px solid #8B7027;background:#ffffff">'
          f'<a href="{wa(n,a["title"])}" style="display:block;padding:11px 22px;{A}font-size:11px;font-weight:bold;letter-spacing:3px;text-transform:uppercase;color:#201F1C;text-decoration:none">This one →</a></td></tr></table>'
          f'</td></tr></table></td></tr>')
    cal='https://calendly.com/studiocharbelmsallem/concept-call-10-min?a1='+U.quote_plus(f'{house} · Concept call')+f'&utm_source=mail&utm_campaign={slug}&utm_content=inline'
    return f'''<div style="{G}font-size:16px;line-height:1.5;color:#201F1C">Dear {html.escape(greet)},<br><br>As promised, a first look made only for {H}: three ways your next campaign could feel. Choose the act that speaks to you and the other seven frames follow within 48 hours.<br><br></div>
<table role="presentation" width="600" cellpadding="0" cellspacing="0" border="0" style="width:100%;max-width:600px;border-collapse:collapse">
<tr><td bgcolor="#13110E" style="background:#13110E;padding:26px 30px 30px">
 <table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0"><tr><td style="{lab}color:#C9A85C">Charbel Msallem</td><td align="right" style="{lab}color:#C9A85C">For {H}</td></tr></table>
 <table role="presentation" width="540" cellpadding="0" cellspacing="0" border="0" align="center" style="margin-top:24px"><tr>
  {film(1,'jw15-skin-play.mp4')}<td width="10">&nbsp;</td>
  <td width="220" valign="middle"><img src="{M}cover.jpg" width="220" height="293" alt="{H}" style="display:block;border:0;width:220px;height:293px"></td>
  <td width="10">&nbsp;</td>{film(2,'jw15-coast-play.mp4')}
 </tr></table>
 <div style="text-align:center;padding-top:26px"><div style="{lab}color:#C9A85C">Three acts · one is already yours</div>
 <div style="{G}font-size:40px;line-height:1.08;color:#EDE9E0;padding:12px 0 10px">{H},<br>in <i style="color:#C9A85C">three</i> acts.</div>
 <div style="{G}font-style:italic;font-size:17px;color:#C9C4B8">{F["line"]}</div></div>
</td></tr>
<tr><td bgcolor="#F3F2EE" style="background:#F3F2EE;padding:28px 30px 8px">
 <div style="{lab}color:#8B7027;border-bottom:1px solid #DAD8D1;padding-bottom:12px;margin-bottom:24px">Choose the act</div>
 <table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0">{acts}</table>
</td></tr>
<tr><td bgcolor="#F3F2EE" style="background:#F3F2EE;padding:0 30px 30px">
 <div style="{G}font-size:22px;line-height:1.25;color:#201F1C;padding-bottom:16px">Pick one. The other <i style="color:#8B7027">seven frames</i> arrive within 48 hours, made only for {H}.</div>
 <table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0"><tr>
  <td width="49%" bgcolor="#201F1C" align="center" style="background:#201F1C"><a href="{cal}" style="display:block;padding:15px 0;{A}font-size:11px;font-weight:bold;letter-spacing:3px;text-transform:uppercase;color:#F3F2EE;text-decoration:none">Reserve 10 minutes →</a></td>
  <td width="2%">&nbsp;</td>
  <td width="49%" align="center" style="border:1px solid #201F1C"><a href="{B}jewellery.html?r={r}" style="display:block;padding:14px 0;{A}font-size:11px;font-weight:bold;letter-spacing:3px;text-transform:uppercase;color:#201F1C;text-decoration:none">The jewellery book →</a></td>
 </tr></table>
 <div style="{G}font-size:13px;color:#8B8A83;padding-top:14px;text-align:center"><a href="{B}acts/{slug.replace('jewelers','').replace('jewelry','') if False else ''}" style="color:#8B7027"></a></div>
</td></tr></table>
<div style="{G}font-size:16px;line-height:1.5;color:#201F1C;padding-top:22px">Warm regards,<br><b style="{A}font-size:12px;letter-spacing:3px;text-transform:uppercase">Charbel Msallem</b> · Fashion Director<br><span style="color:#8B8A83">+961 91 729 713 · studiocharbelmsallem@gmail.com</span></div>'''
if __name__=='__main__':
    house,slug,greet,out=sys.argv[1:5]
    open(out,'w').write(mail(house,slug,greet,'test' if 'test' in out else None))
