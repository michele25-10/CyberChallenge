import pyshark
import jwt

cap = pyshark.FileCapture('jwt.pcap', display_filter="http")

count = 0
for pkt in cap:
    count += 1
    try:
    #Controllo se esiste pkt.http.authorization --> pkt?.http?.authorization
        if hasattr(pkt, 'http'):
            if hasattr(pkt.http, 'authorization'):
                token = pkt.http.authorization.replace("Bearer ", "")
                decode_token = jwt.decode(token, options={"verify_signature": False})
                exp_timestamp = decode_token.get("exp", None)

                #Verifico se questo token è quello valido
                if int(exp_timestamp) == int(1654080761): 
                    flag = decode_token.get("flag", None)
                    print(f"Token trovato: {token}")
                    print(f"La flag di questo esercizio è: {flag}")
                    break
    except Exception as e:
        print(f"Errore nell'analisi del pacchetto: {e}")
    
    print(f"pkt: {count}")

