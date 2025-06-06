import os
import requests
import html
import base64

# Set the output file path for HTML and README
script_dir = os.path.dirname(os.path.abspath(__file__))
html_file_path = os.path.join(script_dir, "Unicode.html")
readme_file_path = os.path.join(script_dir, "README.md")

# Fetch the latest emoji list from Unicode
url = "https://unicode.org/Public/emoji/latest/emoji-test.txt"
response = requests.get(url)
emoji_data = response.text

# Parse emoji entries
rows = []
for line in emoji_data.splitlines():
    if line.strip() and not line.startswith("#"):
        parts = line.split(';')
        if len(parts) > 1 and 'fully-qualified' in parts[1]:
            emoji = line.split('#')[1].strip().split(' ')[0]
            description = ' '.join(line.split('#')[1].strip().split(' ')[1:])
            codepoints = parts[0].strip()
            rows.append((emoji, codepoints, description))

# Create SVG for the 👽 emoji
svg_content = """
<svg xmlns="http://www.w3.org/2000/svg" width="64" height="64" viewBox="0 0 64 64">
  <text x="0" y="50" font-size="50" font-family="Arial, sans-serif">👽</text>
</svg>
"""

# Base64 encode the SVG content
encoded_svg = base64.b64encode(svg_content.encode('utf-8')).decode('utf-8')

# Begin HTML content (adding favicon here)
html_output = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Unicode Emoji List</title>
    
    <!-- Favicon (Base64 encoded SVG with emoji) -->
    <link rel="icon" type="image/svg+xml" href="data:image/svg+xml;base64,{encoded_svg}">
    
    <style>
        :root {{
            --bg-color: #f4f4f4;
            --text-color: #333;
            --header-bg: #f2f2f2;
            --border-color: #ddd;
            --hover-color: #eee;
            --input-bg: #fff;
            --input-border: #ccc;
        }}

        @media (prefers-color-scheme: dark) {{
            :root {{
                --bg-color: #1e1e1e;
                --text-color: #e0e0e0;
                --header-bg: #2d2d2d;
                --border-color: #444;
                --hover-color: #3a3a3a;
                --input-bg: #2d2d2d;
                --input-border: #555;
            }}
        }}

        body {{
            font-family: sans-serif; 
            margin: 0; 
            padding: 20px; 
            display: flex; 
            flex-direction: column; 
            align-items: center; 
            background-color: var(--bg-color);
            color: var(--text-color);
            transition: background-color 0.3s ease, color 0.3s ease;
        }}
        h1 {{ text-align: center; font-size: 2em; margin-bottom: 20px; color: var(--text-color); }}
        input[type="text"] {{
            width: 100%;
            max-width: 600px;
            padding: 12px;
            margin-bottom: 20px;
            font-size: 1.2em;
            border: 2px solid var(--input-border);
            border-radius: 5px;
            box-sizing: border-box;
            background-color: var(--input-bg);
            color: var(--text-color);
        }}
        table {{
            width: 100%;
            max-width: 1000px;
            border-collapse: collapse;
            box-sizing: border-box;
        }}
        th, td {{
            padding: 12px 15px;
            text-align: left;
            border: 1px solid var(--border-color);
        }}
        th {{
            background-color: var(--header-bg);
            font-weight: bold;
        }}
        td.emoji {{
            font-size: 1.5em;
        }}
        tr.hidden {{
            display: none;
        }}
        .copy-btn {{
            padding: 4px 8px;
            font-size: 0.9em;
            cursor: pointer;
            background-color: var(--hover-color);
            border: 1px solid var(--border-color);
            border-radius: 4px;
            color: var(--text-color);
        }}
        .copy-btn:hover {{
            background-color: var(--border-color);
        }}
        @media (max-width: 600px) {{
            h1 {{ font-size: 1.6em; }}
            table {{ font-size: 0.9em; width: 90%; }}
            input[type="text"] {{ font-size: 1em; padding: 10px; }}
        }}
    </style>
</head>
<body>
    <h1>Unicode Emoji List</h1>
    <input type="text" id="searchInput" placeholder="Search emojis...">
    <table id="emojiTable">
        <thead>
            <tr><th>Emoji</th><th>Codepoints</th><th>Description</th><th>Copy</th></tr>
        </thead>
        <tbody>
"""

# Add emoji rows to HTML
for emoji, codepoints, description in rows:
    search_text = f"{emoji} {codepoints} {description}".lower()
    html_output += f"""
        <tr data-search="{html.escape(search_text)}">
            <td class='emoji'>{html.escape(emoji)}</td>
            <td>{html.escape(codepoints)}</td>
            <td>{html.escape(description)}</td>
            <td><button onclick="copyToClipboard(event, '{emoji}')" class="copy-btn">Copy</button></td>
        </tr>
    """ 

# Close HTML
html_output += """
        </tbody>
    </table>
    <script>
        const input = document.getElementById('searchInput');
        const rows = Array.from(document.querySelectorAll('#emojiTable tbody tr'));

        function debounce(func, delay) {
            let timer;
            return function() {
                clearTimeout(timer);
                timer = setTimeout(() => func.apply(this, arguments), delay);
            };
        }

        const filterRows = debounce(function() {
            const filter = input.value.toLowerCase();
            rows.forEach(row => {
                const haystack = row.dataset.search;
                row.classList.toggle('hidden', !haystack.includes(filter));
            });
        }, 100);

        input.addEventListener('input', filterRows);

        function copyToClipboard(event, text) {
            navigator.clipboard.writeText(text).then(() => {
                const btns = document.querySelectorAll('.copy-btn');
                btns.forEach(btn => {
                    if (btn.innerText === 'Copied!') btn.innerText = 'Copy';
                });
                const button = event.target;
                if (button) {
                    button.innerText = 'Copied!';
                    setTimeout(() => button.innerText = 'Copy', 1200);
                }
            }).catch(err => {
                alert('Failed to copy: ' + err);
            });
        }
    </script>
</body>
</html>
"""

# Write HTML to file
with open(html_file_path, "w", encoding="utf-8") as f:
    f.write(html_output)

print(f"✅ Unicode.html created at: {html_file_path}")

# Begin README.md content with Markdown table (Updated)
readme_content = """

<h2>🚀 Instructions</h2>

1. Download and run.
2. Search directly from [Unicode Search Bar](https://pixel-hopper.github.io/Unicode/Unicode.html)

<h2>📜 License</h2>

- Unicode data is sourced from the [Unicode Consortium](https://www.unicode.org) under the [Unicode License](https://www.unicode.org/copyright.html), in `UNICODE-LICENSE`
- The code in this repository is licensed under the [MIT License](https://opensource.org/licenses/MIT), for more details take a look at `LICENSE`

<h2>
  <a href="https://pixel-hopper.github.io/Unicode/Unicode.html" style="text-decoration: none; color: inherit;">
    🔗 Unicode Search Bar :
  </a>
</h2>

| Emoji | Codepoints | Description | 
| ----- | ---------- | ----------- |
"""

# Add emoji rows to README.md
for emoji, codepoints, description in rows:
    readme_content += f"| {emoji} | `{codepoints}` | {description} |\n"

# Write README.md to file
with open(readme_file_path, "w", encoding="utf-8") as f:
    f.write(readme_content)

print(f"✅ README.md created at: {readme_file_path}")
