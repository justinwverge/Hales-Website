#!/usr/bin/env python3
"""Static site generator for haleshvac.com.

python3 build.py            -> dist/     (production: clean /folder/ URLs, deploy this)
python3 build.py --preview  -> preview/  (relative .../index.html links for local/artifact preview)
"""
import json, os, shutil, sys, html
from datetime import date

GITHUB = "--github" in sys.argv
PREVIEW = "--preview" in sys.argv or GITHUB
OUT = "github" if GITHUB else ("preview" if PREVIEW else "dist")
SITE = "https://www.haleshvac.com"
BOOK = "https://appointments.fieldedge.com/book/haleshvac"
PHONE = "706-765-7219"
TEL = "+17067657219"
EMAIL = "office@haleshvac.com"
ADDR = {"street": "1120 Mars Hill Road, Suite 106", "city": "Watkinsville", "region": "GA", "zip": "30677"}
ADDR_LINE = f"{ADDR['street']}, {ADDR['city']}, {ADDR['region']} {ADDR['zip']}"
LICENSE = "GA CR110362"
FB = "https://www.facebook.com/HalesHVAC"
IG = "https://www.instagram.com/haleshvac"
FINANCE = "https://retailservices.wellsfargo.com/pl/0030086094"
GREVIEWS = "https://www.google.com/maps/search/?api=1&query=Hale%27s+Heating+%26+Cooling+1120+Mars+Hill+Rd+Watkinsville+GA"
HOURS_TXT = "Mon–Sun 7:00 AM – 7:00 PM"
TODAY = date.today().isoformat()
E = html.escape

# ---------------------------------------------------------------- icons
I = {
 "phone": '<path d="M22 16.9v3a2 2 0 0 1-2.2 2 19.8 19.8 0 0 1-8.6-3.1 19.5 19.5 0 0 1-6-6A19.8 19.8 0 0 1 2.1 4.2 2 2 0 0 1 4.1 2h3a2 2 0 0 1 2 1.7c.1.9.4 1.8.7 2.7a2 2 0 0 1-.5 2.1L8 9.8a16 16 0 0 0 6 6l1.3-1.3a2 2 0 0 1 2.1-.4c.9.3 1.8.6 2.7.7a2 2 0 0 1 1.7 2z"/>',
 "cal": '<rect x="3" y="4" width="18" height="18" rx="2"/><path d="M16 2v4M8 2v4M3 10h18M8 14h.01M12 14h.01M16 14h.01M8 18h.01M12 18h.01"/>',
 "snow": '<path d="M12 2v20M4.9 4.9l14.2 14.2M2 12h20M4.9 19.1 19.1 4.9M9 3l3 3 3-3M9 21l3-3 3 3M3 9l3 3-3 3M21 9l-3 3 3 3"/>',
 "flame": '<path d="M8.5 14.5A2.5 2.5 0 0 0 11 12c0-1.4-.5-2-1-3-1.1-2.1-.2-4.1 2-6 .5 2.5 2 4.9 4 6.5 2 1.6 3 3.5 3 5.5a7 7 0 1 1-14 0c0-1.2.4-2.3 1-3.3.2 1.4 1.2 2.8 2.5 2.8z"/>',
 "wrench": '<path d="M14.7 6.3a1 1 0 0 0 0 1.4l1.6 1.6a1 1 0 0 0 1.4 0l3.8-3.8a6 6 0 0 1-7.9 7.9l-6.9 6.9a2.1 2.1 0 0 1-3-3l6.9-6.9a6 6 0 0 1 7.9-7.9l-3.8 3.8z"/>',
 "unit": '<rect x="2" y="5" width="20" height="15" rx="2"/><circle cx="9" cy="12.5" r="4.5"/><path d="M9 8v9M4.5 12.5h9M16 9h3M16 12h3M16 15h3"/>',
 "shield": '<path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/><path d="m9 12 2 2 4-4"/>',
 "wind": '<path d="M17.7 7.7A2.5 2.5 0 1 1 19.5 12H2M9.6 4.6A2 2 0 1 1 11 8H2M12.6 19.4A2 2 0 1 0 14 16H2"/>',
 "bldg": '<path d="M6 22V4a2 2 0 0 1 2-2h8a2 2 0 0 1 2 2v18zM6 12H4a2 2 0 0 0-2 2v8h4M18 9h2a2 2 0 0 1 2 2v11h-4M10 6h4M10 10h4M10 14h4M10 18h4"/>',
 "bolt": '<path d="M13 2 3 14h9l-1 8 10-12h-9z"/>',
 "pin": '<path d="M20 10c0 6-8 12-8 12s-8-6-8-12a8 8 0 0 1 16 0z"/><circle cx="12" cy="10" r="3"/>',
 "clock": '<circle cx="12" cy="12" r="10"/><path d="M12 6v6l4 2"/>',
 "check": '<circle cx="12" cy="12" r="10"/><path d="m8 12 3 3 5-5"/>',
 "mail": '<rect x="2" y="4" width="20" height="16" rx="2"/><path d="m22 7-10 6L2 7"/>',
 "dollar": '<path d="M12 2v20M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6"/>',
 "home": '<path d="m3 10 9-7 9 7v10a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"/><path d="M9 22V12h6v10"/>',
 "award": '<circle cx="12" cy="8" r="6"/><path d="M15.5 13 17 22l-5-3-5 3 1.5-9"/>',
 "users": '<path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M23 21v-2a4 4 0 0 0-3-3.9M16 3.1a4 4 0 0 1 0 7.8"/>',
 "chat": '<path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/>',
 "gauge": '<path d="M12 14l4-4"/><path d="M3.3 19a10 10 0 1 1 17.4 0z"/>',
 "fb": '<path d="M18 2h-3a5 5 0 0 0-5 5v3H7v4h3v8h4v-8h3l1-4h-4V7a1 1 0 0 1 1-1h3z"/>',
 "ig": '<rect x="2" y="2" width="20" height="20" rx="5"/><circle cx="12" cy="12" r="4"/><path d="M17.5 6.5h.01"/>',
}
def ic(n, extra=""):
    return f'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"{extra}>{I[n]}</svg>'
STAR = '<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="m12 2 3.1 6.3 6.9 1-5 4.9 1.2 6.8L12 17.8 5.8 21l1.2-6.8-5-4.9 6.9-1z"/></svg>'
LOGO = '''<svg viewBox="0 0 48 48" aria-hidden="true"><rect width="48" height="48" rx="11" fill="#0e2240"/><path d="M24 8 9 20v20h30V20z" fill="#16325c"/><path d="M24 8 9 20" stroke="#c8202f" stroke-width="3.2" stroke-linecap="round"/><path d="M24 8l15 12" stroke="#9cc8ee" stroke-width="3.2" stroke-linecap="round"/><path d="M17 24v12M31 24v12M17 30h14" stroke="#fff" stroke-width="3.6" stroke-linecap="round"/></svg>'''

# ---------------------------------------------------------------- links
def rel_prefix(path):
    depth = 0 if path == "/" else path.strip("/").count("/") + 1
    return "../" * depth
CUR = "/"
def u(path):
    """Link to an internal path like '/repair/'."""
    if not PREVIEW:
        return path
    p = rel_prefix(CUR)
    if path.startswith("/#"):
        return p + "index.html" + path[1:]
    if "#" in path:
        base, frag = path.split("#", 1)
        return p + (base.strip("/") + "/index.html" if base.strip("/") else "index.html") + "#" + frag
    return p + (path.strip("/") + "/index.html" if path != "/" else "index.html")
def asset(p):
    return (rel_prefix(CUR) + p) if PREVIEW else "/" + p

# ---------------------------------------------------------------- data
SERVICES = [
 dict(slug="repair", nav="AC & Heating Repair", icon="wrench", short="Fast, accurate diagnosis and lasting repairs for air conditioners, heat pumps and furnaces."),
 dict(slug="installation", nav="New System Installation", icon="unit", short="Carrier Factory Authorized installs — properly sized AC, heat pump and furnace systems."),
 dict(slug="maintenance", nav="Maintenance & Tune-Ups", icon="shield", short="Seasonal tune-ups that cut breakdowns, lower bills and extend equipment life."),
 dict(slug="indoor-air-quality", nav="Indoor Air Quality", icon="wind", short="Filtration, humidity control and air purification for cleaner, healthier air."),
 dict(slug="commercial-hvac", nav="Commercial HVAC", icon="bldg", short="Service, maintenance and replacement for offices, storage, retail and light commercial."),
 dict(slug="emergency-hvac", nav="Emergency Service", icon="bolt", short="No heat or no cooling? We work to get you back up and running the same day."),
]

CITIES = [
 dict(slug="watkinsville-ga", name="Watkinsville", county="Oconee County",
  intro="Watkinsville is home. Our shop is on Mars Hill Road, so when your system goes down in town we're usually just minutes away — not a dispatch center two counties over.",
  local="From older homes near downtown to newer neighborhoods off Mars Hill Road, Experiment Station Road and Highway 441, we see every kind of system Watkinsville has. A lot of homes here are pushing 15–20-year-old equipment, and we'll give you a straight answer on whether a repair still makes sense or it's time to look at replacement.",
  near=["bishop-ga","bogart-ga","athens-ga"]),
 dict(slug="athens-ga", name="Athens", county="Athens-Clarke County",
  intro="Hale's serves homeowners, landlords and businesses across Athens — from Five Points and Normaltown to the east side and out toward the Oconee line.",
  local="Athens has a big mix of housing: historic homes with tight attics and older ductwork, rental properties that need dependable equipment at a fair price, and newer builds with high-efficiency systems. Our techs diagnose the actual problem, show you what they found, and give you clear options before any work starts.",
  near=["watkinsville-ga","winterville-ga","bogart-ga"]),
 dict(slug="bogart-ga", name="Bogart", county="Oconee & Clarke Counties",
  intro="Bogart homes and businesses count on Hale's for heating and cooling repair, maintenance and new system installs — residential and commercial.",
  local="Bogart sits right on the Oconee–Clarke line, and its growth along Atlanta Highway means a lot of newer systems alongside older farmhouses and commercial buildings. We handle both: residential split systems and heat pumps, plus light commercial work for local businesses like Flex Storage Bogart.",
  near=["watkinsville-ga","statham-ga","athens-ga"]),
 dict(slug="bishop-ga", name="Bishop", county="Oconee County",
  intro="Hale's provides HVAC repair, maintenance and replacement for homes and properties in and around Bishop, just down Highway 441 from our Watkinsville shop.",
  local="Many Bishop properties sit on larger lots, with heat pumps, crawlspace ductwork and outbuildings that need their own comfort. We'll check the whole system — not just the box outside — so you aren't paying to heat and cool the crawlspace.",
  near=["watkinsville-ga","athens-ga","monroe-ga"]),
 dict(slug="statham-ga", name="Statham", county="Barrow County",
  intro="Statham homeowners call Hale's for honest HVAC service — fast diagnosis, upfront options and Carrier equipment installed right.",
  local="Statham has grown fast, and many of its newer homes now have systems coming out of their original warranty. A regular tune-up catches small issues — weak capacitors, dirty coils, clogged drains — before they turn into a July breakdown.",
  near=["bogart-ga","winder-ga","watkinsville-ga"]),
 dict(slug="winder-ga", name="Winder", county="Barrow County",
  intro="Hale's serves Winder with heating and air conditioning repair, seasonal maintenance and new system installation for homes and light commercial buildings.",
  local="Whether you're in an established neighborhood near downtown Winder or a newer subdivision off Highway 316, we bring the same approach: find the real problem, explain it plainly and stand behind the work.",
  near=["statham-ga","monroe-ga","bogart-ga"]),
 dict(slug="monroe-ga", name="Monroe", county="Walton County",
  intro="From historic downtown Monroe to the surrounding Walton County communities, Hale's provides dependable AC and heating service.",
  local="Monroe's older homes often need careful work — tight spaces, aging ductwork and systems that were never sized right in the first place. When it's time to replace, we size the new system to your actual home so it runs efficiently and keeps every room comfortable.",
  near=["winder-ga","bishop-ga","watkinsville-ga"]),
 dict(slug="winterville-ga", name="Winterville", county="Athens-Clarke County",
  intro="Hale's covers Winterville and eastern Clarke County with HVAC repair, maintenance, indoor air quality and Carrier system installs.",
  local="Winterville's mix of older homes and rural properties means we see everything from aging furnaces to heat pumps working overtime. We'll keep your system running through Georgia's hot, humid summers and the cold snaps that sneak up every winter.",
  near=["athens-ga","watkinsville-ga","bogart-ga"]),
]
CITY = {c["slug"]: c for c in CITIES}

# Paraphrased from reviews on the current haleshvac.com/reviews page.
REVIEWS = [
 ("Heather Gray-Jordan", "Residential AC service", "Robert showed up on time, was polite and knowledgeable, gave the AC a thorough check and pointed out the repairs it needed that day. Very satisfied with the service."),
 ("Andrew C.", "New system installation", "Hale's installed a new system at a great price. The technicians were knowledgeable and respectful, and he'll be hiring them again."),
 ("Pam Phillips", "Residential service", "Quick to respond, with a knowledgeable and courteous team."),
 ("Preston Willis", "Multi-unit service", "Hale's took good care of all four of his units."),
 ("John Alexander", "Commercial service", "Uses Hale's for commercial service, is happy with the results and recommends giving them a call."),
 ("Flex Storage Bogart", "Commercial customer", "Praises the company and its people and highly recommends Hale's."),
 ("Joseph Coleman", "Residential service", "Called the service outstanding."),
 ("David C.", "Residential service", "Couldn't be happier with the service."),
]

HOME_FAQ = [
 ("What areas does Hale's Heating & Cooling serve?", "We're based at 1120 Mars Hill Road in Watkinsville and serve Watkinsville, Athens, Bogart, Bishop, Statham, Winder, Monroe, Winterville and the surrounding Oconee, Clarke, Barrow and Walton County areas."),
 ("How do I schedule service?", f"Click any Schedule Now button to book online through our FieldEdge scheduler and pick a time that works for you, or call us at {PHONE}."),
 ("Do you work on brands other than Carrier?", "Yes. We're a Carrier Factory Authorized Dealer, but our NATE-certified technicians repair and maintain most major brands of air conditioners, heat pumps and furnaces."),
 ("Do you offer financing on new systems?", "Yes. We offer financing through Wells Fargo on qualifying Carrier systems, with monthly payment options, subject to credit approval."),
 ("Should I repair or replace my HVAC system?", "It depends on the age of the system, the cost of the repair, how often it's breaking down and how efficient it is. We'll lay out both options honestly, with prices, and let you decide."),
 ("Do you service commercial buildings?", "Yes. We provide repair, maintenance and replacement for light commercial properties including offices, retail and storage facilities."),
]

# ---------------------------------------------------------------- page chrome
def schema_business():
    return {
     "@context": "https://schema.org", "@type": "HVACBusiness", "@id": SITE + "/#business",
     "name": "Hale's Heating & Cooling", "legalName": "Hale's Heating & Cooling, LLC",
     "url": SITE + "/", "logo": SITE + "/assets/img/hales-logo.png", "image": SITE + "/assets/img/og-image.png", "telephone": "+1-706-765-7219", "email": EMAIL, "priceRange": "$$",
     "description": "Locally owned HVAC company in Watkinsville, GA providing AC and heating repair, maintenance, Carrier system installation, indoor air quality and commercial HVAC service.",
     "address": {"@type": "PostalAddress", "streetAddress": ADDR["street"], "addressLocality": ADDR["city"], "addressRegion": ADDR["region"], "postalCode": ADDR["zip"], "addressCountry": "US"},
     "openingHoursSpecification": [{"@type": "OpeningHoursSpecification", "dayOfWeek": ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"], "opens": "07:00", "closes": "19:00"}],
     "areaServed": [{"@type": "City", "name": f"{c['name']}, GA"} for c in CITIES],
     "sameAs": [FB, IG],
     "potentialAction": {"@type": "ReserveAction", "target": {"@type": "EntryPoint", "urlTemplate": BOOK, "actionPlatform": ["http://schema.org/DesktopWebPlatform","http://schema.org/MobileWebPlatform"]}, "name": "Schedule HVAC service"},
     "hasOfferCatalog": {"@type": "OfferCatalog", "name": "HVAC Services", "itemListElement": [{"@type": "Offer", "itemOffered": {"@type": "Service", "name": s["nav"], "url": f"{SITE}/{s['slug']}/"}} for s in SERVICES]},
    }

def jsonld(obj):
    return f'<script type="application/ld+json">{json.dumps(obj, ensure_ascii=False)}</script>'

def crumbs_schema(trail):
    return {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": i+1, "name": n, "item": SITE + p} for i, (n, p) in enumerate(trail)]}

def faq_schema(faq):
    return {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faq]}

def head(title, desc, path, extra_ld=()):
    canon = SITE + path
    ld = jsonld(schema_business()) + "".join(jsonld(x) for x in extra_ld)
    return f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{E(title)}</title>
<meta name="description" content="{E(desc)}">
<link rel="canonical" href="{canon}">
<meta name="robots" content="{"noindex,nofollow" if GITHUB else "index,follow,max-image-preview:large"}">
<meta name="theme-color" content="#0e2240">
<meta name="geo.region" content="US-GA"><meta name="geo.placename" content="Watkinsville">
<meta property="og:type" content="website"><meta property="og:site_name" content="Hale's Heating &amp; Cooling">
<meta property="og:title" content="{E(title)}"><meta property="og:description" content="{E(desc)}">
<meta property="og:url" content="{canon}"><meta property="og:image" content="{SITE}/assets/img/og-image.png">
<meta property="og:locale" content="en_US"><meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="{asset('favicon.ico')}" sizes="any">
<link rel="icon" href="{asset('favicon.svg')}" type="image/svg+xml">
<link rel="icon" type="image/png" sizes="32x32" href="{asset('favicon-32x32.png')}">
<link rel="apple-touch-icon" href="{asset('apple-touch-icon.png')}">
<link rel="manifest" href="{asset('site.webmanifest')}">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Barlow+Condensed:wght@600;700;800&family=Barlow:wght@400;500;600&display=swap" rel="stylesheet">
<link rel="stylesheet" href="{asset('assets/css/site.css')}">
{ld}
</head>
<body>
<a class="skip" href="#main">Skip to content</a>
'''

def book_btn(label="Schedule Now", cls="btn btn-red", track="book"):
    return f'<a class="{cls}" href="{BOOK}" target="_blank" rel="noopener" data-track="{track}">{ic("cal")}{label}</a>'
def call_btn(cls="btn btn-line", label=None):
    return f'<a class="{cls}" href="tel:{TEL}" data-track="call">{ic("phone")}{label or "Call " + PHONE}</a>'

def header():
    cur = lambda p: ' aria-current="page"' if CUR == p else ""
    svc = "".join(f'<a href="{u("/"+s["slug"]+"/")}">{E(s["nav"])}</a>' for s in SERVICES)
    msvc = "".join(f'<a href="{u("/"+s["slug"]+"/")}">{E(s["nav"])}</a>' for s in SERVICES)
    return f'''<div class="topbar"><div class="wrap">
<span>{ic("pin",' width="15"')}Locally owned in <b>Watkinsville, GA</b></span>
<span class="hide-s">{ic("clock",' width="15"')}{HOURS_TXT}</span>
<span class="hide-s">{ic("award",' width="15"')}BBB A+ &middot; Lic. {LICENSE}</span>
<span>{ic("phone",' width="15"')}<a href="tel:{TEL}">{PHONE}</a></span>
</div></div>
<header class="header"><div class="wrap">
<a class="logo" href="{u('/')}" aria-label="Hale's Heating & Cooling home"><img src="{asset('assets/img/hales-logo.png')}" alt="Hale's Heating & Cooling" width="160" height="56"></a>
<nav class="nav" aria-label="Main">
<div class="dd"><button aria-haspopup="true">Services ▾</button><div class="dd-menu">{svc}</div></div>
<a href="{u('/financing/')}"{cur('/financing/')}>Financing</a>
<a href="{u('/reviews/')}"{cur('/reviews/')}>Reviews</a>
<a href="{u('/service-areas/')}"{cur('/service-areas/')}>Service Areas</a>
<a href="{u('/about/')}"{cur('/about/')}>About</a>
<a href="{u('/contact/')}"{cur('/contact/')}>Contact</a>
</nav>
<div class="head-cta"><a class="head-phone" href="tel:{TEL}">{ic("phone")}{PHONE}</a>{book_btn()}</div>
<button class="burger" aria-label="Open menu" aria-expanded="false" aria-controls="mnav"><span></span><span></span><span></span></button>
</div></header>
<nav class="mnav" id="mnav" aria-label="Mobile">
<a href="{u('/')}">Home</a><div class="sub">{msvc}</div>
<a href="{u('/financing/')}">Financing</a><a href="{u('/reviews/')}">Reviews</a><a href="{u('/service-areas/')}">Service Areas</a>
<a href="{u('/about/')}">About</a><a href="{u('/contact/')}">Contact</a>
<div style="display:grid;gap:10px;margin-top:20px">{book_btn()}{call_btn("btn btn-line")}</div>
</nav>
<main id="main">
'''

def footer():
    svc = "".join(f'<li><a href="{u("/"+s["slug"]+"/")}">{E(s["nav"])}</a></li>' for s in SERVICES)
    areas = "".join(f'<li><a href="{u("/service-areas/"+c["slug"]+"/")}">HVAC in {c["name"]}, GA</a></li>' for c in CITIES)
    return f'''</main>
<footer class="footer"><div class="wrap">
<div><a class="logo" href="{u('/')}"><img src="{asset('assets/img/hales-logo-white.png')}" alt="Hale's Heating & Cooling" width="200" height="70"></a>
<p>Locally owned and operated HVAC service and installation in Watkinsville, GA. Honest work, clear communication, comfort you can count on.</p>
<p><a href="tel:{TEL}"><b style="color:#fff;font:700 22px var(--head)">{PHONE}</b></a><br>
<a href="{GREVIEWS}" target="_blank" rel="noopener">{ADDR['street']}<br>{ADDR['city']}, {ADDR['region']} {ADDR['zip']}</a><br>{HOURS_TXT}</p>
<div class="social"><a href="{FB}" target="_blank" rel="noopener" aria-label="Facebook">{ic("fb")}</a><a href="{IG}" target="_blank" rel="noopener" aria-label="Instagram">{ic("ig")}</a></div></div>
<div><h4>Services</h4><ul>{svc}<li><a href="{u('/financing/')}">Financing</a></li></ul></div>
<div><h4>Service Areas</h4><ul>{areas}</ul></div>
<div><h4>Company</h4><ul>
<li><a href="{u('/about/')}">About Hale's</a></li><li><a href="{u('/reviews/')}">Reviews</a></li><li><a href="{u('/contact/')}">Contact</a></li>
<li><a href="{BOOK}" target="_blank" rel="noopener">Schedule Online</a></li>
<li><a href="{u('/privacy/')}">Privacy Policy</a></li><li><a href="{u('/accessibility-statement/')}">Accessibility</a></li></ul>
<img src="{asset('assets/img/carrier-logo.png')}" alt="Carrier Factory Authorized Dealer" width="120" height="48" loading="lazy" style="margin-top:18px;background:#fff;padding:6px 10px;border-radius:8px;box-sizing:content-box">
<p style="margin-top:12px;font-size:14px">Carrier Factory Authorized Dealer<br>NATE-Certified Technicians<br>BBB Accredited, A+ Rating<br>Georgia License {LICENSE.replace('GA ','')}</p></div>
</div>
<div class="legal"><div class="wrap"><span>&copy; {date.today().year} Hale's Heating &amp; Cooling, LLC. All rights reserved.</span><span>Serving Oconee, Clarke, Barrow &amp; Walton Counties</span></div></div>
</footer>
<div class="mbar">{call_btn("btn btn-line","Call")}{book_btn()}</div>
<script src="{asset('assets/js/site.js')}" defer></script>
</body></html>
'''

def page_hero(h1, lead, trail):
    li = "".join((f'<li><a href="{u(p)}">{E(n)}</a></li>' if i < len(trail)-1 else f'<li aria-current="page">{E(n)}</li>') for i, (n, p) in enumerate(trail))
    return f'''<section class="phero"><div class="wrap">
<ol class="crumbs">{li}</ol>
<h1>{h1}</h1><p class="lead">{lead}</p>
<div class="btns" style="margin-top:22px">{book_btn()}{call_btn()}</div>
</div></section>'''

def trust_strip():
    return f'''<section class="trust" aria-label="Credentials"><ul>
<li><img class="carrier" src="{asset('assets/img/carrier-logo.png')}" alt="Carrier" width="90" height="36"><span><b>Factory Authorized</b>Carrier® Dealer</span></li>
<li>{ic("shield")}<span><b>NATE-Certified Techs</b>Trained, tested, professional</span></li>
<li>{ic("check")}<span><b>BBB A+ Rating</b>Accredited since 2020</span></li>
<li>{ic("home")}<span><b>Locally Owned</b>Based in Watkinsville, GA</span></li>
</ul></section>'''

def services_grid(exclude=None, heading=True):
    cards = "".join(f'''<a class="card" href="{u("/"+s["slug"]+"/")}"><span class="ico">{ic(s["icon"])}</span><h3>{E(s["nav"])}</h3><p>{E(s["short"])}</p><span class="more">Learn more →</span></a>''' for s in SERVICES if s["slug"] != exclude)
    h = '''<div class="sec-head"><div><span class="kicker">What we do</span><h2>Heating &amp; Cooling Services</h2></div><p class="lead">Residential and light commercial HVAC — repaired, maintained and installed by people who live and work here.</p></div>''' if heading else ""
    return f'<section class="band paper"><div class="wrap">{h}<div class="grid g3">{cards}</div></div></section>'

def areas_list(cls=""):
    return '<ul class="areas">' + "".join(f'<li><a href="{u("/service-areas/"+c["slug"]+"/")}">{ic("pin")}{c["name"]}</a></li>' for c in CITIES) + '</ul>'

def faq_block(faq, title="Frequently asked questions"):
    items = "".join(f'<details><summary>{E(q)}</summary><p>{E(a)}</p></details>' for q, a in faq)
    return f'<section class="band"><div class="wrap"><span class="kicker">FAQ</span><h2>{title}</h2><div class="faq">{items}</div></div></section>'

def reviews_block(n=3, more=True):
    cards = "".join(f'<article class="review"><div class="stars" aria-hidden="true">{STAR*5}</div><p>{E(t)}</p><footer>{E(nm)}<small>{E(k)}</small></footer></article>' for nm, k, t in REVIEWS[:n])
    m = f'<div class="btns" style="margin-top:26px"><a class="btn btn-line" href="{u("/reviews/")}">Read more reviews</a><a class="btn btn-line" href="{GREVIEWS}" target="_blank" rel="noopener">See us on Google</a></div>' if more else ""
    return f'<section class="band paper"><div class="wrap"><div class="sec-head"><div><span class="kicker">Reviews</span><h2>What our customers say</h2></div><p class="lead">Neighbors across Oconee and Clarke County trust Hale\'s with their comfort.</p></div><div class="grid g3">{cards}</div>{m}</div></section>'

def cta_band(h="Need heating or AC service?", p="Book online in under a minute, or call and talk to a real person in our Watkinsville office."):
    return f'<section class="band cta"><div class="wrap"><div><h2>{h}</h2><p>{p}</p></div><div class="btns">{book_btn()}{call_btn("btn btn-white")}</div></div></section>'

def sidebar(current=None):
    svc = "".join(f'<li><a href="{u("/"+s["slug"]+"/")}">{E(s["nav"])}</a></li>' for s in SERVICES if s["slug"] != current)
    return f'''<aside class="side">
<div class="box dark"><h3>Schedule service online</h3><p>Pick a time that works for you — we'll confirm your appointment.</p>{book_btn()}<a class="btn btn-white" href="tel:{TEL}">{ic("phone")}{PHONE}</a></div>
<div class="box"><h3>Other services</h3><ul>{svc}<li><a href="{u('/financing/')}">Financing options</a></li></ul></div>
<div class="box"><h3>Why Hale's</h3><ul><li>Carrier Factory Authorized Dealer</li><li>NATE-certified technicians</li><li>BBB A+ rated</li><li>Upfront options before work starts</li><li>Locally owned in Watkinsville</li></ul></div>
</aside>'''

def write(path, content):
    out = os.path.join(OUT, path.strip("/"), "index.html") if path != "/" else os.path.join(OUT, "index.html")
    if path == "/404/":
        out = os.path.join(OUT, "404.html")
    os.makedirs(os.path.dirname(out), exist_ok=True)
    with open(out, "w") as f:
        f.write(content)

PAGES = []  # for sitemap
def page(path, title, desc, body, ld=(), prio="0.7"):
    global CUR
    CUR = path
    html_ = head(title, desc, path, ld) + header() + body() + footer()
    write(path, html_)
    if path != "/404/":
        PAGES.append((path, prio))

# ---------------------------------------------------------------- hero scene
SCENE = '''<svg class="scene" viewBox="0 0 560 460" role="img" aria-label="Illustration of a home with an outdoor air conditioning unit">
<defs>
<linearGradient id="g1" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#22487f"/><stop offset="1" stop-color="#132c52"/></linearGradient>
<linearGradient id="g2" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#f4f6f9"/><stop offset="1" stop-color="#c9d2de"/></linearGradient>
<linearGradient id="g3" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#ffb07a"/><stop offset="1" stop-color="#ff7a45"/></linearGradient>
<radialGradient id="sun" cx=".5" cy=".5" r=".5"><stop offset="0" stop-color="#ffd38a"/><stop offset="1" stop-color="#ff9a4d" stop-opacity="0"/></radialGradient>
</defs>
<circle cx="470" cy="70" r="70" fill="url(#sun)" opacity=".55"/>
<circle cx="470" cy="70" r="26" fill="#ffc46b"/>
<ellipse cx="280" cy="420" rx="270" ry="26" fill="#071427" opacity=".55"/>
<!-- house -->
<path d="M70 210 250 80l180 130v200H70z" fill="url(#g1)"/>
<path d="M44 222 250 72l206 150" fill="none" stroke="#c8202f" stroke-width="16" stroke-linecap="round" stroke-linejoin="round"/>
<path d="M250 72l206 150" fill="none" stroke="#e23a48" stroke-width="5" stroke-linecap="round" opacity=".6"/>
<rect x="110" y="250" width="80" height="70" rx="6" fill="#ffd9a6"/><path d="M150 250v70M110 285h80" stroke="#132c52" stroke-width="6"/>
<rect x="290" y="250" width="70" height="70" rx="6" fill="#bfe0ff"/><path d="M325 250v70M290 285h70" stroke="#132c52" stroke-width="6"/>
<rect x="215" y="300" width="70" height="110" rx="6" fill="#0b1c35"/><circle cx="272" cy="358" r="4" fill="#ffc46b"/>
<rect x="70" y="404" width="360" height="8" fill="#0b1c35" opacity=".5"/>
<!-- cool air -->
<g fill="none" stroke="#9cc8ee" stroke-width="5" stroke-linecap="round" opacity=".9">
<path class="flow" d="M300 170c30-14 60 14 90 0"/><path class="flow" d="M290 196c34-14 66 14 100 0"/>
</g>
<!-- condenser -->
<g transform="translate(372 286)">
<rect x="0" y="118" width="168" height="10" rx="3" fill="#0a1830"/>
<rect x="6" y="0" width="156" height="120" rx="10" fill="url(#g2)"/>
<rect x="6" y="0" width="156" height="12" rx="6" fill="#ffffff"/>
<g stroke="#9aa7b8" stroke-width="2">
<path d="M18 26v84M26 26v84M34 26v84M42 26v84M50 26v84M58 26v84M66 26v84M74 26v84M82 26v84M90 26v84M98 26v84M106 26v84M114 26v84M122 26v84M130 26v84M138 26v84M146 26v84"/>
</g>
<circle cx="84" cy="66" r="40" fill="#1a2c44"/><circle cx="84" cy="66" r="40" fill="none" stroke="#d7dee8" stroke-width="5"/>
<g class="fan"><path d="M84 66c-4-18 4-30 16-30-2 12-8 22-16 30zM84 66c18-4 30 4 30 16-12-2-22-8-30-16zM84 66c4 18-4 30-16 30 2-12 8-22 16-30zM84 66c-18 4-30-4-30-16 12 2 22 8 30 16z" fill="#8aa0bb"/></g>
<circle cx="84" cy="66" r="6" fill="#d7dee8"/>
<rect x="128" y="100" width="26" height="8" rx="2" fill="#c8202f"/>
<path d="M6 40h-24v-60" fill="none" stroke="#3b4d66" stroke-width="7" stroke-linecap="round"/>
<path d="M6 54h-34v-74" fill="none" stroke="#5a6c85" stroke-width="5" stroke-linecap="round"/>
</g>
<!-- heat waves off unit -->
<g fill="none" stroke="url(#g3)" stroke-width="5" stroke-linecap="round" opacity=".9">
<path class="flow" d="M430 270c-8-14 8-24 0-38"/><path class="flow" d="M460 270c-8-14 8-24 0-38"/><path class="flow" d="M490 270c-8-14 8-24 0-38"/>
</g>
<!-- tag -->
<g transform="translate(36 150) rotate(-6)">
<rect width="186" height="64" rx="10" fill="#fff"/><circle cx="18" cy="32" r="6" fill="#0e2240"/>
<text x="34" y="28" font-family="Barlow Condensed,Arial Narrow,sans-serif" font-weight="800" font-size="20" fill="#0e2240">SYSTEM CHECK</text>
<text x="34" y="50" font-family="Barlow,Arial,sans-serif" font-weight="600" font-size="14" fill="#1f8a3b">● Running great</text>
</g>
</svg>'''

# ---------------------------------------------------------------- pages
def home_body():
    opts = [("wrench","Repair","AC or heat not working"),("shield","Tune-Up","Seasonal maintenance"),("unit","New System","Free replacement estimate"),("wind","Air Quality","Filtration & humidity")]
    o = "".join(f'<a href="{BOOK}" target="_blank" rel="noopener" data-track="book-{t.lower()}">{ic(i)}{t}<small>{s}</small></a>' for i,t,s in opts)
    return f'''
<section class="hero"><div class="wrap">
<div>
<h1>Heating &amp; Air Conditioning in <em>Watkinsville</em> &amp; Athens, GA</h1>
<p class="lead">Fast, honest AC and furnace repair, maintenance and Carrier® system installation from a locally owned team that treats your home like our own.</p>
<div class="btns" style="margin-top:26px">{book_btn("Schedule Now")}{call_btn()}</div>
<ul class="chips"><li>{ic("check")}NATE-certified techs</li><li>{ic("check")}BBB A+ rated</li><li>{ic("check")}Open 7 days, 7am–7pm</li></ul>
<div class="cbadge"><img src="{asset('assets/img/carrier-logo.png')}" alt="Carrier" width="110" height="44"><span><b>Carrier Factory Authorized Dealer</b>Recognized by Carrier for training, install quality &amp; customer satisfaction</span></div>
</div>
<div style="display:grid;gap:18px">
{SCENE}
<div class="book" style="margin-top:-70px"><h2>What do you need help with?</h2><p>Book online in under a minute — pick your service and a time that works.</p><div class="book-opts">{o}</div>{book_btn("Schedule Now")}<p class="or">Prefer to talk? <a href="tel:{TEL}">Call {PHONE}</a></p></div>
</div>
</div></section>
{trust_strip()}
{services_grid()}
<section class="band navy"><div class="wrap why">
<div><span class="kicker">Why Hale's</span><h2>A local HVAC company that tells you the truth</h2>
<p class="lead">We're not a call center or a franchise. We're a Watkinsville team of about 20 techs, installers and office staff who answer to our neighbors — so we do the job right and explain it in plain English.</p>
<div class="btns" style="margin-top:24px">{book_btn()}<a class="btn btn-line" href="{u('/about/')}">About us</a></div></div>
<ul class="why-list">
<li>{ic("chat")}<div><h3>Honest, upfront options</h3><p>We diagnose the real problem, show you what we found and give you clear choices before any work starts.</p></div></li>
<li><img class="cmini" src="{asset('assets/img/carrier-logo.png')}" alt="Carrier" width="60" height="24" loading="lazy"><div><h3>Carrier Factory Authorized</h3><p>One of a select group of dealers recognized by Carrier for training, installation quality and customer satisfaction.</p></div></li>
<li>{ic("shield")}<div><h3>NATE-certified technicians</h3><p>Our techs are trained and tested on real-world HVAC — and they show up on time, polite and prepared.</p></div></li>
<li>{ic("home")}<div><h3>Residential &amp; commercial</h3><p>From a single heat pump to a building full of rooftop units, we handle homes and light commercial properties.</p></div></li>
</ul></div></section>
<section class="band"><div class="wrap"><div class="sec-head"><div><span class="kicker">How it works</span><h2>Comfort back in four simple steps</h2></div></div>
<ol class="steps">
<li><h3>Book online or call</h3><p>Schedule in under a minute with our online booking, or call {PHONE}.</p></li>
<li><h3>We diagnose it right</h3><p>A NATE-certified tech tests the whole system and finds the actual cause.</p></li>
<li><h3>You choose the fix</h3><p>Clear options and pricing before we start. No pressure, no surprises.</p></li>
<li><h3>Comfort restored</h3><p>We fix it with quality parts, clean up and make sure it's running right.</p></li>
</ol></div></section>
<section class="band promo"><div class="wrap"><div><h2>Don't wait for the first 95° day</h2><p>A spring and fall tune-up catches weak parts before they fail, keeps your energy bills down and protects your equipment. Ask about our maintenance plans — members get priority when the heat hits.</p></div>
<div class="btns">{book_btn("Book a Tune-Up","btn btn-white")}</div></div></section>
{reviews_block()}
<section class="band"><div class="wrap"><div class="sec-head"><div><span class="kicker">Service area</span><h2>Proudly serving Oconee County &amp; beyond</h2></div><p class="lead">Based on Mars Hill Road in Watkinsville, we cover Oconee, Clarke, Barrow and Walton Counties.</p></div>{areas_list()}</div></section>
<section class="band paper" style="padding-top:0;background:#fff"><div class="wrap"><div class="callout" style="display:flex;gap:24px;align-items:center;justify-content:space-between;flex-wrap:wrap;margin:0">
<div><h3 style="margin:0 0 6px">Financing available on new Carrier systems</h3><p style="margin:0;color:var(--muted)">Monthly payment options through Wells Fargo, subject to credit approval.</p></div>
<a class="btn btn-line" href="{u('/financing/')}">{ic("dollar")}See financing</a></div></div></section>
{faq_block(HOME_FAQ)}
{cta_band()}'''

SVC_PAGES = {
"repair": dict(
 title="AC & Heating Repair in Watkinsville, GA | Hale's Heating & Cooling",
 desc="Fast, honest AC, heat pump and furnace repair in Watkinsville, Athens and Oconee County. NATE-certified techs, all major brands. Schedule online or call 706-765-7219.",
 h1="AC &amp; Heating Repair in Watkinsville &amp; Athens, GA",
 lead="When your air conditioner, heat pump or furnace quits, our NATE-certified techs find the real problem fast and fix it right — with clear options and pricing before any work starts.",
 body=f'''<h2>Signs you need HVAC repair</h2>
<ul class="cols2"><li>Warm air blowing from the vents in cooling mode</li><li>Cold air from the vents in heating mode</li><li>System won't turn on, or shuts off too soon (short cycling)</li><li>Grinding, squealing, buzzing or banging noises</li><li>Water around the indoor unit or a clogged drain line</li><li>Ice on the refrigerant lines or outdoor coil</li><li>Energy bills creeping up for no reason</li><li>Some rooms much hotter or colder than others</li><li>A burning or musty smell when the system runs</li><li>Thermostat not responding or reading wrong</li></ul>
<h2>What we repair</h2>
<p>We work on central air conditioners, heat pumps, gas furnaces, air handlers and ductless systems. Common repairs include:</p>
<ul class="cols2"><li>Capacitors, contactors and relays</li><li>Condenser fan and blower motors</li><li>Refrigerant leak detection and repair</li><li>Condensate drains, pumps and float switches</li><li>Thermostats and control boards</li><li>Heat pump defrost and reversing valve issues</li><li>Furnace igniters, flame sensors and gas valves</li><li>Electrical wiring, breakers and disconnects</li></ul>
<h2>How our repair visits work</h2>
<p>Our technicians use modern diagnostic tools to test the whole system — electrical, airflow and refrigerant — instead of guessing and swapping parts. Once we know what's wrong, we explain it in plain English, show you what we found and give you your options with pricing. Nothing happens until you say go.</p>
<p>We use high-quality parts so the repair lasts. And if your system is old enough that a repair doesn't make financial sense, we'll tell you honestly — and give you the numbers on both repair and replacement so you can decide.</p>
<div class="callout"><img src="{asset('assets/img/carrier-logo.png')}" alt="Carrier" width="110" height="44" loading="lazy" style="margin-bottom:12px"><h3>All brands, Carrier specialists</h3><p style="margin:0">As a Carrier Factory Authorized Dealer we know Carrier, Bryant and Payne equipment inside and out — and we repair most other major brands too, including Trane, Lennox, Rheem, Goodman and more.</p></div>''',
 faq=[("How quickly can you come out for a repair?", "Book online to see our available appointment times, or call 706-765-7219. We're open seven days a week, 7am to 7pm, and work to get no-cool and no-heat calls back up and running as fast as possible."),
      ("Do you repair brands other than Carrier?", "Yes. We repair most major brands of air conditioners, heat pumps and furnaces."),
      ("Should I repair or replace my AC?", "If your system is under 10–12 years old and the repair is reasonable, repairing usually makes sense. If it's older, uses R-22 refrigerant, or is breaking down often, replacement may save you money. We'll give you honest numbers on both."),
      ("Why is my AC running but not cooling?", "Common causes are a dirty filter or coil, a failed capacitor or fan motor, low refrigerant from a leak, or a frozen coil. Turn the system off if you see ice and schedule a diagnostic visit.")]),
"installation": dict(
 title="AC, Heat Pump & Furnace Installation | Carrier Dealer Watkinsville GA",
 desc="New HVAC system installation in Watkinsville, Athens & Oconee County. Carrier Factory Authorized Dealer, properly sized systems, Wells Fargo financing. Get a free estimate.",
 h1="New AC, Heat Pump &amp; Furnace Installation",
 lead="Replace your old system with a Carrier® system sized for your home and installed right the first time by a Carrier Factory Authorized Dealer.",
 body=f'''<h2>Systems we install</h2>
<ul class="cols2"><li>Central air conditioners</li><li>Heat pumps (including high-efficiency variable-speed)</li><li>Gas furnaces</li><li>Air handlers and evaporator coils</li><li>Ductless mini-split systems</li><li>Smart thermostats and zoning</li><li>Ductwork repair and replacement</li><li>Light commercial packaged and split systems</li></ul>
<h2>Why a Carrier Factory Authorized Dealer</h2>
<img src="{asset('assets/img/carrier-logo.png')}" alt="Carrier" width="140" height="56" loading="lazy" style="margin:0 0 14px">
<p>Carrier recognizes only a select group of dealers as Factory Authorized, based on training, installation quality and customer satisfaction. That means you get Carrier equipment installed by a team that meets Carrier's standards — and a local company that's here when you need service down the road.</p>
<h2>Our installation process</h2>
<ul><li><b>Free in-home consultation.</b> We look at your home, current system, ductwork and comfort problems — and listen to what you want.</li><li><b>Right-sized recommendation.</b> We size the system to your actual home, not a rule of thumb. Oversized and undersized systems both waste money and leave rooms uncomfortable.</li><li><b>Clear options.</b> Good, better and best choices with real pricing and efficiency ratings, so you can compare.</li><li><b>Clean, professional install.</b> Our install crews protect your home, install to code and manufacturer specs, and clean up when they're done.</li><li><b>Startup and testing.</b> We test refrigerant charge, airflow and controls, and walk you through your new system and warranty coverage.</li></ul>
<div class="callout"><h3>Financing available</h3><p>Spread the cost of a new Carrier system over affordable monthly payments through Wells Fargo, subject to credit approval.</p><a class="btn btn-line" href="{u('/financing/')}">{ic("dollar")}See financing options</a></div>''',
 faq=[("How long does an HVAC installation take?", "Most residential system replacements are completed in one day. Jobs that need new ductwork or major changes can take longer — we'll give you a timeline up front."),
      ("How much does a new HVAC system cost?", "It depends on the size of your home, the type and efficiency of the system, and whether ductwork needs work. We provide a free in-home estimate with clear options at different price points."),
      ("Do you offer financing?", "Yes. We offer financing through Wells Fargo on qualifying Carrier systems, subject to credit approval."),
      ("What size system do I need?", "Proper sizing depends on square footage, insulation, windows, ductwork and how your home is built. We size each system to the home rather than guessing based on the old unit.")]),
"maintenance": dict(
 title="HVAC Maintenance & AC Tune-Ups in Watkinsville, GA | Hale's",
 desc="Seasonal AC and furnace tune-ups in Watkinsville, Athens & Oconee County. Prevent breakdowns, lower energy bills and extend equipment life. Ask about maintenance plans.",
 h1="HVAC Maintenance &amp; Seasonal Tune-Ups",
 lead="Regular maintenance is the cheapest way to avoid a breakdown on the hottest day of the year. We service Carrier and all major brands for homes and businesses.",
 body=f'''<h2>What's included in a Hale's tune-up</h2>
<ul class="cols2"><li>Check and tighten electrical connections</li><li>Inspect and clean coils</li><li>Lubricate moving parts</li><li>Test thermostat settings for accuracy</li><li>Clear and treat condensate drain lines</li><li>Evaluate overall system performance</li><li>Check capacitors, contactors and safety controls</li><li>Inspect the filter and airflow</li></ul>
<h2>Why maintenance matters in Georgia</h2>
<p>Our long, humid summers make your air conditioner or heat pump work harder than in most of the country. Dirt on the coils, weak capacitors and clogged drains are the most common reasons systems fail in July — and nearly all of them are caught during a routine tune-up.</p>
<ul><li><b>Fewer breakdowns.</b> Small problems get fixed before they become big ones.</li><li><b>Lower energy bills.</b> A clean, properly running system uses less power.</li><li><b>Longer equipment life.</b> Regular care helps your system last years longer.</li><li><b>Better comfort and air quality.</b> Clean coils and drains mean better airflow and less moisture.</li></ul>
<div class="callout"><h3>Maintenance plans</h3><p>We recommend two visits a year: cooling in the spring and heating in the fall. Our maintenance plans make it automatic — and plan members get priority scheduling during peak-season breakdowns. Call or book online and ask about plan options.</p></div>''',
 faq=[("How often should my HVAC system be serviced?", "Twice a year is best: once in the spring before cooling season and once in the fall before heating season. Heat pumps run year-round in Georgia, so both visits matter."),
      ("Do you maintain brands other than Carrier?", "Yes. We service Carrier systems and most other major brands."),
      ("How long does a tune-up take?", "Most residential tune-ups take about an hour per system."),
      ("Does maintenance really lower my energy bill?", "Dirty coils, low airflow and worn parts force your system to run longer to reach the same temperature. Cleaning and tuning the system helps it run efficiently.")]),
"indoor-air-quality": dict(
 title="Indoor Air Quality Solutions in Watkinsville & Athens, GA | Hale's",
 desc="Improve indoor air quality with upgraded filtration, air purification, humidity control and duct solutions. Serving Watkinsville, Athens & Oconee County.",
 h1="Indoor Air Quality Solutions",
 lead="Allergies, dust, humidity and stale air are often HVAC problems. We'll find the cause and recommend solutions that fit your home and budget.",
 body=f'''<h2>Signs your indoor air needs attention</h2>
<ul class="cols2"><li>Dust builds up quickly after cleaning</li><li>Allergy symptoms are worse indoors</li><li>Home feels sticky or muggy in summer</li><li>Musty smells or visible mold near vents</li><li>Dry air, static and cracked woodwork in winter</li><li>Stuffy rooms or lingering odors</li></ul>
<h2>Indoor air quality options</h2>
<ul><li><b>Upgraded filtration.</b> High-efficiency media filters capture far more dust, pollen and pet dander than standard 1-inch filters.</li><li><b>Air purification.</b> Whole-home purifiers and UV lights help reduce airborne particles and microbial growth on the coil.</li><li><b>Humidity control.</b> Georgia humidity is a big comfort issue. Whole-home dehumidifiers and variable-speed systems help keep humidity in a comfortable range.</li><li><b>Ventilation.</b> Bring in fresh air without wasting energy.</li><li><b>Duct inspection and sealing.</b> Leaky ducts in attics and crawlspaces pull in dust and humid air.</li></ul>
<p>We'll look at the whole picture — your system, ductwork and home — and recommend only what will actually make a difference.</p>''',
 faq=[("What is the best air filter for my home?", "It depends on your system. Many systems can't handle very restrictive filters, which reduces airflow. We'll recommend a filter or media cabinet that improves filtration without hurting performance."),
      ("Can my HVAC system control humidity?", "Your air conditioner removes some moisture, but an oversized system or Georgia's summer humidity can overwhelm it. A whole-home dehumidifier or a properly sized variable-speed system can help."),
      ("Do air purifiers help with allergies?", "Better filtration and air purification can reduce airborne allergens like pollen, dust and pet dander throughout the home.")]),
"commercial-hvac": dict(
 title="Commercial HVAC Service & Installation | Watkinsville & Athens GA",
 desc="Commercial HVAC repair, preventive maintenance and replacement for offices, retail, storage and light commercial buildings in Oconee, Clarke & Barrow Counties.",
 h1="Commercial HVAC Service, Maintenance &amp; Installation",
 lead="Keep your building comfortable and your business running. We service and install light commercial HVAC for offices, retail, storage facilities, churches and more.",
 body=f'''<h2>Commercial services</h2>
<ul class="cols2"><li>Rooftop and packaged unit service</li><li>Commercial split systems and heat pumps</li><li>VRF and ductless systems</li><li>Preventive maintenance agreements</li><li>Equipment replacement and new installs</li><li>Multi-unit and multi-site properties</li></ul>
<h2>Built around your business</h2>
<p>A down HVAC system costs you customers, inventory and productivity. We work around your schedule, communicate clearly with building owners and managers, and keep records of every visit so you know exactly what's been done to each unit.</p>
<p>Preventive maintenance agreements keep your equipment on a regular schedule, cut emergency calls and help you plan replacements before they become emergencies.</p>''',
 faq=[("What types of commercial buildings do you service?", "We service light commercial buildings including offices, retail stores, storage facilities, churches and multi-unit properties."),
      ("Do you offer commercial maintenance agreements?", "Yes. We set up preventive maintenance schedules based on your equipment and how your building is used."),
      ("Can you work outside business hours?", "Call us to discuss your building's needs and we'll work with your schedule whenever possible.")]),
"emergency-hvac": dict(
 title="Emergency AC & Heating Service in Watkinsville, GA | Hale's",
 desc="No heat or no AC? Hale's Heating & Cooling provides fast emergency HVAC service in Watkinsville, Athens and Oconee County, 7 days a week. Call 706-765-7219.",
 h1="Emergency AC &amp; Heating Service",
 lead=f"No cooling in July or no heat in January? Call {PHONE} or book online. We're open seven days a week, 7am to 7pm, and work to get you back up and running fast.",
 body=f'''<h2>When to call right away</h2>
<ul class="cols2"><li>No cooling during extreme heat</li><li>No heat during freezing weather</li><li>Water leaking from the indoor unit</li><li>Breaker keeps tripping on the HVAC system</li><li>Burning smell from the system</li><li>Loud grinding or banging noises</li></ul>
<div class="note"><b>Smell gas?</b> Leave the home immediately, don't flip any switches, and call your gas utility or 911 from outside. Call us once it's safe.</div>
<h2>Before we arrive</h2>
<ul><li>Check that the thermostat is set to the right mode and has fresh batteries.</li><li>Check the breakers for the indoor and outdoor units.</li><li>Replace a dirty air filter.</li><li>If you see ice on the lines or coil, turn cooling off and run the fan only.</li></ul>
<p>If none of those fixes it, book online or call — we'll get a NATE-certified tech out to diagnose and repair it.</p>''',
 faq=[("What are your hours?", "We're open Monday through Sunday, 7am to 7pm."),
      ("What should I do if my AC stops working?", "Check the thermostat, breakers and filter first. If you see ice, turn cooling off and run the fan. Then call or book online for a repair visit."),
      ("Is no heat an emergency?", "During freezing weather, especially with young children, elderly family members or pets in the home, yes. Call us right away.")]),
}

def service_body(slug):
    d = SVC_PAGES[slug]; s = next(x for x in SERVICES if x["slug"] == slug)
    def b():
        return page_hero(d["h1"], d["lead"], [("Home","/"),(s["nav"],f"/{slug}/")]) + trust_strip() + f'''
<section class="band"><div class="wrap layout"><div class="prose">{d["body"]}
<h2>Serving Watkinsville and nearby</h2><p>We provide {E(s["nav"].lower())} throughout Oconee, Clarke, Barrow and Walton Counties.</p>{areas_list()}</div>{sidebar(slug)}</div></section>
{reviews_block(3)}{faq_block(d["faq"])}{cta_band()}'''
    svc_ld = {"@context":"https://schema.org","@type":"Service","name":s["nav"],"serviceType":s["nav"],"description":d["desc"],"url":f"{SITE}/{slug}/",
              "provider":{"@id":SITE+"/#business"},"areaServed":[{"@type":"City","name":f"{c['name']}, GA"} for c in CITIES]}
    page(f"/{slug}/", d["title"], d["desc"], b, [svc_ld, crumbs_schema([("Home","/"),(s["nav"],f"/{slug}/")]), faq_schema(d["faq"])], "0.9")

def city_page(c):
    path = f"/service-areas/{c['slug']}/"
    n = c["name"]
    faq = [(f"Do you offer same-day HVAC service in {n}?", f"We're open seven days a week, 7am to 7pm, and work to get {n} customers with no heat or no cooling taken care of as fast as possible. Book online to see available times or call {PHONE}."),
           (f"What HVAC services do you provide in {n}, GA?", "AC and heating repair, seasonal maintenance, new Carrier system installation, indoor air quality and light commercial HVAC."),
           (f"Do you charge extra to come to {n}?", f"Call us at {PHONE} and we'll explain our service call fee for your address up front.")]
    def b():
        near = "".join(f'<li><a href="{u("/service-areas/"+x+"/")}">{ic("pin")}{CITY[x]["name"]}</a></li>' for x in c["near"])
        svc = "".join(f'<li><a href="{u("/"+s["slug"]+"/")}"><b>{E(s["nav"])}</b></a> — {E(s["short"])}</li>' for s in SERVICES)
        return page_hero(f"HVAC Service in {n}, GA", c["intro"], [("Home","/"),("Service Areas","/service-areas/"),(f"{n}, GA",path)]) + trust_strip() + f'''
<section class="band"><div class="wrap layout"><div class="prose">
<h2>Heating &amp; air conditioning for {n} homes and businesses</h2>
<p>{E(c["local"])}</p>
<p>Hale's Heating &amp; Cooling is a locally owned Carrier Factory Authorized Dealer based in Watkinsville, serving {n} and the rest of {E(c["county"])}. Our NATE-certified technicians repair and maintain all major brands, and we install new Carrier® systems with financing available.</p>
<h2>Our services in {n}</h2><ul>{svc}</ul>
<h2>Nearby areas we serve</h2><ul class="areas">{near}</ul>
</div>{sidebar()}</div></section>
{reviews_block(3)}{faq_block(faq, f"HVAC questions from {n} homeowners")}{cta_band(f"Need HVAC service in {n}?")}'''
    page(path, f"HVAC Repair & AC Service in {n}, GA | Hale's Heating & Cooling",
         f"Heating and air conditioning repair, maintenance and Carrier installation in {n}, GA. Locally owned, NATE-certified, BBB A+. Schedule online or call {PHONE}.",
         b, [crumbs_schema([("Home","/"),("Service Areas","/service-areas/"),(f"{n}, GA",path)]), faq_schema(faq)], "0.8")

def build():
    if os.path.exists(OUT): shutil.rmtree(OUT)
    shutil.copytree("src/assets", os.path.join(OUT, "assets"))
    for f in os.listdir("src/root"): shutil.copy(os.path.join("src/root", f), OUT)

    page("/", "HVAC Repair & AC Service in Watkinsville, GA | Hale's Heating & Cooling",
         "Locally owned heating & air conditioning company in Watkinsville, GA. AC & furnace repair, maintenance and Carrier installs for Athens & Oconee County. Schedule online.",
         home_body, [faq_schema(HOME_FAQ)], "1.0")

    for s in SERVICES: service_body(s["slug"])

    # Financing
    def fin():
        return page_hero("HVAC Financing in Watkinsville, GA", "Don't let the cost of a new system leave you uncomfortable. Finance a new Carrier® system with affordable monthly payments.", [("Home","/"),("Financing","/financing/")]) + f'''
<section class="band"><div class="wrap layout"><div class="prose">
<h2>Wells Fargo financing for Carrier systems</h2>
<p>Hale's Heating &amp; Cooling offers financing through Wells Fargo for new Carrier® heating and cooling systems, whether you're upgrading or replacing equipment that's reached the end of its life. Monthly payment plans are designed to fit a range of budgets.</p>
<ul><li>Covers new installations and system upgrades</li><li>Monthly payment options</li><li>Quick online application</li><li>Subject to credit approval</li></ul>
<div class="btns" style="margin:24px 0"><a class="btn btn-red" href="{FINANCE}" target="_blank" rel="noopener">{ic("dollar")}Apply with Wells Fargo</a>{book_btn("Get a Free Estimate","btn btn-line")}</div>
<div class="note">Financing is provided by Wells Fargo and is subject to credit approval. Ask us about current offers when we provide your estimate.</div>
<h2>How it works</h2><ul><li><b>Get your estimate.</b> We'll recommend the right system with clear pricing.</li><li><b>Apply online.</b> The Wells Fargo application takes just a few minutes.</li><li><b>Schedule your install.</b> Once approved, we'll set your installation date.</li></ul>
</div>{sidebar()}</div></section>{cta_band("Ready for a new system?","Get a free in-home estimate and see your financing options.")}'''
    page("/financing/", "HVAC Financing | Wells Fargo Financing for Carrier Systems | Hale's",
         "Finance a new Carrier AC, heat pump or furnace with Wells Fargo through Hale's Heating & Cooling in Watkinsville, GA. Monthly payments, subject to credit approval.",
         fin, [crumbs_schema([("Home","/"),("Financing","/financing/")])], "0.7")

    # Reviews
    def rev():
        cards = "".join(f'<article class="review"><div class="stars" aria-hidden="true">{STAR*5}</div><p>{E(t)}</p><footer>{E(nm)}<small>{E(k)}</small></footer></article>' for nm,k,t in REVIEWS)
        return page_hero("Customer Reviews", "See what homeowners and businesses across Watkinsville, Athens and Oconee County say about Hale's Heating &amp; Cooling.", [("Home","/"),("Reviews","/reviews/")]) + f'''
<section class="band paper"><div class="wrap"><div class="grid g3">{cards}</div>
<div class="callout" style="background:#fff;margin-top:32px"><h3>Had a great experience?</h3><p>Reviews help our neighbors find a contractor they can trust. We'd be grateful if you shared yours.</p>
<div class="btns"><a class="btn btn-red" href="{GREVIEWS}" target="_blank" rel="noopener">Review us on Google</a><a class="btn btn-line" href="{FB}/reviews" target="_blank" rel="noopener">{ic("fb")}Review us on Facebook</a></div></div>
</div></section>{cta_band()}'''
    page("/reviews/", "Reviews | Hale's Heating & Cooling | Watkinsville, GA HVAC",
         "Read customer reviews of Hale's Heating & Cooling — HVAC repair, maintenance and installation in Watkinsville, Athens and Oconee County, GA. BBB A+ rated.",
         rev, [crumbs_schema([("Home","/"),("Reviews","/reviews/")])], "0.6")

    # About
    def about():
        return page_hero("About Hale's Heating &amp; Cooling", "A locally owned and operated HVAC company in Watkinsville, GA, built on honest work and clear communication.", [("Home","/"),("About","/about/")]) + trust_strip() + f'''
<section class="band"><div class="wrap layout"><div class="prose">
<h2>Local, honest and here for the long haul</h2>
<p>Hale's Heating &amp; Cooling is a locally owned and operated small business in Watkinsville, Georgia, specializing in HVAC service and installation for homes and light commercial buildings. Our goal is simple: deliver high-quality work at a fair price, and treat every customer the way we'd want our own families treated.</p>
<p>Today we're a team of about 20 — service technicians, install crews and office staff — working out of our shop at 1120 Mars Hill Road. When you call, you reach our local office. When a tech shows up, it's someone who lives and works in this community.</p>
<h2>What we stand for</h2>
<ul><li><b>Honesty.</b> We tell you what's actually wrong and what it actually needs — nothing more.</li><li><b>Transparent communication.</b> Clear options and pricing before work starts, and updates along the way.</li><li><b>Quality work.</b> NATE-certified technicians, quality parts and installs done to manufacturer standards.</li><li><b>Customer satisfaction.</b> We're not done until you're comfortable.</li></ul>
<h2>Credentials</h2>
<ul><li>Carrier Factory Authorized Dealer</li><li>NATE-certified technicians</li><li>Better Business Bureau accredited since April 2020 with an A+ rating</li><li>Licensed Georgia conditioned air contractor — {LICENSE}</li></ul>
</div>{sidebar()}</div></section>{reviews_block(3)}{cta_band()}'''
    page("/about/", "About Us | Locally Owned HVAC Company in Watkinsville, GA | Hale's",
         "Hale's Heating & Cooling is a locally owned HVAC company in Watkinsville, GA. Carrier Factory Authorized Dealer, NATE-certified techs, BBB A+ rated.",
         about, [crumbs_schema([("Home","/"),("About","/about/")])], "0.6")

    # Contact
    def contact():
        mapq = "1120+Mars+Hill+Rd+Suite+106+Watkinsville+GA+30677"
        mapel = (f'<iframe class="map" title="Map to Hale\'s Heating & Cooling" loading="lazy" referrerpolicy="no-referrer-when-downgrade" src="https://www.google.com/maps?q={mapq}&output=embed"></iframe>'
                 if not PREVIEW else f'<a class="map" href="{GREVIEWS}" target="_blank" rel="noopener" style="display:grid;place-items:center;text-decoration:none;font:700 20px var(--head);color:var(--navy)">{ic("pin",' width="40"')}View on Google Maps</a>')
        return page_hero("Contact Hale's Heating &amp; Cooling", f"Book online, call {PHONE}, or send us a message. We're open 7 days a week, 7am–7pm.", [("Home","/"),("Contact","/contact/")]) + f'''
<section class="band"><div class="wrap grid g2" style="gap:48px;align-items:start">
<div>
<h2>Get in touch</h2>
<ul class="info">
<li>{ic("cal")}<div><b>Schedule online</b><a href="{BOOK}" target="_blank" rel="noopener">Book an appointment anytime</a></div></li>
<li>{ic("phone")}<div><b>Call</b><a href="tel:{TEL}">{PHONE}</a></div></li>
<li>{ic("mail")}<div><b>Email</b><a href="mailto:{EMAIL}">{EMAIL}</a></div></li>
<li>{ic("pin")}<div><b>Office</b><a href="{GREVIEWS}" target="_blank" rel="noopener">{ADDR_LINE}</a></div></li>
</ul>
<h3 style="margin-top:32px">Hours</h3>
<table class="hours"><tr><td>Monday – Friday</td><td>7:00 AM – 7:00 PM</td></tr><tr><td>Saturday &amp; Sunday</td><td>7:00 AM – 7:00 PM</td></tr></table>
<div style="margin-top:28px">{mapel}</div>
</div>
<div class="callout" style="margin:0"><h2 style="font-size:32px">Request service</h2><p style="color:var(--muted)">Fastest option: <a href="{BOOK}" target="_blank" rel="noopener"><b>book online</b></a>. Or send us the details and our office will reach out.</p>
<form class="qf" name="service-request">
<div class="row"><label>Name<input name="Name" autocomplete="name" required></label><label>Phone<input name="Phone" type="tel" autocomplete="tel" required></label></div>
<label>Email<input name="Email" type="email" autocomplete="email"></label>
<label>Service address<input name="Address" autocomplete="street-address"></label>
<div class="row"><label>Service needed<select name="Service"><option>Repair</option><option>Maintenance</option><option>Installation / New System</option><option>Indoor Air Quality</option><option>Quote</option><option>Other</option></select></label>
<label>Preferred time<select name="Preferred time"><option>Any time</option><option>Morning</option><option>Afternoon</option></select></label></div>
<label>How did you hear about us?<input name="Referral"></label>
<label>Tell us what's going on<textarea name="Comments" rows="4"></textarea></label>
<button class="btn btn-red" type="submit">Send request</button><p class="msg" aria-live="polite"></p>
</form></div>
</div></section>
<section class="band paper"><div class="wrap"><h2>Service areas</h2>{areas_list()}</div></section>'''
    page("/contact/", "Contact Hale's Heating & Cooling | Watkinsville, GA | 706-765-7219",
         "Contact Hale's Heating & Cooling at 1120 Mars Hill Road, Watkinsville, GA. Call 706-765-7219 or schedule HVAC service online. Open 7 days, 7am–7pm.",
         contact, [crumbs_schema([("Home","/"),("Contact","/contact/")])], "0.8")

    # Service areas hub + cities
    def hub():
        cards = "".join(f'<a class="card" href="{u("/service-areas/"+c["slug"]+"/")}"><span class="ico">{ic("pin")}</span><h3>{c["name"]}, GA</h3><p>{E(c["county"])}</p><span class="more">HVAC in {c["name"]} →</span></a>' for c in CITIES)
        return page_hero("HVAC Service Areas", "From our shop in Watkinsville, Hale's serves homes and businesses across Oconee, Clarke, Barrow and Walton Counties.", [("Home","/"),("Service Areas","/service-areas/")]) + f'''
<section class="band paper"><div class="wrap"><div class="grid g4">{cards}</div>
<p style="margin-top:28px;color:var(--muted)">Don't see your town? Call {PHONE} — if you're nearby, there's a good chance we can help.</p></div></section>{services_grid()}{cta_band()}'''
    page("/service-areas/", "HVAC Service Areas | Watkinsville, Athens, Bogart & More | Hale's",
         "Hale's Heating & Cooling serves Watkinsville, Athens, Bogart, Bishop, Statham, Winder, Monroe and Winterville, GA with HVAC repair, maintenance and installation.",
         hub, [crumbs_schema([("Home","/"),("Service Areas","/service-areas/")])], "0.8")
    for c in CITIES: city_page(c)

    # Legal
    def privacy():
        return page_hero("Privacy Policy", "How Hale's Heating &amp; Cooling collects and uses your information.", [("Home","/"),("Privacy Policy","/privacy/")]) + f'''
<section class="band"><div class="wrap prose" style="max-width:820px">
<p><i>Last updated {date.today().strftime("%B %Y")}.</i></p>
<h2>Information we collect</h2><p>When you contact us, request service or book an appointment, we collect the information you provide, such as your name, phone number, email, service address and details about your HVAC system. Online appointments are processed through our scheduling provider, FieldEdge.</p>
<h2>How we use it</h2><p>We use your information to schedule and perform service, communicate with you about appointments, estimates and invoices, and improve our services. We do not sell your personal information.</p>
<h2>Website analytics</h2><p>Our website may use cookies and analytics tools (such as Google Analytics) to understand how visitors use the site. You can disable cookies in your browser settings.</p>
<h2>Third-party links</h2><p>Our site links to third-party services such as FieldEdge, Wells Fargo, Google, Facebook and Instagram. Their privacy practices are governed by their own policies.</p>
<h2>Contact</h2><p>Questions about this policy? Call {PHONE} or email <a href="mailto:{EMAIL}">{EMAIL}</a>.</p>
</div></section>'''
    page("/privacy/", "Privacy Policy | Hale's Heating & Cooling", "Privacy policy for Hale's Heating & Cooling, LLC in Watkinsville, GA.", privacy, (), "0.2")
    def access():
        return page_hero("Accessibility Statement", "We want everyone to be able to use our website.", [("Home","/"),("Accessibility","/accessibility-statement/")]) + f'''
<section class="band"><div class="wrap prose" style="max-width:820px">
<p>Hale's Heating &amp; Cooling is committed to making our website accessible to people of all abilities. This site is built to follow the Web Content Accessibility Guidelines (WCAG) 2.1 Level AA, including keyboard navigation, readable color contrast, descriptive labels and responsive layouts that work on phones, tablets and desktops.</p>
<p>If you have trouble using any part of this website, please call us at <a href="tel:{TEL}">{PHONE}</a> or email <a href="mailto:{EMAIL}">{EMAIL}</a>, and we'll be glad to help you schedule service or get the information you need.</p>
</div></section>'''
    page("/accessibility-statement/", "Accessibility Statement | Hale's Heating & Cooling", "Accessibility statement for the Hale's Heating & Cooling website.", access, (), "0.2")

    # 404
    def nf():
        return f'<section class="phero"><div class="wrap"><h1>Page not found</h1><p class="lead">That page has moved or doesn\'t exist. Let\'s get you where you need to go.</p><div class="btns" style="margin-top:22px">{book_btn()}<a class="btn btn-line" href="{u("/")}">Go to homepage</a></div></div></section>{services_grid()}'
    page("/404/", "Page Not Found | Hale's Heating & Cooling", "Page not found.", nf)

    # sitemap / robots / llms
    sm = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + "".join(
        f'  <url><loc>{SITE}{p}</loc><lastmod>{TODAY}</lastmod><priority>{pr}</priority></url>\n' for p, pr in PAGES) + '</urlset>\n'
    open(os.path.join(OUT, "sitemap.xml"), "w").write(sm)
    open(os.path.join(OUT, "robots.txt"), "w").write("User-agent: *\nDisallow: /\n" if GITHUB else f"User-agent: *\nAllow: /\n\nSitemap: {SITE}/sitemap.xml\n")
    llms = f"""# Hale's Heating & Cooling

> Locally owned HVAC service and installation company in Watkinsville, GA (Oconee County), serving residential and light commercial customers. Carrier Factory Authorized Dealer, NATE-certified technicians, BBB A+ rated. Georgia license {LICENSE}.

- Phone: {PHONE}
- Address: {ADDR_LINE}
- Hours: Monday–Sunday, 7:00 AM – 7:00 PM
- Online booking: {BOOK}
- Service area: {", ".join(c["name"] for c in CITIES)}, GA

## Services
""" + "".join(f"- [{s['nav']}]({SITE}/{s['slug']}/): {s['short']}\n" for s in SERVICES) + f"""- [Financing]({SITE}/financing/): Wells Fargo financing for Carrier systems, subject to credit approval.

## Service areas
""" + "".join(f"- [HVAC in {c['name']}, GA]({SITE}/service-areas/{c['slug']}/)\n" for c in CITIES) + f"""
## Company
- [About]({SITE}/about/)
- [Reviews]({SITE}/reviews/)
- [Contact]({SITE}/contact/)
"""
    open(os.path.join(OUT, "llms.txt"), "w").write(llms)
    # Netlify/Cloudflare Pages redirects for old URLs without trailing slash are automatic; keep old /home alias just in case
    open(os.path.join(OUT, "_redirects"), "w").write("/home  /  301\n/index.html  /  301\n")
    print(f"Built {len(PAGES)} pages into {OUT}/")

build()
