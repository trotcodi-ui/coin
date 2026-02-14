import requests

# [주의] 본인의 웹 앱 URL로 다시 한번 확인하세요!
WEB_APP_URL = "https://script.google.com/macros/s/AKfycbwlpTg25tibNN3zgQ4UGLX45pqokONs-U1jVT3sbbB1NRZnRyG4M_LDL4yR6GYUecqVyg/exec"

def get_coin_data():
    coins = ["BTC", "ETH", "XRP"]  # 여기에 XRP(리플)를 추가했습니다.
    result = []
    
    # 환율 가져오기
    ex_rate = requests.get("https://api.exchangerate-api.com/v4/latest/USD").json()['rates']['KRW']
    
    for coin in coins:
        # 업비트 가격
        upbit = requests.get(f"https://api.upbit.com/v1/ticker?markets=KRW-{coin}").json()[0]['trade_price']
        # 바이낸스 가격
        binance = float(requests.get(f"https://api.binance.com/api/v3/ticker/price?symbol={coin}USDT").json()['price'])
        
        binance_krw = binance * ex_rate
        premium = ((upbit - binance_krw) / binance_krw) * 100
        
        result.append({
            "name": coin,
            "upbit_price": upbit,
            "binance_price": binance,
            "exchange_rate": ex_rate,
            "binance_krw": round(binance_krw, 2),
            "premium": round(premium, 2)
        })
    return result

def main():
    data = get_coin_data()
    print("--- 실시간 데이터 수집 완료 ---")
    
    try:
        response = requests.post(WEB_APP_URL, json=data, timeout=15)
        print(f"전송 결과: {response.text}")
    except Exception as e:
        print(f"에러: {e}")

if __name__ == "__main__":
    main()
