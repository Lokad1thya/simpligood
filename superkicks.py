from playwright.sync_api import sync_playwright

def search_superkicks_products(search_query):
    base_url = 'https://www.superkicks.in/search?q='
    search_url = f"{base_url}{search_query.replace(' ', '%20')}"
    
    results = []
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        
        print(f'Navigating to {search_url}')
        page.goto(search_url)
        page.wait_for_load_state('networkidle')
        
        # Wait for the product cards to be loaded
        try:
            print('Waiting for product cards')
            page.wait_for_selector('div.st-product', timeout=120000)  # Increased timeout
        except Exception as e:
            print(f'Error waiting for selector: {e}')
            # Print page content for debugging
            print(page.content())
            browser.close()
            return results
        
        # Scroll to the bottom if needed
        print('Scrolling to the bottom to load more content')
        page.evaluate('window.scrollTo(0, document.body.scrollHeight)')
        page.wait_for_timeout(5000)  # Wait for 5 seconds
        
        # Find and process product cards
        products = page.query_selector_all('div.st-product')
        if not products:
            print("No products found. Printing page content for debugging:")
            print(page.content())
        else:
            for product in products:
                try:
                    link = product.query_selector('figure.st-product-media a')
                    link = link.get_attribute('href') if link else '#'
                    absolute_link = link if link.startswith('http') else f"https://superkicks.in{link}"
                    
                    title = product.query_selector('div.st-product-name a')
                    title = title.inner_text().strip() if title else 'No title available'
                    
                    subtitle = product.query_selector('div.st-secondary-title')
                    subtitle = subtitle.inner_text().strip() if subtitle else 'No subtitle available'
                    
                    price = product.query_selector('div.st-product-price span.new-price')
                    price = price.inner_text().strip() if price else 'No price available'
                    
                    image = product.query_selector('figure.st-product-media img')
                    image_url = image.get_attribute('src') if image else 'No image available'
                    
                    print(f'Link: {absolute_link}')
                    print(f'Title: {title}')
                    print(f'Subtitle: {subtitle}')
                    print(f'Price: {price}')
                    print(f'Image URL: {image_url}')
                    print('-' * 40)
                    
                    results.append({
                        'link': absolute_link,
                        'title': title,
                        'subtitle': subtitle,
                        'price': price,
                        'image_url': image_url
                    })
                except Exception as e:
                    print(f'Error occurred while processing a product: {e}')
        
        browser.close()
    
    return results
