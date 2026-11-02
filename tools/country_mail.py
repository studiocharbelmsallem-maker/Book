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
        "italic": "A city that keeps losing its electricity and never its standard. Here the studio learned to decide instead of decorate: one source, one hour, no second day.",
        "films": [
            ("film-couture.jpg", "films/beirut-couture.mp4", "Couture", "17 s"),
            ("film-casual.jpg", "films/beirut-casual.mp4", "Casual", "12 s"),
        ],
        "acts": [
            ("couture.jpg", "Couture", "The Atelier", "Red-carpet weight, shot for the moment before the flashbulb",
             "Industrial dreams meet couture fantasy. Elegance emerges from the machinery.",
             ["#3A2A22", "#B79AAE", "#8C6A5A", "#D9C3B6"],
             "Couture is judged on construction, so the light must explain it. One hard source, low and to the side, draws every fold and leaves the room in shadow. Nothing in the frame is brighter than the dress. The handwork becomes the only thing the eye can read."),
            ("editorial.jpg", "Editorial", "The Coast", "Winter couture walked across raw Beirut stone",
             "Soft fabric against rough stone. The rocky coastline becomes a runway.",
             ["#2B2420", "#6E5A4C", "#E8E4DE", "#8FA6B2"],
             "An editorial gives a collection a place to belong. Pale beadwork on dark rock is the strongest contrast nature offers: it reads at three metres and rewards at thirty centimetres. The cliff gives the train its scale. The open sky keeps the frame calm."),
            ("casual.jpg", "Casual", "The Field", "Customised to every campaign, aimed at the woman it was cut for",
             "A pleated sleeve, a dry field, a wide pale sky. A life, not an occasion.",
             ["#2A2430", "#F2EFEA", "#C8A97A", "#B9B4AE"],
             "Ready-to-wear sells a life, not an occasion. Out of the studio, in open daylight, pleats move with the wind and fabric shows its true weight. White, straw and sky. The silhouette leads, and the image reads in one breath on a phone."),
        ],
    },
    "dubai": {
        "city": "Dubai",
        "chapter": "Chapter 02",
        "tagline": "where the collection is wanted",
        "italic": "The Gulf does not ask a gown to be quiet. Every frame here has to survive two distances: a phone held at arm's length, and a print three metres wide.",
        "films": [
            ("film-dubai.jpg", "films/dubai-16.mp4", "Couture", "16 s"),
        ],
        "acts": [
            ("couture.jpg", "Couture", "The Mosaic", "Shot on the mosaic rather than in front of it",
             "Haute couture laid on the legendary patterns of Versace.",
             ["#3B2C20", "#B08A5A", "#E7DCCB", "#6B5A48"],
             "In the Gulf a gown is read as wealth of work, so the handwork needs an equal partner. Shot from above, on a floor that took years to lay, the frame becomes ornament with the dress at its centre. Warm stone keeps gold and ivory rich without one added light."),
            ("editorial.jpg", "Editorial", "The Plumes", "Flowers are composed, not picked",
             "The pampas circle was the loud moment. The handwork finishes the story alone.",
             ["#1F4A3A", "#3C7A5E", "#E6D3B0", "#7FA7D1"],
             "The desert leaves nowhere to hide. Hard sun and a clean sky give colour the clarity of print, and the pampas repeats the texture of the gown in nature. Handwork answering handwork. One bold colour against sand stops the eye in the first second."),
            ("bridal.jpg", "Bridal", "The Desert Train", "Bridal carried into open desert",
             "A desert oasis in reflection, and the shimmering allure of crystals.",
             ["#E9E2D6", "#CDBB9E", "#A7957C", "#DCE4EA"],
             "Bridal is sold on light more than on the dress. With the sun behind her, tulle turns translucent and every crystal finds its own highlight. The dunes give the train the length it was cut for. Sand tones keep the white pure, never grey."),
        ],
    },
    "barcelona": {
        "city": "Barcelona",
        "chapter": "Chapter 06",
        "tagline": "where it breathes",
        "italic": "Mediterranean daylight and modernist stone. Light that forgives nothing and flatters everything, used at the hours when it is honest.",
        "films": [
            ("film-barcelona.jpg", "films/barcelona-16.mp4", "Bridal", "15 s"),
        ],
        "acts": [
            ("bridal.jpg", "Bridal", "The Staircase", "Wedding shot in open daylight rather than a studio",
             "Dare to dream. Dare to rise. Shot in Barcelona, designed in Turkey, envisioned in Lebanon.",
             ["#F1ECE6", "#C9B79C", "#8F7B62", "#5E5A4A"],
             "Romance without sentiment is a matter of restraint. The architecture carries the grandeur and the bride stays still, so veil and stair draw one long line. Morning light on warm stone keeps the white soft and the skin true."),
            ("editorial.jpg", "Editorial", "The Pavilion", "Modernist stone at Mediterranean noon",
             "Timeless romance in Barcelona's hidden gardens, every detail a story of modern glamour.",
             ["#14141A", "#F2EFE6", "#C8B48C", "#7D7266"],
             "A strong silhouette needs a strong setting. From below, the gown rises against carved busts and garlands, and the frame turns graphic: black, ivory, sand. Noon light is unforgiving, so we use it only where the shape is bold enough to take it."),
            ("evening.jpg", "Evening", "The Colonnade", "Two frames, silver against stone",
             "Where the artistry of Lebanese couture meets the city's timeless beauty.",
             ["#5A6E9E", "#C9C6CF", "#B98C66", "#E8D9C6"],
             "Evening wear lives in movement and catch-light. Low sun along the colonnade turns every fringe and crystal into a moving highlight as she walks, and warm columns frame the cool blue of the gown. The frame sells the dress before anyone touches it."),
        ],
    },
    "milano": {
        "city": "Milano",
        "chapter": "Chapter 04",
        "tagline": "where it is sold",
        "italic": "The marble has seen kings. In Milano a collection walks into rooms that have judged centuries of beauty, and it has to hold there: on the runway, in the showroom, on the page. Old stone. New devotion.",
        "films": [("film-milano.jpg", "films/milano.mp4", "Couture", "14 s")],
        "acts": [
            ("couture.jpg", "Couture", "The Frescoes", "A palazzo where the ceiling competes with the gown",
             "Painting with light, emotion and three hundred years of dialogue. The dress is only the beginning.",
             ["#481806", "#874A2D", "#E3A9B4", "#C8A35A"],
             "In a palazzo the ceiling competes with the gown, and the gown must win. The room stays warm and low, the chandeliers fall away, the brightest light goes to the embroidery. Every flower reads before the ceiling does, on a showroom wall and on a phone."),
            ("editorial.jpg", "Editorial", "The Window", "One gesture the height of the room",
             "Black feathers, gold brocade, embroidery laid like armour. The walls still listening.",
             ["#1A0E0D", "#77462C", "#C9A77A", "#E8DFD2"],
             "An editorial gives a collection its attitude. Shot low in a tall window, the black silhouette takes the height of the palazzo, and the daylight behind her cuts the shape clean against gold walls. One strong line is what an editor remembers from forty pages."),
            ("bridal.jpg", "Bridal", "The Rotunda", "The room turned into the frame of the train",
             "The marble has seen kings. It had never seen this.",
             ["#2D1D0F", "#89745F", "#D9CEC0", "#F2EEE6"],
             "Bridal is sold on the length of one moment. We step back and let the rotunda work: dark floor, tall windows, the train laid in a full circle at her feet. Window light keeps the white pure. Symmetry gives the gown the weight of a ceremony."),
        ],
    },
    "istanbul": {
        "city": "Istanbul",
        "chapter": "Chapter 05",
        "tagline": "where it crosses",
        "italic": "East and west arguing politely, in silk. A collection directed here has to read in two markets at once, from Riyadh to Milan, without apologising to either.",
        "films": [("film-istanbul.jpg", "films/istanbul.mp4", "Couture", "13 s")],
        "acts": [
            ("couture.jpg", "Couture", "The Workshop", "The gown among the tools of the room",
             "Vintage moods, a modern lens, eternity in a single frame.",
             ["#141C4A", "#2A3A7A", "#3F2A2C", "#C98A3A"],
             "Couture earns its price in construction, and satin hides nothing. One warm lamp draws the long folds of the navy and leaves the walls in shadow. The working room behind her says how much hand went into it. The beaded hem stays at the floor, where a buyer looks last."),
            ("editorial.jpg", "Editorial", "The Forest Floor", "Autumn leaves as the only set",
             "Coral silk on copper leaves. Autumn as the only set.",
             ["#C87971", "#E8C9D2", "#824635", "#572418"],
             "Nature gives its strongest palette when one colour is allowed to answer it. Coral against fallen copper stays warm yet separates clean, and from above the layers of the skirt open like petals. Soft shade keeps the skin true and the sheen intact."),
            ("bridal.jpg", "Bridal", "The Grand Stair", "A bride between two traditions",
             "A love story written in the light of chandeliers.",
             ["#2D201B", "#5D483E", "#D8CDBE", "#F0EADF"],
             "An Istanbul bride speaks to two traditions at once. Centred between twin stairs under the chandelier, she lets symmetry carry the ceremony, and the long sleeves and beaded column read as one quiet line. The room gives the grandeur. The gown stays the only light thing in it."),
        ],
    },
    "paris": {
        "city": "Paris",
        "chapter": "Chapter 03",
        "tagline": "where it is judged",
        "italic": "Couture week is a room that has already seen everything. A Paris image is not shot to please; it is shot to survive an editor with forty other collections open on her desk.",
        "films": [
            ("film-couture.jpg", "films/paris-couture.mp4", "Couture", "24 s"),
            ("film-show.jpg", "films/paris-fashion-show.mp4", "Fashion show", "23 s"),
        ],
        "acts": [
            ("show.jpg", "Fashion show", "The Courtyard", "Haussmann interiors, then the courtyard show",
             "Not a gown. A presence. Five women enter Paris in sculpted light.",
             ["#E9D9B8", "#B8862E", "#2E3FA0", "#9A8C7E"],
             "A show image has one job: to make the collection read as a single idea before it reads as pieces. We shoot the courtyard show in open daylight, with the next looks queued in soft focus behind the first, so the eye reads the sequence of the collection in one frame. Sunlight is honest with fabric: silk keeps its sheen, construction keeps its edges, and the front row's phones in the frame say the moment was real."),
            ("editorial.jpg", "Editorial", "The Château", "A gown in the company of stone that has waited longer",
             "One silhouette, a château across the water, a grey sky that flatters silk.",
             ["#5B6362", "#868D90", "#B2B5B6", "#E1E3E3"],
             "An editorial is the frame that puts a house on a page instead of in a feed. Northern light is soft and directional, so texture survives on print and on a phone. We keep the palette in one cool family, stone, water, sky, so nothing in the frame competes with the dress, and the embroidery becomes the only detail the eye returns to."),
            ("casual.jpg", "Casual", "Off Duty", "The register that humanises a house",
             "The same city on a Tuesday: a beret, a white collar, a column at her back.",
             ["#302922", "#554933", "#827156", "#C5B4A2"],
             "Couture earns respect; ready-to-wear earns desire. The casual register shows the woman the collection was cut for, living in it. We shoot it in passing daylight against architecture, so the clothes feel worn rather than styled, and we keep the tones earthy and close so the image reads as one breath in the first second of a Reel."),
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
