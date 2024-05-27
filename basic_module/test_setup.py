import os
import asyncio
from playwright.async_api import async_playwright, Page, BrowserContext
import allure

DEFAULT_URL = "https://wap-q6.qbpink01.com/"


async def setup_browser(device_name='iPhone 11', headless=False):
    """设置浏览器环境并返回浏览器上下文和实例。"""
    playwright = await async_playwright().start()
    device = playwright.devices[device_name]
    browser = await playwright.chromium.launch(headless=headless)
    context = await browser.new_context(**device)
    return playwright, browser, context


async def login(page: Page, username: str, password: str):
    """登录到网站的通用函数。"""
    await page.click("button.login")
    await asyncio.sleep(3)
    await page.fill("input#username", username)
    await asyncio.sleep(2)
    await page.fill("input#password", password)
    await asyncio.sleep(2)
    await page.click("div.submitBtn.btns")
    await asyncio.sleep(3)


async def load_and_check_page(context, url=DEFAULT_URL):
    """加载页面。"""
    page = await context.new_page()
    try:
        await page.goto(url)
        print("Page loaded successfully.")
    except Exception as e:
        print(f"Failed to load page: {str(e)}")
    return page


async def take_screenshot_and_attach(page, step_name):
    """Capture screenshot and attach it to Allure report, and save it to disk."""
    if page.is_closed():
        print("Page is closed, cannot take screenshot.")
        return
    try:
        screenshots_dir = 'screenshots'  # Specify your desired directory
        # Ensure the directory exists
        os.makedirs(screenshots_dir, exist_ok=True)
        screenshot_path = os.path.join(screenshots_dir, f"{step_name}.png")

        # Take screenshot and save it to the defined path
        await page.screenshot(path=screenshot_path, full_page=True)

        # Attach the screenshot to Allure report
        allure.attach.file(screenshot_path, name=step_name,
                           attachment_type=allure.attachment_type.PNG)
    except Exception as e:
        print(f"Failed to take or attach screenshot: {str(e)}")


async def run_tests():
    """Main test function to perform tests and capture screenshots."""
    playwright, browser, context = await setup_browser()
    try:
        page = await load_and_check_page(context)
        await take_screenshot_and_attach(page, "Landing Page")
        # Add more interactions and screenshots here
    finally:
        await browser.close()
        await playwright.stop()

if __name__ == "__main__":
    asyncio.run(run_tests())
