#!/usr/bin/env python3
"""
The Pasture Content Generator for Substack
Generates 150-250 word responsive Markdown and HTML preview files.
"""

import os
import sys
import json
import argparse
from datetime import datetime

# Built-in fallbacks if config/editorial_queue.json is missing
FALLBACK_DATA = {
    "mom_volatility": {
        "character": "Mom (Au)",
        "image_file": "stills/mom_volatility.png",
        "caption": "Mom doesn't check the ticker. She checks the pasture.",
        "hook": "Most crypto charts look like a roller coaster designed by someone with a personal grudge.",
        "paragraphs": [
            "When the market drops 20% before your morning coffee, panic is usually the default setting.",
            "Mom doesn't panic. She simply switches pastures.",
            "If Bitcoin is an open, choppy sea, stablecoins are the concrete dock where your boat stops spinning. You don't have to cash out into fiat, deal with bank wires, and wait three business days just to catch your breath.",
            "You park your balance in a digital dollar, let the market storm pass, and keep your breakfast down."
        ],
        "glossary_term": "Stablecoin",
        "glossary_def": "A digital dollar (like USDC) designed to stay pegged to $1.00 so your balance remains steady while the market swings."
    },
    "dad_stablecoin": {
        "character": "Dad (Fe)",
        "image_file": "stills/dad_security.png",
        "caption": "Dad changed the barn combination again.",
        "hook": "In crypto, there is no friendly branch manager named Bob to reset your forgotten password.",
        "paragraphs": [
            "Dad treats passwords like military secrets because on a blockchain, self-custody means full responsibility.",
            "If someone gets their hands on your master recovery phrase, they don't just access an account—they take the keys to the entire farm.",
            "Keeping your crypto secure isn't about paranoia; it's about basic hygiene. Never store seed phrases in cloud notes, never take screenshots of private keys, and never trust a link sent in an unsolicited direct message."
        ],
        "glossary_term": "Seed Phrase",
        "glossary_def": "A master recovery sequence of 12 to 24 words that unlocks your digital vault on any device. Guard it like physical cash."
    },
    "blue_custody": {
        "character": "Blue Twin (Bi)",
        "image_file": "stills/blue_custody.png",
        "caption": "Blue Twin brought a clipboard to inspect the pasture fence.",
        "hook": "Everyone hates the fence until wolves start circling the barnyard.",
        "paragraphs": [
            "In traditional finance, rules usually mean stacks of paperwork designed to make your eyes glaze over.",
            "In crypto, understanding custody rules is the difference between owning your assets and holding an unsecured IOU from an offshore platform.",
            "Blue Twin reads the disclosures so you don't have to. When you hold your own keys, you don't have to worry about an exchange freezing withdrawals when trading volume spikes."
        ],
        "glossary_term": "Self-Custody",
        "glossary_def": "Holding your own private keys directly so no third-party bank or exchange can freeze, lend, or lose your funds."
    },
    "son_acceptance": {
        "character": "Son (Ge)",
        "image_file": "stills/son_acceptance.png",
        "caption": "Son is trying to buy a latte with cold storage.",
        "hook": "Digital wealth is exciting until the cashier asks why you are waving a flash drive at the card reader.",
        "paragraphs": [
            "The future of money isn't supposed to stay locked on a desktop screen. It's supposed to work at the corner bodega.",
            "Credit card networks charge merchants up to 3% on every single purchase. Over a year, that is enough to put a small retailer out of business.",
            "Son is out mapping the spots where paying with digital currency settles in under two seconds for less than a tenth of a penny. That is real adoption."
        ],
        "glossary_term": "Merchant Settlement",
        "glossary_def": "The payment rail that allows a store to accept digital dollars instantly without paying traditional swipe fees."
    },
    "weekly_digest": {
        "character": "The Full Herd",
        "image_file": "stills/weekly_digest_header.png",
        "caption": "What the herd learned this week under the aurora.",
        "hook": "Crypto moves fast, but the pasture keeps it simple.",
        "paragraphs": [
            "Here are the three lessons the herd brought back to the barn this week:",
            "• **Volatility:** Mom showed why switching into a stablecoin dock beats riding out a 20% drop on an empty stomach.",
            "• **Security:** Dad reminded us that seed phrases never go into your phone's Notes app or screenshots.",
            "• **Acceptance:** Son mapped out how local shops save 3% in swipe fees by settling on modern digital rails.",
            "Next week: Red Twin investigates why a $5 transaction shouldn't cost $15 in network gas fees."
        ],
        "glossary_term": "Algorithmic Liberty",
        "glossary_def": "Using automation and smart systems to reduce financial stress and make calmer decisions about your money."
    }
}

def load_lane_data(lane_key):
    """Loads lane from config file if available, otherwise uses fallback."""
    config_path = "config/editorial_queue.json"
    if os.path.exists(config_path):
        try:
            with open(config_path, "r") as f:
                cfg = json.load(f)
                sched = cfg.get("weekday_schedule", {})
                for day, entry in sched.items():
                    if entry.get("lane") == lane_key:
                        return {
                            "character": entry.get("character", "CryptoCowz"),
                            "image_file": entry.get("image_file", f"stills/{lane_key}.png"),
                            "caption": entry.get("joke_caption", ""),
                            "hook": entry.get("hook_premise", ""),
                            "paragraphs": [entry.get("lesson_topic", "")],
                            "glossary_term": entry.get("glossary_term", "Crypto"),
                            "glossary_def": entry.get("glossary_definition", "")
                        }
        except Exception as e:
            print(f"[!] Warning reading {config_path}: {e}. Using fallback data.")

    return FALLBACK_DATA.get(lane_key, FALLBACK_DATA["mom_volatility"])

def build_outputs(lane_key):
    data = load_lane_data(lane_key)
    date_str = datetime.now().strftime("%Y-%m-%d")
    out_dir = "output/substack"
    os.makedirs(out_dir, exist_ok=True)

    body_text = "\n\n".join(data["paragraphs"])

    # 1. Generate Substack-Ready Markdown
    md_content = f"""![{data['character']}](../../{data['image_file']})
*{data['caption']}*

---

**{data['hook']}**

{body_text}

> 💡 **Herd Glossary: {data['glossary_term']}**  
> {data['glossary_def']}

---

<p align="center">
  <b>Making crypto less scary, one cartoon cow at a time.</b><br><br>
  👉 <b>Herd up free.</b>
</p>
"""

    # 2. Generate HTML Preview for Mobile/Desktop check
    html_content = f"""<!DOCTYPE html>
<html>
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{data['character']} - Substack Preview</title>
  <style>
    body {{ background: #f7f7f7; padding: 20px; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; }}
    .card {{ max-width: 580px; margin: 0 auto; background: #fff; border: 1px solid #ddd; border-radius: 8px; padding: 24px; }}
    img {{ width: 100%; border-radius: 6px; display: block; }}
    .caption {{ font-size: 13px; color: #666; text-align: center; margin: 8px 0 20px 0; font-style: italic; }}
    hr {{ border: none; border-top: 1px solid #eee; margin: 20px 0; }}
    p {{ font-size: 16px; line-height: 1.6; color: #222; margin-bottom: 14px; }}
    .hook {{ font-weight: bold; font-size: 17px; }}
    blockquote {{ background: #f8fafc; border-left: 4px solid #10b981; padding: 12px 16px; margin: 18px 0; }}
    .cta {{ text-align: center; margin-top: 20px; }}
    .cta-btn {{ display: inline-block; padding: 10px 24px; background: #10b981; color: #fff; text-decoration: none; border-radius: 20px; font-weight: bold; }}
  </style>
</head>
<body>
  <div class="card">
    <img src="../../{data['image_file']}" alt="{data['character']}">
    <div class="caption">{data['caption']}</div>
    <hr>
    <p class="hook">{data['hook']}</p>
    {"".join([f"<p>{p}</p>" for p in data['paragraphs']])}
    <blockquote>
      <strong>💡 Herd Glossary: {data['glossary_term']}</strong><br>
      {data['glossary_def']}
    </blockquote>
    <hr>
    <div class="cta">
      <p><b>Making crypto less scary, one cartoon cow at a time.</b></p>
      <a href="#" class="cta-btn">Herd up free.</a>
    </div>
  </div>
</body>
</html>
"""

    md_path = os.path.join(out_dir, f"{date_str}_{lane_key}.md")
    html_path = os.path.join(out_dir, f"{date_str}_{lane_key}.html")

    with open(md_path, "w", encoding="utf-8") as f:
        f.write(md_content.strip() + "\n")
    with open(html_path, "w", encoding="utf-8") as f:
        f.write(html_content.strip() + "\n")

    word_count = len(md_content.split())
    print(f"[✓] Created Markdown: {md_path} ({word_count} words)")
    print(f"[✓] Created HTML Preview: {html_path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", default="daily_note")
    parser.add_argument("--lane", default="mom_volatility")
    args = parser.parse_args()

    # Normalize lane parameter
    lane = args.lane if args.lane and args.lane != "auto" else "mom_volatility"
    if args.mode == "weekly_digest":
        lane = "weekly_digest"

    print(f"[*] Starting Pasture Generator (Mode: {args.mode}, Lane: {lane})...")
    build_outputs(lane)
    print("[*] Generation finished successfully.")
