# Access Control Theory

## Access Control

La priorità di ogni sistema è quella di proteggere i dati e le risorse da:

- accessi non autorizzati
- modifiche non autorizzate
  L'access control si interpone quindi tra il sistema e l'utente malintenzionato.
  Una entità attiva accede a una risorsa con una operazione specifica mentre un monitor di riferimento concede o nega l'accesso a quest'ultima.

I tre pilastri sono (AAA):

- Authentication -> verifica l'identità dell'utente
- Authorization -> funzione che specifica i privilegi di una risorsa o un dato
- Accounting -> raccolta di log sugli eventi scatenati

## Access Matrix

Le security policy determinano l'insieme di regole adottate per determinare chi può accedere a quale risorsa.
Ce ne sono di diversi tipi:

- Discretionary (DAC) -> Accesso consentito o meno basato sull'identità dell'utente (un utente può o non può aprire una risorsa)
- Mandatory (MAC) -> confronto tra etichette di sicurezza (che indicano quanto sono sensibili o critiche le risorse di sistema) e autorizzazioni di sicurezza (che indicano se le entità di sistema sono idonee ad accedere a determinate risorse)
- Role-based (RBAC) -> dipende dal ruolo che l'utente ha nel sistema e può fare determinate azioni
- Attribute-based (ABAC) -> controllano l'accesso in base agli attributi dell'utente, alla risorsa a cui accedere e alle condizioni ambientali correnti, nonché alle regole di accesso

La capabilities di un soggetto enumera l'elenco delle risorse accessibili al soggetto. Ogni voce identifica un oggetto
insieme dei diritti di accesso conferiti al soggetto per quella risorsa. Le capacità corrispondono alle righe di una matrice di accesso.

> Esempio
>
> Alice -> FILE1(read, write) -> FILE2(read)
>
> Bob -> FILE1(read) -> FILE2(exec)

Le ACL sono comunemente usate per realizzare una access matrix, una struttura dati che associa a una risorsa una lista di soggetti assieme ai loro permessi
| File1 | File2 |
|------------------------------|------------------------------|
| Alice(read, write) -> Bob(read) | Alice(read) -> Bob(exec) |

ACL vs Capabilities:

- ACL:

  - Utilizzare elenchi per esprimere la vista di ogni oggetto o: la voce i-esima nell'elenco fornisce il nome di un soggetto si e i diritti in M(si, o) della matrice di accesso
  - Il proprietario ha l'autorità esclusiva di concedere, revocare o diminuire i diritti di accesso a F ad altri utenti.
  - Gli ACL sono utilizzati nel sistema operativo UNIX/Linux.

- Capabilities Lists:

  - Non compatibile con la visualizzazione orientata agli oggetti
  - Difficile ottenere una panoramica di chi ha i permessi su un oggetto.
  - Difficile revocare una capacità.
  - Utilizzato in un ambiente distribuito (ad esempio, agente mobile): gli utenti sono dotati di credenziali (ad esempio, da un
    server di credenziali) che presentano agli oggetti di rete.

## Assegnazione dei permessi

- Discretionary Access Control (DAC): per soggetto stesso(permessi settati dall'owner).
  - alta flessibilità e i permessi possono essere trasferiti
  - Difficili le revoche a causa della mancanza di un controllo centrale
- Mandatory Access Control (MAC): dall'autorità centrale.
  - La soluzione migliore per organizzazioni
  - Bassa flessibilità ed alti costi di gestione.

# Unix File permission

## Principals and Subjects

Un subject è un programma eseguito per conto di alcuni principali e operante sulle risorse di sistema (object).
Un principals può in qualsiasi momento essere inattivo o avere uno o più soggetti associati.

Principals sono users (username e UID) e groups (group name e GID).

Superuser è un utente con speciali privilegi con UID 0 (username spesso root). Il superuser può diventare qualsiasi altro utente.
Tutti i controlli di sicurezza sonon spenti con lui, ma non possiamo scrivere su un filesystem montato come in sola lettura e non possiamo leggere le password.

In linux i subjects sono i processi.
Ogni processo è associato a:

- un UID/GID reale (ruid/rgid): l'UID reale è ereditato dal processo padre. In genere è l'UID dell'utente che ha avviato il processo.
- un UID/GID effettivo (euid/egid): l'UID effettivo è ereditato dal processo padre o dal file in esecuzione. Questo UID è utilizzato per concedere diritti di accesso a un processo.
- un UID/GID salvato: questo consente a un processo di passare dall'UID effettivo all'UID reale e viceversa.

Linux objects sono i permessi legati ad un file (12 bit di permessi e 9 bit di protezione) sono del tipo rwx.
Solo il proprietario può cambiare i bit di permessi, solo il superuser può cambiare i permessi del proprietario.

Access control usa UID/GID:

- se il processo di UID è proprietario del file controlla i bit di permesso del proprietario.
- se il processo UID non è il prprietario del file controllo se lo è il gruppo (GID)
- se il processo UID e GID non sono i proprietari del file controllo others permissions.

# Weaknesses

## Confused Deputy

Esempio:
Un programma fornisce servizi di compilazione ad altri programmi Il servizio del compilatore è a pagamento: il servizio del compilatore memorizza le informazioni di fatturazione in un file BILL. Solo il programma ha accesso a BILL.

I client possono compilare e impostare il nome del file di output Un client dannoso chiama l'output BILL I client non possono aprire BILL, ma il programma può. Il programma sovrascrive il file BILL con l'output di compilazione.

Protezione contro Confused Deputy -> I sistemi basati sulla lista di controllo degli accessi sono inefficaci

I programmi Open SetUID consentono agli utenti di eseguirli come proprietari. Se il programma è vulnerabile, gli utenti possono eseguire comandi arbitrari come proprietari. Il programma dovrebbe offrire solo le capacità giuste.
Ad esempio, eseguire solo comandi predefiniti

## Race Conditions

In situazioni di programmazione concorrente può capitare che due thread distiniti scrivano contemporaneamente su una stessa risorsa.
Chiamate di sistemi per consentire accesso mutualmente esclusivo.

TOCTOU
Come posso modificare un file? "Ottieni percorso file" è già stato superato. Crea un collegamento simbolico a un file valido A. Fai in modo che il programma legga il percorso del collegamento simbolico. Modifica il collegamento simbolico in modo che punti al file B. Il programma restituisce il contenuto del file B
