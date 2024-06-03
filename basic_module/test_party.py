import asyncio
import pytest
from allure import step
from test_setup import load_and_check_page, setup_browser, take_screenshot_and_attach, login


@pytest.mark.asyncio
async def test_specific_feature():
    playwright, browser, context = await setup_browser()  # 使用默认设备iPhone 11
    test_failed = False
    fail_message = ""

    async def handle_response(response):
        nonlocal test_failed, fail_message
        if response.url == "https://wap-q6.qbpink01.com/activity/frontend/extrabonus/applyAward":
            json_data = await response.json()
            print(f"Response from getAvailableBalance: {json_data}")
            if json_data.get('code') != '0000':
                test_failed = True
                fail_message = f"测试失败: {json_data.get('msg')}"

    try:
        page = await load_and_check_page(context)
        print("Page loaded successfully.")
        await login(page, "all24042501", "396012")  # 使用公共登录函数
        page.on('response', handle_response)

        with step("导航到个人中心"):
            await page.click("div.label:has-text('個人中心')")
            await asyncio.sleep(3)
            await take_screenshot_and_attach(page, "导航到个人中心后")

        with step("点击优惠中心"):
            await page.click("div.promote .label:has-text('優惠中心')")
            await asyncio.sleep(2)
            await take_screenshot_and_attach(page, "点击优惠中心后")

        with step("点击优惠活动"):
            await page.click("li.tab-item:has-text('活動優惠')")
            await asyncio.sleep(2)
            await take_screenshot_and_attach(page, "点击优惠活动后")

        with step("点击立即申请"):
            viewport_size = page.viewport_size
            x = viewport_size['width'] * 0.8
            y = viewport_size['height'] * 0.35
            await page.mouse.click(x, y)
            await asyncio.sleep(2)
            await take_screenshot_and_attach(page, "点击立即申请后")

        with step("點擊確定"):
            await page.click("a.am-modal-button[role='button']:has-text('確定')")
            await asyncio.sleep(2)
            await take_screenshot_and_attach(page, "点击确定后")

    except Exception as e:
        print(f"An error occurred: {e}")
        fail_message = str(e)
        test_failed = True
    finally:
        page.remove_listener('response', handle_response)
        if browser:
            await browser.close()
        if playwright:
            await playwright.stop()
        if test_failed:
            pytest.fail(fail_message)

if __name__ == "__main__":
    asyncio.run(test_specific_feature())
