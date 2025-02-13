
length = []
row = []

with open("words.txt" , "r") as f:
    for line in f:
        row.append(line.replace("\n", "")) 

with open("flusso.txt", "r") as f:
    i = 0
    for line in f:    
        if "-- end --" in line:
            length.append(i)
            i = 0        
        else: 
            i += 1

alphabet = "abcdefghijklmnopqrstuvwxyz"

#Seleziona le parole aventi lunghezza 10
start = 0
word = ""
while start < len(length):
    for lect in alphabet:        
        counter = 0
        tmp_str = word + lect
        for line in row: 
            if(start == 0): 
                if line[0] == tmp_str:
                    counter += 1            
            else:
                if line[0:(start+1)] == tmp_str:
                    counter += 1            
        if counter == length[start]:
            word = tmp_str
            start += 1
            print(f"parola: {word}")
            break
        counter = 0

