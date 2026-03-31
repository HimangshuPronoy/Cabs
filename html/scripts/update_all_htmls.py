import os
import re

def main():
    html_dir = '.'
    index_path = os.path.join(html_dir, 'index.html')
    
    with open(index_path, 'r', encoding='utf-8') as f:
        index_content = f.read()

    # Extract Blocks
    # 1. Header
    header_match = re.search(r'<header class="main-header">.*?</header>\s*<!--/\.main-header-->', index_content, flags=re.DOTALL)
    if not header_match:
        print("Header not found in index.html")
        return
    header_block = header_match.group(0)

    # 1b. Popup Sidebox & Overlay
    sidebox_match = re.search(r'<div class="popup-sidebox" id="popup-sidebox">.*?</div>\s*<!--/\.popup-sidebox-->', index_content, flags=re.DOTALL)
    sidebox_block = sidebox_match.group(0) if sidebox_match else ""
    
    overlay_match = re.search(r'<div id="sidebox-overlay"></div>', index_content)
    overlay_block = overlay_match.group(0) if overlay_match else ""

    # 2. Footer
    footer_match = re.search(r'<footer class="footer-section".*?</footer>\s*<!--/\.footer-section-->', index_content, flags=re.DOTALL)
    if not footer_match:
        print("Footer not found in index.html")
        return
    footer_block = footer_match.group(0)

    # 3. Tawk.to
    tawk_match = re.search(r'<!--Start of Tawk\.to Script-->.*?<!--End of Tawk\.to Script-->', index_content, flags=re.DOTALL)
    if not tawk_match:
        print("Tawk.to script not found in index.html")
        return
    tawk_block = tawk_match.group(0)

    # Favicon
    favicon_html = '<link rel="shortcut icon" type="image/x-icon" href="assets/img/buf-can-favicon.png">'

    html_files = [f for f in os.listdir(html_dir) if f.endswith('.html')]
    
    for file in html_files:
        if file == 'index.html':
            continue
            
        filepath = os.path.join(html_dir, file)
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        changed = False

        # Replace Favicon
        new_content, count = re.subn(r'<link[^>]*rel=["\']shortcut icon["\'][^>]*>', favicon_html, content, flags=re.IGNORECASE)
        if count == 0:
            new_content = re.sub(r'</head>', f'{favicon_html}\n</head>', new_content, flags=re.IGNORECASE)
        
        # Replace Header
        header_pattern = r'<header class="main-header">.*?(?:<!--/\.main-header-->|</header>)'
        
        # Prepare the header block for this specific file (handle 'active' class)
        current_header = header_block
        # Remove all 'active' classes from the copied block
        current_header = current_header.replace(' class="active ', ' class="')
        current_header = current_header.replace('class="active"', '')
        current_header = current_header.replace('active dropdown_menu', 'dropdown_menu')
        
        # Determine which menu item should be active
        # Define mapping of file names to their unique link identifiers
        active_map = {
            'index.html': 'index.html">Home',
            'about-us.html': 'about-us.html">About Us',
            'booking.html': 'booking.html">Booking',
            'faqs.html': 'faqs.html">FAQ',
            'contact.html': '#footer-top-wrap">Contact'
        }
        
        if file in active_map:
            target_text = active_map[file]
            # Find the <li> that wraps this specific link and add the active class
            # This regex looks for <li> tags that contain our target_text
            pattern = rf'(<li[^>]*?)(class=")?(dropdown_menu)?("?[^>]*?>\s*<a[^>]*?href="{re.escape(target_text)})'
            
            def add_active(match):
                prefix = match.group(1)
                has_class = match.group(2)
                is_dropdown = match.group(3)
                suffix = match.group(4)
                
                if is_dropdown:
                    return f'<li class="active dropdown_menu"{suffix}'
                else:
                    return f'<li class="active"{suffix}'

            # Simple replacement if regex is too complex for this structure
            # Let's try a simpler one first: find the link and track back to the nearest <li>
            # But the previous match failed, so let's use a very specific but flexible search
            
            # Alternative: Search for the specific <li> block for each page
            if file == 'index.html':
                 current_header = re.sub(r'<li class="dropdown_menu">\s*<a href="index\.html">Home', '<li class="active dropdown_menu"><a href="index.html">Home', current_header)
            elif file == 'about-us.html':
                 current_header = re.sub(r'<li class="dropdown_menu">\s*<a href="about-us\.html">About Us', '<li class="active dropdown_menu"><a href="about-us.html">About Us', current_header)
            elif file == 'booking.html':
                 current_header = re.sub(r'<li class="dropdown_menu">\s*<a href="booking\.html">Booking', '<li class="active dropdown_menu"><a href="booking.html">Booking', current_header)
            elif file == 'faqs.html':
                 current_header = re.sub(r'<li class="dropdown_menu">\s*<a href="faqs\.html">FAQ', '<li class="active dropdown_menu"><a href="faqs.html">FAQ', current_header)
            elif file == 'contact.html':
                 current_header = current_header.replace('<li><a href="#footer-top-wrap">Contact', '<li class="active"><a href="#footer-top-wrap">Contact')

        new_content, count = re.subn(header_pattern, current_header, new_content, flags=re.DOTALL)

        # Replace Sidebox & Overlay
        # 1. Strip the standard wrapped sidebox
        new_content = re.sub(r'<div class="popup-sidebox" id="popup-sidebox">.*?<!--/\.popup-sidebox-->', '', new_content, flags=re.DOTALL)
        
        # 2. Strip the 'naked' fragments that often appear due to previous regex failures
        # These usually start with <!--/.main-header--> and contain the unique "Everything your cross-border..." text
        naked_pattern = r'(?:<!--/\.main-header-->\s*)+<p>Everything your cross-border transportation needs is right here!.*?(?:<!--/\.popup-sidebox-->|</div>\s*</div>\s*</div>\s*<!--/\.popup-sidebox-->)'
        new_content = re.sub(naked_pattern, '', new_content, flags=re.DOTALL)

        new_content = re.sub(r'<div id="sidebox-overlay"></div>', '', new_content)
        new_content = re.sub(r'(<!--/\.main-header-->|</header>)', r'\1\n' + sidebox_block + r'\n' + overlay_block, new_content, flags=re.DOTALL, count=1)

        # Replace Footer
        footer_pattern = r'<footer class="footer-section".*?(?:<!--/\.footer-section-->|</footer>)'
        new_content, count = re.subn(footer_pattern, footer_block, new_content, flags=re.DOTALL)

        # Add / Replace Tawk.to
        new_content = re.sub(r'<!--Start of Tawk\.to Script-->.*?<!--End of Tawk\.to Script-->\n?', '', new_content, flags=re.DOTALL)
        new_content = re.sub(r'(</body>)', r'\n' + tawk_block + r'\n\1', new_content, flags=re.IGNORECASE)

        if content != new_content:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(new_content)
            print(f"Propagated Master Nav to {file}")

if __name__ == "__main__":
    main()
