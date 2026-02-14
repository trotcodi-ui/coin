import requests
import time

# [본인의 웹 앱 URL 확인!]
WEB_APP_URL = "https://script.google.com/macros/s/AKfycbwlpTg25tibNN3zgQ4UGLX45pqokONs-U1jVT3sbbB1NRZnRyG4M_LDL4yR6GYUecqVyg/exec"

def get_coin_data():
    coins = ["BTC", "ETH", "XRP"]
    result = []
    
    # 1. 환율 가져오기
    try:
        ex_rate = requests.get("https://api.exchangerate-api.com/v4/latest/USD").json()['rates']['KRW']
    except:
        ex_rate = 1450.0 # 환율 실패시 대비
    
    for coin in coins:
        try:
            # 2. 업비트 가격
            upbit = requests.get(f"https://api.upbit.com/v1/ticker?markets=KRW-{coin}").json()[0]['trade_price']
            
            # 3. 바이낸스 가격 (차단 방지를 위해 api1, api3 등 보조 주소 사용)
            # 요청 사이에 0.5초 짧은 휴식을 줍니다.
            time.sleep(0.5) 
            binance_url = f"https://api3.binance.com/api/v3/ticker/price?symbol={coin}USDT"
            binance_res = requests.get(binance_url).json()
            binance_price = float(binance_res['price'])
            
            # 4. 김프 계산
            binance_krw = binance_price * ex_rate
            premium = ((upbit - binance_krw) / binance_krw) * 100
            
            result.append({
                "name": coin,
                "upbit_price": upbit,
                "binance_price": binance_price,
                "exchange_rate": ex_rate,
                "binance_krw": round(binance_krw, 2),
                "premium": round(premium, 2)
            })
            print(f"{coin} 성공: {upbit}")
        except Exception as e:
            print(f"{coin} 실패 원인: {e}")
            
    return result

def main():
    data = get_coin_data()
    if data:
        res = requests.post(WEB_APP_URL, json=data)
        print(f"구글 전송 결과: {res.text}")

if __name__ == "__main__":
    main()
