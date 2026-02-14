import requests
import json
import os

def get_coin_data():
    try:
        ex_res = requests.get("https://api.exchangerate-api.com/v4/latest/USD").json()
        exchange_rate = ex_res['rates']['KRW']
    except:
        exchange_rate = 1350.0

    # 바이낸스 심볼은 반드시 대문자여야 합니다.
    coins = {
        'BTC': {'upbit': 'KRW-BTC', 'binance': 'BTCUSDT'},
        'ETH': {'upbit': 'KRW-ETH', 'binance': 'ETHUSDT'},
        'XRP': {'upbit': 'KRW-XRP', 'binance': 'XRPUSDT'}
    }

    results = []
    for name, tickers in coins.items():
        try:
            up_res = requests.get(f"https://api.upbit.com/v1/ticker?markets={tickers['upbit']}").json()
            up_price = up_res[0]['trade_price']

            bi_res = requests.get(f"https://api.binance.com/api/v3/ticker/price?symbol={tickers['binance']}").json()
            # 에러 방지를 위해 get() 메서드 사용
            bi_price = float(bi_res.get('price', 0))

            if bi_price > 0:
                bi_krw = bi_price * exchange_rate
                premium = ((up_price / bi_krw) - 1) * 100
                
                results.append({
                    "name": name,
                    "upbit_price": up_price,
                    "binance_price": bi_price,
                    "exchange_rate": exchange_rate,
                    "binance_krw": round(bi_krw, 2),
                    "premium": round(premium, 2)
                })
        except Exception as e:
            print(f"Error processing {name}: {e}")
            
    return results

# 설정
WEB_APP_URL = "https://script.google.com/macros/s/AKfycbwlptg25tibNN3zgQ4UGLX45pqokONs-U1jVT3sbbB1NRZnRyG4M_LDL4yR6GYUecqVyg/exec"

if __name__ == "__main__":
    data = get_coin_data()
    
    # 1. 구글 시트로 전송
    if data:
        requests.post(WEB_APP_URL, json=data)
        
        # 2. 티스토리용 JSON 파일 저장
        with open('coin_data.json', 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        print("데이터 업데이트 및 JSON 생성 완료")
