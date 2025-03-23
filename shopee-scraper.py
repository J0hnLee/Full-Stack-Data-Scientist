import asyncio
from playwright.async_api import async_playwright
import pandas as pd
from datetime import datetime
import json
import random
import time

async def scrape_shopee():
    try:
        playwright = await async_playwright().start()
        # 啟動瀏覽器
        browser = await playwright.chromium.launch(
            headless=True,
            args=['--disable-blink-features=AutomationControlled']  # 降低被檢測為自動化的可能性
        )
        
        # 設定瀏覽器上下文
        context = await browser.new_context(
            viewport={'width': 1920, 'height': 1080},
            user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36'
        )
        
        # 新增頁面
        page = await context.new_page()

        try:
            # 設定更長的超時時間（60秒）
            await page.set_default_timeout(60000)
            
            # 訪問 Shopee 首頁
            print('正在訪問 Shopee 首頁...')
            await page.goto('https://shopee.tw/', wait_until='networkidle')
            
            # 隨機等待 2-5 秒，模擬人類行為
            await asyncio.sleep(random.uniform(2, 5))
            
            print('等待產品列表載入...')
            # 等待產品列表載入
            await page.wait_for_selector('.shopee-search-item-result__item', timeout=60000)
            
            # 獲取產品資訊
            print('正在提取產品資訊...')
            products = await page.evaluate('''() => {
                const items = document.querySelectorAll('.shopee-search-item-result__item');
                return Array.from(items).map(item => {
                    const title = item.querySelector('.shopee-item-card__text-name')?.textContent || '';
                    const price = item.querySelector('.shopee-item-card__current-price')?.textContent || '';
                    const sales = item.querySelector('.shopee-item-card__sold-count')?.textContent || '';
                    const link = item.querySelector('a')?.href || '';
                    const image = item.querySelector('img')?.src || '';
                    
                    return {
                        title: title.trim(),
                        price: price.trim(),
                        sales: sales.trim(),
                        link: link,
                        image: image
                    };
                });
            }''')

            if not products:
                print('警告：沒有找到產品資訊')
                return None

            # 將結果轉換為 DataFrame
            df = pd.DataFrame(products)
            
            # 儲存為 CSV
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            csv_filename = f'shopee_products_{timestamp}.csv'
            df.to_csv(csv_filename, index=False, encoding='utf-8-sig')
            
            # 儲存為 JSON
            json_filename = f'shopee_products_{timestamp}.json'
            with open(json_filename, 'w', encoding='utf-8') as f:
                json.dump(products, f, ensure_ascii=False, indent=2)
            
            print(f'已成功爬取 {len(products)} 個產品')
            print(f'CSV 檔案已儲存為: {csv_filename}')
            print(f'JSON 檔案已儲存為: {json_filename}')
            
            return products

        except Exception as e:
            print(f'發生錯誤: {str(e)}')
            # 儲存錯誤截圖
            try:
                await page.screenshot(path=f'error_{datetime.now().strftime("%Y%m%d_%H%M%S")}.png')
                print('已儲存錯誤截圖')
            except:
                pass
            return None
        
        finally:
            # 關閉瀏覽器和 playwright
            await browser.close()
            await playwright.stop()

    except Exception as e:
        print(f'Playwright 初始化錯誤: {str(e)}')
        return None

async def main():
    max_retries = 3
    retry_count = 0
    
    while retry_count < max_retries:
        try:
            products = await scrape_shopee()
            if products:
                print('爬蟲完成！')
                break
            else:
                retry_count += 1
                if retry_count < max_retries:
                    wait_time = random.uniform(5, 10)
                    print(f'等待 {wait_time:.1f} 秒後重試...')
                    await asyncio.sleep(wait_time)
        except Exception as e:
            print(f'發生錯誤: {str(e)}')
            retry_count += 1
            if retry_count < max_retries:
                wait_time = random.uniform(5, 10)
                print(f'等待 {wait_time:.1f} 秒後重試...')
                await asyncio.sleep(wait_time)
    
    if retry_count >= max_retries:
        print('已達到最大重試次數，爬蟲失敗')

if __name__ == '__main__':
    asyncio.run(main())
