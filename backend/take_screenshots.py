import asyncio
from playwright.async_api import async_playwright
import os

async def capture_submission_screenshots():
    screenshot_dir = os.path.join(os.getcwd(), "screenshots")
    if not os.path.exists(screenshot_dir):
        os.makedirs(screenshot_dir)

    print("Starting screenshot capture for hackathon submission...")
    
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(viewport={"width": 1440, "height": 900})
        page = await context.new_page()
        
        try:
            # 1. Main Dashboard Screenshot
            print("1. Capturing Dashboard...")
            await page.goto("http://localhost:5173", wait_until="networkidle")
            await page.wait_for_timeout(2000) # Wait for animations
            await page.screenshot(path=os.path.join(screenshot_dir, "1_dashboard.png"))
            
            # 2. Click Auto-Apply and capture 'Drafting' state
            print("2. Capturing Apply State...")
            apply_button = await page.wait_for_selector('button:has-text("Agent Auto-Apply ⚡")')
            if apply_button:
                await apply_button.click()
                await page.wait_for_timeout(1000) # Wait for alert/state change
                
                # Handle the alert pop up from the browser
                page.on("dialog", lambda dialog: dialog.accept())
                
                await page.screenshot(path=os.path.join(screenshot_dir, "2_agent_launched.png"))
                
                # Wait for the calendar button to appear
                await page.wait_for_timeout(2000)
                await page.screenshot(path=os.path.join(screenshot_dir, "3_calendar_sync_ready.png"))
            
            # 3. Devpost Hackathons Page
            print("3. Capturing Devpost...")
            await page.goto("https://devpost.com/hackathons", wait_until="domcontentloaded")
            await page.wait_for_timeout(3000)
            await page.screenshot(path=os.path.join(screenshot_dir, "4_devpost_target.png"))
            
            print(f"Screenshots saved successfully in {screenshot_dir}!")
            
        except Exception as e:
            print(f"Error taking screenshots: {e}")
        finally:
            await browser.close()

if __name__ == "__main__":
    asyncio.run(capture_submission_screenshots())
