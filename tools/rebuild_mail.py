#!/usr/bin/env python3
"""Rebuild every unsent outreach mail in the approved designs (2 Nov 2026).

    python3 tools/rebuild_mail.py

First touch : x/mail-<slug>.html       six cities, master = x/mail-tskaff.html
Second touch: x/mail-paris-<slug>.html the Paris mood board
Writes x/queue.json: slug, house, to, subject, touch, file, due.
"""
import json, pathlib, re, shutil, sys
from urllib.parse import quote
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from country_mail import build

ROOT = pathlib.Path(__file__).resolve().parent.parent
X = ROOT / "x"

# slug, house, greeting, to
FIRST = [
    ("tskaff", "TSKAFF", "TSKAFF", "customercare@tskaff.com"),
    ("hebaalqurashi", "Heba Alqurashi", "Heba", "Pr@hebaalqurashi.com"),
    ("ehsanchamoun", "Ehsan Chamoun", "Ehsan", "info@ehsanchamoun.com"),
]

# slug, house, greeting, to, due
SECOND = [
    ("wadha", "Wadha", "Wadha", "info@wadha.co", "2026-11-03"),
    ("sarapedram", "Sara Pedram", "Sara", "info@sarapedram.com", "2026-11-03"),
    ("timaabid", "Tima Abid", "Tima", "info@timaabid.com", "2026-11-03"),
    ("adnanakbar", "Adnan Akbar", "Adnan", "info@adnanakbar.com", "2026-11-03"),
    ("emanalajlan", "Eman Alajlan", "Eman", "info@emanalajlan.co", "2026-11-03"),
    ("qirdala", "Qirdala", "Qirdala", "info@qirdala.com", "2026-11-03"),
    ("ranizakhem", "Rani Zakhem", "Rani", "info@ranizakhem.com", "2026-11-03"),
    ("mukhisisters", "Mukhi Sisters", "Mukhi Sisters", "info@mukhisisters.com", "2026-11-03"),
    ("khawlaalaiban", "Khawla Alaiban", "Khawla", "info@khawlaalaiban.co", "2026-11-03"),
    ("ronyabouhamdan", "Rony Abou Hamdan", "Rony", "info@ronyabouhamdan.com", "2026-11-03"),
    ("manel", "Manel", "Manel", "customercare@manel-fashion.com", "2026-11-03"),
    ("oscarkraye", "Oscar Kraye", "Haidar", "press@oscarkraye.com", "2026-11-04"),
    ("geyannayouness", "Geyanna Youness", "Geyanna", "info@geyannayouness.com", "2026-11-04"),
    ("hassidriss", "Hass Idriss", "Hassan", "press@hassidriss.com", "2026-11-04"),
    ("ikhfashion", "IKH", "Khadeejah", "customerservice@ikhfashion.sa", "2026-11-05"),
    ("ferhanturker", "Ferhan Türker", "Ferhan", "ferhan.turker.hautecoture@gmail.com", "2026-11-05"),
    ("aleensabbagh", "Aleen Sabbagh", "Aleen and Natalie", "Customercare@aleensabbagh.com", "2026-11-06"),
    ("hadikatra", "Hadi Katra", "Hadi", "info@hadikatra.com", "2026-11-06"),
    ("rebirth", "Rebirth", "Tala", "connect@rebirth.sa", "2026-11-06"),
    ("reemalkanhal", "Reem Alkanhal", "Reem", "ReemAlkanhal@outlook.com", "2026-11-06"),
    ("renaissancerenaissance", "Renaissance Renaissance", "Cynthia", "hello@renaissancerenaissance.com", "2026-11-06"),
    ("shakhsia", "Shakhsia", "Fatima", "info@shakhsia-design.com", "2026-11-06"),
    ("tallermarmo", "Taller Marmo", "Taller Marmo team", "press@tallermarmo.com", "2026-11-06"),
    ("ziyadbuainain", "Ziyad Buainain", "Ziyad", "press@ziyadbuainain.com", "2026-11-06"),
    ("hanayencouture", "Hanayen Couture", "Hanan", "info@hanayencouture.com", "2026-11-06"),
    ("manaalalhammadi", "Manaal Al Hammadi", "Manaal", "aa@manaalalhammadi.com", "2026-11-06"),
    ("samiragallery", "Samira Gallery", "Samira", "samirahalawani3@gmail.com", "2026-11-06"),
    ("daralhanouf", "Dar Al Hanouf", "Dar Al Hanouf team", "info@daralhanouf.com", "2026-11-09"),
    ("noursabi", "Nour Sabi", "Nour", "contact@noursabi.com", "2026-11-09"),
    ("antonios", "Antonios Couture", "Ghassan", "ga@antonioscouture.com", "2026-11-24"),
    ("basilsoda", "Basil Soda", "Basil Soda team", "customercare@basilsoda.com", "2026-11-24"),
    ("francksorbier", "Franck Sorbier", "Maison Franck Sorbier", "hautecouturefrancksorbier@gmail.com", "2026-11-24"),
    ("jasive", "Jasive", "Jasive team", "atencion@jasive.com", "2026-11-24"),
    ("laithmaalouf", "Laith Maalouf", "Laith", "laithmaalouf.sr@gmail.com", "2026-11-24"),
    ("maisonberrada", "Maison Berrada", "Maison Berrada", "contact.maisonberrada@gmail.com", "2026-11-24"),
    ("maisonrabihkayrouz", "Maison Rabih Kayrouz", "Maison Rabih Kayrouz", "sales@maisonrabihkayrouz.com", "2026-11-24"),
    ("monyibrahim", "Mony Ibrahim", "Mony", "mony.ibrahim@hotmail.com", "2026-11-24"),
    ("taghridelhage", "Taghrid El Hage", "Taghrid", "taghrid@taghridelhage.com", "2026-11-24"),
    ("youssefkamoun", "Youssef Kamoun", "Youssef", "shop@youssefkamoun.com", "2026-11-24"),
]

FILM = {"milano": 'Milano', "istanbul": 'Istanbul'}


def add_films(s):
    """Milano and Istanbul: the second tile becomes the film cover, as for the other cities."""
    for key, city in FILM.items():
        s = re.sub(
            rf'<img src="([^"]*)/acts/mail/couture/{key}-2\.jpg\?v=\d+" width="236" height="296" alt="{city}, photograph" '
            r'style="display:block;border:0;width:236px;height:296px;margin:0 auto"></a></td></tr><tr>'
            r'(<td align="center"[^>]*>)Photograph</td><td></td>(<td align="center"[^>]*>)[^<]*</td>',
            lambda m: (f'<img src="{m[1]}/acts/mail/couture/film-{key}.jpg?v=6" width="175" height="312" alt="{city}, film, plays with sound" '
                       'style="display:block;border:0;width:175px;height:312px;margin:0 auto"></a></td></tr><tr>'
                       f'{m[2]}Photograph</td><td></td>{m[3]}&#9654;&nbsp; Film</td>'),
            s)
    return s


def house_page(slug, house):
    src = (ROOT / "acts" / "tskaff" / "index.html").read_text()
    out = ROOT / "acts" / slug
    out.mkdir(exist_ok=True)
    (out / "index.html").write_text(src.replace("TSKAFF", house).replace("tskaff", slug).replace(f"h={house}&", f"h={quote(house)}&"))


def main():
    master = add_films((X / "mail-tskaff.html").read_text())
    queue = []
    for slug, house, greet, to in FIRST:
        if slug != "tskaff":
            house_page(slug, house)
        s = master.replace("Dear TSKAFF,", f"Dear {greet},").replace("TSKAFF", house).replace("tskaff", slug)
        s = s.replace(f"h={house}&", f"h={quote(house)}&")
        (X / f"mail-{slug}.html").write_text(s)
        queue.append(dict(slug=slug, house=house, to=to, subject=f"{house}, in six cities", touch=1,
                          file=f"x/mail-{slug}.html", due="2026-11-02"))
    for slug, house, greet, to, due in SECOND:
        s = build("paris", house)
        s = s.replace(f"Dear {house},", f"Dear {greet},", 1)
        s = re.sub(r"r=em-paris(-[a-z0-9-]*)?", f"r=em-{slug}", s)
        (X / f"mail-paris-{slug}.html").write_text(s)
        queue.append(dict(slug=slug, house=house, to=to, subject=f"{house}, Paris in three registers", touch=2,
                          file=f"x/mail-paris-{slug}.html", due=due))
    (X / "queue.json").write_text(json.dumps(queue, ensure_ascii=False, indent=1))
    print(len(queue))


if __name__ == "__main__":
    main()
