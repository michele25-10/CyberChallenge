import time
import csv
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import ElementClickInterceptedException

#Funzione per ottenere i dati dalla pagina che viene aperta:
def get_text_or_none(by, value):
    try:
        return WebDriverWait(driver, 5).until(EC.presence_of_element_located((by, value))).text
    except:
        return None
    
def extract_rappresentante_legale():
    """Estrae i dati del rappresentante legale con gestione degli errori"""
    try:
        # Prima prova a trovare "Persona 1"
        persona1_div = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.XPATH, "//span[text()='Persona 1']/ancestor::div"))
        )
        spans = persona1_div.find_elements(By.TAG_NAME, "span")
        
        # Trova l'indice di "Persona 1"
        index = next(i for i, span in enumerate(spans) if span.text.strip() == "Persona 1")
        
        # Estrai i dati (con controlli di sicurezza)
        cf = spans[index + 6].text.strip() if len(spans) > index + 6 else ""
        nome = spans[index + 8].text.strip() if len(spans) > index + 8 else ""
        cognome = spans[index + 10].text.strip() if len(spans) > index + 10 else ""
        
        return cf, nome, cognome
        
    except TimeoutException:
        print("Elemento 'Persona 1' non trovato - potrebbe non esserci un rappresentante legale")
        
        # Prova con selettori alternativi più generici
        try:
            # Cerca div che contengono informazioni su persone
            person_divs = driver.find_elements(By.XPATH, "//div[contains(@class, 'person') or contains(text(), 'Codice Fiscale')]")
            
            if person_divs:
                # Analizza il primo div trovato
                spans = person_divs[0].find_elements(By.TAG_NAME, "span")
                print(f"Trovato div alternativo con {len(spans)} span")
                
                # Cerca pattern comuni per codice fiscale, nome, cognome
                cf, nome, cognome = "", "", ""
                
                for i, span in enumerate(spans):
                    text = span.text.strip().upper()
                    # Pattern per codice fiscale (16 caratteri alfanumerici)
                    if len(text) == 16 and text.isalnum():
                        cf = text
                    # Pattern per nome/cognome (cerca etichette)
                    elif text in ["NOME:", "COGNOME:"] and i + 1 < len(spans):
                        if text == "NOME:":
                            nome = spans[i + 1].text.strip()
                        elif text == "COGNOME:":
                            cognome = spans[i + 1].text.strip()
                
                return cf, nome, cognome
            
        except Exception as e:
            print(f"Errore nella ricerca alternativa: {e}")
        
        return "", "", ""
        
    except StopIteration:
        print("Testo 'Persona 1' non trovato negli span")
        return "", "", ""
        
    except Exception as e:
        print(f"Errore imprevisto nell'estrazione rappresentante legale: {e}")
        return "", "", ""


def click_button_with_retry(button_id, max_attempts=3):
                for attempt in range(max_attempts):
                    try:
                        # Scroll per assicurarsi che l'elemento sia visibile
                        element = WebDriverWait(driver, 10).until(
                            EC.presence_of_element_located((By.ID, button_id))
                        )
                        #driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)
                        time.sleep(0.5)  # Pausa breve dopo lo scroll
                        
                        # Attendi che sia cliccabile e fai click
                        WebDriverWait(driver, 10).until(
                            EC.element_to_be_clickable((By.ID, button_id))
                        ).click()
                        
                        return True  # Click riuscito
                        
                    except TimeoutException:
                        print(f"Tentativo {attempt + 1}: Bottone {button_id} non trovato o non cliccabile. Uscita dal ciclo.")
                        return False  # Elemento non trovato, esci dal ciclo principale
                        
                    except ElementClickInterceptedException:
                        print(f"Tentativo {attempt + 1}: Elemento {button_id} coperto. Riprovo...")
                        # Scroll più aggressivo
                        #driver.execute_script("window.scrollTo(0, document.body.scrollHeight * 0.4);")
                        time.sleep(1)
                        # Se è l'ultimo tentativo, proviamo JavaScript click
                        if attempt == max_attempts - 1:
                            try:
                                element = driver.find_element(By.ID, button_id)
                                driver.execute_script("arguments[0].click();", element)
                                print(f"Click JavaScript riuscito per {button_id}")
                                return True
                            except Exception as e:
                                print(f"Anche il click JavaScript è fallito per {button_id}: {e}")
                                continue  # Salta questo elemento
                                
                    except Exception as e:
                        print(f"Tentativo {attempt + 1}: Errore imprevisto per {button_id}: {e}")
                        time.sleep(1)
                
                print(f"Tutti i tentativi falliti per {button_id}. Salto questo elemento.")
                return None  # Indica che dobbiamo saltare questo elemento
            


#lista con tutti i dati delle associazioni e comuni da cui minare i dati
associations = []
comuni = [
    #"Padova",
    "Santa Caterina d'Este", 
]

for comune in comuni:
    # Apri il browser abilitando impostazione che non rilevi i bot
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--log-level=3") 
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
            
            # Usa la funzione con retry
            click_result = click_button_with_retry(id_button)
            
            if click_result is False:
                # Elemento non trovato, probabilmente siamo all'ultima pagina
                print(f"Bottone {id_button} non trovato. Fine degli elementi in questa pagina.")
                break
            elif click_result is None:
                # Elemento trovato ma non cliccabile, salta e continua con il prossimo
                print(f"Salto l'elemento {id_button} e continuo con il prossimo.")
                continue
            
            tmp = {}
            #Prelevto i dati dalla pagina dell'associazione
            tmp["name_association"] = get_text_or_none(By.ID, "dnn_ctr448_View_spnDenominazione")
            tmp["codice_fiscale"] = get_text_or_none(By.ID, "dnn_ctr448_View_spnCodiceFiscale")
            tmp["sezione"] = get_text_or_none(By.ID, "dnn_ctr448_View_spnSezione")
            tmp["atto_costitutivo"] = get_text_or_none(By.ID, "dnn_ctr448_View_spnAttoCostitutivo")
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
            tmp["cinque_per_mille"] = get_text_or_none(By.ID, "dnn_ctr448_View_spnCinquePerMille")
            
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
            try:
                cf, nome, cognome = extract_rappresentante_legale()
                tmp["codice_fiscale_rappresentante_legale"] = cf
                tmp["nome_rappresentante_legale"] = nome
                tmp["cognome_rappresentante_legale"] = cognome
                
            except Exception as e:
                print(f"Errore critico nell'estrazione rappresentante legale: {e}")
                tmp["codice_fiscale_rappresentante_legale"] = ""
                tmp["nome_rappresentante_legale"] = ""
                tmp["cognome_rappresentante_legale"] = ""
            associations.append(tmp)    
            
            driver.back()

        #Click del bottone successivo
        if k != (n_pages - 1):
            driver.execute_script(f"window.scrollTo(0, 850);")
            time.sleep(1)
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "dnn_ctr446_View_ltlProssimaPaginaBottom"))).click()
            time.sleep(1)
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


