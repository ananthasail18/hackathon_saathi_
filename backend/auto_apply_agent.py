import asyncio
import json
from playwright.async_api import async_playwright
from groq import Groq
from config import settings

client = Groq(api_key=settings.GROQ_API_KEY)

async def map_profile_to_form(profile: dict, form_fields: list) -> dict:
    """
    Uses the LLM to decide what text to put into which form field based on the user's profile.
    """
    prompt = f"""
    You are an AI assistant helping a user fill out a hackathon application form.
    
    User Profile:
    {json.dumps(profile, indent=2)}
    
    Form Fields found on the page (name or id attributes):
    {json.dumps(form_fields, indent=2)}
    
    Map the User Profile data to the Form Fields. 
    Return a JSON object where the keys are the exact form field names/ids, and the values are the text to insert.
    If a field asks for a portfolio or github, provide the link.
    If a field asks "Why do you want to join?", use the bio to generate a short 1-sentence answer.
    """
    
    try:
        completion = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {"role": "system", "content": "You are a helpful JSON-outputting assistant."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.1,
            response_format={"type": "json_object"}
        )
        return json.loads(completion.choices[0].message.content)
    except Exception as e:
        print(f"Error mapping form: {e}")
        return {}

async def auto_fill_form(profile: dict, application_url: str):
    """
    Launches a visible browser, navigates to the form, and fills it out.
    Crucially, it DOES NOT SUBMIT. It leaves the browser open for manual review.
    """
    print("Launching Auto-Apply Agent...")
    # headless=False so the user can see the browser and review the form
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context()
        page = await context.new_page()
        
        print(f"Navigating to {application_url}")
        try:
            await page.goto(application_url, wait_until="domcontentloaded")
            
            # Wait an extra second to ensure dynamic inputs render
            await page.wait_for_timeout(1000)
            
            # 1. Extract all text inputs and textareas
            input_elements = await page.query_selector_all('input[type="text"], input[type="email"], textarea')
            form_fields = []
            
            for el in input_elements:
                name = await el.get_attribute("name")
                id_attr = await el.get_attribute("id")
                placeholder = await el.get_attribute("placeholder")
                # Use whatever attribute is available to identify the field
                identifier = name or id_attr or placeholder or "unknown"
                form_fields.append(identifier)
            
            print(f"Detected form fields: {form_fields}")
            
            if not form_fields:
                print("No form fields detected. The page might require login or uses a complex framework.")
            else:
                # 2. Use LLM to figure out what to type
                print("Asking LLM how to fill these fields...")
                field_mapping = await map_profile_to_form(profile, form_fields)
                print(f"LLM Mapping Strategy: {field_mapping}")
                
                # 3. Fill the fields
                for el in input_elements:
                    name = await el.get_attribute("name")
                    id_attr = await el.get_attribute("id")
                    placeholder = await el.get_attribute("placeholder")
                    identifier = name or id_attr or placeholder
                    
                    if identifier in field_mapping:
                        value_to_fill = field_mapping[identifier]
                        print(f"Typing '{value_to_fill}' into {identifier}")
                        await el.fill(value_to_fill)
            
            print("=========================================================")
            print("AGENT FINISHED FILLING FORM.")
            print("ACTION REQUIRED: Please review the browser window.")
            print("The agent will intentionally NOT click Submit.")
            print("You must manually click 'Submit' when you are ready.")
            print("Closing this terminal process will close the browser.")
            print("=========================================================")
            
            # Keep the browser open indefinitely (or until user closes it)
            # In a real app, you might pause execution here. 
            # We'll sleep for a long time to keep the headless=False window open.
            await asyncio.sleep(3600) 
            
        except Exception as e:
            print(f"Error during auto-fill: {e}")
        finally:
            await browser.close()

if __name__ == "__main__":
    mock_profile = {
        "name": "Anant",
        "email": "anant@example.com",
        "github": "https://github.com/anant",
        "bio": "I love building autonomous AI agents."
    }
    
    # We use a dummy form for testing. 
    # Example: A simple HTML page with some inputs. We can use a public form tester.
    test_url = "https://www.w3schools.com/html/html_forms.asp" 
    
    asyncio.run(auto_fill_form(mock_profile, test_url))
