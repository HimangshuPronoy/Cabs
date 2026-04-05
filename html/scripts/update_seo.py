import os
import re

def update_seo():
    html_dir = '.'
    title = '<title>Affordable BUF Airport Taxi to Niagara Falls &amp; Toronto | Buffalo Canada Airport Taxi</title>'
    desc = '<meta name="description" content="24/7 BUF Airport taxi service to Niagara Falls and Toronto. Cross-border rides, spacious vehicles, and simple booking. Call +1 716-957-8900.">'
    
    html_files = [f for f in os.listdir(html_dir) if f.endswith('.html')]
    for file in html_files:
        filepath = os.path.join(html_dir, file)
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Replace title
        content = re.sub(r'<title>.*?</title>', title, content, flags=re.IGNORECASE | re.DOTALL)
        
        # Replace or insert meta description
        new_content, count = re.subn(r'<meta[^>]*name=["\']description["\'][^>]*>', desc, content, flags=re.IGNORECASE)
        if count == 0:
            new_content = re.sub(r'</title>', f'</title>\n    {desc}', new_content, flags=re.IGNORECASE)

        if content != new_content:
            pass # we used search/replace logic that handled string mutation safely
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"SEO updated in {file}")

if __name__ == '__main__':
    update_seo()
