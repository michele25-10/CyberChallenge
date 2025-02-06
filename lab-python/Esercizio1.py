# Si legga tutto il file creando un dizionario le cui chiavi rappresentano le età. A ciascuna età viene
#associata una lista con i nomi di persone che hanno quell'età. Una volta realizzato il dizionario, lo si
#stampi a video.

dict = {}

with open("dati.txt", "r") as f:
    for line in f:
        val = line.replace("\n", "").split(" ")
        dict[val[0]] = val[1]
        

val = {}
for key, item in dict.items():
    if(val.get(item) == None):
        val[item] = [key]
    else:
        val[item] = val[item] + [key]
        
print(val)