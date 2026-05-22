#!/usr/bin/env python3
"""
Markdown to HTML Converter
Converts markdown files to elegant HTML with professional CSS styling.
"""

import os
import sys
import argparse
import html as html_lib
from datetime import datetime
from pathlib import Path

try:
    import markdown
    import re
except ImportError:
    print("Error: markdown package not installed")
    print("Install it with: pip install markdown")
    sys.exit(1)


# Elegant CSS Styling
DARK_CSS = """
* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

body {
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    line-height: 1.6;
    color: #333;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    min-height: 100vh;
    padding: 20px;
    overflow-x: hidden;
}

.container {
    max-width: 900px;
    margin: 0 auto;
    background: white;
    border-radius: 12px;
    box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
    overflow: hidden;
}

.header {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    padding: 15px;
    text-align: center;
}

.header h1 {
    font-size: 2.5em;
    margin-bottom: 10px;
    font-weight: 700;
    letter-spacing: -0.5px;
    border-bottom: none;
}

.header p {
    font-size: 1.1em;
    opacity: 0.95;
    font-weight: 300;
}

.content {
    padding: 50px 40px;
    font-size: 1.05em;
}

h1 {
    font-size: 2.2em;
    margin: 40px 0 20px 0;
    color: #2c3e50;
    border-bottom: 3px solid #667eea;
    padding-bottom: 10px;
    font-weight: 700;
}

h2 {
    font-size: 1.8em;
    margin: 35px 0 15px 0;
    color: #34495e;
    border-left: 4px solid #667eea;
    padding-left: 15px;
    font-weight: 600;
}

h3 {
    font-size: 1.4em;
    margin: 25px 0 12px 0;
    color: #476282;
    font-weight: 600;
}

h4, h5, h6 {
    margin: 20px 0 10px 0;
    color: #555;
    font-weight: 600;
}

p {
    margin-bottom: 15px;
    line-height: 1.8;
}

a {
    color: #667eea;
    text-decoration: none;
    border-bottom: 1px solid transparent;
    transition: all 0.3s ease;
}

a:hover {
    border-bottom-color: #667eea;
    color: #764ba2;
}

a:focus, button:focus, input:focus, select:focus, [tabindex]:focus {
    outline: 2px solid #667eea;
    outline-offset: 2px;
}

ul, ol {
    margin: 20px 0 20px 40px;
    line-height: 1.8;
}

ul li, ol li {
    margin-bottom: 8px;
}

ul li:before {
    color: #667eea;
}

code {
    background: #f5f7fa;
    border-radius: 4px;
    padding: 2px 6px;
    font-family: 'Courier New', monospace;
    color: #d63384;
    font-size: 0.95em;
}

pre {
    background: #2c3e50;
    color: #ecf0f1;
    padding: 20px;
    border-radius: 8px;
    overflow-x: auto;
    margin: 20px 0;
    line-height: 1.4;
    font-family: 'Courier New', monospace;
    font-size: 0.95em;
}

pre code {
    background: none;
    color: #ecf0f1;
    padding: 0;
}

blockquote {
    border-left: 4px solid #667eea;
    padding-left: 20px;
    margin: 20px 0;
    color: #555;
    font-style: italic;
    background: #f8f9fa;
    padding: 15px 20px;
    border-radius: 4px;
}

.table-wrapper {
    width: 100%;
    overflow-x: auto;
    -webkit-overflow-scrolling: touch;
    margin: 20px 0;
}

table {
    width: 100%;
    border-collapse: collapse;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

table thead {
    background: #667eea;
    color: white;
}

table th {
    padding: 15px;
    text-align: left;
    font-weight: 600;
    white-space: nowrap;
}

table td {
    padding: 12px 15px;
    border-bottom: 1px solid #ecf0f1;
}

table tbody tr:hover {
    background: #f8f9fa;
}

hr {
    border: 0;
    height: 2px;
    background: linear-gradient(to right, transparent, #667eea, transparent);
    margin: 40px 0;
}

img {
    max-width: 100%;
    height: auto;
    border-radius: 8px;
    margin: 20px 0;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}

.footer {
    background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
    padding: 30px 40px;
    text-align: center;
    color: #666;
    font-size: 0.9em;
    border-top: 1px solid #ecf0f1;
    letter-spacing: 0.3px;
}

.footer a {
    color: #667eea;
    font-weight: 600;
}

.footer a:hover {
    color: #764ba2;
}

@media (max-width: 768px) {
    .content {
        padding: 30px 20px;
    }
    
    h1 {
        font-size: 1.8em;
    }
    
    h2 {
        font-size: 1.4em;
    }
    
    .header {
        padding: 30px 20px;
    }
    
    .header h1 {
        font-size: 1.8em;
    }
}
"""

LIGHT_CSS = """
* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

body {
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    line-height: 1.6;
    color: #333;
    background: #f5f7fa;
    padding: 20px;
    overflow-x: hidden;
}

.container {
    max-width: 900px;
    margin: 0 auto;
    background: white;
    border-radius: 8px;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
    overflow: hidden;
}

.header {
    background: white;
    border-bottom: 2px solid #e8e8e8;
    padding: 10px 40px;
    text-align: center;
}

.header h1 {
    font-size: 2.2em;
    margin-bottom: 8px;
    color: #2c3e50;
    font-weight: 700;
    border-bottom: none;
}

.header p {
    font-size: 1em;
    color: #555;
}

.content {
    padding: 40px;
    font-size: 1.05em;
}

h1 {
    font-size: 2em;
    margin: 30px 0 15px 0;
    color: #2c3e50;
    border-bottom: 1px solid #ecf0f1;
    padding-bottom: 10px;
}

h2 {
    font-size: 1.6em;
    margin: 25px 0 12px 0;
    color: #34495e;
}

h3 {
    font-size: 1.3em;
    margin: 20px 0 10px 0;
    color: #476282;
}

p {
    margin-bottom: 15px;
    line-height: 1.8;
}

a {
    color: #3498db;
    text-decoration: none;
    transition: color 0.3s ease;
}

a:hover {
    color: #2980b9;
    text-decoration: underline;
}

a:focus, button:focus, input:focus, select:focus, [tabindex]:focus {
    outline: 2px solid #3498db;
    outline-offset: 2px;
}

ul, ol {
    margin: 15px 0 15px 30px;
}

ul li, ol li {
    margin-bottom: 5px;
}

code {
    background: #ecf0f1;
    border-radius: 3px;
    padding: 2px 5px;
    font-family: 'Courier New', monospace;
    color: #c0392b;
}

pre {
    background: #2c3e50;
    color: #ecf0f1;
    padding: 15px;
    border-radius: 5px;
    overflow-x: auto;
    margin: 15px 0;
    line-height: 1.4;
}

pre code {
    background: none;
    color: inherit;
    padding: 0;
}

blockquote {
    border-left: 3px solid #3498db;
    padding-left: 15px;
    margin: 15px 0;
    color: #555;
    font-style: italic;
}

.table-wrapper {
    width: 100%;
    overflow-x: auto;
    -webkit-overflow-scrolling: touch;
    margin: 15px 0;
}

table {
    width: 100%;
    border-collapse: collapse;
}

table th {
    background: #ecf0f1;
    padding: 10px;
    text-align: left;
    font-weight: 600;
    border-bottom: 2px solid #bdc3c7;
    white-space: nowrap;
}

table td {
    padding: 10px;
    border-bottom: 1px solid #ecf0f1;
}

hr {
    border: 0;
    border-top: 1px solid #ecf0f1;
    margin: 30px 0;
}

img {
    max-width: 100%;
    height: auto;
    margin: 15px 0;
}

.footer {
    background: #f8f9fa;
    padding: 30px 40px;
    text-align: center;
    color: #666;
    font-size: 0.9em;
    border-top: 1px solid #ecf0f1;
    letter-spacing: 0.3px;
}

.footer a {
    color: #3498db;
    font-weight: 600;
}

.footer a:hover {
    color: #2980b9;
}

@media (max-width: 768px) {
    .content {
        padding: 20px;
    }
    
    h1 {
        font-size: 1.6em;
    }
    
    h2 {
        font-size: 1.3em;
    }
}
"""


TOOLBAR_CSS = """
.skip-link {
    position: absolute;
    top: -100%;
    left: 16px;
    background: #667eea;
    color: white;
    padding: 8px 16px;
    border-radius: 4px;
    z-index: 1000;
    font-size: 0.9em;
}

.skip-link:focus {
    top: 16px;
}

.a11y-toolbar {
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    display: flex;
    justify-content: center;
    align-items: center;
    gap: 16px;
    padding: 12px 24px;
    background: #1a1a2e;
    z-index: 9999;
    box-shadow: 0 4px 12px rgba(0,0,0,0.25);
    height: 64px;
    overflow: hidden;
    transition: height 0.3s cubic-bezier(0.4, 0, 0.2, 1),
                box-shadow 0.3s ease;
}

.a11y-toolbar.collapsed {
    height: 3px;
    padding: 0;
    box-shadow: none;
}

.a11y-toolbar.collapsed button {
    opacity: 0;
    pointer-events: none;
}

.progress-bar {
    position: absolute;
    top: 0;
    left: 0;
    height: 3px;
    width: 0%;
    background: rgba(255,255,255,0.9);
    transition: width 0.1s linear;
    pointer-events: none;
    z-index: 1;
}

.a11y-toolbar button {
    background: rgba(255,255,255,0.12);
    border: none;
    color: #fff;
    padding: 10px 20px;
    border-radius: 20px;
    cursor: pointer;
    font-size: 15px;
    font-weight: 600;
    line-height: 1;
    white-space: nowrap;
    min-width: 44px;
    min-height: 44px;
    display: inline-flex;
    align-items: center;
    justify-content: center;
    transition: background 0.2s, opacity 0.15s;
    flex-shrink: 0;
}

.a11y-toolbar button:hover {
    background: rgba(255,255,255,0.25);
}

.a11y-toolbar button:focus {
    outline: 2px solid rgba(255,255,255,0.7);
    outline-offset: 1px;
}

body {
    padding-top: 64px;
}

body.toolbar-collapsed {
    padding-top: 3px;
}
"""


def resolve_safe_path(filepath, base=None):
    """Resolve and validate path to prevent traversal attacks."""
    base = Path(base or Path.cwd()).resolve()
    resolved = (base / filepath).resolve() if not Path(filepath).is_absolute() else Path(filepath).resolve()
    if not resolved.is_relative_to(base):
        print(f"Error: Access to '{filepath}' is outside the allowed directory.")
        sys.exit(1)
    return resolved


def get_css(theme="dark"):
    """Get CSS for the specified theme."""
    if theme.lower() == "light":
        return LIGHT_CSS + TOOLBAR_CSS
    return DARK_CSS + TOOLBAR_CSS


def get_title_from_markdown(filepath):
    """Extract title from markdown file (first h1)."""
    safe = resolve_safe_path(filepath)
    with open(safe, 'r', encoding='utf-8') as f:
        for line in f:
            if line.strip().startswith('# '):
                return html_lib.escape(line.strip()[2:])
    return html_lib.escape(Path(safe).stem.replace('_', ' ').replace('-', ' ').title())


def markdown_to_html(input_file, output_file=None, theme="dark", include_toc=False):
    """
    Convert markdown file to HTML.
    
    Args:
        input_file: Path to markdown file
        output_file: Path to save HTML (default: same name with .html)
        theme: CSS theme ('dark' or 'light')
        include_toc: Include table of contents
    """
    
    # Validate input file
    safe_input = resolve_safe_path(input_file)
    if not safe_input.exists():
        print(f"Error: File '{input_file}' not found")
        sys.exit(1)

    # Set output file
    if output_file is None:
        output_file = safe_input.stem + '.html'
    safe_output = resolve_safe_path(output_file)

    # Read markdown
    try:
        with open(safe_input, 'r', encoding='utf-8') as f:
            md_content = f.read()
    except Exception as e:
        print(f"Error reading file: {e}")
        sys.exit(1)
    
    # Convert markdown to HTML
    extensions = ['tables', 'fenced_code', 'toc'] if include_toc else ['tables', 'fenced_code']
    html_body = markdown.markdown(md_content, extensions=extensions)
    
    # Wrap tables in scrollable container for mobile
    html_body = re.sub(r'(<table.*?</table>)', r'<div class="table-wrapper">\1</div>', html_body, flags=re.DOTALL)
    
    # Add scope="col" to th elements for screen readers
    html_body = html_body.replace('<th>', '<th scope="col">')
    
    # Get title
    title = get_title_from_markdown(safe_input)
    
    # Remove first h1 from body to avoid duplicate with header
    html_body = re.sub(r'<h1>.*?</h1>', '', html_body, count=1)
    
    # Get CSS
    css = get_css(theme)
    
    # Build complete HTML
    html_template = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <style>
{css}
    </style>
</head>
<body>
    <div class="a11y-toolbar" role="toolbar" aria-label="Accessibility controls">
        <div class="progress-bar" id="progress-bar"></div>
        <button onclick="adjustFont(-1)" aria-label="Decrease font size"><big>𝔸</big>⁻</button>
        <button onclick="adjustFont(1)" aria-label="Increase font size"><big>𝔸</big>⁺</button>
        <button onclick="adjustZoom(-0.1)" aria-label="Zoom out"><big>🔎</big>⁻</button>
        <button onclick="adjustZoom(0.1)" aria-label="Zoom in"><big>🔎</big>⁺</button>
    </div>
    <a href="#main-content" class="skip-link">Skip to content</a>
    <div class="container">
        <header class="header" role="banner">
            <h1>{title}</h1>
        </header>
        <main class="content" role="main" id="main-content">
{html_body}
        </main>
        <footer class="footer" role="contentinfo">
            <p>Generated via <strong>md2html</strong> &middot; <a href="https://github.com/kopihao">kopihao</a> &copy; {datetime.now().year}</p>
        </footer>
    </div>
    <script>
    (function(){{
        let fs=100, zm=1;
        const content=document.querySelector('.content');
        const toolbar=document.querySelector('.a11y-toolbar');
        const progressBar=document.getElementById('progress-bar');
        let lastScroll=0;
        function updateProgress(){{
            const docH=document.documentElement.scrollHeight-window.innerHeight;
            progressBar.style.width=(docH>0?(window.pageYOffset/docH*100):0)+'%';
        }}
        window.adjustFont=function(d){{ fs=Math.max(50,Math.min(200,fs+d*10)); content.style.fontSize=fs+'%'; }};
        window.adjustZoom=function(d){{ zm=Math.max(0.5,Math.min(2,zm+d)); document.querySelector('.container').style.zoom=zm; }};
        window.addEventListener('scroll',function(){{
            const y=window.pageYOffset;
            const delta=y-lastScroll;
            if(Math.abs(delta)>4){{
                if(delta>0&&y>40){{ toolbar.classList.add('collapsed'); document.body.classList.add('toolbar-collapsed'); }}
                else{{ toolbar.classList.remove('collapsed'); document.body.classList.remove('toolbar-collapsed'); }}
                lastScroll=y;
            }}
            updateProgress();
        }},{{passive:true}});
        updateProgress();
        window.addEventListener('load', updateProgress);
    }})();
    </script>
</body>
</html>"""
    
    # Write HTML file
    try:
        with open(safe_output, 'w', encoding='utf-8') as f:
            f.write(html_template)
        print(f"✓ Successfully converted: {input_file} → {safe_output}")
        print(f"  Theme: {theme}")
        return output_file
    except Exception as e:
        print(f"Error writing file: {e}")
        sys.exit(1)


def interactive_select():
    """Scan current working directory for .md files and let user choose."""
    cwd = Path.cwd()
    md_files = sorted(cwd.glob('*.md'))
    if not md_files:
        print(f"No .md files found in {cwd}")
        sys.exit(1)
    print(f"\nMarkdown files in {cwd}:\n")
    for i, f in enumerate(md_files, 1):
        print(f"  [{i}] {f.name}")
    print(f"  [0] Convert ALL\n")
    try:
        choice = int(input("Select file to convert: "))
    except (ValueError, EOFError):
        print("Invalid input."); sys.exit(1)
    if choice == 0:
        return [str(resolve_safe_path(f, cwd)) for f in md_files]
    if 1 <= choice <= len(md_files):
        return [str(resolve_safe_path(md_files[choice - 1], cwd))]
    print("Invalid selection."); sys.exit(1)


def main():
    parser = argparse.ArgumentParser(
        description='Convert Markdown files to elegant HTML with CSS styling',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python md_to_html.py README.md
  python md_to_html.py README.md -o output.html
  python md_to_html.py README.md --theme light
  python md_to_html.py README.md --toc
  python md_to_html.py              (interactive mode)
        """
    )
    
    parser.add_argument('input', nargs='?', default=None, help='Input markdown file (omit for interactive mode)')
    parser.add_argument('-o', '--output', help='Output HTML file (default: same name as input)')
    parser.add_argument('--theme', choices=['dark', 'light'], default='light',
                        help='CSS theme style (default: light)')
    parser.add_argument('--toc', action='store_true',
                        help='Include table of contents')
    
    args = parser.parse_args()
    
    if args.input:
        markdown_to_html(args.input, args.output, args.theme, args.toc)
    else:
        for f in interactive_select():
            markdown_to_html(f, theme=args.theme, include_toc=args.toc)


if __name__ == '__main__':
    main()
