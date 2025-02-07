import pwn

conn = pwn.remote("localhost", 54321)

while True:
    cmd = input("Inserisci il comando: ")
    conn.send(cmd.encode('utf-8'))
    result = conn.recv().decode('utf-8')
    print(result)

