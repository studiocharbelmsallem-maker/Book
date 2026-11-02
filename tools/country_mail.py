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
IMG = "https://studiocharbelmsallem-maker.github.io/Book"  # files: the domain serves pages, not static files
WA = "9613729713"
V = "3"

COUNTRIES = {
    "beirut": {
        "city": "Beirut",
        "chapter": "Chapter 01",
        "tagline": "where the light is learned",
        "italic": "The region's atelier capital. Where couture learned to be built by hand and judged by light.",
        "films": [
            ("film-couture.jpg", "films/beirut-couture.mp4", "Couture", "17 s"),
            ("film-casual.jpg", "films/beirut-casual.mp4", "Casual", "12 s"),
        ],
        "acts": [
            ("couture.jpg", "Couture", "The Atelier", "Red-carpet weight, shot for the moment before the flashbulb",
             "Industrial dreams meet couture fantasy.",
             ["#3A2A22", "#B79AAE", "#8C6A5A", "#D9C3B6"],
             "Satin against iron. The machine gives the gown its contrast; one hard light gives it its construction."),
            ("editorial.jpg", "Editorial", "The Coast", "Winter couture walked across raw Beirut stone",
             "Soft fabric, rough stone. The coastline becomes a runway.",
             ["#2B2420", "#6E5A4C", "#E8E4DE", "#8FA6B2"],
             "Embroidery set against volcanic rock. The texture of the land proves the texture of the hand."),
            ("casual.jpg", "Casual", "The Field", "Customised to every campaign, aimed at the woman it was cut for",
             "A pleated sleeve, a dry field, a wide pale sky.",
             ["#2A2430", "#F2EFEA", "#C8A97A", "#B9B4AE"],
             "Ready-to-wear sells a life. Open daylight lets the pleat move and the woman lead."),
        ],
    },
    "dubai": {
        "city": "Dubai",
        "chapter": "Chapter 02",
        "tagline": "where the collection is wanted",
        "italic": "The Gulf's buying capital. A gown here must read as wealth of work, from a phone screen to a ballroom wall.",
        "films": [
            ("film-dubai.jpg", "films/dubai-16.mp4", "Couture", "16 s"),
        ],
        "acts": [
            ("couture.jpg", "Couture", "The Mosaic", "Shot on the mosaic rather than in front of it",
             "Haute couture laid on the legendary patterns of Versace.",
             ["#3B2C20", "#B08A5A", "#E7DCCB", "#6B5A48"],
             "Myth underfoot, handwork above. The floor is ornament; the gown is the answer."),
            ("editorial.jpg", "Editorial", "The Plumes", "Flowers are composed, not picked",
             "The pampas circle was the loud moment.",
             ["#1F4A3A", "#3C7A5E", "#E6D3B0", "#7FA7D1"],
             "Feather echoed by plume. Nature repeats the texture, so the eye stays on the craft."),
            ("bridal.jpg", "Bridal", "The Desert Train", "Bridal carried into open desert",
             "A desert oasis, and the shimmering allure of crystals.",
             ["#E9E2D6", "#CDBB9E", "#A7957C", "#DCE4EA"],
             "Sun behind her, nothing to hide behind. Crystal and tulle lit by the desert alone."),
        ],
    },
    "barcelona": {
        "city": "Barcelona",
        "chapter": "Chapter 06",
        "tagline": "where it breathes",
        "italic": "Europe's bridal capital. Mediterranean light and modernist stone, for romance without sentiment.",
        "films": [
            ("film-barcelona.jpg", "films/barcelona-16.mp4", "Bridal", "15 s"),
        ],
        "acts": [
            ("bridal.jpg", "Bridal", "The Staircase", "Wedding shot in open daylight rather than a studio",
             "Dare to dream. Dare to rise.",
             ["#F1ECE6", "#C9B79C", "#8F7B62", "#5E5A4A"],
             "Veil and stair draw one long line. The architecture carries the grandeur; she stays still."),
            ("editorial.jpg", "Editorial", "The Pavilion", "Modernist stone at Mediterranean noon",
             "Timeless romance in Barcelona's hidden gardens.",
             ["#14141A", "#F2EFE6", "#C8B48C", "#7D7266"],
             "Black and ivory against carved stone. A silhouette bold enough for noon light."),
            ("evening.jpg", "Evening", "The Colonnade", "Two frames, silver against stone",
             "Where Lebanese couture meets the city's timeless beauty.",
             ["#5A6E9E", "#C9C6CF", "#B98C66", "#E8D9C6"],
             "Low sun along the columns. Every crystal becomes a moving highlight."),
        ],
    },
    "milano": {
        "city": "Milano",
        "chapter": "Chapter 04",
        "tagline": "where it is sold",
        "italic": "Fashion's marketplace. Where a collection becomes an order: the runway, the showroom, the buyer's linesheet.",
        "films": [("film-milano.jpg", "films/milano.mp4", "Couture", "14 s")],
        "acts": [
            ("couture.jpg", "Couture", "The Frescoes", "A palazzo where the ceiling competes with the gown",
             "Painting with light, and three hundred years of dialogue.",
             ["#481806", "#874A2D", "#E3A9B4", "#C8A35A"],
             "Painted flowers above, embroidered ones below. The light gives the win to the gown."),
            ("editorial.jpg", "Editorial", "The Window", "One gesture the height of the room",
             "Black feathers, gold brocade, embroidery laid like armour.",
             ["#1A0E0D", "#77462C", "#C9A77A", "#E8DFD2"],
             "Arms open, the palazzo behind her. A silhouette an editor remembers."),
            ("bridal.jpg", "Bridal", "The Rotunda", "The room turned into the frame of the train",
             "Organza, lace, pearl. The walls leaned in to listen.",
             ["#2D1D0F", "#89745F", "#D9CEC0", "#F2EEE6"],
             "Window light keeps the white pure. Symmetry gives the gown the weight of a ceremony."),
        ],
    },
    "istanbul": {
        "city": "Istanbul",
        "chapter": "Chapter 05",
        "tagline": "where it crosses",
        "italic": "The bridge between East and West. A collection made here must speak to Riyadh and Milan in one frame.",
        "films": [("film-istanbul.jpg", "films/istanbul.mp4", "Couture", "13 s")],
        "acts": [
            ("couture.jpg", "Couture", "The Workshop", "The gown among the tools of the room",
             "Vintage moods, a modern lens, eternity in a single frame.",
             ["#141C4A", "#2A3A7A", "#3F2A2C", "#C98A3A"],
             "Midnight satin under one lamp. The working room tells how much hand went into it."),
            ("editorial.jpg", "Editorial", "The Forest Floor", "Autumn leaves as the only set",
             "Coral silk on copper leaves.",
             ["#C87971", "#E8C9D2", "#824635", "#572418"],
             "One colour answering autumn. From above, the skirt opens like petals."),
            ("bridal.jpg", "Bridal", "The Grand Stair", "A bride between two traditions",
             "A love story written in the light of chandeliers.",
             ["#2D201B", "#5D483E", "#D8CDBE", "#F0EADF"],
             "Twin stairs under one chandelier. East and West held in one symmetry."),
        ],
    },
    "paris": {
        "city": "Paris",
        "chapter": "Chapter 03",
        "tagline": "where it is judged",
        "italic": "Couture's highest court. A Paris image is made to survive an editor with forty collections on her desk.",
        "films": [
            ("film-couture.jpg", "films/paris-couture.mp4", "Couture", "24 s"),
            ("film-show.jpg", "films/paris-fashion-show.mp4", "Fashion show", "23 s"),
        ],
        "acts": [
            ("show.jpg", "Fashion show", "The Courtyard", "Haussmann interiors, then the courtyard show",
             "Not a gown. A presence.",
             ["#E9D9B8", "#B8862E", "#2E3FA0", "#9A8C7E"],
             "The show in open daylight. The line reads as one idea, the front row as proof it was real."),
            ("editorial.jpg", "Editorial", "The Château", "A gown in the company of stone that has waited longer",
             "One silhouette, a ch\u00e2teau across the water.",
             ["#5B6362", "#868D90", "#B2B5B6", "#E1E3E3"],
             "Stone, water and a grey sky in one cool family. Nothing competes with the embroidery."),
            ("casual.jpg", "Casual", "Off Duty", "The register that humanises a house",
             "A beret, a white collar, a column at her back.",
             ["#302922", "#554933", "#827156", "#C5B4A2"],
             "Couture earns respect; ready-to-wear earns desire. The woman the collection was cut for, living in it."),
        ],
    },
}

F_SERIF = "font-family:'EB Garamond',Georgia,'Times New Roman',serif"
F_SANS = "font-family:Archivo,Helvetica,Arial,sans-serif"
KICK = F_SANS + ";font-size:10px;letter-spacing:2.6px;text-transform:uppercase;color:#9A7B2E"
ROMAN = ["I", "II", "III"]


FILM_WORDS = {0: "", 1: "a film and ", 2: "two films and "}


def wa(house, text):
    return f"https://wa.me/{WA}?text=" + quote(f"Hello Charbel, {house} here. {text}")


def strip(colors):
    cells = "".join(f'<td height="6" bgcolor="{c}" style="font-size:0;line-height:0">&nbsp;</td>' for c in colors)
    return f'<table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0" style="margin:14px 0 12px"><tr>{cells}</tr></table>'


def act(key, house, i, a):
    img, register, name, sub, line, colors, concept = a
    link = wa(house, f"For {COUNTRIES[key]['city']} we choose {ROMAN[i]} · {name}.")
    return f'''<tr><td style="padding:0 0 34px"><table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0"><tr><td width="200" valign="top"><a href="{link}"><img src="{IMG}/acts/mail/{key}/{img}?v={V}" width="200" height="300" alt="{register}, {name}" style="display:block;border:0;width:200px;height:auto"></a></td><td width="24">&nbsp;</td><td valign="top"><div style="{KICK};font-size:9px">{ROMAN[i]} · {register}</div><div style="{F_SERIF};font-size:28px;line-height:1.06;color:#1E1C18;padding:8px 0 4px">{name}</div><div style="{F_SERIF};font-style:italic;font-size:13px;color:#8A8478;padding-bottom:10px">{sub}</div><div style="{F_SERIF};font-style:italic;font-size:16px;line-height:1.42;color:#4A4740">{line}</div>{strip(colors)}<div style="{F_SERIF};font-size:14px;line-height:1.5;color:#4A4740"><span style="{KICK};font-size:8px">Why it works</span>&nbsp; {concept}</div><table role="presentation" width="170" cellpadding="0" cellspacing="0" border="0" style="margin-top:16px"><tr><td><a href="{link}" style="display:block;padding:14px 0;{F_SANS};font-size:10px;font-weight:bold;letter-spacing:2.6px;text-transform:uppercase;text-decoration:none;text-align:center;background:#FFFFFF;color:#1E1C18;border:1px solid #9A7B2E;">This one &rarr;</a></td></tr></table></td></tr></table></td></tr>'''


def films_block(key, city, films):
    if not films:
        return ""
    head = f'<tr><td style="padding:26px 32px 8px">\n <div style="{KICK};padding-bottom:14px">{"Two films" if len(films) == 2 else "The film"} · {city}</div>\n'
    if len(films) == 1:
        p, m, l, d = films[0]
        return head + f' <a href="{SITE}/films/watch/{m[6:-4]}/?r=em-{key}"><img src="{IMG}/acts/mail/{key}/{p}?v={V}" width="300" height="533" alt="{city} · {l} film, plays with sound" style="display:block;border:0;width:100%;max-width:300px;height:auto"></a>\n <div style="{KICK};font-size:9px;padding-top:9px">&#9654;&nbsp; {l} · {d}</div>\n</td></tr>\n'
    cells, caps = [], []
    for n, (p, m, l, d) in enumerate(films):
        if n: cells.append('<td width="8" style="font-size:0">&nbsp;</td>'); caps.append('<td></td>')
        cells.append(f'<td width="264" valign="top"><a href="{SITE}/films/watch/{m[6:-4]}/?r=em-{key}"><img src="{IMG}/acts/mail/{key}/{p}?v={V}" width="264" height="469" alt="{city} · {l} film, plays with sound" style="display:block;border:0;width:100%;max-width:264px;height:auto"></a></td>')
        caps.append(f'<td style="{KICK};font-size:9px;padding-top:9px">&#9654;&nbsp; {l} · {d}</td>')
    return head + ' <table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0"><tr>' + "".join(cells) + '</tr><tr>' + "".join(caps) + '</tr></table>\n</td></tr>\n'


def build(key, house="{House}"):
    c = COUNTRIES[key]
    city = c["city"]
    slug = re.sub(r"[^a-z0-9]+", "", house.lower()) or "house"
    films = films_block(key, city, c["films"])
    acts = "".join(act(key, house, i, a) for i, a in enumerate(c["acts"]))
    cal = f"https://calendly.com/studiocharbelmsallem/concept-call-10-min?a1={quote(house + ' · ' + city + ' concept call')}&utm_source=mail&utm_campaign={key}-{slug}"
    return f'''<div style="{F_SERIF};font-size:17px;line-height:1.55;color:#1E1C18">Dear {house},<br><br>This is the {city} chapter of the book, opened for you: {FILM_WORDS[len(c['films'])]}the three registers a collection can be told in here, with a few lines on why each one works. Tell me which register is closest to your next season, and I will build the first frames around it.<br><br></div>
<table role="presentation" width="600" cellpadding="0" cellspacing="0" border="0" style="width:100%;max-width:600px;border-collapse:collapse;background:#FFFFFF;border:1px solid #E6DCC4">
<tr><td style="padding:22px 32px 0">
 <table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0" style="border-bottom:1px solid #E6DCC4"><tr><td style="padding-bottom:14px;{F_SERIF};font-size:14px;letter-spacing:3.4px;text-transform:uppercase;color:#1E1C18">Charbel Msallem<span style="color:#9A7B2E">&nbsp;&nbsp;|&nbsp;&nbsp;</span><span style="{F_SANS};font-size:9px;letter-spacing:2.2px;color:#9A7B2E">Fashion Photographer &amp; Film Director</span></td></tr></table>
</td></tr>
<tr><td style="padding:30px 32px 6px">
 <div style="{KICK}">For {house} · {c["chapter"]} · {city}</div>
 <div style="{F_SERIF};font-size:44px;line-height:1.04;color:#1E1C18;padding:12px 0 16px">{city},<br><i style="color:#9A7B2E">{c["tagline"]}</i>.</div>
 <table role="presentation" width="120" cellpadding="0" cellspacing="0" border="0"><tr><td height="1" bgcolor="#9A7B2E" style="font-size:0;line-height:0">&nbsp;</td></tr></table>
 <div style="{F_SERIF};font-style:italic;font-size:18px;line-height:1.45;color:#4A4740;padding:16px 0 4px">{c["italic"]}</div>
</td></tr>
{films}<tr><td style="padding:26px 32px 0">
 <table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0" style="border-bottom:1px solid #E6DCC4;margin-bottom:26px"><tr><td style="{KICK};padding-bottom:12px">Choose the register</td><td align="right" style="{F_SANS};font-size:9px;letter-spacing:2.2px;text-transform:uppercase;color:#8A8478;padding-bottom:12px">The mood board</td></tr></table>
 <table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0">{acts}</table>
</td></tr>
<tr><td bgcolor="#F7F4EC" style="background:#F7F4EC;padding:30px 32px 32px">
 <div style="{F_SERIF};font-size:26px;line-height:1.22;color:#1E1C18;padding-bottom:20px"><span style="{F_SANS};font-size:10px;letter-spacing:2.6px;text-transform:uppercase;color:#9A7B2E;display:block;padding-bottom:12px">Architect your campaign</span>Pick one. The first frames follow within <i style="color:#9A7B2E">48 hours</i>, every pixel choreographed, made only for {house}.</div>
 <table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0"><tr>
  <td width="49%"><a href="{cal}&utm_content=inline" style="display:block;padding:14px 0;{F_SANS};font-size:10px;font-weight:bold;letter-spacing:2.6px;text-transform:uppercase;text-decoration:none;text-align:center;background:#9A7B2E;color:#FFFFFF;">Reserve 10 minutes &rarr;</a></td><td width="2%">&nbsp;</td>
  <td width="49%"><a href="{SITE}/?r=em-{key}-{slug}#chapters" style="display:block;padding:14px 0;{F_SANS};font-size:10px;font-weight:bold;letter-spacing:2.6px;text-transform:uppercase;text-decoration:none;text-align:center;background:#FFFFFF;color:#1E1C18;border:1px solid #9A7B2E;">The {city} chapter &rarr;</a></td>
 </tr></table>
</td></tr>
<tr><td style="padding:20px 32px 22px;border-top:1px solid #E6DCC4">
 <div style="{F_SERIF};font-size:15px;line-height:1.5;color:#1E1C18"><i>Let's create magic together.</i><br><br>Warm regards,<br><span style="letter-spacing:3px;text-transform:uppercase;font-size:13px">Charbel Msallem</span> <span style="color:#8A8478">· Fashion Photographer &amp; Film Director</span></div>
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
