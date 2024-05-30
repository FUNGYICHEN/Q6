import asyncio
import pytest
from allure import step
from test_setup import load_and_check_page, setup_browser, take_screenshot_and_attach, login


@pytest.mark.asyncio
async def test_specific_feature():
    playwright, browser, context = await setup_browser()  # 使用默认设备iPhone 11
    try:
        page = await load_and_check_page(context)
        print("页面加载成功。")

        await login(page, "all24042501", "396012")  # 使用公共登录函数

        with step("点击娱乐城"):
            await page.click("div.label:has-text('娛樂城')")
            await asyncio.sleep(3)
            await take_screenshot_and_attach(page, "点击娱乐城后")

        with step("关闭导览页"):
            await page.click("svg[width='24px'][height='24px'][viewBox='0 0 1024 1024'] path[fill='#999']")
            await asyncio.sleep(2)
            await take_screenshot_and_attach(page, "关闭导览页后")

        with step("关闭导览页2"):
            await page.click("svg[width='24px'][height='24px'][viewBox='0 0 1024 1024'] path[fill='#999']")
            await asyncio.sleep(2)
            await take_screenshot_and_attach(page, "关闭导览页后")

        with step("关闭公告"):
            viewport_size = page.viewport_size
            # 点击屏幕中心位置
            click_x = viewport_size['width'] * 0.5
            click_y = viewport_size['height'] * 0.10
            await page.mouse.click(click_x, click_y)
            await asyncio.sleep(2)
            await take_screenshot_and_attach(page, "公告关闭后")

        with step("选择CQ9电子游戏"):
            await page.click("div.enter-game-button.bk-cq9-slot.zh-TW")
            await asyncio.sleep(3)
            await take_screenshot_and_attach(page, "选择CQ9电子游戏后")

        with step("点击水果派对游戏图标"):
            await page.click("img[alt='水果派對']")
            await asyncio.sleep(20)
            await take_screenshot_and_attach(page, "点击水果派对游戏图标后")

        with step("在Canvas上进行点击"):
            viewport_size = page.viewport_size
            click_x = viewport_size['width'] * 0.10
            click_y = viewport_size['height'] * 0.76
            await page.mouse.click(click_x, click_y)
            print(f"在 X: {click_x}, Y: {click_y} 位置点击")
            await asyncio.sleep(5)  # 等待可能的页面响应或跳转
            await take_screenshot_and_attach(page, "在Canvas进行点击后")

        print("测试执行完毕。")

    except Exception as e:
        print(f"发生错误: {e}")
    finally:
        if browser:
            await browser.close()
        if playwright:
            await playwright.stop()

if __name__ == "__main__":
    asyncio.run(test_specific_feature())
