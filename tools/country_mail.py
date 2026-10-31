#!/usr/bin/env python3
"""Country outreach mail: one fixed layout, one entry per country.

    python3 tools/country_mail.py paris "Maison Example"   -> x/mail-paris-maison-example.html
    python3 tools/country_mail.py paris                    -> x/mail-country-paris.html  ({House} left in)

Each country = 3 photos (fashion show, editorial, casual) with a 4-colour strip,
plus 2 short films shown as covers that open the mp4 on the site.
Assets live in acts/mail/<country>/ : show.jpg editorial.jpg casual.jpg film-1.jpg film-2.jpg
"""
import sys, re, pathlib
from urllib.parse import quote

SITE = "https://charbelmsallem.net"
WA = "9613729713"
V = "1"

COUNTRIES = {
    "paris": {
        "city": "Paris",
        "italic": "A salon show under the chandeliers. A château at the water. The street in a beret.",
        "films": [
            ("film-couture.jpg", "films/paris-couture.mp4", "Couture", "24 s"),
            ("film-show.jpg", "films/paris-fashion-show.mp4", "Fashion show", "23 s"),
        ],
        "acts": [
            ("show.jpg", "Fashion show", "The Salon", "For the collection's first walk",
             "Every look on the floor at once, under gold and candlelight.",
             ["#190C07", "#EFE7D8", "#B39072", "#82552F"],
             "A Paris show is a room before it is a runway. We film the salon the way the front row sees it: the chandelier, the line of gowns, one face that holds the room. The collection reads as a whole before it reads as pieces."),
            ("editorial.jpg", "Editorial", "The Château", "For the campaign image",
             "One gown, a château across the water, and a grey Paris sky that flatters silk.",
             ["#5B6362", "#868D90", "#B2B5B6", "#E1E3E3"],
             "The editorial is the image that stays on the wall. Soft northern light, stone and water, a single silhouette in its own landscape. Nothing in the frame competes with the dress."),
            ("casual.jpg", "Casual", "Off Duty", "For ready-to-wear and the street",
             "The same city on a Tuesday: a beret, a white collar, a column at her back.",
             ["#302922", "#554933", "#827156", "#C5B4A2"],
             "Ready-to-wear needs the street, not the salon. We shoot it in passing light along the avenues, so the clothes look lived in from the first frame. Built for the first second of a Reel."),
        ],
    },
}

F_SERIF = "font-family:'EB Garamond',Georgia,'Times New Roman',serif"
F_SANS = "font-family:Archivo,Helvetica,Arial,sans-serif"
KICK = F_SANS + ";font-size:10px;letter-spacing:2.6px;text-transform:uppercase;color:#9A7B2E"
ROMAN = ["I", "II", "III"]


def wa(house, text):
    return f"https://wa.me/{WA}?text=" + quote(f"Hello Charbel, {house} here. {text}")


def strip(colors):
    cells = "".join(f'<td height="6" bgcolor="{c}" style="font-size:0;line-height:0">&nbsp;</td>' for c in colors)
    return f'<table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0" style="margin:14px 0 12px"><tr>{cells}</tr></table>'


def act(key, house, i, a):
    img, register, name, sub, line, colors, concept = a
    link = wa(house, f"For {COUNTRIES[key]['city']} we choose {ROMAN[i]} · {name}.")
    return f'''<tr><td style="padding:0 0 34px"><table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0"><tr><td width="200" valign="top"><a href="{link}"><img src="{SITE}/acts/mail/{key}/{img}?v={V}" width="200" height="300" alt="{register}, {name}" style="display:block;border:0;width:200px;height:auto"></a></td><td width="24">&nbsp;</td><td valign="top"><div style="{KICK};font-size:9px">{ROMAN[i]} · {register}</div><div style="{F_SERIF};font-size:28px;line-height:1.06;color:#1E1C18;padding:8px 0 4px">{name}</div><div style="{F_SERIF};font-style:italic;font-size:13px;color:#8A8478;padding-bottom:10px">{sub}</div><div style="{F_SERIF};font-style:italic;font-size:16px;line-height:1.42;color:#4A4740">{line}</div>{strip(colors)}<div style="{F_SERIF};font-size:14px;line-height:1.5;color:#4A4740"><span style="{KICK};font-size:8px">The concept</span>&nbsp; {concept}</div><table role="presentation" width="170" cellpadding="0" cellspacing="0" border="0" style="margin-top:16px"><tr><td><a href="{link}" style="display:block;padding:14px 0;{F_SANS};font-size:10px;font-weight:bold;letter-spacing:2.6px;text-transform:uppercase;text-decoration:none;text-align:center;background:#FFFFFF;color:#1E1C18;border:1px solid #9A7B2E;">This one &rarr;</a></td></tr></table></td></tr></table></td></tr>'''


def build(key, house="{House}"):
    c = COUNTRIES[key]
    city = c["city"]
    slug = re.sub(r"[^a-z0-9]+", "", house.lower()) or "house"
    (p1, m1, l1, d1), (p2, m2, l2, d2) = c["films"]
    acts = "".join(act(key, house, i, a) for i, a in enumerate(c["acts"]))
    cal = f"https://calendly.com/studiocharbelmsallem/concept-call-10-min?a1={quote(house + ' · ' + city + ' concept call')}&utm_source=mail&utm_campaign={key}-{slug}"
    return f'''<div style="{F_SERIF};font-size:17px;line-height:1.55;color:#1E1C18">Dear {house},<br><br>{city}, in three registers: the show, the editorial, the street. Two films first, sound on. Tell me which register is closest to your next season and I will build the first frames around it.<br><br></div>
<table role="presentation" width="600" cellpadding="0" cellspacing="0" border="0" style="width:100%;max-width:600px;border-collapse:collapse;background:#FFFFFF;border:1px solid #E6DCC4">
<tr><td style="padding:22px 32px 0">
 <table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0" style="border-bottom:1px solid #E6DCC4"><tr><td style="padding-bottom:14px;{F_SERIF};font-size:14px;letter-spacing:3.4px;text-transform:uppercase;color:#1E1C18">Charbel Msallem<span style="color:#9A7B2E">&nbsp;&nbsp;|&nbsp;&nbsp;</span><span style="{F_SANS};font-size:9px;letter-spacing:2.2px;color:#9A7B2E">Fashion Photographer &amp; Film Director</span></td></tr></table>
</td></tr>
<tr><td style="padding:30px 32px 6px">
 <div style="{KICK}">For {house} · {city}</div>
 <div style="{F_SERIF};font-size:44px;line-height:1.04;color:#1E1C18;padding:12px 0 16px">{city},<br>in <i style="color:#9A7B2E">three</i> registers.</div>
 <table role="presentation" width="120" cellpadding="0" cellspacing="0" border="0"><tr><td height="1" bgcolor="#9A7B2E" style="font-size:0;line-height:0">&nbsp;</td></tr></table>
 <div style="{F_SERIF};font-style:italic;font-size:18px;line-height:1.45;color:#4A4740;padding:16px 0 4px">{c["italic"]}</div>
</td></tr>
<tr><td style="padding:26px 32px 8px">
 <div style="{KICK};padding-bottom:14px">Two films · {city}</div>
 <table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0"><tr>
  <td width="264" valign="top"><a href="{SITE}/{m1}"><img src="{SITE}/acts/mail/{key}/{p1}?v={V}" width="264" height="469" alt="{city} · {l1} film, plays with sound" style="display:block;border:0;width:100%;max-width:264px;height:auto"></a></td>
  <td width="8" style="font-size:0">&nbsp;</td>
  <td width="264" valign="top"><a href="{SITE}/{m2}"><img src="{SITE}/acts/mail/{key}/{p2}?v={V}" width="264" height="469" alt="{city} · {l2} film, plays with sound" style="display:block;border:0;width:100%;max-width:264px;height:auto"></a></td>
 </tr><tr>
  <td style="{KICK};font-size:9px;padding-top:9px">&#9654;&nbsp; {l1} · {d1}</td><td></td>
  <td style="{KICK};font-size:9px;padding-top:9px">&#9654;&nbsp; {l2} · {d2}</td>
 </tr></table>
</td></tr>
<tr><td style="padding:26px 32px 0">
 <table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0" style="border-bottom:1px solid #E6DCC4;margin-bottom:26px"><tr><td style="{KICK};padding-bottom:12px">Choose the register</td><td align="right" style="{F_SANS};font-size:9px;letter-spacing:2.2px;text-transform:uppercase;color:#8A8478;padding-bottom:12px">The mood board</td></tr></table>
 <table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0">{acts}</table>
</td></tr>
<tr><td bgcolor="#F7F4EC" style="background:#F7F4EC;padding:30px 32px 32px">
 <div style="{F_SERIF};font-size:26px;line-height:1.22;color:#1E1C18;padding-bottom:20px">Pick one. The first frames follow within <i style="color:#9A7B2E">48 hours</i>, made only for {house}.</div>
 <table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0"><tr>
  <td width="49%"><a href="{cal}&utm_content=inline" style="display:block;padding:14px 0;{F_SANS};font-size:10px;font-weight:bold;letter-spacing:2.6px;text-transform:uppercase;text-decoration:none;text-align:center;background:#9A7B2E;color:#FFFFFF;">Reserve 10 minutes &rarr;</a></td><td width="2%">&nbsp;</td>
  <td width="49%"><a href="{SITE}/?r=em-{key}-{slug}#chapters" style="display:block;padding:14px 0;{F_SANS};font-size:10px;font-weight:bold;letter-spacing:2.6px;text-transform:uppercase;text-decoration:none;text-align:center;background:#FFFFFF;color:#1E1C18;border:1px solid #9A7B2E;">The {city} chapter &rarr;</a></td>
 </tr></table>
</td></tr>
<tr><td style="padding:20px 32px 22px;border-top:1px solid #E6DCC4">
 <div style="{F_SERIF};font-size:15px;line-height:1.5;color:#1E1C18">Warm regards,<br><span style="letter-spacing:3px;text-transform:uppercase;font-size:13px">Charbel Msallem</span> <span style="color:#8A8478">· Fashion Photographer &amp; Film Director</span></div>
 <div style="{F_SANS};font-size:10px;letter-spacing:1.4px;color:#8A8478;padding-top:8px">CHARBEL MSALLEM STUDIOS · +961 3 729713 · info@charbelmsallem.net · studiocharbelmsallem@gmail.com · @charbelmsallemstudios</div>
</td></tr></table>
'''


if __name__ == "__main__":
    key = sys.argv[1] if len(sys.argv) > 1 else "paris"
    house = sys.argv[2] if len(sys.argv) > 2 else None
    root = pathlib.Path(__file__).resolve().parent.parent
    if house:
        slug = re.sub(r"[^a-z0-9]+", "-", house.lower()).strip("-")
        out = root / "x" / f"mail-{key}-{slug}.html"
        html = build(key, house)
    else:
        out = root / "x" / f"mail-country-{key}.html"
        html = build(key)
    out.write_text(html)
    print(out)
