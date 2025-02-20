# Dispositivi di sicurezza delle reti

### Router

Il border router è la parte più vulnerabile della nostra rete.
Tutte le richieste di uscita passano da lui.
E' fondamentale proteggerlo adeguatamente.
Stateless filtering viene usato in questo caso (filtra IP e porte), in compenso è molto efficiente.
I parametri di filtraggio del traffico:

- MAC
- IP (srg, dst, protocol, flags)
- TCP/UDP (srg_port, dst_port, flags TCP)

### Firewall

Si interpone tra la rete interne ed esterna, definisce quale traffico può passare attraverso una serie di regole.
Consente di fare logging e di gestirlo di conseguenza.
Può eseguire funzioni come NAT e forwarding (tra vlan) può funzionare come proxy.
Se viene eseguito il Content filtering essendo più pesante come controllo vengono eseguiti i controlli in un "canale" distinto (granularità)
Così facendo solo il traffico autorizzato può entrare o uscire dalla rete.
Le politiche di sicurezza così facendo sono centralizzate.
Ovviamente se tutto il traffico passa dal firewall significa che ne risentono le performance (collo di bottiglia) ed aumenta il grado di complessità della rete.
Il firewall può operare in due modi

- Routed --> Operazioni a livello 3, segmenta la rete, IP di un firewall configurato come default gateway dalla sottorete
- Transparent --> Operazioni a livello 2, non segmenta la rete, (l'IP del firewall non deve essere configurato in mod. default gateway).

Usare un firewall diminuisce il carico di lavoro dovuto al filtraggio sulle CPU degli altri dispositivi di rete (es. Router).

Stateful filtering:

- Tiene in considerazione anche la sessione (id sessione, handshake, ip, porte).

### Come scrivere le ACL

Il traffico è considerato in ingresso e in uscita.

- Chi può accedere a queste informazioni?
- Quando è possibile accedere?
- Da dove è possibile accedere?

Le policy sono:

- Deny all: Nulla può passare quello che può passare è scritto nelle regole.
- Allow all: Passa tutto eccetto quello che dico che non può passare.

Content filtering (filtra il traffico anche in base a livello applicativo):

- Un esempio sono le reti delle scuole che bloccano determinati URL (social media, gioco d'azzardo, contenuti particolari...)...

_N.B_: E' importante l'ordine delle regole, vengono passate in ordine dalla prima all'ultima quindi le prime regole sono quelle che contano maggiormente. Importante in caso di contraddizioni nelle regole.

Le ACL vanno applicate il più vicino possibile ai dispositivi riguardanti.

## IP address Spoofing:

L'attaccante modifica il proprio indirizzo IP e si finge qualcun'altro.
Molto semplice sopprattutto modificando l'ip sorgente di un pacchetto.
Per proteggersi basta dire che tutto il traffico in entrata sull'interfaccia del router non può avere come IP sorgente un indirizzo della mia rete. E viceversa per il traffico interno non può avere un ip esterno, significa che è stato manipolato il traffico.

# Docker

Docker è un sw per la virtualizzazione.
La virtualizzazione consente di far girare sistemi operativi diversi sopra la stessa macchina attraverso all'hypervisor.
La virtualizzazione serve ad isolare le proprie applicazioni e a rendere scalabile la nostra architettura.
I container permettono di isolare e virtualizzare le applicazioni ma usando lo stesso SO sottostante evitando così le ridondanze.
Le immagini sono template di container già preconfigurati con dipendenze già installati e immutabili oppure create da noi.
I container sono associati a delle immagini crendo dei layer con alcune politiche di ottimizzazione (https://nicogaspa.medium.com/introduzione-a-docker-d61f2b46d84c).

I container hanno un loro ciclo di vita:

- Created
- Running
- Stopped
- Removed

Necessito di un Dockerfile per definire una immagine custom, creata effettivamente attraverso un docker build.
I volumi servono per mappare la cartella di un nostro host all'interno del nostro container.

# Docker networking

Un container può essere in modalità:

- Bridge: può accedere all'esterno solamente attraverso l'host (con una NAT), in questo modo è più isolato.
- HOST: esce effettivamente come se fosse un host (senza passare per esso attraverso una NAT).

# Docker compose

Ci sono tanti Dockerfile e troviamo un docker-compose.yaml che crea le istanze di questi container tutti in una volta sola.
