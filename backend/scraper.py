import asyncio
from playwright.async_api import async_playwright
from bs4 import BeautifulSoup

async def scrape_devfolio_hackathons():
    """
    Discovery Agent: Navigates to Devfolio and scrapes active hackathons.
    This is a simplified example. Real scraping might need to handle pagination and complex DOM structures.
    """
    hackathons = []
    
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context()
        page = await context.new_page()
        
        try:
            print("Discovery Agent: Accessing devfolio.co/hackathons...")
            # We use a 30s timeout and wait for domcontentloaded
            await page.goto("https://devfolio.co/hackathons", wait_until="domcontentloaded", timeout=30000)
            
            # Allow some time for dynamic content to load
            await page.wait_for_timeout(3000)
            
            # Extract the raw HTML to parse with BeautifulSoup for ease of use
            content = await page.content()
            soup = BeautifulSoup(content, 'html.parser')
            
            # Note: The exact selectors depend on Devfolio's current DOM structure.
            # This is a generic approach assuming a list of cards.
            # In a production environment, we'd use specific data-testid or robust CSS selectors.
            
            # Let's mock a few extraction logic based on common patterns
            # Assuming hackathons are wrapped in a container that looks like a link or a card div
            cards = soup.find_all('a', href=True)
            
            for card in cards:
                href = card['href']
                if 'hackathons/' in href or card.find('h3'):
                    title_elem = card.find('h3') or card.find('h2')
                    title = title_elem.text.strip() if title_elem else "Unknown Title"
                    
                    if title != "Unknown Title":
                        hackathons.append({
                            "title": title,
                            "url": href if href.startswith('http') else f"https://devfolio.co{href}",
                            "platform": "Devfolio",
                            "tags": ["Scraped Data"] # We'd extract tags/themes here
                        })
                        
            # Filter out some noise (e.g., standard links)
            hackathons = [h for h in hackathons if len(h['title']) > 5][:5]
            
        except Exception as e:
            print(f"Discovery Agent Error: {e}")
        finally:
            await browser.close()
            
    return hackathons

# To test the scraper independently
if __name__ == "__main__":
    results = asyncio.run(scrape_devfolio_hackathons())
    print("Scraped Hackathons:")
    for r in results:
        print(r)
