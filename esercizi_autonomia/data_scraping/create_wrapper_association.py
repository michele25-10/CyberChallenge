import csv

comuni = [
    "Alfonsine",
    "Bagnacavallo",
    "Bagnara di Romagna",
    "Brisighella",
    "Casola Valsenio",
    "Castel Bolognese",
    "Cervia",
    "Conselice",
    "Cotignola",
    "Faenza",
    "Fusignano",
    "Lugo",
    "Massa Lombarda",
    "Ravenna",
    "Riolo Terme",
    "Russi",
    "Sant'Agata sul Santerno",
    "Solarolo"
]

filename = []
for comune in comuni:
    filename.append(comune.replace(" ", "_") + ".csv")

# Nome del file di output
output_file = "associazioni_ravenna.csv"

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