import asyncio
import pytest
from allure import step
from test_setup import load_and_check_page, setup_browser, take_screenshot_and_attach, login
import re


@pytest.mark.asyncio
async def test_full_user_journey():
    playwright, browser, context = await setup_browser()  # 使用默认设备iPhone 11
    try:
        page = await load_and_check_page(context)
        await login(page, "all24042501", "396012")  # 使用公共登录函数

        async def click_and_capture(step_description, selector):
            with step(step_description):
                await page.click(selector)
                await asyncio.sleep(1.5)
                await take_screenshot_and_attach(page, step_description)

        # 执行详细的点击和交互序列
        await click_and_capture("点击个个人中心", 'text=個人中心')
        await click_and_capture("点击合营代理", "div.menu-item:has(div.main-label-text:text('合營代理'))")
        await click_and_capture("点击查询按钮", 'button.date-search:has-text("查詢")')
        await click_and_capture("点击申请佣金", 'text=申請佣金')
        await click_and_capture("点击佣金申请记录", 'text=佣金申請紀錄')
        await click_and_capture("点击通用按钮", 'role=button')
        await click_and_capture("点击返水领取", "div.main-label:has(div.icon-getrebate)")
        await click_and_capture("点击VIP福利", "div.menu-item:has(div.icon.icon-rebate)")
        await click_and_capture("点击VIP详情", 'text=VIP詳情')
        await click_and_capture("点击TOP按钮", 'role=button[name="TOP"]')
        await click_and_capture("点击com-header按钮", "#com-header >> role=button")
        await click_and_capture("点击VIP返水", "div.vip-card-left:has-text('VIP返水')")
        await click_and_capture("点击领取记录", 'text=領取記錄')
        await click_and_capture("点击通用按钮2", 'role=button')
        await click_and_capture("点击每周福利", "div.vip-card-left:has(div.vip-card-check:text('每週福利'))")
        await click_and_capture("点击领取记录2", 'text=領取記錄')
        await click_and_capture("点击通用按钮3", 'role=button')
        await click_and_capture("点击每月福利", "div.vip-card-left:has(div.vip-card-check:text('每月福利'))")
        await click_and_capture("点击领取记录3", 'text=領取記錄')
        await click_and_capture("点击通用按钮4", 'role=button')
        await click_and_capture("点击通用按钮5", 'role=button')
        await click_and_capture("点击今日盈亏", "div.menu-item:has(div.icon.icon-profit)")
        await click_and_capture("点击通用按钮6", 'role=button')
        await click_and_capture("点击充提记录", "div.menu-item:has(div.icon.icon-history)")
        await click_and_capture("点击com-header按钮2", "#com-header >> role=button")
        await click_and_capture("点击交易记录", "div.menu-item:has(div.icon.icon-statement)")
        await click_and_capture("点击通用按钮7", 'role=button')
        await click_and_capture("点击银行卡管理", "div.menu-item:has(div.icon.icon-bank-card)")
        await click_and_capture("点击通用按钮7", 'role=button')
        await click_and_capture("点击投注记录", "div.menu-item:has(div.icon.icon-record)")
        await click_and_capture("点击com-header按钮3", "#com-header >> role=button")
        await click_and_capture("点击推广链接", "div.menu-item:has(div.icon.icon-invitefriend)")
        await click_and_capture("点击通用按钮8", 'role=button')
        await click_and_capture("点击赛果查询", "div.menu-item:has(div.icon.icon-game-result) >> text=賽果查詢")
        await click_and_capture("点击篮球", 'role=button[name="籃 球"]')
        await click_and_capture("点击网球", 'role=button[name="網 球"]')
        await click_and_capture("点击棒球", 'role=button[name="棒 球"]')
        await click_and_capture("点击com-header按钮5", "#com-header >> role=button")
        await click_and_capture("点击关于港体会", "div.menu-item:has(div.icon.icon-alert.logo) >> text=關於 港體會")
        await click_and_capture("点击span", 'span')
        await click_and_capture("点击下载港体会APP", "div.menu-item:has(div.icon.icon-alert) >> text=下載 港體會 APP")

    finally:
        await browser.close()
        await playwright.stop()

if __name__ == "__main__":
    asyncio.run(test_full_user_journey())
