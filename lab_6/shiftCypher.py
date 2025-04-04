from pwn import remote

def caesar(s, k, decode = False):
	if decode: k = 26 - k
	return "".join([chr((ord(i) - 65 + k) % 26 + 65)
				for i in s.upper()
				if ord(i) >= 65 and ord(i) <= 90 ])

conn = remote("ctf.unife.it", 8003)
print(conn.recvline().decode())
print(conn.recvline().decode())
print(conn.recvline().decode())
print(conn.recvline().decode())
str = conn.recvline().decode()
print(str)

for i in range(1,27):
    new_string = caesar(str.upper(), i, decode = True)      
    print(f"Key[{i}]: {new_string}")
    conn.sendline(new_string.lower().encode("utf-8"))

second_string = "b ehox max lfxee hy yetzl bg max fhkgbgz lfxeel ebdx obvmhkr"
print(caesar(second_string.upper(), 19, decode=True))

flag = "wnlfufnmbczn"

for i in range(1,27):
    new_string = caesar(flag.upper(), i, decode = True)      
    print(f"Key[{i}]: {new_string}")