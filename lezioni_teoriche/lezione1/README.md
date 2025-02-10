# Pila ISO/OSI

Classiche cose che ormai si sanno a memoria tra superiori e università.

# Pila TCP/IP

Classiche cose che ormai si sanno a memoria tra superiori e università.

### Protocol Data Unit --> incapsulmaneto

# Ethernet

Incapsula dati all'interno di un frame, i suoi indirizzi sono di tipo mac (Scheda di rete).
I bridge e switch operano al livello 2 della pila ISO/OSI.
Lo switch per far comunicare i dispositivi tra loro usa la MAC address table (popola questa tabella attraverso il protocollo ARP).

# IP

Indirizzo logico IP:

- IPv4 --> 32 bit
- IPv6 --> 128 bit

I router per effettuare gli instradamenti dei pacchetti utilizzano appunto il protocollo IP e le routing table. Un indirizzo IP ha
l'identificativo dell'host e il suo indirizzo di rete identificabile attraverso una AND con la netmask.
Da ricordare le classi per indirizzi IPv4: A, B, C (più importanti) ognuna delle quali ha un gruppo di indirizzi privati.

# TCP e UDP

TCP sicuro con certezza dell'arrivo del pacchetto a destinazione.
UDP meno sicuro ma più performante utile per streaming audio e video.
Questi protocolli associano l'indirizzo ip ad una porta per accedere un servizio (socket)

# NAT (Network Address Translation)

Consente ad un IP privato di uscire dalla rete privata sotto un unico indirizzo pubblico (quello dell'interfaccia di uscita del nostro router).
Tutte le informazioni necessarie sono contenute all'interno della NAT Table.

# HTTP Hypertext Transfer Protocol

Porta 80

- HTTP request --> method, path, headers, body
- HTTP response --> status code, status message, headers, body

Richiesta HTTP viene fatta ad uno URL (ci dice dove è la risorsa).
Porta tipicamente

# Network analysis And monitoring tools

## Dominio

Suddivisione di dispositivi in domini di sicurezza.
Un dominio sono un insieme di dispositivi aventi privilegi e funzionalità simili.

## DMZ

Zona demilitarizzata: Esterna alla rete (DB, server...)

## Firewall

Un insieme di regole per far fluire o bloccare il traffico specializzato su protocollo e numero di porta.

## Sniffer

Acquisisce tutto il traffico a livello data-link, legge tutti i pacchetti in transito.
Dispositivo che acquisisce tutto il traffico a livello data-link, legge tutti i pacchetti in transito.
Se non rispetta una serie di regole viene segnalato come malevolo.

Funzionalità:

- Automatic Network Analysis
- Anomaly analysis
- Performance Analysis
- Detection of Network Intrusion
- Recording of Network Traffic

Tcpdump viene usato in linux per sniffare il traffico una sorta di wireshark da terminale.
