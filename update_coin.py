import requests
import json

# [본인의 웹 앱 URL로 꼭 확인하세요!]
WEB_APP_URL = "https://script.google.com/macros/s/AKfycbwIpTg25tibNN3zgQ4UGLX45pqokONs-U1jVT3sbBb1NRZnRyG4M_LDL4yR6GYUecqVyg/exec"

def main():
    # 1. 테스트용 데이터 생성 (실제 데이터 수집 코드 대신 우선 테스트)
    # 나중에 실제 수집 코드로 교체하더라도 전송 구조는 동일합니다.
    data = [
        {"name": "BTC", "upbit_price": 100000000, "binance_price": 70000, "exchange_rate": 1400, "binance_krw": 98000000, "premium": 2.04},
        {"name": "ETH", "upbit_price": 3500000, "binance_price": 2400, "exchange_rate": 1400, "binance_krw": 3360000, "premium": 4.16}
    ]

    print("--- 생성된 JSON 데이터 확인 ---")
    print(json.dumps(data, indent=2))
    print("----------------------------")

    # 2. 구글 시트로 전송
    try:
        print("구글 시트로 전송을 시작합니다...")
        response = requests.post(WEB_APP_URL, json=data, timeout=15)
        print(f"구글 응답 코드: {response.status_code}")
        print(f"구글 응답 내용: {response.text}")
    except Exception as e:
        print(f"전송 중 에러 발생: {e}")

if __name__ == "__main__":
    main()
