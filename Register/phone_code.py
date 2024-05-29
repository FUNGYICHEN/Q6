import asyncio
import pytest
from allure import step
from allcommon import setup_browser, take_screenshot_and_attach, load_and_check_page
import string
import random
# 導入 fetch_verification_code 函數
from phone_code import fetch_verification_code  # type: ignore


def generate_random_string(length=12, digits=6):
    letters = ''.join(random.choices(string.ascii_letters, k=length - digits))
    numbers = ''.join(random.choices(string.digits, k=digits))
    return ''.join(random.sample(letters + numbers, len(letters + numbers)))


def generate_hk_phone_number():
    prefixes = ['6', '9', '5']
    return random.choice(prefixes) + ''.join(random.choice(string.digits) for _ in range(7))


@pytest.mark.asyncio
async def test_registration():
    playwright, browser, context = await setup_browser(device_name='iPhone 11', headless=False)
    try:
        page = await context.new_page()
        await page.goto('https://wap-q6.qbpink01.com/reg')

        username = generate_random_string(6, 3)
        password = generate_random_string(6, 3)
        phone_number = generate_hk_phone_number()

        with step("填写用户名"):
            await page.fill('input[placeholder="請輸入帳號"]', username)
            await asyncio.sleep(3)
            await take_screenshot_and_attach(page, "after_filling_username")

        with step("填写手机号码"):
            await page.fill('input[placeholder="請輸入手機號"]', phone_number)
            await asyncio.sleep(3)
            await take_screenshot_and_attach(page, "after_filling_phone_number")

        with step("点击发送验证码"):
            await page.click('div#validate')
            await asyncio.sleep(3)
            await take_screenshot_and_attach(page, "after_clicking_validate")

        # 從後台獲取驗證碼
        verification_code = await fetch_verification_code()
        if verification_code:
            with step("填写验证码"):
                await page.fill('input[placeholder="請輸入手機驗證碼"]', verification_code)
                await asyncio.sleep(3)
                await take_screenshot_and_attach(page, "after_filling_verification_code")

        with step("填写密码"):
            await page.fill('input[placeholder="請輸入登入密碼"]', password)
            await asyncio.sleep(3)
            await take_screenshot_and_attach(page, "after_filling_password")

        # 點擊註冊按鈕
        with step("点击注册按钮"):
            await page.click('div.submitBtn:has-text("會員註冊")')
            await asyncio.sleep(3)
            await take_screenshot_and_attach(page, "after_clicking_register")

    finally:
        await page.close()
        await context.close()
        await browser.close()

if __name__ == "__main__":
    asyncio.run(test_registration())
