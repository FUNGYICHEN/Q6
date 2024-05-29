import asyncio
import allure_commons
from playwright.async_api import async_playwright

# 默认的URL
DEFAULT_URL = "https://wap-q6.qbpink01.com/"


async def setup_browser(device_name='iPhone 11', headless=False):
    """设置浏览器环境并返回浏览器上下文和实例。"""
    playwright = await async_playwright().start()
    device = playwright.devices[device_name]
    browser = await playwright.chromium.launch(headless=headless)
    context = await browser.new_context(**device)
    return playwright, browser, context


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
    """捕获屏幕截图并附加到Allure报告。"""
    if page.is_closed():
        print("Page is closed, cannot take screenshot.")
        return
    try:
        screenshot_bytes = await page.screenshot(full_page=True)
        allure_commons.attach(screenshot_bytes, name=step_name,
                              attachment_type=allure.attachment_type.PNG)  # type: ignore
    except Exception as e:
        print(f"Failed to take or attach screenshot: {str(e)}")


async def run_tests():
    """主测试函数，执行测试和截图逻辑。"""
    playwright, browser, context = await setup_browser()
    try:
        page = await load_and_check_page(context)
        await take_screenshot_and_attach(page, "Landing Page")
        # 这里可以添加更多页面交互和截图
    finally:
        await browser.close()
        await playwright.stop()

if __name__ == "__main__":
    import asyncio
    asyncio.run(run_tests())
