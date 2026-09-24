#!/usr/bin/env python3
"""
The Pasture Sunday Production Engine
Generates 3 assets every Sunday for the rotating character of the week:
1. Daily In-Depth Note
2. Meet-the-Herd Short
3. Weekly "What the Herd Learned" Digest
"""

import os
import sys
import json
import argparse
from datetime import datetime

ROTATION = ["mom", "dad", "son", "red_twin", "blue_twin"]

CHARACTERS = {
    "mom": {
        "id": "mom",
        "name": "Mom (Au)",
        "domain": "Volatility & Stablecoins",
        "panel_img": "stills/mom_volatility.png",
        "portrait_img": "stills/portraits/mom_au.png",
        "panel_caption": "Mom doesn't check the 1-minute candle chart. She checks the pasture.",
        "portrait_caption": "Unbothered by red candles, unimpressed by green spikes.",
        "daily_title": "Why Does the Market Move Like That? A Pasture Guide to Volatility and Stablecoins",
        "daily_subtitle": "Mom (Au) explains why crypto charts look like roller coasters, why volatility isn't the enemy, and how digital dollars keep everyday families grounded.",
        "glossary_term": "Stablecoin",
        "glossary_def": "A cryptocurrency whose value is pegged to another currency or asset (most commonly $1.00 USD). Examples include USDC, which provides instant global settlement on blockchain networks without price fluctuations.",
        "prompt": "When the market gets turbulent, what is your instinctive reaction: do you check charts every ten minutes, ignore your screen entirely, or move to stable ground?",
        "daily_sections": [
            ("The Anatomy of a Crypto Swing", 
             "Most cryptocurrency price charts look like an EKG recorded during a lightning strike. If you are new to digital finance, waking up to see an asset you bought yesterday swing 15% by lunch can feel like watching your checking account ride a mechanical bull. It is the single biggest reason 70% of crypto owners report feeling overwhelmed, and why millions of everyday families stay outside the pasture fence.\n\nMom (Au) doesn’t panic. She puts the kettle on, pulls on her green plaid vest, and looks past the noise. Gold has anchored monetary history for thousands of years because it doesn't bend every time the wind blows. In the CryptoCowz universe, that is Mom’s job: to teach the difference between market weather and actual structural value, and to show newcomers where the calm ground is."),
            ("1. Why Does Crypto Move Like That?", 
             "In the traditional stock market, companies report earnings quarterly, markets close at 4:00 PM, and circuit breakers freeze trading if prices drop too fast.\n\nCrypto doesn't have closing bells, weekends, or bank holidays. It is a 24/7 global auction running across dozens of time zones simultaneously. More importantly, most crypto assets are in their price discovery phase. When a new technology emerges, nobody knows the exact equilibrium price yet.\n\nHigh volatility makes an asset attractive for speculators looking for adrenaline, but stressful for buying groceries or budgeting for a household. If money loses 10% of its purchasing power between the checkout line and the receipt printing, it isn't behaving like money yet."),
            ("2. Enter the Stablecoin: The Concrete Dock", 
             "If Bitcoin and Ethereum are open, choppy seas, stablecoins are the concrete dock where your boat stops spinning.\n\nA stablecoin is a digital token engineered to stay pegged to an external benchmark—most commonly the United States Dollar ($1.00 USD). For every digital dollar issued on-chain, reputable issuers hold cash equivalents and short-term US Treasuries in audited reserve accounts.\n\nWhy does this matter for ordinary people? Because it gives you the speed, borderless reach, and programmatic power of a blockchain without exposing your grocery fund to the market rollercoaster. You don’t have to cash out into a commercial bank or wait three business days over a holiday weekend. With a single tap, you park volatile assets into digital dollars and let the storm pass."),
            ("3. The Real-World Alpha: Why Merchants Are Watching", 
             "Stablecoins aren't just a shelter for traders; they are the bridge to Capitalism 2.0.\n\nEvery time you swipe a traditional credit card at a local shop, the retailer pays a fee of roughly 3.0% to legacy processing networks. A standard bank debit card costs them about 1.5%. On a $100 purchase, credit cards siphon $3.00, debit siphons $1.50, but digital dollars on high-speed rails (like USDC on Solana) settle for less than $0.001 in under two seconds.\n\nWhat iTunes did to record stores, digital dollar settlement is poised to do to legacy swipe fees. By eliminating price swings with stablecoins, retailers can embrace digital payments without worrying that tomorrow's revenue won't cover today's inventory."),
            ("4. Mom’s 3 Pasture Rules for Market Swings", 
             "1. Never Risk the Winter Hay: Only allocate capital to volatile assets if you don’t need that money for immediate living expenses. Your rent and emergency savings belong in calm waters.\n\n2. Separate Speculation from Utility: Understand what you are holding. A meme coin behaves differently than a network protocol with real fee revenue, and both behave differently than a stablecoin.\n\n3. Know Where the Dock Sits: Before entering any position, know how to swap into a stablecoin. Practicing when the market is quiet prevents mistakes when emotions run hot.")
        ],
        "short_hook": "When prices start swinging like a rodeo gate, Mom (Au) pulls on her green plaid vest and turns the kettle on.",
        "short_body": "Gold has anchored monetary systems for millennia because it doesn't flinch when headlines get dramatic. In the pasture, Mom represents emotional discipline, balance management, and the power of stable value. Her rule is simple: if market volatility is keeping you awake at night, you don't understand your exit dock yet. In a world obsessed with 100x gains, Mom teaches you how to keep what you've already built.",
        "digest_takeaways": [
            "**Price Discovery vs. Panicking:** Volatility happens because global crypto markets run 24/7 without circuit breakers—not because the tech broke.",
            "**The Stablecoin Dock:** Digital dollars (like USDC) give you the speed and ownership of blockchain without exposing your family budget to price swings.",
            "**The 3% Merchant Tax:** Traditional cards take $3.00 on every $100 purchase. Digital dollars settle for a fraction of a cent in under two seconds."
        ],
        "next_tease": "Dad (Fe) changes the locks and reveals why your seed phrase never belongs in the Notes app."
    },
    "dad": {
        "id": "dad",
        "name": "Dad (Fe)",
        "domain": "Security, Wallets & Private Keys",
        "panel_img": "stills/dad_security.png",
        "portrait_img": "stills/portraits/dad_fe.png",
        "panel_caption": "Dad changed the barn combination again. Because security never takes a day off.",
        "portrait_caption": "Has never clicked an unverified email link in his life.",
        "daily_title": "Keeping Your Digital Barn Locked: A Beginner's Guide to Wallets and Keys",
        "daily_subtitle": "Dad (Fe) breaks down why self-custody matters, why seed phrases are not passwords, and how to protect family assets from modern scams.",
        "glossary_term": "Seed Phrase",
        "glossary_def": "A master recovery sequence of 12 to 24 words that generates your private keys on any device. Guard it like physical cash; anyone with these words controls your assets.",
        "prompt": "Where do you store your critical backups: on paper in a fireproof safe, or are you still taking digital screenshots?",
        "daily_sections": [
            ("Why Dad Never Shares His Seed Phrase", 
             "In traditional banking, if you forget your password, you click 'Forgot Password' or visit your local branch with a photo ID. On a decentralized blockchain, there is no corporate customer service hotline. You are the sole custodian of your wealth.\n\nDad (Fe) wears green polos, inspects the family hardware vault twice before bed, and treats security like a structural iron beam. Iron doesn't bend, and your security habits shouldn't either."),
            ("1. Custodial vs. Non-Custodial: Who Holds the Keys?", 
             "When your crypto sits on a centralized exchange, you do not hold coins—you hold an IOU. If that exchange freezes withdrawals or mismanages reserves, you become an unsecured creditor standing in line.\n\nA non-custodial wallet stores cryptographic private keys directly on your physical hardware or secure device. You hold the actual asset, meaning no third party can freeze, confiscate, or re-lend your balance."),
            ("2. The Cardinal Rules of the Seed Phrase", 
             "A seed phrase is not a routine web password. It is the cryptographic master root to every address in your wallet.\n\n• Never type your seed phrase on a keyboard connected to the internet.\n• Never screenshot your seed phrase on a phone.\n• Never upload your seed phrase to cloud storage, notes apps, or email drafts.\n• Write it down on physical paper or stamp it into stainless steel, and lock it in a fireproof location."),
            ("3. Spotting Scams Before They Spot You", 
             "Blockchain transactions are irreversible. Once funds leave your address, no bank manager can reverse the charge. Scammers exploit urgency, impersonate official support accounts, and set up fake dApp clones.\n\nDad's rule: Double-check every transaction prompt on your hardware screen, verify contract URLs, and treat any unsolicited message offering 'wallet verification' as a direct attack.")
        ],
        "short_hook": "Dad (Fe) has checked the barn padlocks twice, updated his password manager, and still won't let you use the public Wi-Fi.",
        "short_body": "Iron represents strength, vaults, and the quiet heavy lifting that keeps things from falling apart. On a blockchain, freedom and responsibility are two sides of the same coin. If you don't control your private keys, you don't own your money. Dad is the resident sentry ensuring the herd learns good habits before paying expensive tuition to an online scam.",
        "digest_takeaways": [
            "**Self-Custody Reality:** Centralized exchanges issue promises; private wallets give you mathematical ownership.",
            "**Zero Digital Footprints for Keys:** Seed phrases must never touch the cloud, camera rolls, or notes apps.",
            "**Hardware is Essential:** For significant balances, dedicated hardware signing devices isolate keys from compromised laptops."
        ],
        "next_tease": "Son (Ge) takes digital dollars to the street to find out where you can actually buy coffee with crypto."
    },
    "son": {
        "id": "son",
        "name": "Son (Ge)",
        "domain": "Merchant Acceptance & Real-World Utility",
        "panel_img": "stills/son_acceptance.png",
        "portrait_img": "stills/portraits/son_ge.png",
        "panel_caption": "Son is trying to buy a latte with cold storage.",
        "portrait_caption": "Convinced every store in town can run without swipe fees by Friday.",
        "daily_title": "Beyond the Screen: Where Can You Actually Spend Crypto in the Real World?",
        "daily_subtitle": "Son (Ge) maps out point-of-sale adoption, QR code payments, and how small businesses save thousands by cutting out credit card swipe fees.",
        "glossary_term": "Merchant Settlement",
        "glossary_def": "The infrastructure and payment rails that allow a business to accept digital currency at the register and receive instant, guaranteed settlement without legacy bank delays.",
        "prompt": "Have you ever tried paying for a real-world item with crypto? What was the biggest barrier—merchant confusion or transaction speed?",
        "daily_sections": [
            ("Digital Wealth Is Useless If You Can't Buy Lunch", 
             "Having digital wealth on a computer screen is fine, but the real revolution happens when you can buy groceries, pay a plumber, or purchase coffee without paying tribute to legacy financial tollbooths.\n\nSon is Ge (germanium)—the semiconductor material that bridges hardware and software. In the pasture, he is the curious scout walking into local businesses, asking why card processing fees are so high, and mapping out the real-world utility of digital currency."),
            ("1. The Retail Dilemma: The Hidden 3% Tax", 
             "Every time an everyday customer taps a credit card, the merchant loses 2.5% to 3.5% of the total ticket price to payment gateways, interchange processors, and card networks. For high-volume, low-margin businesses like grocery stores and cafes, credit card swipe fees often exceed their total utility costs.\n\nWith digital dollars on high-speed networks, payment settlement happens peer-to-peer in seconds for less than a penny. That margin stays in the business or gets passed back as customer discounts."),
            ("2. Point-of-Sale Integration: The QR Revolution", 
             "Nobody wants to copy-paste a 42-character alphanumeric address into a phone at a busy checkout counter. Modern crypto merchant solutions use dynamic QR codes and Solana Pay rails that let users scan, approve on their mobile wallet, and settle instantly.\n\nThe merchant receives guaranteed digital dollars directly into their treasury account—with zero chargeback risk, zero foreign exchange markup, and instant access to cash flow.")
        ],
        "short_hook": "Son (Ge) already walked three miles ahead of the herd to find out which diners in town accept QR payments.",
        "short_body": "Named after Germanium, the foundational semiconductor that connects physical elements to digital processing, Son is focused on practical adoption. While market traders argue about token charts, Son cares about whether a family can buy groceries without paying 3% card fees to a conglomerate bank. He is building the merchant map for the new economy.",
        "digest_takeaways": [
            "**The 3% Swipe Tax:** Credit card processing fees quietly drain small retailers; digital payment rails eliminate them.",
            "**Sub-Second QR Checkout:** Modern merchant crypto payments use simple QR scans that settle in 2 seconds flat.",
            "**Zero Chargeback Fraud:** Blockchain settlement is final and guaranteed, protecting retailers from costly friendly fraud."
        ],
        "next_tease": "Red Twin (Li) hits the gas to explain why blockchain transactions shouldn't take ten minutes or cost $15."
    },
    "red_twin": {
        "id": "red_twin",
        "name": "Red Twin (Li)",
        "domain": "Speed, Fees & Layer 2 Scaling",
        "panel_img": "stills/red_speed_l2.png",
        "portrait_img": "stills/portraits/red_li.png",
        "panel_caption": "Red Twin is tapping her hoof waiting for the block confirmation.",
        "portrait_caption": "Life is too short for slow blocks and high gas fees.",
        "daily_title": "The Fast Lane: Why Transaction Speed and Layer 2s Matter for Everyday Life",
        "daily_subtitle": "Red Twin (Li) breaks down gas fees, network congestion, and how Layer 2 scaling makes digital payments practical for the real world.",
        "glossary_term": "Layer 2 (L2)",
        "glossary_def": "A secondary network built on top of a base blockchain (Layer 1) that bundles transactions together to achieve high speed and fees under a penny while maintaining security.",
        "prompt": "What is the highest transaction fee you've ever encountered? Did it make you reconsider using that network?",
        "daily_sections": [
            ("Why Is the Blockchain So Slow Sometimes?", 
             "Imagine pulling up to a highway toll booth, and instead of paying a fixed $2 fee, the attendant asks you to bid against a hundred other drivers for the privilege of driving through first.\n\nThat is how gas fees work during peak traffic on congested base chains. If thousands of people try to mint NFTs or execute trades simultaneously, transaction fees spike from pennies to $40, and confirmations grind to a halt. Red Twin (Li)—named after light, energetic Lithium—has zero patience for waiting in line."),
            ("1. How Layer 2 Networks Build the Express Highway", 
             "A Layer 1 blockchain like Ethereum is the supreme court of security—highly decentralized, robust, but inherently limited in transaction throughput. You wouldn't use the supreme court to adjudicate a parking ticket.\n\nLayer 2 solutions (like Arbitrum, Optimism, or Polygon) and high-throughput chains like Solana act as regional express lanes. They process thousands of transactions off the main bottleneck, bundle them together, and write a single cryptographic proof back to the base layer. You get the ironclad security of Layer 1 with the speed of a credit card swipe."),
            ("2. Micropayments: The Unlocked Frontier", 
             "When transaction costs drop below $0.001, entirely new business models become possible. You can stream fractions of a cent per minute to music artists, tip creators half a penny for an article, or automate tiny machine-to-machine payments without overhead. That is what Red Twin is racing toward.")
        ],
        "short_hook": "Red Twin (Li) has already crossed the transaction bridge twice while everyone else is still waiting for their gas estimate.",
        "short_body": "Lithium is light, fast, and packed with energy. If an app takes more than two seconds or costs more than a stick of gum to send a dollar, Red Twin wants to know why we are settling for yesterday's infrastructure. She is the advocate for Layer 2 rollups, sub-penny fees, and lightning-fast rails that make crypto feel invisible to the user.",
        "digest_takeaways": [
            "**Gas Fees Explained:** Gas is the bidding market for limited blockspace; when demand surges, legacy chains get expensive.",
            "**The Layer 2 Solution:** L2 networks bundle hundreds of transfers into single proofs, keeping fees under a penny.",
            "**Real-Time Settlement:** Everyday money requires sub-second finality so nobody stands awkwardly at the register waiting for confirmations."
        ],
        "next_tease": "Blue Twin (Bi) pulls out the rulebook to show why smart regulation and consumer rights protect the herd."
    },
    "blue_twin": {
        "id": "blue_twin",
        "name": "Blue Twin (Bi)",
        "domain": "Regulation, Compliance & Rights",
        "panel_img": "stills/blue_custody.png",
        "portrait_img": "stills/portraits/blue_bi.png",
        "panel_caption": "Blue Twin brought a binder and a tape measure to inspect the pasture fence.",
        "portrait_caption": "Actually reads the terms of service and regulatory disclosures.",
        "daily_title": "Fences in the Pasture: Why Clear Rules and Consumer Protections Matter",
        "daily_subtitle": "Blue Twin (Bi) unpacks crypto regulations, custodial rights, KYC, and how smart guardrails keep innovators safe from bad actors.",
        "glossary_term": "KYC / AML",
        "glossary_def": "Know Your Customer and Anti-Money Laundering—compliance standards that require financial services to verify customer identity to prevent illicit activity.",
        "prompt": "Do you view regulation as an obstacle to innovation, or as necessary guardrails for mass adoption?",
        "daily_sections": [
            ("Everyone Hates the Fence Until Wolves Show Up", 
             "Crypto culture loves to celebrate decentralization and total freedom, but without clear fences, bad actors exploit unsuspecting newcomers. When an offshore exchange collapses, regular families find out that 'unregulated' often just meant 'unprotected.'\n\nBlue Twin is Bi (bismuth)—an element known for forming orderly, multi-colored stair-step crystals. In the pasture, she represents legal clarity, structural order, and consumer rights. Rules aren't villains when they are designed to protect users instead of entrenching monopoly banks."),
            ("1. The Difference Between Ownership and an IOU", 
             "If you deposit cash in a traditional bank, FDIC insurance protects your balance up to $250,000. If you keep tokens on an unregulated offshore exchange, there is no safety net. If the company mismanages customer funds, your assets can be locked in bankruptcy court for years.\n\nBlue Twin advocates for clear reserve auditing, segregated customer assets, and transparent custody standards. When regulation is done right, it forces platforms to prove they actually have your money."),
            ("2. Privacy vs. Compliance: Finding the Balance", 
             "Legitimate users deserve financial privacy, but society requires safeguards against money laundering and fraud. The path forward is verifiable cryptographic proofs (zero-knowledge technology) that allow people to prove they are compliant law-abiding citizens without handing over their entire financial life history to third-party databases.")
        ],
        "short_hook": "Blue Twin (Bi) brought a highlighter, a binder, and thirty pages of compliance filings to the morning pasture meeting.",
        "short_body": "Bismuth is architectural, vibrant, and precise. Regulation can sound dry, but Blue Twin understands that clear legal guardrails are what turn experimental technology into institutional infrastructure. She stands at the fence line making sure bad actors stay out and everyday users keep their rights.",
        "digest_takeaways": [
            "**Regulation Protects Users:** Sensible guardrails distinguish legitimate financial tools from predatory schemes.",
            "**Segregated Reserves:** Exchanges must hold customer assets 1:1, preventing rehypothecation and insolvency.",
            "**Zero-Knowledge Compliance:** New cryptography allows identity verification without exposing personal financial privacy."
        ],
        "next_tease": "Mom (Au) returns to the pasture to show how to anchor family finances during unexpected market storms."
    }
}

def render_html_preview(title, subtitle, img_src, caption, body_html, cta_text="Herd up free."):
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{title}</title>
  <style>
    body {{ background: #f4f4f5; padding: 24px 16px; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; color: #18181b; line-height: 1.65; }}
    .container {{ max-width: 620px; margin: 0 auto; background: #fff; border: 1px solid #e4e4e7; border-radius: 12px; padding: 32px 28px; box-shadow: 0 4px 12px rgba(0,0,0,0.04); }}
    h1 {{ font-size: 26px; line-height: 1.25; margin-top: 0; color: #09090b; }}
    .subtitle {{ font-size: 16px; color: #71717a; margin-bottom: 24px; line-height: 1.45; }}
    .img-wrap {{ text-align: center; margin: 20px 0; }}
    .img-wrap img {{ max-width: 480px; width: 100%; height: auto; border-radius: 8px; border: 1px solid #e4e4e7; }}
    .caption {{ font-size: 13px; color: #71717a; font-style: italic; margin-top: 8px; }}
    hr {{ border: none; border-top: 1px solid #e4e4e7; margin: 28px 0; }}
    h3 {{ font-size: 20px; margin-top: 24px; color: #18181b; }}
    p {{ font-size: 16px; margin-bottom: 16px; color: #27272a; }}
    blockquote {{ background: #f0fdf4; border-left: 4px solid #16a34a; margin: 24px 0; padding: 14px 18px; border-radius: 0 8px 8px 0; }}
    blockquote strong {{ color: #15803d; }}
    .prompt-box {{ background: #fafafa; border: 1px dashed #d4d4d8; border-radius: 8px; padding: 16px; margin: 20px 0; }}
    .cta-wrap {{ text-align: center; margin-top: 32px; }}
    .cta-btn {{ display: inline-block; margin-top: 10px; padding: 12px 28px; background: #16a34a; color: #fff; text-decoration: none; border-radius: 24px; font-weight: 600; font-size: 15px; }}
  </style>
</head>
<body>
  <div class="container">
    <h1>{title}</h1>
    <div class="subtitle">{subtitle}</div>
    <div class="img-wrap">
      <img src="../../{img_src}" alt="Pasture Still">
      <div class="caption">{caption}</div>
    </div>
    <hr>
    {body_html}
    <hr>
    <div class="cta-wrap">
      <p style="font-weight: 600; margin-bottom: 8px;">The pasture is open. Learn crypto without the headache.</p>
      <a href="#" class="cta-btn">{cta_text}</a>
    </div>
  </div>
</body>
</html>
"""

def generate_weekly_bundle(char_key):
    c = CHARACTERS.get(char_key, CHARACTERS["mom"])
    date_str = datetime.now().strftime("%Y-%m-%d")
    out_dir = "output/substack"
    os.makedirs(out_dir, exist_ok=True)

    # 1. Daily In-Depth Note
    daily_md_sections = []
    daily_html_sections = []
    for heading, text in c["daily_sections"]:
        daily_md_sections.append(f"## {heading}\n\n{text}")
        paras_html = "".join([f"<p>{p.strip()}</p>" for p in text.split("\n\n") if p.strip()])
        daily_html_sections.append(f"<h3>{heading}</h3>{paras_html}")

    daily_md = f"""# {c['daily_title']}

### {c['daily_subtitle']}

<div align="center">
  <img src="../../{c['panel_img']}" alt="{c['name']}" width="480" style="border-radius: 8px; max-width: 100%; height: auto;" />
  <br>
  <em>{c['panel_caption']}</em>
</div>

---

{"\n\n---\n\n".join(daily_md_sections)}

---

> 💡 **Herd Glossary: {c['glossary_term']}**  
> {c['glossary_def']}

---

### Pasture Prompt
{c['prompt']}

---

<p align="center">
  <b>The pasture is open. Learn crypto without the headache.</b><br><br>
  👉 <b>Herd up free.</b>
</p>
"""
    daily_html_body = "".join(daily_html_sections) + f"""
    <blockquote>
      <strong>💡 Herd Glossary: {c['glossary_term']}</strong><br>
      {c['glossary_def']}
    </blockquote>
    <div class="prompt-box">
      <strong>Pasture Prompt:</strong> {c['prompt']}
    </div>
    """
    daily_html = render_html_preview(c['daily_title'], c['daily_subtitle'], c['panel_img'], c['panel_caption'], daily_html_body)

    # 2. Meet-the-Herd Short
    short_title = f"Meet the Herd: {c['name']} on {c['domain']}"
    short_subtitle = f"One character, one lane, and zero lore dumps."
    short_md = f"""# {short_title}

### {short_subtitle}

<div align="center">
  <img src="../../{c['portrait_img']}" alt="{c['name']}" width="320" style="border-radius: 50%; max-width: 80%; height: auto;" />
  <br>
  <em>{c['portrait_caption']}</em>
</div>

---

**{c['short_hook']}**

{c['short_body']}

> 💡 **Pasture Role:** {c['name']} leads the educational lane for **{c['domain']}**.

---

<p align="center">
  <b>Meet the family turning finance into plain English.</b><br><br>
  👉 <b>Herd up free.</b>
</p>
"""
    short_html_body = f"""
    <p><strong>{c['short_hook']}</strong></p>
    <p>{c['short_body']}</p>
    <blockquote>
      <strong>💡 Pasture Role:</strong> {c['name']} leads the educational lane for <strong>{c['domain']}</strong>.
    </blockquote>
    """
    short_html = render_html_preview(short_title, short_subtitle, c['portrait_img'], c['portrait_caption'], short_html_body)

    # 3. Weekly Digest
    digest_title = f"What the Herd Learned This Week: The {c['name']} Report"
    digest_subtitle = f"Three key takeaways from {c['name']} on {c['domain']}, plus what’s grazing next."
    takeaways_md = "\n\n".join([f"• {t}" for t in c["digest_takeaways"]])
    takeaways_html = "<ul>" + "".join([f"<li style='margin-bottom: 12px;'>{t}</li>" for t in c["digest_takeaways"]]) + "</ul>"

    digest_md = f"""# {digest_title}

### {digest_subtitle}

<div align="center">
  <img src="../../{c['panel_img']}" alt="{c['name']}" width="480" style="border-radius: 8px; max-width: 100%; height: auto;" />
  <br>
  <em>{c['panel_caption']}</em>
</div>

---

### What the Herd Learned This Week

{takeaways_md}

---

### Grazing Next Week
{c['next_tease']}

---

<p align="center">
  <b>Never miss a lesson from the pasture.</b><br><br>
  👉 <b>Herd up free.</b>
</p>
"""
    digest_html_body = f"""
    <h3>What the Herd Learned This Week</h3>
    {takeaways_html}
    <hr>
    <h3>Grazing Next Week</h3>
    <p>{c['next_tease']}</p>
    """
    digest_html = render_html_preview(digest_title, digest_subtitle, c['panel_img'], c['panel_caption'], digest_html_body)

    # Save to output/substack
    files_to_write = [
        (f"{date_str}_{c['id']}_daily_note.md", daily_md),
        (f"{date_str}_{c['id']}_daily_note.html", daily_html),
        (f"{date_str}_{c['id']}_character_short.md", short_md),
        (f"{date_str}_{c['id']}_character_short.html", short_html),
        (f"{date_str}_{c['id']}_weekly_digest.md", digest_md),
        (f"{date_str}_{c['id']}_weekly_digest.html", digest_html),
    ]

    print(f"\n=======================================================")
    print(f"[*] Generating Sunday Bundle for: {c['name']} ({c['domain']})")
    print(f"=======================================================")
    for fname, content in files_to_write:
        fpath = os.path.join(out_dir, fname)
        with open(fpath, "w", encoding="utf-8") as fp:
            fp.write(content.strip() + "\n")
        words = len(content.split())
        print(f"[✓] Created {fname} ({words} words)")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--character", default="auto", choices=["auto", "mom", "dad", "son", "red_twin", "blue_twin"])
    args = parser.parse_args()

    if args.character == "auto":
        week_num = datetime.now().isocalendar()
        char_key = ROTATION[week_num % len(ROTATION)]
        print(f"[*] Auto-selected character based on Calendar Week {week_num}: {char_key.upper()}")
    else:
        char_key = args.character
        print(f"[*] Manually selected character: {char_key.upper()}")

    generate_weekly_bundle(char_key)
    print("\n[*] Sunday Production Bundle Complete.")
