import requests

url = "http://sqlinjection.challs.cyberchallenge.it/api/blind"

# Fai una richiesta OPTIONS per scoprire i metodi supportati
response = requests.options(url)

# Stampa gli headers della risposta per cercare "Allow"
print(response.headers)

# Verifica se l'header 'Allow' è presente
if 'Allow' in response.headers:
    print("Metodi supportati:", response.headers['Allow'])
else:
    print("L'header 'Allow' non è presente.")
