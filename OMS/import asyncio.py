import asyncio
import pytest
from allure import step
from allcommon import setup_browser, take_screenshot_and_attach


@pytest.mark.asyncio
async def test_navigation_process():
    playwright, browser, context = await setup_browser(device_name='iPhone 11', headless=True)
    try:
        page = await context.new_page()
        await page.goto('https://your-target-url.com')  # 请替换为您的目标URL

        with step("点击首页"):
            # 点击页面上的“首页”按钮
            await page.click('li.el-menu-item.is-active.submenu-title-noDropdown')
            await asyncio.sleep(3)
            await take_screenshot_and_attach(page, "after_clicking_home")

        with step("点击综合查询"):
            # 点击“综合查询”按钮
            await page.click('span:has-text("綜合查詢")')
            await asyncio.sleep(3)
            await take_screenshot_and_attach(page, "after_clicking_comprehensive_query")

        with step("点击平台盈亏"):
            # 点击“平台盈亏”选项
            await page.click('li.el-menu-item:has-text("平台盈虧")')
            await asyncio.sleep(3)
            await take_screenshot_and_attach(page, "after_clicking_platform_profit_loss")

    finally:
        await page.close()
        await context.close()
        await browser.close()

if __name__ == "__main__":
    asyncio.run(test_navigation_process())
