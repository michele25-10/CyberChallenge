from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from Crypto.Signature import PKCS1_v1_5
from Crypto.Hash import SHA256

msg="Ciao sono alice, piacere di consocerti Bob!!".encode("utf-8")

#Genero mazzo di chiavi di Alice
key_alice = RSA.generate(2048)  
private_key_alice = key_alice.export_key()
public_key_alice = key_alice.publickey().export_key()

#Genero mazzo di chiavi di Bob
key_bob = RSA.generate(2048)
private_key_bob = key_bob.export_key()
public_key_bob = key_bob.publickey().export_key()

#Alice encrypt + signature del msg
cipher_alice = PKCS1_OAEP.new(key_bob)
msg_cifrato = cipher_alice.encrypt(msg)
hash_msg_cifrato = SHA256.new(msg_cifrato) 
msg_firmato = PKCS1_v1_5.new(key_alice).sign(hash_msg_cifrato)

print(f"Messaggio cifrato per BOB: \n{msg_cifrato.hex()}\n")
print(f"HASH SHA-256 messaggio cifrato per Bob: \n{hash_msg_cifrato.digest().hex()}\n")
print(f"Messaggio firmato per Bob: \n{msg_firmato.hex()}\n")

hash_msg_cifrato_bob = SHA256.new(msg_cifrato)
print(f"HASH SHA-256 calcolato da Bob: \n{hash_msg_cifrato_bob.digest().hex()}\n")

try:
    public_key_alice = RSA.import_key(public_key_alice)
    PKCS1_v1_5.new(public_key_alice).verify(hash_msg_cifrato_bob, msg_firmato)
    print("La firma del messaggio è valida, quindi è verificato che il mittente è Alice.\n")
except:
    print("La firma non è valida, non posso verificare che il mittente sia Alice.\n")

cipher_bob = PKCS1_OAEP.new(key_bob)
msg_decifrato = cipher_bob.decrypt(msg_cifrato)
print(f"Messaggio decifrato da Bob: \n{msg_decifrato.decode('utf-8')}")
