import csv

comuni = [
    "Bastiglia",
    "Bomporto",
    "Campogalliano",
    "Camposanto",
    "Carpi",
    "Castelfranco Emilia",
    "Castelnuovo Rangone",
    "Castelvetro di Modena",
    "Cavezzo",
    "Concordia sulla Secchia",
    "Fanano",
    "Finale Emilia",         
    "Fiorano Modenese",
    "Fiumalbo",
    "Formigine",
    "Frassinoro",
    "Guiglia",
    "Lama Mocogno",
    "Maranello",
    "Marano sul Panaro",
    "Medolla",
    "Mirandola",
    "Modena",
    "Montecreto",
    "Montefiorino",
    "Montese",
    "Nonantola",
    "Novi di Modena",
    "Palagano",
    "Pavullo nel Frignano",
    "Pievepelago",
    "Polinago",
    "Prignano sulla Secchia",
    "Ravarino",
    "Riolunato",
    "San Cesario sul Panaro",
    "San Felice sul Panaro",
    "San Possidonio",
    "San Prospero",
    "Sassuolo",
    "Savignano sul Panaro",
    "Serramazzoni",
    "Sestola",
    "Soliera",
    "Spilamberto",
    "Vignola",
    "Zocca"
]

filename = []
for comune in comuni:
    filename.append(comune.replace(" ", "_") + ".csv")

# Nome del file di output
output_file = "associazioni_modena.csv"

# Apri il file di output in modalità scrittura
with open(output_file, mode="w", newline="", encoding="utf-8") as outfile:
    writer = None  # Variabile per il writer
    for file in filename:
        print(file)
        with open(file, mode="r", encoding="utf-8") as infile:
            reader = csv.reader(infile)
            headers = next(reader)  # Legge l'intestazione
            
            # Scrive l'header solo per il primo file
            if writer is None:
                writer = csv.writer(outfile)
                writer.writerow(headers)
            
            # Scrive i dati
            writer.writerows(reader)