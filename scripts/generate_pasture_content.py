import os
from datetime import datetime

def format_responsive_post(lane_key, char_name, image_path, joke_caption, hook, body_paras, glossary_term, glossary_def):
    """
    Formats the herd note with mobile/desktop spacing and native Substack callouts.
    """
    body_formatted = "\n\n".join(body_paras)
    
    # 1. Substack-native Markdown
    markdown_content = f"""![{char_name}]({image_path})
*{joke_caption}*

---

**{hook}**

{body_formatted}

> 💡 **Herd Glossary: {glossary_term}**  
> {glossary_def}

---

<p align="center">
  <b>Making crypto less scary, one cartoon cow at a time.</b><br><br>
  👉 <b>Herd up free.</b>
</p>
"""

    # 2. Companion HTML Preview for Mobile/Desktop check
    html_preview = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{char_name} - Herd Note Preview</title>
  <style>
    body {{
      background-color: #f7f7f7;
      margin: 0;
      padding: 20px;
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
    }}
    .container {{
      max-width: 580px;
      margin: 0 auto;
      background: #ffffff;
      border: 1px solid #e5e5e5;
      border-radius: 8px;
      padding: 24px;
      box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }}
    img {{
      width: 100%;
      height: auto;
      border-radius: 6px;
      display: block;
    }}
    .caption {{
      font-size: 13px;
      color: #737373;
      text-align: center;
      margin-top: 8px;
      margin-bottom: 20px;
      font-style: italic;
    }}
    hr {{
      border: none;
      border-top: 1px solid #eaeaea;
      margin: 24px 0;
    }}
    p {{
      font-size: 16px;
      line-height: 1.6;
      color: #262626;
      margin: 0 0 16px 0;
    }}
    .hook {{
      font-weight: 700;
      color: #111111;
    }}
    blockquote {{
      background: #fbfbfb;
      border-left: 4px solid #10b981;
      margin: 20px 0;
      padding: 12px 16px;
      border-radius: 0 6px 6px 0;
    }}
    blockquote strong {{
      color: #065f46;
    }}
    .cta-box {{
      text-align: center;
      padding-top: 8px;
    }}
    .cta-button {{
      display: inline-block;
      margin-top: 8px;
      padding: 10px 24px;
      background-color: #10b981;
      color: #ffffff;
      text-decoration: none;
      font-weight: 600;
      border-radius: 20px;
    }}
  </style>
</head>
<body>
  <div class="container">
    <img src="../../{image_path}" alt="{char_name}">
    <div class="caption">{joke_caption}</div>
    <hr>
    <p class="hook">{hook}</p>
    {"".join([f"<p>{p}</p>" for p in body_paras])}
    <blockquote>
      <strong>💡 Herd Glossary: {glossary_term}</strong><br>
      {glossary_def}
    </blockquote>
    <hr>
    <div class="cta-box">
      <p style="margin-bottom: 6px; font-weight: 600;">Making crypto less scary, one cartoon cow at a time.</p>
      <a href="#" class="cta-button">Herd up free.</a>
    </div>
  </div>
</body>
</html>
"""
    return markdown_content, html_preview
