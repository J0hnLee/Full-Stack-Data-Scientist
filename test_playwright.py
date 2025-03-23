import asyncio
from playwright.async_api import async_playwright
import os

async def test_playwright():
    try:
        print('開始測試 Playwright...')
        
        # 初始化 Playwright
        playwright = await async_playwright().start()
        print('Playwright 初始化成功')
        
        # 啟動瀏覽器，在容器中使用 headless 模式
        browser = await playwright.chromium.launch(
            headless=False,  # 在容器中使用 headless 模式
            args=[
                '--disable-blink-features=AutomationControlled',
                '--no-sandbox',  # 在容器中需要
                '--disable-setuid-sandbox',  # 在容器中需要
                '--disable-dev-shm-usage',  # 避免記憶體問題
                '--disable-gpu'  # 在容器中禁用 GPU
            ]
        )
        print('瀏覽器啟動成功')
        
        # 創建新頁面
        page = await browser.new_page()
        print('新頁面創建成功')
        
        # 訪問測試網站
        print('正在訪問測試網站...')
        await page.goto('https://example.com')
        print('網站訪問成功')
        
        # 獲取頁面標題
        title = await page.title()
        print(f'頁面標題: {title}')
        
        # 截圖
        screenshot_path = './test_screenshot.png'
        await page.screenshot(path=screenshot_path)
        print(f'截圖已儲存為 {screenshot_path}')
        
        # 檢查截圖是否成功創建
        if os.path.exists(screenshot_path):
            print(f'截圖檔案大小: {os.path.getsize(screenshot_path)} bytes')
        else:
            print('警告：截圖檔案未創建')
        
        # 等待 3 秒以便觀察
        await asyncio.sleep(3)
        
        print('測試完成，正在清理資源...')
        
    except Exception as e:
        print(f'測試過程中發生錯誤: {str(e)}')
    
    finally:
        # 清理資源
        try:
            await browser.close()
            await playwright.stop()
            print('資源清理完成')
        except Exception as e:
            print(f'清理資源時發生錯誤: {str(e)}')

async def main():
    print('開始執行 Playwright 測試...')
    await test_playwright()
    print('測試結束')

if __name__ == '__main__':
    asyncio.run(main()) 