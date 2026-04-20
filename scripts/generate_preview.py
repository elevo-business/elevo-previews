#!/usr/bin/env python3
"""
ELEVO Preview Generator
Generates personalized website previews from templates.
Usage: python generate_preview.py --config prospect.json
"""

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
from datetime import datetime
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent
ROOT_DIR = SCRIPT_DIR.parent
TEMPLATES_DIR = ROOT_DIR / "templates"
PREVIEWS_DIR = ROOT_DIR / "previews"

# Industry colors (primary, secondary, primary_rgb, secondary_rgb)
BRANCHE_FARBEN = {
    "immobilien": {
        "primary": "#1a5276",
        "secondary": "#2980b9",
        "primary_rgb": "26,82,118",
        "secondary_rgb": "41,128,185",
    },
    "handwerk_sanitaer": {
        "primary": "#1565C0",
        "secondary": "#42A5F5",
        "primary_rgb": "21,101,192",
        "secondary_rgb": "66,165,245",
    },
    "handwerk_elektro": {
        "primary": "#F57F17",
        "secondary": "#FFB300",
        "primary_rgb": "245,127,23",
        "secondary_rgb": "255,179,0",
    },
    "handwerk_heizung": {
        "primary": "#BF360C",
        "secondary": "#FF7043",
        "primary_rgb": "191,54,12",
        "secondary_rgb": "255,112,67",
    },
    "handwerk_allgemein": {
        "primary": "#2E7D32",
        "secondary": "#66BB6A",
        "primary_rgb": "46,125,50",
        "secondary_rgb": "102,187,106",
    },
    "dienstleister_it": {
        "primary": "#6200EA",
        "secondary": "#AA00FF",
        "primary_rgb": "98,0,234",
        "secondary_rgb": "170,0,255",
    },
    "dienstleister_marketing": {
        "primary": "#E91E63",
        "secondary": "#FF4081",
        "primary_rgb": "233,30,99",
        "secondary_rgb": "255,64,129",
    },
    "dienstleister_recht": {
        "primary": "#37474F",
        "secondary": "#78909C",
        "primary_rgb": "55,71,79",
        "secondary_rgb": "120,144,156",
    },
    "dienstleister_allgemein": {
        "primary": "#00796B",
        "secondary": "#26A69A",
        "primary_rgb": "0,121,107",
        "secondary_rgb": "38,166,154",
    },
}

# Template mapping by branche_typ
TEMPLATE_MAP = {
    "immobilien": "immobilien",
    "handwerk_sanitaer": "handwerk",
    "handwerk_elektro": "handwerk",
    "handwerk_heizung": "handwerk",
    "handwerk_allgemein": "handwerk",
    "dienstleister_it": "dienstleister",
    "dienstleister_marketing": "dienstleister",
    "dienstleister_recht": "dienstleister",
    "dienstleister_allgemein": "dienstleister",
}


def slugify(name: str) -> str:
    name = name.lower()
    name = re.sub(r"[äÄ]", "ae", name)
    name = re.sub(r"[öÖ]", "oe", name)
    name = re.sub(r"[üÜ]", "ue", name)
    name = re.sub(r"[ß]", "ss", name)
    name = re.sub(r"[^a-z0-9]+", "-", name)
    name = name.strip("-")
    return name


def load_template(branche_typ: str) -> str:
    template_folder = TEMPLATE_MAP.get(branche_typ)
    if not template_folder:
        raise ValueError(f"Unknown branche_typ: {branche_typ}. Available: {list(TEMPLATE_MAP.keys())}")
    template_path = TEMPLATES_DIR / template_folder / "index.html"
    if not template_path.exists():
        raise FileNotFoundError(f"Template not found: {template_path}")
    return template_path.read_text(encoding="utf-8")


def fill_template(html: str, variables: dict) -> str:
    for key, value in variables.items():
        html = html.replace(f"{{{{{key}}}}}", str(value))
    # Report unfilled placeholders
    remaining = re.findall(r"\{\{([A-Z_0-9]+)\}\}", html)
    if remaining:
        print(f"  ⚠  Unfilled placeholders: {set(remaining)}", file=sys.stderr)
    return html


def build_variables(config: dict) -> dict:
    branche_typ = config["branche_typ"]
    farben = BRANCHE_FARBEN.get(branche_typ, BRANCHE_FARBEN["dienstleister_allgemein"])
    jahr = datetime.now().year

    vars = {
        "FIRMENNAME": config["firmenname"],
        "FIRMENNAME_KURZ": config.get("firmenname_kurz", config["firmenname"].split()[0]),
        "BRANCHE_BEZEICHNUNG": config.get("branche_bezeichnung", branche_typ.replace("_", " ").title()),
        "GRUENDUNGSJAHR": config.get("gruendungsjahr", "2010"),
        "JAHR": str(jahr),
        "FARBE_PRIMARY": config.get("farbe_primary") or farben["primary"],
        "FARBE_SECONDARY": config.get("farbe_secondary") or farben["secondary"],
        "FARBE_PRIMARY_RGB": config.get("farbe_primary_rgb") or farben["primary_rgb"],
        "FARBE_SECONDARY_RGB": config.get("farbe_secondary_rgb") or farben["secondary_rgb"],
        "HERO_HEADLINE": config.get("hero_headline", f"Ihr Partner für {config.get('branche_bezeichnung', 'professionelle Dienstleistungen')}"),
        "HERO_HEADLINE_2": config.get("hero_headline_2", "in Ihrer Region"),
        "HERO_SUBTEXT": config.get("hero_subtext", f"Wir stehen für Qualität, Verlässlichkeit und persönliche Betreuung. Entdecken Sie, was {config['firmenname']} für Sie leisten kann."),
        "ADRESSE": config.get("adresse", "Musterstraße 1, 40000 Düsseldorf"),
        "TELEFON": config.get("telefon", "+49 211 123456"),
        "EMAIL": config.get("email", f"info@{slugify(config['firmenname'])}.de"),
        "OEFFNUNGSZEITEN": config.get("oeffnungszeiten", "Mo–Fr 8:00–18:00 Uhr"),
        # Stats
        "STAT_1_NUM": config.get("stat_1_num", "15+"),
        "STAT_1_LABEL": config.get("stat_1_label", "Jahre Erfahrung"),
        "STAT_2_NUM": config.get("stat_2_num", "500+"),
        "STAT_2_LABEL": config.get("stat_2_label", "Zufriedene Kunden"),
        "STAT_3_NUM": config.get("stat_3_num", "4.9★"),
        "STAT_3_LABEL": config.get("stat_3_label", "Google Bewertung"),
        "STAT_4_NUM": config.get("stat_4_num", "24h"),
        "STAT_4_LABEL": config.get("stat_4_label", "Reaktionszeit"),
        # Services
        "SERVICE_1_TITEL": config.get("service_1_titel", "Kernleistung 1"),
        "SERVICE_1_TEXT": config.get("service_1_text", "Professionelle Beratung und Umsetzung für Ihren Bedarf."),
        "SERVICE_2_TITEL": config.get("service_2_titel", "Kernleistung 2"),
        "SERVICE_2_TEXT": config.get("service_2_text", "Schnelle und zuverlässige Ausführung durch erfahrene Fachkräfte."),
        "SERVICE_3_TITEL": config.get("service_3_titel", "Kernleistung 3"),
        "SERVICE_3_TEXT": config.get("service_3_text", "Kompetente Begleitung von A bis Z."),
        "SERVICE_4_TITEL": config.get("service_4_titel", "Kernleistung 4"),
        "SERVICE_4_TEXT": config.get("service_4_text", "Langfristige Betreuung und Support für nachhaltigen Erfolg."),
        # USPs
        "USP_1_TITEL": config.get("usp_1_titel", "Erfahrung & Kompetenz"),
        "USP_1_TEXT": config.get("usp_1_text", "Über 15 Jahre Branchenerfahrung und tiefes Fachwissen."),
        "USP_2_TITEL": config.get("usp_2_titel", "Transparente Preise"),
        "USP_2_TEXT": config.get("usp_2_text", "Keine versteckten Kosten – klare Angebote vor Auftragserteilung."),
        "USP_3_TITEL": config.get("usp_3_titel", "Schnelle Reaktion"),
        "USP_3_TEXT": config.get("usp_3_text", "Innerhalb von 24 Stunden erhalten Sie eine Rückmeldung."),
        "USP_HIGHLIGHT_NUM": config.get("usp_highlight_num", "98%"),
        "USP_HIGHLIGHT_LABEL": config.get("usp_highlight_label", "Kundenzufriedenheit"),
        "USP_HIGHLIGHT_SUB": config.get("usp_highlight_sub", "Unsere Kunden empfehlen uns weiter – das ist unser bester Beweis."),
        # Testimonials
        "TESTIMONIAL_1_TEXT": config.get("testimonial_1_text", "Hervorragende Arbeit und absolut zuverlässig. Ich bin sehr zufrieden mit dem Ergebnis und werde definitiv wiederkommen."),
        "TESTIMONIAL_1_NAME": config.get("testimonial_1_name", "Klaus M."),
        "TESTIMONIAL_1_INITIAL": config.get("testimonial_1_initial", "K"),
        "TESTIMONIAL_1_ROLLE": config.get("testimonial_1_rolle", "Privatperson"),
        "TESTIMONIAL_2_TEXT": config.get("testimonial_2_text", "Professionell, pünktlich und zu einem fairen Preis. Genau das, was ich gesucht habe."),
        "TESTIMONIAL_2_NAME": config.get("testimonial_2_name", "Sandra H."),
        "TESTIMONIAL_2_INITIAL": config.get("testimonial_2_initial", "S"),
        "TESTIMONIAL_2_ROLLE": config.get("testimonial_2_rolle", "Unternehmerin"),
        "TESTIMONIAL_3_TEXT": config.get("testimonial_3_text", "Endlich jemand, der sich wirklich Zeit nimmt und die Arbeit mit Herzblut macht. Klare Empfehlung!"),
        "TESTIMONIAL_3_NAME": config.get("testimonial_3_name", "Thomas B."),
        "TESTIMONIAL_3_INITIAL": config.get("testimonial_3_initial", "T"),
        "TESTIMONIAL_3_ROLLE": config.get("testimonial_3_rolle", "Geschäftsführer"),
    }
    return vars


def generate_preview(config: dict) -> Path:
    firmenname = config["firmenname"]
    branche_typ = config["branche_typ"]
    slug = config.get("slug") or slugify(firmenname)

    print(f"🏗  Generating preview for: {firmenname} ({branche_typ}) → /{slug}")

    html = load_template(branche_typ)
    variables = build_variables(config)
    filled_html = fill_template(html, variables)

    output_dir = PREVIEWS_DIR / slug
    output_dir.mkdir(parents=True, exist_ok=True)
    output_file = output_dir / "index.html"
    output_file.write_text(filled_html, encoding="utf-8")

    print(f"✅ Preview generated: {output_file}")
    return output_dir


def main():
    parser = argparse.ArgumentParser(description="ELEVO Preview Generator")
    parser.add_argument("--config", required=True, help="Path to JSON config file")
    parser.add_argument("--batch", action="store_true", help="Config is a JSON array of prospects")
    parser.add_argument("--serve", action="store_true", help="Serve previews locally after generation")
    args = parser.parse_args()

    config_path = Path(args.config)
    if not config_path.exists():
        print(f"❌ Config file not found: {config_path}", file=sys.stderr)
        sys.exit(1)

    PREVIEWS_DIR.mkdir(parents=True, exist_ok=True)

    raw = json.loads(config_path.read_text(encoding="utf-8"))
    configs = raw if isinstance(raw, list) else [raw]

    generated = []
    for cfg in configs:
        try:
            out = generate_preview(cfg)
            generated.append(out)
        except Exception as e:
            print(f"❌ Failed for {cfg.get('firmenname', '?')}: {e}", file=sys.stderr)

    print(f"\n🎉 Done. {len(generated)}/{len(configs)} previews generated in: {PREVIEWS_DIR}")

    if args.serve and generated:
        print(f"\n🌐 Starting local server at http://localhost:8000/previews/")
        os.chdir(ROOT_DIR)
        subprocess.run([sys.executable, "-m", "http.server", "8000"])


if __name__ == "__main__":
    main()
