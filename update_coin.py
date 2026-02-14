import requests

# [본인의 웹 앱 URL로 다시 한번 확인하세요!]
WEB_APP_URL = "https://script.google.com/macros/s/AKfycbwlpTg25tibNN3zgQ4UGLX45pqokONs-U1jVT3sbbB1NRZnRyG4M_LDL4yR6GYUecqVyg/exec"

def get_coin_data():
    # 수집할 코인 목록
    coins = ["BTC", "ETH", "XRP"]
    result = []
    
    # 1. 환율 가져오기
    try:
        ex_rate = requests.get("https://api.exchangerate-api.com/v4/latest/USD").json()['rates']['KRW']
    except:
        ex_rate = 1400.0  # 환율 API 오류 시 기본값 설정
    
    for coin in coins:
        try:
            # 2. 업비트 가격 (KRW-BTC, KRW-ETH, KRW-XRP)
            upbit_url = f"https://api.upbit.com/v1/ticker?markets=KRW-{coin}"
            upbit_price = requests.get(upbit_url).json()[0]['trade_price']
            
            # 3. 바이낸스 가격 (BTCUSDT, ETHUSDT, XRPUSDT)
            # 바이낸스는 코인 이름 뒤에 바로 USDT가 붙어야 합니다.
            binance_url = f"https://api.binance.com/api/v3/ticker/price?symbol={coin}USDT"
            binance_res = requests.get(binance_url).json()
            binance_price = float(binance_res['price'])
            
            # 4. 김프 계산
            binance_krw = binance_price * ex_rate
            premium = ((upbit_price - binance_krw) / binance_krw) * 100
            
            result.append({
                "name": coin,
                "upbit_price": upbit_price,
                "binance_price": binance_price,
                "exchange_rate": ex_rate,
                "binance_krw": round(binance_krw, 2),
                "premium": round(premium, 2)
            })
            print(f"{coin} 수집 완료: {upbit_price}")
            
        except Exception as e:
            print(f"{coin} 수집 중 에러 발생: {e}")
            continue # 에러 난 코인은 건너뛰고 다음 코인 진행
            
    return result

def main():
    data = get_coin_data()
    if not data:
        print("수집된 데이터가 없습니다.")
        return

    try:
        print("구글 시트로 전송 시작...")
        response = requests.post(WEB_APP_URL, json=data, timeout=15)
        print(f"전송 결과: {response.text}")
    except Exception as e:
        print(f"전송 에러: {e}")

if __name__ == "__main__":
    main()
