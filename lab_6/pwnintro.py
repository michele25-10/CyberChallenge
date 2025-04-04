from pwn import remote

conn = remote("ctf.unife.it", 8001)
print(conn.recvline().decode())
number = int(conn.recvline().decode().split(" ")[1])
print(f"Numero di volte: {number}")
print(conn.recvline().decode())

for i in range(number):
    operation = conn.recvline().decode().split("=")[0]
    #print(f"{operation} = {eval(operation)}" )
    conn.sendline(f"{eval(operation)}".encode("utf-8"))
    print(conn.recvline().decode())

print(conn.recvline().decode())