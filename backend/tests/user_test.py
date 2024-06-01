from playwright.sync_api import expect, sync_playwright


def test_can_signup_web(test_client):
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.goto("http://localhost:8000/login")
        page.get_by_label("Username").fill("random")
        page.get_by_label("Password").fill("random")
        page.get_by_label("Password").press("Enter")
        expect(page.locator("pre")).to_contain_text('"Incorrect username or password"')
