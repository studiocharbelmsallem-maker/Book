"""SEO pass for the Book site. Run from the repo root.
BASE is the live address today; swap to https://charbelmsallem.net/ when the domain points at GitHub."""
import json, re, sys

BASE = sys.argv[1] if len(sys.argv) > 1 else "https://studiocharbelmsallem-maker.github.io/Book/"
EMAIL = "admin@charbelmsallem.net"
IG = "https://www.instagram.com/charbelmsallemstudios/"
PHONE = "+96191729713"

LOGOS = {
 15:"Paris Fashion Week",16:"Milano Fashion Week",17:"Dubai Fashion Week",18:"Beirut Fashion Week",
 19:"Elie Saab",20:"Dovita Milano",21:"Bvlgari",22:"Saiid Kobeisy",23:"La Bourjoisie",24:"Terani Couture",
 25:"Mitra Couture",26:"Marwan",27:"Yeprem",28:"Voyageur",29:"Damas",30:"Charmaleena",31:"Zoughaib & Co.",
 32:"Mimia Leblanc",33:"Bianca Nera",34:"Scarbina",35:"Haifa",36:"Ramy Ayach",37:"Tony Ward",38:"Michael Cinco",
 39:"Sharbel Azar",40:"Gaby Charbachy",41:"Gosace Couture",42:"Dana Al Mulla",43:"Layla Line",44:"District 5 Luxe",
 45:"Bilal El Dana",46:"Maria Pino",47:"Narin Moda",48:"Reema Cherfan",49:"Dar Sara",50:"Reema Moula",
 51:"Elham",52:"Missaki",53:"Kevork",54:"Elie Feghali",55:"Manal Ajaj",
}
CITY = {"ch01":"Beirut","ch02":"Dubai","ch03":"Paris","ch04":"Milano","ch05":"Istanbul","ch06":"Barcelona","ch07":"Jewellery"}
SUBJECT = {"Jewellery":"Jewellery campaign"}

def esc(t):
    return t.replace("&","&amp;").replace('"',"&quot;").replace("<","&lt;").replace(">","&gt;")

def clean(t):
    t = re.sub(r"<[^>]+>","",t); t = re.sub(r"\s+"," ",t).replace("&nbsp;"," ").strip()
    return t

def short(cap, n=110):
    cap = clean(cap).replace("&amp;","&")
    first = re.split(r"(?<=[.;])\s", cap)[0].rstrip(".;")
    if len(first) > n: first = first[:n].rsplit(" ",1)[0]
    return first

def org_graph(page_url, page_name, page_desc, image):
    return {"@context":"https://schema.org","@graph":[
      {"@type":["ProfessionalService","Organization"],"@id":BASE+"#studio","name":"Charbel Msallem Studios",
       "url":BASE,"logo":BASE+"cover.jpg","image":image,"email":EMAIL,"telephone":PHONE,
       "description":"Fashion films and couture campaign photography for couture houses and jewellery maisons — concept, filming, photography and full production. Arabic couture, seen with a European eye.",
       "foundingDate":"2012","founder":{"@id":BASE+"#charbel"},
       "address":{"@type":"PostalAddress","addressLocality":"Beirut","addressCountry":"LB"},
       "areaServed":[{"@type":"City","name":c} for c in ["Beirut","Dubai","Paris","Milan","Istanbul","Barcelona","Doha","Kuwait City"]],
       "knowsAbout":["Fashion film","Couture campaign photography","Jewellery photography","Fashion week coverage","Bridal campaigns","Creative direction"],
       "sameAs":[IG]},
      {"@type":"Person","@id":BASE+"#charbel","name":"Charbel Msallem","jobTitle":"Fashion photographer and film director",
       "worksFor":{"@id":BASE+"#studio"},"url":BASE,"sameAs":[IG]},
      {"@type":"WebSite","@id":BASE+"#site","url":BASE,"name":"Charbel Msallem Studios","publisher":{"@id":BASE+"#studio"},"inLanguage":"en"},
      {"@type":"WebPage","@id":page_url+"#page","url":page_url,"name":page_name,"description":page_desc,
       "isPartOf":{"@id":BASE+"#site"},"about":{"@id":BASE+"#studio"},"primaryImageOfPage":image,"inLanguage":"en"},
    ]}

def set_head(s, title, desc, url, image, image_alt, noindex=False, graph=True):
    head_end = s.find("</head>")
    head = s[:head_end]
    # title
    if re.search(r"<title>.*?</title>", head, re.S):
        head = re.sub(r"<title>.*?</title>", f"<title>{esc(title)}</title>", head, count=1, flags=re.S)
    else:
        head = head.replace('<meta charset="utf-8">', f'<meta charset="utf-8">\n<title>{esc(title)}</title>', 1)
    head = re.sub(r'<meta name="description" content="[^"]*">', f'<meta name="description" content="{esc(desc)}">', head, count=1)
    head = re.sub(r'<meta property="og:url" content="[^"]*">\n?', "", head)
    head = re.sub(r'<meta property="og:image" content="https://studiocharbelmsallem-maker\.github\.io/Book/', f'<meta property="og:image" content="{BASE}', head)
    # remove a previous SEO block so the script can be re-run (e.g. for the domain switch)
    head = re.sub(r"\n?<!-- SEO -->.*?<!-- /SEO -->\n?", "\n", head, flags=re.S)
    block = ["<!-- SEO -->",
      f'<link rel="canonical" href="{url}">',
      f'<meta name="robots" content="{"noindex, follow" if noindex else "index, follow, max-image-preview:large"}">',
      '<meta name="author" content="Charbel Msallem">',
      f'<meta property="og:url" content="{url}">',
      '<meta property="og:site_name" content="Charbel Msallem Studios">',
      '<meta property="og:locale" content="en_GB">',
      f'<meta name="twitter:title" content="{esc(title)}">',
      f'<meta name="twitter:description" content="{esc(desc)}">',
      f'<meta name="twitter:image" content="{image}">']
    if image_alt and 'og:image:alt' not in head:
        block.append(f'<meta property="og:image:alt" content="{esc(image_alt)}">')
    if graph and not noindex:
        block.append('<script type="application/ld+json">' + json.dumps(org_graph(url, title, desc, image), ensure_ascii=False) + "</script>")
    block.append("<!-- /SEO -->")
    head = head.rstrip() + "\n" + "\n".join(block) + "\n"
    return head + s[head_end:]

def contact(s):
    s = s.replace("studiocharbelmsallem@gmail.com", EMAIL)
    if 'rel="noopener me"' not in s:
        s = re.sub(r'(<a class="em" href="mailto:[^"]*">[^<]*</a>)',
                   r'\1\n  <a class="em" href="'+IG+r'" target="_blank" rel="noopener me">@charbelmsallemstudios</a>', s, count=1)
    return s

def alts_book(s):
    # walk the body and give every frame a caption-based alt
    out=[]; pos=0; sec=None; cap=""
    for m in re.finditer(r'<section[^>]*\bid="([^"]+)"|<p class="cap">(.*?)</p>|<img\b[^>]*>', s, re.S):
        if m.group(1): sec=m.group(1); cap=""; continue
        if m.group(2) is not None: cap=m.group(2); continue
        tag=m.group(0)
        src=re.search(r'src="img/(\d{3})-', tag)
        if not src or not re.search(r'alt=""', tag): continue
        n=int(src.group(1)); alt=None
        if n in LOGOS: alt=LOGOS[n]
        elif sec in CITY and cap:
            city=CITY[sec]
            alt = f"{short(cap)} — {'jewellery campaign' if city=='Jewellery' else 'couture campaign in '+city}, Charbel Msallem Studios"
        if alt:
            new=tag.replace('alt=""', f'alt="{esc(alt)}"',1)
            out.append(s[pos:m.start()]); out.append(new); pos=m.end()
    out.append(s[pos:])
    s="".join(out)
    # chapter tiles and film covers: the label sits after the image inside the same <a>
    def tile(m):
        a=m.group(0); c=re.search(r'class="c">([^<]+)<',a); k=re.search(r'class="k">([^<]+)<',a)
        if not c: return a
        city=c.group(1)
        alt = f"{city} {k.group(1).split('·')[-1].strip().lower()} — fashion film by Charbel Msallem" if k else f"{city} — couture campaigns by Charbel Msallem Studios"
        return a.replace('alt=""', f'alt="{esc(alt)}"',1)
    s=re.sub(r'<a class="f?tile[^"]*"[^>]*>.*?</a>', tile, s, flags=re.S)
    return s

def run():
    # ---- index.html: the book
    f="index.html"; s=open(f,encoding="utf-8").read()
    s=set_head(s,
      "Charbel Msallem Studios — Couture Fashion Films & Campaign Photography | Beirut · Paris · Milan · Dubai",
      "Fashion films and couture campaign photography by Charbel Msallem, Beirut-based fashion director since 2012. Concept, filming and full production for couture houses and jewellery maisons in Beirut, Dubai, Paris, Milan, Istanbul and Barcelona.",
      BASE, BASE+"cover.jpg", "Couture on a Beirut hillside — Charbel Msallem Studios")
    s=contact(alts_book(s)); open(f,"w",encoding="utf-8").write(s)

    # ---- jewellery.html
    f="jewellery.html"; s=open(f,encoding="utf-8").read()
    s=set_head(s,
      "Jewellery Campaign Photography & Films — Charbel Msallem Studios | Beirut · Paris · Dubai",
      "Jewellery campaign photography and films for jewellery maisons by Charbel Msallem Studios. High jewellery on the body, studio still life and campaign films, directed from Beirut, Paris and Dubai since 2012.",
      BASE+"jewellery.html", BASE+"cover-jewellery.jpg", None)
    s=contact(alts_book(s)); open(f,"w",encoding="utf-8").write(s)

    # ---- service.html
    f="service.html"; s=open(f,encoding="utf-8").read()
    s=set_head(s,
      "The Maison Service — Couture Campaign, Fashion Film & Fashion Week Production | Charbel Msallem",
      "One shoot, the whole season: concept, campaign and fashion film, a runway in Paris or Milan, bridal fairs in Barcelona and Izmir, campaigns in Beirut and Dubai, showroom and press. Charbel Msallem Studios, couture campaigns since 2012.",
      BASE+"service.html", BASE+"cover.jpg", None)
    s=contact(s); open(f,"w",encoding="utf-8").write(s)

    # ---- edit.html: a send-only short edition, kept out of search so it does not compete with the book
    f="edit.html"; s=open(f,encoding="utf-8").read()
    s=set_head(s,"Charbel Msallem · The Edit","Twelve frames from Charbel Msallem Studios — couture campaigns and films.",
      BASE+"edit.html", BASE+"cover.jpg", None, noindex=True)
    s=contact(s); open(f,"w",encoding="utf-8").write(s)

    # ---- sitemap + robots
    pages=[("",1.0,"cover.jpg"),("jewellery.html",0.8,"cover-jewellery.jpg"),("service.html",0.7,"cover.jpg")]
    xml=['<?xml version="1.0" encoding="UTF-8"?>','<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:image="http://www.google.com/schemas/sitemap-image/1.1">']
    for p,pr,img in pages:
        xml.append(f"  <url><loc>{BASE}{p}</loc><changefreq>monthly</changefreq><priority>{pr}</priority><image:image><image:loc>{BASE}{img}</image:loc></image:image></url>")
    xml.append("</urlset>")
    open("sitemap.xml","w").write("\n".join(xml)+"\n")
    root = re.match(r"https?://[^/]+/", BASE).group(0)
    open("robots.txt","w").write(f"User-agent: *\nAllow: /\n\nSitemap: {BASE}sitemap.xml\n")

run()
print("done for", BASE)
