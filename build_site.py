#!/usr/bin/env python3
"""Build phyllux.app — Phyllux apps catalog for all apps."""
from __future__ import annotations

import re
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parent
ASSETS = ROOT / "assets"
STAGING = ASSETS / "staging"
CATALOG_ICONS = ASSETS / "catalog"
CSS = ROOT / "css"
CATALOG = Path(r"D:\WS\KB\sources\research_db\Quantonics-Applications.md")
ANDROID_ROOT = Path(r"D:\WS\programs\Quantonics-repos\quantonics-android")
ANDROID_REGISTRY = ANDROID_ROOT / "docs" / "assets" / "asset-registry.yaml"
ORG_ASSETS = Path(r"D:\WS\programs\Phyllux-repos\phyllux-org\assets")
PITCH_ASSETS = Path(
    r"D:\WS\communications\people\paul-mattys-place\quantonics-pitch-2026-09-14\assets"
)

# Catalog title overrides when Applications.md wording differs from registry displayName
TITLE_TO_PRODUCT = {
    "insight capture": "insight-capture",
    "insight capture app": "insight-capture",
    "quanton suite": "_suite",
    "uncertainty manager": "uncertainty-manager",
    "qelr translator": "qelr-translator",
    "quantonics keyboard": "quantonics-keyboard",
    "quantonics academy": "quantonics-academy",
    "qualitative time journal": "qualitative-time-journal",
    "quantonic second brain": "second-brain",
    "second brain": "second-brain",
    "quantonic philosopher agent": "quantonic-philosopher-agent",
}

# Honest Android soft launch faces (registry status placed)
PLACED_SHELLS = [
    {
        "productId": "_suite",
        "name": "Quanton Suite",
        "kind": "Suite APK",
        "note": "One local first mega app. Modules and category launcher inside one install. Soft launch depth demo, not Play ship ready theater.",
    },
]

CSS_TEXT = r"""
:root {
  --ink: #14212b;
  --muted: #4a5d6a;
  --paper: #f4f7f6;
  --card: #ffffff;
  --teal: #0f6b6d;
  --teal-deep: #0a4547;
  --gold: #c4a35a;
  --line: #d0ddd9;
  --accent: #1a8a7a;
}
* { box-sizing: border-box; }
html { scroll-behavior: smooth; }
body {
  margin: 0;
  font-family: "Source Sans 3", "Segoe UI", sans-serif;
  color: var(--ink);
  background:
    radial-gradient(1000px 480px at 0% -5%, #cfeceb 0%, transparent 55%),
    radial-gradient(800px 420px at 100% 5%, #e8f0ea 0%, transparent 50%),
    var(--paper);
  line-height: 1.55;
}
a { color: var(--teal); }
.wrap { max-width: 1100px; margin: 0 auto; padding: 0 1.15rem 3.5rem; }
.site-header {
  position: sticky; top: 0; z-index: 20;
  backdrop-filter: blur(10px);
  background: rgba(244,247,246,.92);
  border-bottom: 1px solid var(--line);
}
.header-inner {
  max-width: 1100px; margin: 0 auto; padding: .75rem 1.15rem;
  display: flex; gap: 1rem; align-items: center; justify-content: space-between; flex-wrap: wrap;
}
.brand { font-family: Fraunces, Georgia, serif; font-weight: 700; font-size: 1.35rem; color: var(--teal-deep); text-decoration: none; }
.brand span { color: var(--accent); font-weight: 600; font-size: .95rem; margin-left: .35rem; }
.nav { display: flex; flex-wrap: wrap; gap: .55rem .85rem; }
.nav a { text-decoration: none; color: var(--muted); font-size: .92rem; font-weight: 600; }
.nav a:hover { color: var(--teal); }
.hero {
  margin: 1.2rem 0 1.5rem; border-radius: 18px; overflow: hidden;
  box-shadow: 0 18px 40px rgba(20,33,43,.14); position: relative;
}
.hero img { width: 100%; display: block; max-height: 380px; object-fit: cover; }
.badge {
  display: inline-block; background: #e3f4f1; color: var(--teal-deep);
  padding: .25rem .7rem; border-radius: 999px; font-size: .85rem; font-weight: 700; margin-bottom: .6rem;
}
h1,h2,h3 { font-family: Fraunces, Georgia, serif; color: var(--teal-deep); line-height: 1.15; }
h1 { font-size: clamp(2rem, 4.5vw, 3rem); margin: .35rem 0; }
h2 { font-size: 1.4rem; margin: 1.7rem 0 .5rem; }
.lede { font-size: 1.12rem; color: var(--muted); max-width: 56ch; }
.note, .disclaimer { color: var(--muted); font-size: .92rem; }
.disclaimer {
  background: #fff6e8; border: 1px solid var(--gold); border-radius: 12px; padding: .85rem 1rem; margin: 1rem 0;
}
.tile-grid, .app-grid, .cat-grid {
  display: grid; grid-template-columns: repeat(auto-fill, minmax(220px, 1fr)); gap: .9rem; margin: 1.1rem 0;
}
.tile, .app-card, .cat-card {
  background: var(--card); border: 1px solid var(--line); border-radius: 14px;
  padding: 1rem; text-decoration: none; color: inherit;
  box-shadow: 0 8px 18px rgba(20,33,43,.05);
}
.tile:hover, .app-card:hover, .cat-card:hover { border-color: var(--teal); }
.tile strong, .cat-card strong, .app-card strong { display: block; color: var(--teal-deep); margin-bottom: .25rem; }
.tile em, .cat-card em, .app-card em, .meta {
  display: block; font-style: normal; color: var(--muted); font-size: .88rem;
}
.app-card img.icon, .apk-card img.icon {
  width: 56px; height: 56px; border-radius: 12px; object-fit: cover;
  display: block; margin-bottom: .65rem; background: #e8f0ea;
}
.apk-card {
  background: var(--card); border: 1px solid var(--line); border-radius: 14px;
  padding: 1rem; box-shadow: 0 8px 18px rgba(20,33,43,.05);
}
.apk-card .kind { font-size: .8rem; font-weight: 700; color: var(--teal); text-transform: uppercase; letter-spacing: .04em; }
.apk-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(240px, 1fr)); gap: .9rem; margin: 1.1rem 0; }
.cta-row { display: flex; flex-wrap: wrap; gap: .7rem; margin: 1.2rem 0; }
.btn {
  display: inline-block; background: var(--teal-deep); color: #fff !important; text-decoration: none;
  font-weight: 700; padding: .65rem 1.1rem; border-radius: 999px;
}
.btn.secondary { background: transparent; color: var(--teal-deep) !important; border: 2px solid var(--teal); }
button.btn { border: none; cursor: pointer; font: inherit; }
.wait-form {
  max-width: 28rem; margin: 1.2rem 0; padding: 1.1rem 1.15rem;
  background: var(--card); border: 1px solid var(--line); border-radius: 14px;
}
.wait-form label { display: block; font-weight: 600; margin: .7rem 0 .25rem; color: var(--ink); }
.wait-form input, .wait-form select, .wait-form textarea {
  width: 100%; padding: .55rem .7rem; border: 1px solid var(--line); border-radius: 8px;
  font: inherit; color: var(--ink); background: #fff;
}
.wait-form .row { margin-top: 1rem; }
.site-footer {
  margin-top: 3rem; padding: 1.4rem 0 2rem; border-top: 1px solid var(--line); color: var(--muted); font-size: .9rem;
}
.footer-links { display: flex; flex-wrap: wrap; gap: .5rem .9rem; margin: .6rem 0 1rem; }
ul { padding-left: 1.15rem; }
li { margin: .3rem 0; }
.status-live { color: #0a7a4a; font-weight: 700; }
.status-soon { color: #9a6b12; font-weight: 700; }
.status-plan { color: var(--muted); font-weight: 700; }
"""


def slugify(name: str) -> str:
    s = name.lower()
    s = re.sub(r"[^a-z0-9]+", "-", s).strip("-")
    return s


def parse_catalog() -> list[dict]:
    text = CATALOG.read_text(encoding="utf-8")
    cats: list[dict] = []
    cur = None
    for line in text.splitlines():
        m = re.match(r"^## (\d+)\. (.+)$", line)
        if m:
            cur = {
                "n": int(m.group(1)),
                "name": m.group(2).strip(),
                "slug": slugify(m.group(2)),
                "apps": [],
            }
            cats.append(cur)
            continue
        if not cur or not line.startswith("|"):
            continue
        if line.startswith("| #") or line.startswith("|---") or line.startswith("| Id"):
            continue
        parts = [x.strip() for x in line.strip("|").split("|")]
        if len(parts) >= 3 and parts[0].isdigit():
            cur["apps"].append(
                {
                    "id": parts[0],
                    "title": parts[1],
                    "platforms": parts[2],
                    "blurb": parts[3] if len(parts) > 3 else "",
                }
            )
    return cats


FEATURED = [
    {
        "name": "Finally Me",
        "href": "https://finallyme.help",
        "status": "live",
        "blurb": "Recovery adjacent practice tools. Non clinical.",
    },
    {
        "name": "Novelmate Studio",
        "href": "https://novelmatestudio.com",
        "status": "live",
        "blurb": "Local first novel pipeline for writers.",
    },
    {
        "name": "Sproule Lit / Phyllux books",
        "href": "https://phyllux.com",
        "status": "live",
        "blurb": "Literary storefront and Phyllux books.",
    },
    {
        "name": "Phyllux engineering",
        "href": "https://phyllux.io",
        "status": "live",
        "blurb": "Phyllux Technologies engineering site.",
    },
    {
        "name": "Quanton Suite",
        "href": "/suite/",
        "status": "soon",
        "blurb": "The Quantonics product: one Suite, many modules.",
    },
    {
        "name": "Today notebook",
        "href": "https://phyllux.com/today.html",
        "status": "soon",
        "blurb": "Recovery notebook on phyllux.com (in development).",
    },
]


def status_html(status: str) -> str:
    label = {"live": "Live", "soon": "Soft launch", "plan": "Planned"}[status]
    return f'<span class="status-{status}">{label}</span>'


def nav_for(depth: int) -> str:
    p = "../" * depth
    links = [
        ("", "Home"),
        ("featured/", "Featured"),
        ("suite/", "Quanton Suite"),
        ("catalog/", "Inside Suite"),
        ("ecosystem/", "Ecosystem"),
        ("manifesto/", "Manifesto"),
        ("pricing/", "Pricing"),
        ("waitlist/", "Waitlist"),
        ("about/", "About"),
    ]
    return "".join(f'<a href="{p}{href}">{label}</a>' for href, label in links)


def page_shell(title: str, lede: str, body: str, depth: int = 0, hero: str | None = None) -> str:
    p = "../" * depth
    hero_html = ""
    if hero:
        hero_html = f'<div class="hero"><img src="{p}assets/{hero}" alt=""/></div>'
    desc = lede[:160].replace('"', "'")
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8"/>
<meta name="viewport" content="width=device-width, initial-scale=1"/>
<title>{title} · phyllux.app</title>
<meta name="description" content="{desc}"/>
<link rel="preconnect" href="https://fonts.googleapis.com"/>
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin/>
<link href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,600;9..144,700&family=Source+Sans+3:wght@400;600;700&display=swap" rel="stylesheet"/>
<link rel="stylesheet" href="{p}css/site.css"/>
</head>
<body>
<header class="site-header"><div class="header-inner">
  <a class="brand" href="{p}">phyllux<span>.app</span></a>
  <nav class="nav">{nav_for(depth)}</nav>
</div></header>
<main class="wrap">
{hero_html}
  <p class="badge">Phyllux apps hub</p>
  <h1>{title}</h1>
  <p class="lede">{lede}</p>
{body}
</main>
<footer class="site-footer"><div class="wrap">
  <div class="footer-links">
    <a href="{p}suite/">Quanton Suite</a>
    <a href="{p}ecosystem/">Ecosystem map</a>
    <a href="{p}manifesto/">Manifesto</a>
    <a href="https://phyllux.io">phyllux.io</a>
    <a href="https://phyllux.com">phyllux.com</a>
    <a href="https://novelmatestudio.com">Novelmate</a>
    <a href="https://finallyme.help">Finally Me</a>
    <a href="{p}honesty/">Honesty</a>
    <a href="{p}privacy/">Privacy</a>
    <a href="{p}waitlist/">Waitlist</a>
  </div>
  <p>phyllux.app · Quanton Suite door · David E. Sproule · Edmonton</p>
</div></footer>
</body>
</html>
"""


def write(rel: str, html: str) -> Path:
    path = ROOT / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(html, encoding="utf-8")
    return path


def norm_title(s: str) -> str:
    s = s.lower().strip()
    s = re.sub(r"[^a-z0-9]+", " ", s)
    return re.sub(r"\s+", " ", s).strip()


def load_android_registry() -> list[dict]:
    if not ANDROID_REGISTRY.is_file():
        return []
    import yaml

    doc = yaml.safe_load(ANDROID_REGISTRY.read_text(encoding="utf-8"))
    return list(doc.get("products") or [])


def sync_catalog_icons(products: list[dict]) -> dict[str, str]:
    """
    Copy catalog tiles from quantonics-android asset registry into assets/catalog/.
    Returns map productId -> web path relative to site root (assets/catalog/<id>.png).
    Cap: derived + placed only (blocked icons stay without tiles; no silent fakes).
    """
    CATALOG_ICONS.mkdir(parents=True, exist_ok=True)
    STAGING.mkdir(parents=True, exist_ok=True)
    out: dict[str, str] = {}
    for row in products:
        status = row.get("status") or ""
        if status not in ("derived", "placed"):
            continue
        pid = row["productId"]
        tile = row.get("catalogTile") or ""
        src = ANDROID_ROOT / tile if tile else None
        if not src or not src.is_file():
            # fallback play icon
            play = row.get("iconPlay") or ""
            src = ANDROID_ROOT / play if play else None
        if not src or not src.is_file():
            continue
        dest_name = f"{pid}.png"
        # sacred site staging copy then ship
        shutil.copy2(src, STAGING / f"catalog-{dest_name}")
        shutil.copy2(src, CATALOG_ICONS / dest_name)
        out[pid] = f"assets/catalog/{dest_name}"
    # Prefer suite catalog tile as suite hero brand mark when present
    suite_tile = CATALOG_ICONS / "_suite.png"
    if suite_tile.is_file():
        shutil.copy2(suite_tile, ASSETS / "org-tile-quanton.png")
        shutil.copy2(suite_tile, STAGING / "org-tile-quanton.png")
    return out


def title_index(products: list[dict], icon_paths: dict[str, str]) -> dict[str, str]:
    """Map normalized catalog title -> productId for icon lookup."""
    idx: dict[str, str] = dict(TITLE_TO_PRODUCT)
    for row in products:
        pid = row["productId"]
        if pid not in icon_paths:
            continue
        name = row.get("displayName") or ""
        idx[norm_title(name)] = pid
        idx[norm_title(name.replace(" App", ""))] = pid
    return idx


def copy_assets() -> None:
    STAGING.mkdir(parents=True, exist_ok=True)
    ASSETS.mkdir(parents=True, exist_ok=True)
    names = [
        "org-hero-apps.png",
        "org-hero-home.png",
        "org-tile-quanton.png",
        "org-hero-roadmap.png",
        "org-hero-privacy.png",
    ]
    for n in names:
        for src_root in (ORG_ASSETS, PITCH_ASSETS):
            src = src_root / n
            if src.exists():
                shutil.copy2(src, STAGING / n)
                shutil.copy2(src, ASSETS / n)
                break


def build() -> None:
    cats = parse_catalog()
    total_apps = sum(len(c["apps"]) for c in cats)
    CSS.mkdir(parents=True, exist_ok=True)
    (CSS / "site.css").write_text(CSS_TEXT, encoding="utf-8")
    copy_assets()
    products = load_android_registry()
    icon_paths = sync_catalog_icons(products)
    title_idx = title_index(products, icon_paths)
    android_art = sum(1 for p in products if p.get("status") in ("derived", "placed"))
    matched_icons = 0

    featured_cards = "".join(
        f'<a class="tile" href="{f["href"]}"><strong>{f["name"]}</strong>'
        f'{status_html(f["status"])}<em>{f["blurb"]}</em></a>'
        for f in FEATURED
    )
    cat_cards_home = "".join(
        f'<a class="cat-card" href="catalog/{c["slug"]}/"><strong>{c["n"]}. {c["name"]}</strong>'
        f'<em>{len(c["apps"])} modules</em></a>'
        for c in cats
    )
    cat_cards_inner = "".join(
        f'<a class="cat-card" href="{c["slug"]}/"><strong>{c["n"]}. {c["name"]}</strong>'
        f'<em>{len(c["apps"])} modules</em></a>'
        for c in cats
    )

    write(
        "index.html",
        page_shell(
            "Quanton Suite and Phyllux apps",
            "Home for Quanton Suite and live Phyllux apps. One Suite. Modules inside it.",
            f"""
  <div class="cta-row">
    <a class="btn" href="suite/">Open Quanton Suite</a>
    <a class="btn secondary" href="waitlist/">Suite waitlist</a>
    <a class="btn secondary" href="ecosystem/">Ecosystem map</a>
  </div>
  <h2>Quanton Suite</h2>
  <p class="note">One Android mega app with a category launcher. Concepts below are <strong>modules and ideas inside the Suite</strong>, not separate apps to install one by one.</p>
  <div class="cta-row">
    <a class="btn secondary" href="suite/">Suite details</a>
    <a class="btn secondary" href="catalog/">Inside Suite ({total_apps} concepts)</a>
  </div>
  <h2>Live Phyllux circle</h2>
  <div class="tile-grid">{featured_cards}</div>
  <h2>Module families (inside Suite)</h2>
  <p class="note">{len(cats)} families · {total_apps} concepts on the map · Android art tiles sync from the Suite asset registry ({len(icon_paths)} on disk this build; {android_art} derived or placed). Shipping order follows the Suite roadmap.</p>
  <div class="cat-grid">{cat_cards_home}</div>
  <div class="disclaimer">Quantonics is a philosophical and speculative design source, not a physics proof. Wellness and recovery tools are not medical advice. Hospital admin tools mean ops literacy, not clinical devices. Soft launch APKs are depth demos, not a Play ship ready claim.</div>
""",
            hero="org-hero-apps.png",
        ),
    )

    write(
        "featured/index.html",
        page_shell(
            "Featured apps",
            "Products you can open today, plus the Suite path that is coming online.",
            f'<div class="tile-grid">{featured_cards}</div>'
            '<p class="note">More Phyllux circle apps land here as each surface ships.</p>',
            depth=1,
        ),
    )

    apk_cards = []
    for shell in PLACED_SHELLS:
        pid = shell["productId"]
        icon = ""
        if pid in icon_paths:
            icon = f'<img class="icon" src="../{icon_paths[pid]}" alt=""/>'
        apk_cards.append(
            f'<div class="apk-card">{icon}<span class="kind">{shell["kind"]}</span>'
            f'<strong>{shell["name"]}</strong><em>{shell["note"]}</em>'
            f'<span class="meta">Provenance: quantonics-android · assembleDebug · soft launch demo</span></div>'
        )
    apk_grid = "".join(apk_cards)
    write(
        "suite/index.html",
        page_shell(
            "Quanton Suite",
            "One Android Suite for Quantonics. Modules and category launcher in one install.",
            f"""
  <ul>
    <li>One Suite home. One shared core.</li>
    <li>Category launcher for module families inside the Suite</li>
    <li>Offline first where practical</li>
    <li>One install. Modules live inside the Suite.</li>
  </ul>
  <h2>Android soft launch</h2>
  <p class="note">Depth demo, not Play ship ready theater. Sideload only if you trust this build and know how to install unknown sources.</p>
  <div class="apk-grid">{apk_grid}</div>
  <div class="cta-row">
    <a class="btn" href="../downloads/Quanton-Suite-softlaunch-debug.apk">Download Suite APK (debug)</a>
    <a class="btn secondary" href="../waitlist/">Join Suite waitlist</a>
    <a class="btn secondary" href="../catalog/">See modules inside Suite</a>
  </div>
  <div class="disclaimer">Debug soft launch APK from <code>assembleDebug</code>. No analytics SDK. Local first notes stay on device. Not a Play Store build. Install at your own risk.</div>
""",
            depth=1,
            hero="org-tile-quanton.png",
        ),
    )

    write(
        "catalog/index.html",
        page_shell(
            "Inside Suite",
            f"Concept map of what lives inside Quanton Suite: {len(cats)} families and {total_apps} modules. Not a store of separate singles.",
            f'<p class="note">These are Suite modules and research concepts. They are not separate apps for sale.</p><div class="cat-grid">{cat_cards_inner}</div><p class="note"><a href="../suite/">Back to Quanton Suite</a></p>',
            depth=1,
        ),
    )

    for c in cats:
        cards = []
        for a in c["apps"]:
            pid = title_idx.get(norm_title(a["title"]))
            icon = ""
            if pid and pid in icon_paths:
                icon = f'<img class="icon" src="../../{icon_paths[pid]}" alt=""/>'
                matched_icons += 1
            android_bit = ""
            if "Android" in a["platforms"]:
                if pid and pid in icon_paths:
                    android_bit = " · Android art synced"
                else:
                    android_bit = " · Android art pending"
            cards.append(
                f'<div class="app-card">{icon}<strong>{a["id"]}. {a["title"]}</strong>'
                f'<span class="meta">{a["platforms"]}{android_bit}</span><em>{a["blurb"]}</em></div>'
            )
        apps_html = "".join(cards)
        write(
            f'catalog/{c["slug"]}/index.html',
            page_shell(
                f'{c["n"]}. {c["name"]}',
                f'{len(c["apps"])} modules in this Suite family. Soft launch lists the map; depth grows as Suite modules ship.',
                f'<p><a href="../">All categories</a></p><div class="app-grid">{apps_html}</div>',
                depth=2,
            ),
        )

    write(
        "platforms/index.html",
        page_shell(
            "Platforms",
            "Near term: Quanton Suite on Android. Later desktop and iPhone parity from the same core.",
            """
  <ul>
    <li><strong>Android</strong> Quanton Suite (primary soft launch)</li>
    <li><strong>iPhone</strong> later parity where store policy allows</li>
    <li><strong>Windows / Linux / Mac</strong> Suite or companion tools later</li>
    <li><strong>Web</strong> waitlists and demos on Phyllux hosts</li>
  </ul>
""",
            depth=1,
        ),
    )

    write(
        "pricing/index.html",
        page_shell(
            "Pricing",
            "Planning bands in CAD for Quanton Suite. Soft launch may test different SKUs.",
            """
  <ul>
    <li>Free tier: useful offline local first core inside Suite</li>
    <li>Suite: 14.99/mo or 119.99/yr · test SKUs 9.99/mo or 79.99/yr</li>
    <li>Education / B2B seats: custom</li>
  </ul>
  <p class="note">Live products (Finally Me, Novelmate, books) keep their own pricing on their own sites.</p>
""",
            depth=1,
        ),
    )

    write(
        "waitlist/index.html",
        page_shell(
            "Waitlist",
            "Get notified when Quanton Suite soft launch opens.",
            """
  <p class="note" id="thanks" hidden>Thanks. You are on the Suite waitlist. We only use this to notify you.</p>
  <form class="wait-form" action="https://formsubmit.co/hello@phyllux.app" method="POST">
    <input type="hidden" name="_subject" value="Suite waitlist"/>
    <input type="hidden" name="_captcha" value="false"/>
    <input type="hidden" name="_template" value="table"/>
    <input type="hidden" name="_next" value="https://phyllux.app/waitlist/?thanks=1"/>
    <input type="text" name="_honey" style="display:none" tabindex="-1" autocomplete="off"/>
    <label for="email">Email</label>
    <input id="email" type="email" name="email" required placeholder="you@example.com" autocomplete="email"/>
    <label for="platforms">Platforms you care about</label>
    <select id="platforms" name="platforms" required>
      <option value="Android">Android</option>
      <option value="Desktop">Desktop</option>
      <option value="Both">Both</option>
    </select>
    <label for="note">Optional note</label>
    <textarea id="note" name="note" rows="3" maxlength="500" placeholder="Anything you want us to know"></textarea>
    <div class="row"><button class="btn" type="submit">Join Suite waitlist</button></div>
  </form>
  <p class="note">Or email <a href="mailto:hello@phyllux.app?subject=Suite%20waitlist">hello@phyllux.app</a>. No spam list. No clinical claims. First submit may ask FormSubmit to confirm the inbox.</p>
  <script>
  (function(){
    if (new URLSearchParams(location.search).get("thanks") === "1") {
      var el = document.getElementById("thanks");
      if (el) { el.hidden = false; }
    }
  })();
  </script>
""",
            depth=1,
        ),
    )

    write(
        "about/index.html",
        page_shell(
            "About",
            "phyllux.app is the door for Quanton Suite and live Phyllux circle apps.",
            """
  <p>Built by David E. Sproule in Edmonton. Crosslinks:</p>
  <ul>
    <li><a href="../suite/">Quanton Suite</a> on this site</li>
    <li><a href="../ecosystem/">Ecosystem map</a></li>
    <li><a href="https://phyllux.io">phyllux.io</a> engineering and research status</li>
    <li><a href="https://phyllux.com">phyllux.com</a> books and Today</li>
    <li><a href="https://novelmatestudio.com">novelmatestudio.com</a></li>
    <li><a href="https://finallyme.help">finallyme.help</a></li>
  </ul>
""",
            depth=1,
        ),
    )

    write(
        "honesty/index.html",
        page_shell(
            "Honesty",
            "Claim boundaries for this catalog.",
            """
  <div class="disclaimer">
    Quantonics is a philosophical and speculative design source, not a physics proof.
    Wellness, recovery, and Parkinsons related tools are education, journaling, logistics, and community support. Not medical advice, diagnosis, or treatment.
    Hospital admin tools mean ops and training literacy. Not clinical devices.
    The concept map is what can live inside Suite. Shipping order follows the Suite roadmap. The old singles storefront count is retired.
  </div>
""",
            depth=1,
        ),
    )

    write(
        "privacy/index.html",
        page_shell(
            "Privacy",
            "Local first by default for Quanton Suite where the product allows it.",
            """
  <p>Waitlist email is used only to notify you about apps. No sale of contact lists. Live products have their own privacy pages on their hosts.</p>
""",
            depth=1,
        ),
    )


    write(
        "ecosystem/index.html",
        page_shell(
            "Ecosystem map",
            "One house. Many rooms. Start with Quanton Suite for Quantonics.",
            """
  <div class="tile-grid">
    <a class="tile" href="../suite/"><strong>Quanton Suite</strong><span class="status-soon">Soft launch</span><em>phyllux.app · one mega app</em></a>
    <a class="tile" href="https://novelmatestudio.com"><strong>Novelmate Studio</strong><span class="status-live">Live</span><em>Local first fiction workspace</em></a>
    <a class="tile" href="https://finallyme.help"><strong>Finally Me</strong><span class="status-live">Live</span><em>Practice companion · non clinical</em></a>
    <a class="tile" href="https://phyllux.com"><strong>Sproule Lit</strong><span class="status-live">Live</span><em>Books on phyllux.com</em></a>
    <a class="tile" href="https://phyllux.com/today.html"><strong>Today</strong><span class="status-soon">In development</span><em>Recovery notebook</em></a>
    <a class="tile" href="https://phyllux.io"><strong>Phyllux.io</strong><span class="status-live">Live</span><em>Research, archive, conscience</em></a>
  </div>
  <p class="note">Status language: Live = open now · Soft launch = demo path · In development = shipping soon. Evidence and claim ceilings live on each product and on phyllux.io research status.</p>
""",
            depth=1,
        ),
    )

    write(
        "manifesto/index.html",
        page_shell(
            "Manifesto",
            "Local first. Honest ceiling. Human first craft.",
            """
  <ul>
    <li>Humans set the vision.</li>
    <li>Machines assist, locally, on hardware you control.</li>
    <li>We never sell your inner work or your manuscripts as training data.</li>
    <li>We tell you where the ceiling is. We do not fake certainty.</li>
    <li>Every product exists to serve real people, not dashboards.</li>
    <li>Quantonics ships as <strong>Quanton Suite</strong>. The old singles storefront story is retired.</li>
  </ul>
  <p class="note"><a href="../ecosystem/">See the ecosystem map</a> · <a href="../honesty/">Honesty rails</a></p>
""",
            depth=1,
        ),
    )

    # sitemap
    urls = ["https://phyllux.app/"]
    for rel in [
        "featured/",
        "suite/",
        "catalog/",
        "ecosystem/",
        "manifesto/",
        "platforms/",
        "pricing/",
        "waitlist/",
        "about/",
        "honesty/",
        "privacy/",
    ]:
        urls.append(f"https://phyllux.app/{rel}")
    for c in cats:
        urls.append(f'https://phyllux.app/catalog/{c["slug"]}/')
    (ROOT / "sitemap.xml").write_text(
        '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        + "\n".join(f"  <url><loc>{u}</loc></url>" for u in urls)
        + "\n</urlset>\n",
        encoding="utf-8",
    )
    (ROOT / "robots.txt").write_text(
        "User-agent: *\nAllow: /\nSitemap: https://phyllux.app/sitemap.xml\n",
        encoding="utf-8",
    )
    print(
        f"Built phyllux.app: {len(cats)} categories, {total_apps} apps, {len(urls)} urls; "
        f"catalog icons synced {len(icon_paths)}; title matches with art {matched_icons}"
    )


if __name__ == "__main__":
    build()
