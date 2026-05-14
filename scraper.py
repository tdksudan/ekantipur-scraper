import json
import re
from playwright.sync_api import sync_playwright

def scrape_ekantipur():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()
        
        print("Navigating to Ekantipur...")
        page.goto("https://ekantipur.com", wait_until="networkidle")

        # --- Handle Advertisement Overlay ---
        try:
            skip_button = page.locator("text=Skip")  # adjust if localized
            if skip_button.count() > 0:
                skip_button.click()
                print("Advertisement skipped.")
        except Exception as e:
            print("No advertisement overlay found or could not skip:", e)

        # --- Task 1: Extract Entertainment News ---
        page.goto("https://ekantipur.com/entertainment", wait_until="networkidle")

        entertainment_data = []
        cards = page.locator(
            "div.category-main-wrapper div.category-wrapper div.category div.category-inner-wrapper"
        ).all()[:5]

        print("Found entertainment cards:", len(cards))

        for i, card in enumerate(cards, start=1):
            try:
                description_block = card.locator("div.category-description")
                raw_text = description_block.text_content().strip()

                # Clean title: remove trailing "MINS READ"
                title = re.sub(r"\d+\s*MINS READ", "", raw_text).strip()

                image_url = card.locator("div.category-image img").get_attribute("src")

                # Author inside description block → div.author-name p a
                author_locator = description_block.locator("div.author-name p a")
                author = author_locator.text_content().strip() if author_locator.count() > 0 else None

                entertainment_data.append({
                    "title": title,
                    "image_url": image_url,
                    "category": "मनोरञ्जन",
                    "author": author
                })
            except Exception as e:
                print(f"Error extracting article {i}: {e}")

        # --- Task 2: Extract Cartoon of the Day ---
        page.goto("https://ekantipur.com/cartoon", wait_until="networkidle")

        cartoon_section = page.locator(
            "section.cartoon-main-wrapper div.row.g-5 div.col-lg-4"
        ).first

        # Flexible title locator
        if cartoon_section.locator("h2").count() > 0:
            title = cartoon_section.locator("h2").text_content().strip()
        elif cartoon_section.locator("h3").count() > 0:
            title = cartoon_section.locator("h3").text_content().strip()
        elif cartoon_section.locator("a").count() > 0:
            title = cartoon_section.locator("a").text_content().strip()
        else:
            title = cartoon_section.text_content().strip()

        cartoon_data = {
            "title": title,
            "image_url": cartoon_section.locator("img").get_attribute("src"),
            "author": cartoon_section.locator(".author").text_content().strip()
                      if cartoon_section.locator(".author").count() > 0 else "Unknown"
        }

        # Prepare final output structure
        final_output = {
            "entertainment_news": entertainment_data,
            "cartoon_of_the_day": cartoon_data
        }

        # Save to output.json with Devanagari support
        with open("output.json", "w", encoding="utf-8") as f:
            json.dump(final_output, f, ensure_ascii=False, indent=4)
        
        print("Data extraction complete. Saved to output.json")
        browser.close()

if __name__ == "__main__":
    scrape_ekantipur()
