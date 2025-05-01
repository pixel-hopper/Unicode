import os
import requests
import html

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

# Begin HTML content
html_output = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Unicode Emoji List</title>
    <style>
        body { font-family: sans-serif; margin: 0; padding: 20px; display: flex; flex-direction: column; align-items: center; background-color: #f4f4f4; }
        h1 { text-align: center; font-size: 2em; margin-bottom: 20px; color: #333; }
        input[type="text"] {
            width: 100%%;
            max-width: 600px;
            padding: 12px;
            margin-bottom: 20px;
            font-size: 1.2em;
            border: 2px solid #ccc;
            border-radius: 5px;
            box-sizing: border-box;
        }
        table {
            width: 100%%;
            max-width: 1000px;
            border-collapse: collapse;
            box-sizing: border-box;
        }
        th, td {
            padding: 12px 15px;
            text-align: left;
            border: 1px solid #ddd;
        }
        th {
            background-color: #f2f2f2;
            font-weight: bold;
        }
        td.emoji {
            font-size: 1.5em;
        }
        tr.hidden {
            display: none;
        }
        .copy-btn {
            padding: 4px 8px;
            font-size: 0.9em;
            cursor: pointer;
            background-color: #eee;
            border: 1px solid #ccc;
            border-radius: 4px;
        }
        .copy-btn:hover {
            background-color: #ddd;
        }
        @media (max-width: 600px) {
            h1 { font-size: 1.6em; }
            table { font-size: 0.9em; width: 90%%; }
            input[type="text"] { font-size: 1em; padding: 10px; }
        }
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
readme_content = """## License

- This repository includes emoji data sourced from the [Unicode Consortium](https://www.unicode.org) under the terms of the [Unicode License](https://www.unicode.org/copyright.html).  
- A copy of the Unicode License is included in this repository as `UNICODE-LICENSE.txt`.
- This repository is licensed under the MIT License. See the `LICENSE` file for more details.

## Emojis:

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
