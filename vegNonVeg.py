from playwright.sync_api import sync_playwright

def search_vegnonveg_products(search_query):
    base_url = 'https://www.vegnonveg.com/search?q='
    search_url = f"{base_url}{search_query.replace(' ', '+')}"

    print(f'Search URL: {search_url}')  # Debugging line to check the constructed URL

    results = []

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(search_url)

        # Wait for the content to load
        page.wait_for_selector('div.product')

        # Extract product information
        products = page.query_selector_all('div.product')
        if not products:
            print("No products found or incorrect HTML structure.")
        else:
            for product in products:
                try:
                    # Extract product link
                    link = product.query_selector('a')
                    link = link.get_attribute('href') if link else '#'
                    absolute_link = link if link.startswith('http') else f"https://www.vegnonveg.com{link}"
                    
                    # Extract product title
                    title = product.query_selector('span.p-name')
                    title = title.inner_text().strip() if title else 'No title available'
                    
                    # Extract product price
                    price = product.query_selector('span.p-price')
                    price = price.inner_text().strip() if price else 'No price available'
                    
                    # Extract product image URL
                    image = product.query_selector('img.img-normal')
                    image_url = image.get_attribute('src') if image else 'No image available'
                    
                    print(f'Link: {absolute_link}')
                    print(f'Title: {title}')
                    print(f'Price: {price}')
                    print(f'Image URL: {image_url}')
                    print('-' * 40)
                    
                    results.append({
                        'link': absolute_link,
                        'title': title,
                        'price': price,
                        'image_url': image_url
                    })
                except Exception as e:
                    print(f'Error occurred: {e}')
        
        browser.close()

    return results
