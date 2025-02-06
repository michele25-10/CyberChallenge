def cifra_messaggio(str):
    cifrata = ""
    for let in str:
        cifrata += chr(ord(let) + 5)  
    
    return cifrata
    

def decifra_messaggio(str):
    decifrata = ""
    for let in str:
        decifrata += chr(ord(let) - 5)  
    
    return decifrata


stringa = input("Inserisci stringa: ")

cifrata = cifra_messaggio(stringa)
print(f"Messaggio cifrato: {cifrata}")

decifrata = decifra_messaggio(cifrata)
print(f"Messaggio decifrato: {decifrata}")
