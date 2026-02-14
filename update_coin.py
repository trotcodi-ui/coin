import requests

def get_coin_data():
    # 1. 실시간 환율 가져오기
    try:
        ex_res = requests.get("https://api.exchangerate-api.com/v4/latest/USD").json()
        exchange_rate = ex_res['rates']['KRW']
    except:
        exchange_rate = 1350.0  # 실패 시 기본값

    coins = {
        'BTC': {'upbit': 'KRW-BTC', 'binance': 'BTCUSDT'},
        'ETH': {'upbit': 'KRW-ETH', 'binance': 'ETHUSDT'},
        'XRP': {'upbit': 'KRW-XRP', 'binance': 'XRPUSDT'}
    }

    results = []
    for name, tickers in coins.items():
        # 업비트 가격 (KRW)
        up_res = requests.get(f"https://api.upbit.com/v1/ticker?markets={tickers['upbit']}").json()
        up_price = up_res[0]['trade_price']

        # 바이낸스 가격 (USD)
        bi_res = requests.get(f"https://api.binance.com/api/v3/ticker/price?symbol={tickers['binance']}").json()
        bi_price = float(bi_res['price'])

        # 김치 프리미엄 계산
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
    return results

# ★ 중요: 아까 복사한 구글 웹 앱 URL을 여기에 붙여넣으세요
WEB_APP_URL = "https://script.google.com/macros/s/AKfycbwlptg25tibNN3zgQ4UGLX45pqokONs-U1jVT3sbbB1NRZnRyG4M_LDL4yR6GYUecqVyg/exec"

if __name__ == "__main__":
    data = get_coin_data()
    response = requests.post(WEB_APP_URL, json=data)
    print(f"전송 결과: {response.text}")
