# Realizzare uno script Python che legga riga per riga il file e salvi all'interno di una lista di tuple, dove
# ogni tupla è composta dal nome dello studente e un'ulteriore lista contenente i suoi relativi voti. Una
# volta realizzato questo, per ogni studente registrato, calcolare e stampare la media dei suoi voti.

list = []

with open("voti.txt", "r") as f:
    for line in f:
        tmp = line.replace("\n", "").split(" ")
        name = tmp[0]
        tmp.pop(0)
        list.append((name, tmp))
        
for item in list:
    tot = 0
    for voto in item[1]:
        tot += int(voto)
    
    print(f"Studente {item[0]}, Media voti: {tot/len(item[1])}")
        
            

