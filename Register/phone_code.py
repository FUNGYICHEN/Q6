import asyncio
import httpx


async def fetch_verification_code():
    url = "http://oms.npf2.uat2.qit1.net/message/otp-list"
    headers = {
        'Content-Type': 'application/json;charset=UTF-8',
        'Accept': '*/*',
    }
    payload = {
        "phoneNumber": "ALL",  # 固定使用"ALL"
        "token": "1514193320D94315039B120D2971A77CB1DB411FE9C9C8C5D6CE5DC1CC54A3371B6050C4AE6548B37A9F995472284F9805BFF2EF77CF5C10F598936B0F908A8AE1ACFB902D5917E08D7A64A3784D1EE5B7C7FA8B9BA2F7FFED0CBBAC1F7D221F8238B5526F49AEF34752BBC27BE99BF4D9B6B36565F00C77E7BF83CFCEE211AA3FBE57865D42B82A1C2CE074FEEB1C95308C744E4B882ADB8DC55F9BEB452BF8"  # 请替换为实际的Token
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
