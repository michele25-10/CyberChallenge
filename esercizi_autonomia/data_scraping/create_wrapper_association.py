import csv

comuni = [
    "Abano Terme", "Agna", "Albignasego", "Anguillara Veneta", "Arquà Petrarca", "Arre", "Arzergrande",
    "Bagnoli di Sopra", "Baone", "Battaglia Terme", "Boara Pisani", "Borgoricco", "Borgo Veneto",
    "Bovolenta", "Brugine", "Cadoneghe", "Campo San Martino", "Campodarsego", "Campodoro", "Camposampiero",
    "Candiana", "Carmignano di Brenta", "Cartura", "Casale di Scodosia", "Casalserugo", "Castelbaldo",
    "Cervarese Santa Croce", "Cinto Euganeo", "Cittadella", "Codevigo", "Conselve", "Correzzola", "Curtarolo",
    "Due Carrare", "Este", "Fontaniva", "Galliera Veneta", "Galzignano Terme", "Gazzo", "Grantorto", "Granze",
    "Legnaro", "Limena", "Loreggia", "Lozzo Atestino", "Maserà di Padova", "Masi", "Massanzago",
    "Megliadino San Vitale", "Merlara", "Mestrino", "Monselice", "Montagnana", "Montegrotto Terme",
    "Noventa Padovana", "Ospedaletto Euganeo", "Padova", "Pernumia", "Piacenza d'Adige", "Piazzola sul Brenta",
    "Piombino Dese", "Piove di Sacco", "Polverara", "Ponso", "Ponte San Nicolò", "Pontelongo", "Pozzonovo",
    "Rovolon", "Rubano", "Saccolongo", "San Giorgio delle Pertiche", "San Giorgio in Bosco",
    "San Martino di Lupari", "San Pietro Viminario", "San Pietro in Gu", "Sant'Angelo di Piove di Sacco",
    "Sant'Elena", "Sant'Urbano", "Santa Giustina in Colle", "Saonara",
    "Selvazzano Dentro", "Solesino", "Stanghella", "Teolo", "Terrassa Padovana", "Tombolo", "Torreglia",
    "Trebaseleghe", "Tribano", "Urbana", "Veggiano", "Vescovana", "Vigodarzere", "Vigonza", "Villa Estense",
    "Villa del Conte", "Villafranca Padovana", "Villanova di Camposampiero", "Vo'"
]


filename = []
for comune in comuni:
    filename.append(comune.replace(" ", "_") + ".csv")

# Nome del file di output
output_file = "associazioni_padova.csv"

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