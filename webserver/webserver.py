import socket

def response(name = "world"):
    return bytes(f"""HTTP/1.1 200 OK
Server: 4KT | OTF
Content-Type: text/html
Connection: Closed

<html>
<body>
<h1>Hello {name}</h1>
</body>
</html>
""",
"utf-8")

def exiting():
    return bytes(f"""HTTP/1.1 200 OK
Server: 4KT | OTF
Content-Type: text/html
Connection: Closed

<html>
<body>
<h1>Exiting</h1>
</body>
</html>
""",
"utf-8")

addr = ("127.0.0.1", 27015)

s = socket.create_server(addr)

s.listen()

while True:
    conn,addr =  s.accept()
    req = conn.recv(1000).decode()
    a = req.split("\n")[0].split(' ')[1]
    if a == "/quit":

        conn.close()
        break
    else:
        if a == "/":
            conn.send(response())
        conn.send(response(a[1:]))
            
    conn.close()
    

