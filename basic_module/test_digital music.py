import asyncio
import pytest
from allure import step
from test_setup import load_and_check_page, setup_browser, take_screenshot_and_attach, login


@pytest.mark.asyncio
async def test_specific_feature():
    playwright, browser, context = await setup_browser()  # 使用默认设备iPhone 11
    test_failed = False
    fail_message = ""
    try:
        page = await load_and_check_page(context)
        print("Page loaded successfully.")

        await login(page, "all24042501", "396012")  # 使用公共登录函数

        with step("导航到个人中心"):
            await page.click("div.label:has-text('個人中心')")
            await asyncio.sleep(2)
            await take_screenshot_and_attach(page, "after_navigate_to_personal_center")

        with step("点击存款"):
            await page.click("div.label:has-text('存款')")
            await asyncio.sleep(2)
            await take_screenshot_and_attach(page, "after_click_deposit")

        with step("选择数字乐"):
            await page.click("div.am-list-content:has-text('數字樂')")
            await asyncio.sleep(2)
            await take_screenshot_and_attach(page, "after_select_bank_transfer")

        with step("输入充值金额"):
            await page.fill("input#chargeAmount.fc-red", "100")
            await asyncio.sleep(2)
            await take_screenshot_and_attach(page, "after_enter_deposit_amount")

        async def handle_response(response):
            if response.url == "https://wap-q6.qbpink01.com/payment/frontend/doPay":
                json_data = await response.json()
                print(f"Response from doPay: {json_data}")
                if json_data.get('code') == '2313':
                    nonlocal test_failed, fail_message
                    test_failed = True
                    fail_message = f"Test failed with message: {
                        json_data.get('msg')}"

        page.on('response', handle_response)

        with step("点击下一步按钮"):
            await page.click("a.submitBtn:has-text('下一步')")
            await asyncio.sleep(2)
            await take_screenshot_and_attach(page, "after_confirm_deposit")

        with step("确认充值完成"):
            await page.click("a:has-text('已完成充值')")
            await asyncio.sleep(2)
            await take_screenshot_and_attach(page, "after_confirm_deposit")

    except Exception as e:
        print(f"An error occurred: {e}")
        if page is not None:
            await take_screenshot_and_attach(page, "error_during_test")
    finally:
        # 注销监听器
        page.remove_listener('response', handle_response)
        if browser is not None:
            await browser.close()
        if playwright is not None:
            await playwright.stop()
        if test_failed:
            pytest.fail(fail_message)

if __name__ == "__main__":
    asyncio.run(test_specific_feature())
