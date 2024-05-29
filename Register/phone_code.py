import asyncio
import httpx


async def fetch_verification_code():
    url = "https://oms-q6.qbpink01.com/manage/backend/func/otp/queryCode"
    headers = {
        'Content-Type': 'application/json;charset=UTF-8',
        'Accept': '*/*',
    }
    payload = {
        "phoneNumber": "ALL",  # 固定使用"ALL"
        "token": "YourActualTokenHere"  # 请替换为实际的Token
    }

    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(url, json=payload, headers=headers)
            response.raise_for_status()
            data = response.json()
            print(f"API Response: {data}")
            if data['result']['data']:
                verification_code = data['result']['data'][0]['code']
                return verification_code
            else:
                print("No verification code received")
                return None
        except httpx.HTTPStatusError as e:
            print(f"HTTP error occurred: {e}")
            return None
        except Exception as e:
            print(f"An error occurred: {e}")
            return None


async def main():
    verification_code = await fetch_verification_code()
    print(f"Verification Code: {verification_code}")

if __name__ == "__main__":
    asyncio.run(main())
