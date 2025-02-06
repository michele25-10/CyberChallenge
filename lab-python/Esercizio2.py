#Scrivere un codice Python che legga un file di testo e crei un dizionario che tenga traccia della
#frequenza di comparsa di ogni carattere letto dal file.
#Ad esempio, se il testo è il seguente:

freq_dict = {}

with open("dati2.txt", "r") as f:
    for line in f:
        for word in line.replace("\n", ""):
            for let in word:
                if(freq_dict.get(let) == None):
                    freq_dict[let] = 1
                else:
                    freq_dict[let] += 1
                    
                    
print (freq_dict)