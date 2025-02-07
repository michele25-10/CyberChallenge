import requests

#request sito www.example.com
res = requests.get("http://www.example.com")
print(f"Stato request: {res.status_code}")

#Scrittura della risposta in un file html
fd = open("www_example_com.html", "w")
fd.write(res.text)
fd.close()
res.close()

#Il sito jsonplaceholder.typicode.com simula una REST API che utilizza JSON come formato delle informazioni.
#Contattando la pagina jsonplaceholder.typecode.com/todos è possibile vedere una lista di todo, 
#inoltre è possibile aggiungerli eliminarli o modificarli

#Richiesta POST todo

data = {
    "userId":12345,
    "title": "Esercizio Requests", 
    "completed": True
}
res_post = requests.post("https://jsonplaceholder.typicode.com/todos", data)
print(f"Status POST {res_post.status_code}")

#Essendo un json già un dictionary posso accederci anche in questo modo
res_json = res_post.json()
id_todo = res_json["id"]

#Richiesta DELETE todo
delete_url = f"https://jsonplaceholder.typicode.com/todos/{id_todo}"
res_delete = requests.delete(delete_url)
print(f"Status DELETE: {res_delete.status_code}")


