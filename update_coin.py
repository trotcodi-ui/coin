import requests
import json
import os

def get_coin_data():
    try:
        # 실시간 환율
        ex_res = requests.get("https://api.exchangerate-api.com/v4/latest/USD", timeout=10).json()
        exchange_rate = ex_res['rates']['KRW']
    except:
        exchange_rate = 1350.0

    coins = {
        'BTC': {'upbit': 'KRW-BTC', 'binance': 'BTCUSDT'},
        'ETH': {'upbit': 'KRW-ETH', 'binance': 'ETHUSDT'},
        'XRP': {'upbit': 'KRW-XRP', 'binance': 'XRPUSDT'}
    }

    results = []
    for name, tickers in coins.items():
        try:
            # 업비트
            up_res = requests.get(f"https://api.upbit.com/v1/ticker?markets={tickers['upbit']}", timeout=10).json()
            up_price = up_res[0]['trade_price']

            # 바이낸스 (KeyError 방지)
            bi_res = requests.get(f"https://api.binance.com/api/v3/ticker/price?symbol={tickers['binance']}", timeout=10).json()
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
            print(f"Error {name}: {e}")
            
    return results

# 수정된 정확한 URL입니다. (중간에 l 소문자 확인 완료)
WEB_APP_URL = "https://script.google.com/macros/s/AKfycbwlpTg25tibNN3zgQ4UGLX45pqokONs-U1jVT3sbbB1NRZnRyG4M_LDL4yR6GYUecqVyg/exec"

if __name__ == "__main__":
    data = get_coin_data()
    
    # 데이터가 있을 때만 시트 전송
    if data:
        try:
            requests.post(WEB_APP_URL, json=data, timeout=10)
        except:
            print("Google Sheet 전송 실패 (무시하고 진행)")

    # ★ 파일 생성을 명시적으로 실행 (에러 방지용)
    with open('coin_data.json', 'w', encoding='utf-8') as f:
        json.dump(data if data else [], f, ensure_ascii=False, indent=4)
    print("coin_data.json 파일 생성 완료")
