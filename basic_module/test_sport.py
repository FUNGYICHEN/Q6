import asyncio
import pytest
from allure import step
from test_setup import load_and_check_page, setup_browser, take_screenshot_and_attach, login


@pytest.mark.asyncio
async def test_new_feature():
    playwright, browser, context = await setup_browser()  # 使用默认设备iPhone 11
    try:
        page = await load_and_check_page(context)
        print("Page loaded successfully.")

        await login(page, "all24042501", "396012")  # 使用公共登录函数

        with step("点击走地"):
            await page.click("div.label:has-text('走地')")
            await asyncio.sleep(3.5)
            await take_screenshot_and_attach(page, "after_clicking_ground")

        with step("点击联赛位置"):
            viewport_size = page.viewport_size
            click_x = viewport_size['width'] * 0.55
            click_y = viewport_size['height'] * 0.35
            await page.mouse.click(click_x, click_y)
            print(f"Clicked at X: {click_x}, Y: {click_y}")
            await asyncio.sleep(3)
            await take_screenshot_and_attach(page, "点击联赛位置")

        with step("点击赔率"):
            viewport_size = page.viewport_size
            click_x = viewport_size['width'] * 0.55
            click_y = viewport_size['height'] * 0.47
            await page.mouse.click(click_x, click_y)
            print(f"Clicked at X: {click_x}, Y: {click_y}")
            await asyncio.sleep(3)
            await take_screenshot_and_attach(page, "点击赔率")

        with step("点击輸入框"):
            viewport_size = page.viewport_size
            click_x = viewport_size['width'] * 0.50
            click_y = viewport_size['height'] * 0.45
            await page.mouse.click(click_x, click_y)
            print(f"Clicked at X: {click_x}, Y: {click_y}")
            await asyncio.sleep(5)
            await take_screenshot_and_attach(page, "点击輸入框")

        with step("输入金额"):
            # 指定更精确的选择器以确保点击正确的数字
            await page.click("div.typeNumer > div:has-text('1')")
            await asyncio.sleep(2)
            await page.click("div.typeNumer > div:has-text('5')")
            await asyncio.sleep(5)
            await take_screenshot_and_attach(page, "输入金额")

        with step("点击投注"):
            await page.click("button.accept")
            await asyncio.sleep(6)
            await take_screenshot_and_attach(page, "点击投注")

    finally:
        await browser.close()
        await playwright.stop()

if __name__ == "__main__":
    asyncio.run(test_new_feature())
