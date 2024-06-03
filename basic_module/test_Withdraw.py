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
        if response.url == "https://wap-q6.qbpink01.com/member/frontend/getAvailableBalance":
            json_data = await response.json()
            print(f"Response from getAvailableBalance: {json_data}")
            if json_data.get('code') != '0000':
                test_failed = True
                fail_message = f"测试失败: {json_data.get('msg')}"
        elif response.url == "https://wap-q6.qbpink01.com/payment/frontend/insertWithdrawRecord":
            json_data = await response.json()
            print(f"Response from insertWithdrawRecord: {json_data}")
            if json_data.get('code') != '0000':
                test_failed = True
                fail_message = f"测试失败: {json_data.get('msg')}"

    try:
        page = await load_and_check_page(context)
        print("页面加载成功。")

        await login(page, "all24042501", "396012")  # 使用公共登录函数

        page.on('response', handle_response)

        with step("导航到个人中心"):
            await page.click("div.label:has-text('個人中心')")
            await asyncio.sleep(2)
            await take_screenshot_and_attach(page, "导航到个人中心后")

        with step("点击提款按钮"):
            await page.click("div.icon.icon-withdraw")
            await asyncio.sleep(2)
            await take_screenshot_and_attach(page, "点击提款按钮后")

        with step("输入提款金额"):
            await page.fill("input[type='number'][placeholder='最少提款金額10元']", "10")
            await asyncio.sleep(2)
            await take_screenshot_and_attach(page, "输入提款金额后")

        with step("点击确认提款"):
            await page.click("div.submitBtn:has-text('確認提款')")
            await asyncio.sleep(2)
            await take_screenshot_and_attach(page, "点击确认提款后")

        with step("点击确定"):
            await page.click("a.am-modal-button:has-text('確定')")
            await asyncio.sleep(2)
            await take_screenshot_and_attach(page, "点击确定后")

    except Exception as e:
        print(f"发生错误: {e}")
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
