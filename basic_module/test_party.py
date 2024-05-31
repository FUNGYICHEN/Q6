import asyncio
import pytest
from allure import step
from test_setup import load_and_check_page, setup_browser, take_screenshot_and_attach, login


@pytest.mark.asyncio
async def test_specific_feature():
    playwright, browser, context = await setup_browser()  # 使用默认设备iPhone 11
    test_failed = False
    fail_message = ""
    response_received = False
    response_data = {}

    async def handle_response(response):
        nonlocal response_received, response_data
        if "api/path/you/expect" in response.url():
            response_received = True
            try:
                response_json = await response.json()
                response_data = response_json
                print("API response received:", response_json)
            except Exception as e:
                print(f"Error parsing JSON response: {e}")

    try:
        page = await load_and_check_page(context)
        print("页面加载成功。")

        page.on('response', handle_response)

        await login(page, "all24042501", "396012")  # 使用公共登录函数

        with step("导航到个人中心"):
            await page.click("div.label:has-text('個人中心')")
            await asyncio.sleep(2)
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

        with step("点击确定"):
            await page.click("a.am-modal-button[role='button']:has-text('確定')")
            await asyncio.sleep(5)  # 增加等待时间，以确保响应接收
            await take_screenshot_and_attach(page, "点击确定后")

            if response_received:
                # 检查返回代码是否为'0000'
                if response_data.get('code') == '0000':
                    print("API 返回正确的代码 0000")
                else:
                    test_failed = True
                    fail_message = f"API返回错误代码或信息: {response_data.get('msg')}"
            else:
                test_failed = True
                fail_message = "未收到API响应"

    except Exception as e:
        print(f"发生错误: {e}")
        fail_message = str(e)
        test_failed = True
        await take_screenshot_and_attach(page, "error_during_test")

    finally:
        page.off('response', handle_response)
        if browser is not None:
            await browser.close()
        if playwright is not None:
            await playwright.stop()
        if test_failed:
            pytest.fail(fail_message)

if __name__ == "__main__":
    asyncio.run(test_specific_feature())
