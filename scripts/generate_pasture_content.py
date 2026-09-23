#!/usr/bin/env python3
"""
The Pasture Content Generator for Substack
Generates comprehensive 600-900 word educational essays paired with properly-scaled visual stills.
"""

import os
import sys
import json
import argparse
from datetime import datetime

ARTICLES = {
    "mom_volatility": {
        "title": "Why Does the Market Move Like That? A Pasture Guide to Volatility and Stablecoins",
        "subtitle": "Mom (Au) explains why crypto charts look like roller coasters, why volatility isn't the enemy, and how digital dollars keep everyday families grounded.",
        "character": "Mom (Au)",
        "image_file": "stills/mom_volatility.png",
        "caption": "Mom doesn't check the 1-minute candle chart. She checks the pasture.",
        "sections": [
            {
                "heading": "The Anatomy of a Crypto Swing",
                "content": (
                    "Most cryptocurrency price charts look like an EKG recorded during a lightning strike. "
                    "If you are new to digital finance, waking up to see an asset you bought yesterday swing 15% by lunch can feel like watching your checking account ride a mechanical bull. "
                    "It is the single biggest reason 70% of crypto owners report feeling overwhelmed, and why millions of everyday families stay outside the pasture fence.\n\n"
                    "Mom (Au) doesn’t panic. She puts the kettle on, pulls on her green plaid vest, and looks past the noise. "
                    "Gold has anchored monetary history for thousands of years because it doesn't bend every time the wind blows. "
                    "In the CryptoCowz universe, that is Mom’s job: to teach the difference between market weather and actual structural value, and to show newcomers where the calm ground is."
                )
            },
            {
                "heading": "1. Why Does Crypto Move Like That?",
                "content": (
                    "In the traditional stock market, companies report earnings quarterly, markets close at 4:00 PM, and circuit breakers freeze trading if prices drop too fast.\n\n"
                    "Crypto doesn't have closing bells, weekends, or bank holidays. It is a 24/7 global auction running across dozens of time zones simultaneously. "
                    "More importantly, most crypto assets are in their price discovery phase. When a new technology emerges—whether railroad stocks in the 1800s or decentralized networks today—nobody knows the exact equilibrium price yet.\n\n"
                    "High volatility makes an asset attractive for speculators looking for adrenaline, but stressful for buying groceries or budgeting for a household. "
                    "If money loses 10% of its purchasing power between the checkout line and the receipt printing, it isn't behaving like money yet."
                )
            },
            {
                "heading": "2. Enter the Stablecoin: The Concrete Dock",
                "content": (
                    "If Bitcoin and Ethereum are open, choppy seas, stablecoins are the concrete dock where your boat stops spinning.\n\n"
                    "A stablecoin is a digital token engineered to stay pegged to an external benchmark—most commonly the United States Dollar ($1.00 USD). "
                    "For every digital dollar issued on-chain, reputable issuers hold cash equivalents and short-term US Treasuries in audited reserve accounts.\n\n"
                    "Why does this matter for ordinary people? Because it gives you the speed, borderless reach, and programmatic power of a blockchain without exposing your grocery fund to the market rollercoaster. "
                    "You don’t have to cash out into a commercial bank or wait three business days over a holiday weekend. With a single tap, you park volatile assets into digital dollars and let the storm pass."
                )
            },
            {
                "heading": "3. The Real-World Alpha: Why Merchants Are Watching",
                "content": (
                    "Stablecoins aren't just a shelter for traders; they are the bridge to Capitalism 2.0.\n\n"
                    "Every time you swipe a traditional credit card at a local shop, the retailer pays a fee of roughly 3.0% to legacy processing networks. "
                    "A standard bank debit card costs them about 1.5%. On a $100 purchase, credit cards siphon $3.00, debit siphons $1.50, but digital dollars on high-speed rails (like USDC on Solana) settle for less than $0.001 in under two seconds.\n\n"
                    "What iTunes did to record stores, digital dollar settlement is poised to do to legacy swipe fees. By eliminating price swings with stablecoins, retailers can embrace digital payments without worrying that tomorrow's revenue won't cover today's inventory."
                )
            },
            {
                "heading": "4. Mom’s 3 Pasture Rules for Market Swings",
                "content": (
                    "1. Never Risk the Winter Hay: Only allocate capital to volatile assets if you don’t need that money for immediate living expenses. Your rent and emergency savings belong in calm waters.\n\n"
                    "2. Separate Speculation from Utility: Understand what you are holding. A meme coin behaves differently than a network protocol with real fee revenue, and both behave differently than a stablecoin.\n\n"
                    "3. Know Where the Dock Sits: Before entering any position, know how to swap into a stablecoin. Practicing when the market is quiet prevents mistakes when emotions run hot."
                )
            }
        ],
        "glossary_term": "Stablecoin",
        "glossary_def": "A cryptocurrency whose value is pegged to another currency, commodity, or financial instrument (most commonly $1.00 USD). Examples include USDC, which provides instant global settlement on blockchain networks without price fluctuations.",
        "prompt": "When the market gets turbulent, what is your instinctive reaction: do you check charts every ten minutes, ignore your screen entirely, or move to stable ground?"
    },
    "dad_stablecoin": {
        "title": "Keeping Your Digital Barn Locked: A Beginner's Guide to Wallets and Keys",
        "subtitle": "Dad (Fe) breaks down why self-custody matters, why seed phrases are not passwords, and how to protect family assets from modern scams.",
        "character": "Dad (Fe)",
        "image_file": "stills/dad_security.png",
        "caption": "Dad changed the barn combination again. Because security never takes a break.",
        "sections": [
            {
                "heading": "Why Dad Never Shares His Seed Phrase",
                "content": (
                    "In traditional banking, if you forget your password, you click a link or call a customer service line. "
                    "On a decentralized blockchain, there is no corporate help desk. You are the sole custodian of your wealth.\n\n"
                    "Dad (Fe) wears green polo shirts, checks his hardware vault twice before bed, and treats security like a structural pillar. "
                    "Iron doesn't bend, and your security habits shouldn't either."
                )
            },
            {
                "heading": "Custodial vs. Non-Custodial: Who Actually Holds the Reins?",
                "content": (
                    "When your crypto sits on a centralized exchange, you hold an IOU. If that exchange halts withdrawals, your access vanishes.\n\n"
                    "A non-custodial wallet puts the cryptographic keys directly on your device. You hold the actual assets—not a promise from a third party."
                )
            }
        ],
        "glossary_term": "Seed Phrase",
        "glossary_def": "A 12-to-24-word recovery phrase that generates your private keys. Whoever controls the phrase controls the funds.",
        "prompt": "Where do you keep your most critical backups: on paper in a fireproof safe, or are you still relying on digital notes?"
    }
}

def generate_markdown_and_html(lane_key):
    data = ARTICLES.get(lane_key, ARTICLES["mom_volatility"])
    date_str = datetime.now().strftime("%Y-%m-%d")
    out_dir = "output/substack"
    os.makedirs(out_dir, exist_ok=True)

    # Build sections
    sections_md = []
    sections_html = []
    for sec in data["sections"]:
        sections_md.append(f"## {sec['heading']}\n\n{sec['content']}")
        paras_html = "".join([f"<p>{p.strip()}</p>" for p in sec['content'].split("\n\n") if p.strip()])
        sections_html.append(f"<h3>{sec['heading']}</h3>{paras_html}")

    sections_md_joined = "\n\n---\n\n".join(sections_md)

    # Markdown File (for Substack Editor)
    md_content = f"""# {data['title']}

### {data['subtitle']}

<div align="center">
  <img src="../../{data['image_file']}" alt="{data['character']}" width="480" style="border-radius: 8px; max-width: 100%; height: auto;" />
  <br>
  <em>{data['caption']}</em>
</div>

---

{sections_md_joined}

---

> 💡 **Herd Glossary: {data['glossary_term']}**  
> {data['glossary_def']}

---

### Pasture Prompt
{data['prompt']}

---

<p align="center">
  <b>The pasture is open. Learn crypto without the headache.</b><br><br>
  👉 <b>Herd up free.</b>
</p>
"""

    # HTML Preview File (with mobile & desktop max-width constraints)
    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{data['title']}</title>
  <style>
    body {{
      background: #f4f4f5;
      padding: 24px 16px;
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
      color: #18181b;
      line-height: 1.65;
    }}
    .article-container {{
      max-width: 640px;
      margin: 0 auto;
      background: #ffffff;
      border: 1px solid #e4e4e7;
      border-radius: 12px;
      padding: 32px 28px;
      box-shadow: 0 4px 12px rgba(0,0,0,0.04);
    }}
    h1 {{
      font-size: 26px;
      line-height: 1.25;
      margin-top: 0;
      color: #09090b;
    }}
    .subtitle {{
      font-size: 16px;
      color: #71717a;
      margin-bottom: 24px;
      line-height: 1.45;
    }}
    .hero-img-wrap {{
      text-align: center;
      margin: 20px 0;
    }}
    .hero-img {{
      max-width: 480px;
      width: 100%;
      height: auto;
      border-radius: 8px;
      border: 1px solid #e4e4e7;
    }}
    .caption {{
      font-size: 13px;
      color: #71717a;
      font-style: italic;
      margin-top: 8px;
    }}
    hr {{
      border: none;
      border-top: 1px solid #e4e4e7;
      margin: 28px 0;
    }}
    h3 {{
      font-size: 20px;
      margin-top: 24px;
      color: #18181b;
    }}
    p {{
      font-size: 16px;
      margin-bottom: 16px;
      color: #27272a;
    }}
    blockquote {{
      background: #f0fdf4;
      border-left: 4px solid #16a34a;
      margin: 24px 0;
      padding: 14px 18px;
      border-radius: 0 8px 8px 0;
    }}
    blockquote strong {{
      color: #15803d;
    }}
    .prompt-box {{
      background: #fafafa;
      border: 1px dashed #d4d4d8;
      border-radius: 8px;
      padding: 16px;
      margin: 20px 0;
    }}
    .cta-wrap {{
      text-align: center;
      margin-top: 32px;
    }}
    .cta-btn {{
      display: inline-block;
      margin-top: 10px;
      padding: 12px 28px;
      background: #16a34a;
      color: #ffffff;
      text-decoration: none;
      font-weight: 600;
      border-radius: 24px;
      font-size: 15px;
    }}
  </style>
</head>
<body>
  <div class="article-container">
    <h1>{data['title']}</h1>
    <div class="subtitle">{data['subtitle']}</div>
    <div class="hero-img-wrap">
      <img src="../../{data['image_file']}" alt="{data['character']}" class="hero-img">
      <div class="caption">{data['caption']}</div>
    </div>
    <hr>
    {"".join(sections_html)}
    <hr>
    <blockquote>
      <strong>💡 Herd Glossary: {data['glossary_term']}</strong><br>
      {data['glossary_def']}
    </blockquote>
    <div class="prompt-box">
      <strong>Pasture Prompt:</strong> {data['prompt']}
    </div>
    <hr>
    <div class="cta-wrap">
      <p style="font-weight: 600; margin-bottom: 8px;">The pasture is open. Learn crypto without the headache.</p>
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

    words = len(md_content.split())
    print(f"[✓] Generated in-depth article: {md_path} ({words} words)")
    print(f"[✓] Generated constrained preview: {html_path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", default="daily_note")
    parser.add_argument("--lane", default="mom_volatility")
    args = parser.parse_args()

    lane = args.lane if args.lane and args.lane != "auto" else "mom_volatility"
    generate_markdown_and_html(lane)
