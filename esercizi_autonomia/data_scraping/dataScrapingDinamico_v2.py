import time
import csv
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

#Funzione per ottenere i dati dalla pagina che viene aperta:
def get_text_or_none(by, value):
    try:
        return WebDriverWait(driver, 5).until(EC.presence_of_element_located((by, value))).text
    except:
        return None


#lista con tutti i dati delle associazioni e comuni da cui minare i dati
associations = []
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

for comune in comuni:
    # Apri il browser abilitando impostazione che non rilevi i bot
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_experimental_option("detach", True)
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    driver = webdriver.Chrome(options=chrome_options)
    driver.maximize_window()
    driver.get("https://servizi.lavoro.gov.it/runts/it-it/Ricerca-enti") 
    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")

    #Accetto i cookies sennò appaiono ogni volta
    try:
        driver.find_element(By.CLASS_NAME, "cookieClose").click()
        print("Banner cookie chiuso")
    except:
        print("Nessun banner cookie trovato, procedo...")

    
    # Compilo il form e poi invio, inizia così la ricerca
    driver.find_element(By.ID, "dnn_ctr446_View_txtComune").send_keys(comune)
    driver.find_element(By.ID, "dnn_ctr446_View_btnRicercaEnti").click()

    #La pagina avvia la ricerca, attendo finche non compare la tabella e ottengo il numero di risultati
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "dnn_ctr446_View_spnLabelNumeroTotaleItems")))
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "dnn_ctr446_View_spnLabelNumeroPaginaTop")))
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "dnn_ctr446_View_gvEnti")))

    n_rows = int(driver.find_element(By.ID, "dnn_ctr446_View_spnLabelNumeroTotaleItems").text)  
    n_pages = int((driver.find_element(By.ID, "dnn_ctr446_View_spnLabelNumeroPaginaTop").text).split(" ")[3]) #Pagina 1 di 55
    print(f"{datetime.now()} --- INIZIO procedura per comune: {comune} ")
    print(f"Numero di righe da copiare: {n_rows}")
    print(f"Numero di pagine da navigare: {n_pages}")

    driver.execute_script(f"window.scrollTo(0, 700);")
    time.sleep(1.5)

    for k in range(0, n_pages):
        for i in range(0, 10):
            id_button = "dnn_ctr446_View_gvEnti_btnDettaglio_" + str(i)
            
            try:
                WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, id_button)))
                driver.find_element(By.ID, id_button).click()
            except TimeoutException:
                print(f"Bottone {id_button} non trovato. Uscita dal ciclo.")
                break  # Esce dal ciclo se il bottone non esiste
            
            tmp = {}
            #Prelevto i dati dalla pagina dell'associazione
            tmp["name_association"] = get_text_or_none(By.ID, "dnn_ctr448_View_spnDenominazione")
            tmp["codice_fiscale"] = get_text_or_none(By.ID, "dnn_ctr448_View_spnCodiceFiscale")
            tmp["sezione"] = get_text_or_none(By.ID, "dnn_ctr448_View_spnSezione")
            tmp["forma_giuridica"] = get_text_or_none(By.ID, "dnn_ctr448_View_spnFormaGiuridica")
            tmp["email_pec"] = get_text_or_none(By.ID, "dnn_ctr448_View_spnEmailPEC") 
            tmp["provincia"] = get_text_or_none(By.ID, "dnn_ctr448_View_spnProvinciaSL")
            tmp["comune"] = get_text_or_none(By.ID, "dnn_ctr448_View_spnComuneSL")
            tmp["indirizzo"] = get_text_or_none(By.ID, "dnn_ctr448_View_spnIndirizzoSL")
            tmp["civico"] = get_text_or_none(By.ID, "dnn_ctr448_View_spnCivicoSL")
            tmp["cap"] = get_text_or_none(By.ID, "dnn_ctr448_View_spnCAP_SL")
            tmp["ente_non_commerciale"] = get_text_or_none(By.ID, "dnn_ctr448_View_spnEnteNonCommerciale")
            tmp["attivita"] = get_text_or_none(By.CLASS_NAME, "dashed")
            tmp["attivita_interesse_generale"] = get_text_or_none(By.XPATH, "//div[@id='dnn_ctr448_View_divAttivitaInteresseGenerale']/ul")
            tmp["n_lavoratori_subordinati"] = get_text_or_none(By.ID, "dnn_ctr448_View_spnLavoratoriSubordinati")
            tmp["n_volontari"] = get_text_or_none(By.ID, "dnn_ctr448_View_spnVolontari")
            tmp["n_volontari_enti_aderenti"] = get_text_or_none(By.ID, "dnn_ctr448_View_spnEntiAderenti")
            tmp["compagine_sociale"] = get_text_or_none(By.ID, "dnn_ctr448_View_spnSociPersonaFisica")
            
            #Div degli organi di amminstrazione
            organi_amministrazione = driver.find_elements(By.ID, "dnn_ctr448_View_divOrganiAffiliazioneProcedure")
            tmp["data_nomina_organo"] = None
            tmp["tipo_organo"] = None
            tmp["numero_componenti_organo"] = None
            if organi_amministrazione:  # Controlla se la lista non è vuota
                spans = organi_amministrazione[0].find_elements(By.TAG_NAME, "span")
                if len(spans) >= 7:  # Assicura che ci siano abbastanza elementi nella lista
                    tmp["data_nomina_organo"] = spans[2].text
                    tmp["tipo_organo"] = spans[4].text
                    tmp["numero_componenti_organo"] = spans[6].text

            #Non ho trovato un id univoco o classe univoca per riuscire a prendere i dati, la soluzione è la seguente.
            persona1_div = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//span[text()='Persona 1']/ancestor::div")))
            spans = persona1_div.find_elements(By.TAG_NAME, "span")
            try:
                index = next(i for i, span in enumerate(spans) if span.text == "Persona 1")
                tmp["codice_fiscale_rappresentante_legale"] = spans[index + 6].text
                tmp["nome_rappresentante_legale"] = spans[index + 8].text
                tmp["cognome_rappresentante_legale"] = spans[index + 10].text
            except StopIteration:
                # Se "Persona 1" non è presente, assegna valori vuoti o gestisci l'errore
                tmp["codice_fiscale_rappresentante_legale"] = ""
                tmp["nome_rappresentante_legale"] = ""
                tmp["cognome_rappresentante_legale"] = ""
            del spans
            associations.append(tmp)    
            
            time.sleep(1)
            driver.back()

        #Click del bottone successivo
        if k != (n_pages - 1):
            driver.execute_script(f"window.scrollTo(0, 850);")
            time.sleep(1)
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "dnn_ctr446_View_ltlProssimaPaginaBottom"))).click()
            driver.execute_script(f"window.scrollTo(0, 700);")
            time.sleep(1.5)
        
        print(f"Numero elementi copiati: {len(associations)}")
            
    #Salvataggio dati nel file csv
    filename = f"{comune.replace(" ", "_")}.csv"
    with open(filename, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=associations[0].keys())  
        
        # Scrive l'intestazione (nomi delle colonne)
        writer.writeheader()
        
        # Scrive i dati riga per riga
        writer.writerows(associations)
    print(f"File CSV '{filename}' salvato correttamente!")
    associations.clear()
    print(f"{datetime.now()} --- FINE procedura per comune: {comune} ")
    driver.quit()


