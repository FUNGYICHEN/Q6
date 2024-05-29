import asyncio
import pytest
from allure import step
from test_setup import load_and_check_page, setup_browser, take_screenshot_and_attach, login


@pytest.mark.asyncio
async def test_specific_feature():
    playwright, browser, context = await setup_browser()  # 使用默认设备iPhone 11
    try:
        page = await load_and_check_page(context)
        print("Page loaded successfully.")

        await login(page, "all24042501", "396012")  # 使用公共登录函数

        with step("导航到个人中心"):
            await page.click("div.label:has-text('個人中心')")
            await asyncio.sleep(3)
            await take_screenshot_and_attach(page, "after_navigate_to_personal_center")

        with step("进入我的钱包"):
            try:
                await page.click("div.buttons:has-text('我的錢包')")
                await asyncio.sleep(1.5)
                await take_screenshot_and_attach(page, "after_click_my_wallet")
            except Exception as e:
                print(f"Failed to click on the my wallet button: {str(e)}")
                await take_screenshot_and_attach(page, "error_clicking_my_wallet")

        # 准备捕获API响应
        api_call_success = False

        async def handle_response(response):
            print("Response received from URL:", response.url)
            if response.url == "https://wap-q6.qbpink01.com/member/frontend/returnGameBalance":
                json_data = await response.json()
                print("API Response Data:", json_data)  # 打印看看实际的响应数据
                if json_data.get('code') == '0000':
                    nonlocal api_call_success
                    api_call_success = True
                    print("API call was successful and the data is correct.")

        # 注册响应处理器
        page.on('response', handle_response)

        with step("点击一键转回按钮"):
            await page.click("div.money_back")
            await asyncio.sleep(4)  # 等待API响应完成
            await take_screenshot_and_attach(page, "after_click_money_back")

    finally:
        # 注销监听器
        page.remove_listener('response', handle_response)
        await browser.close()
        await playwright.stop()

if __name__ == "main":
    asyncio.run(test_specific_feature())
