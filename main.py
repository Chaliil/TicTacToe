import os
import platform
import socket
import threading

#Socket Variablen
HEADER = 64
PORT = 5050
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"

#Globale Variablen
spielfeld = ["",
            "1", "2", "3",
            "4", "5", "6",
            "7", "8", "9",]

number = ""
symbol = ""
won = ""
player = ""

#set up Server and client Object
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

#Handle connections from Clients
def handle_client(conn, addr):
    print(f"{addr} connected to your game.")

    connected = True
    while connected:
        msg_length = conn.recv(HEADER).decode(FORMAT)
        if msg_length:
            msg_length = int(msg_length)
            msg = conn.recv(msg_length).decode(FORMAT)
            if msg == DISCONNECT_MESSAGE:
                connected = False

            print(f"[{addr}] {msg}")
            conn.send("Msg recieved".encode(format))
    
    conn.close()

#Start in Server Mode
def startserver():
    server.listen()
    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.daemon = True
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.activeCount() -1}")

#Sending Server Messages
def send(msg):
    message = msg.encode(FORMAT)
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' * (HEADER - len(send_length))
    server.send(send_length)
    server.send(message)
    print(server.recv(2048))

#Hosting Settings
def hosting():
    global SERVER
    while True:
        print("Do you want to be the host[1] or the client[2]")
        settings = input()
        if settings == "1":
            thread = threading.Thread(target=startserver)
            thread.daemon = True
            thread.start()
            print(f"New Game started on {SERVER}")
            print("Send this address to your friend to play together")
            break
        if settings == "2":
            print("Please enter a Server address")
            SERVER = input()
            break
        else:
            print("please enter a valid number")
    return SERVER

#Bildschirm leeren
def clear():
    if(platform.system() == "Windows"):
        os.system('cls')
    else:
        os.system('clear')

# Spielfeld ausgeben
def output (spielfeld = spielfeld):
    print (spielfeld[1] + " | " + spielfeld[2] + " | " + spielfeld[3] )
    print ("---------")
    print (spielfeld[4] + " | " + spielfeld[5] + " | " + spielfeld[6] )
    print ("---------")
    print (spielfeld[7] + " | " + spielfeld[8] + " | " + spielfeld[9] )

#Set x and O in spielfeld
def checknumber (number = number, symbol = symbol):
    print(number)
    print(symbol)
    global spielfeld 
    spielfeld = [feld.replace(number, symbol) for feld in spielfeld]
    return spielfeld

def checkwon():
    # wenn alle 3 Felder gleich sind, hat der entsprechende Spieler gewonnen
    # Kontrolle auf Reihen
    if spielfeld[1] == spielfeld[2] == spielfeld[3]:
        return spielfeld[1]
    if spielfeld[4] == spielfeld[5] == spielfeld[6]:
        return spielfeld[4]
    if spielfeld[7] == spielfeld[8] == spielfeld[9]:
        return spielfeld[7]
    # Kontrolle auf Spalten
    if spielfeld[1] == spielfeld[4] == spielfeld[7]:
        return spielfeld[1]
    if spielfeld[2] == spielfeld[5] == spielfeld[8]:
        return spielfeld[2]
    if spielfeld[3] == spielfeld[6] == spielfeld[9]:
        return spielfeld[3]
    # Kontrolle auf Diagonalen
    if spielfeld[1] == spielfeld[5] == spielfeld[9]:
        return spielfeld[5]
    if spielfeld[7] == spielfeld[5] == spielfeld[3]:
        return spielfeld[5]

#Gewinnmechanik
def winning():
    global won
    global player
    won = checkwon()
    tie = checktie()
    if(won):
        if(won == 'X'):
            player = player1
        if(won == 'O'):
            player = player2
    if(tie):
        player = "tie"

    return player

#Test for Tied
def checktie():
    if (spielfeld[1] == 'X' or spielfeld[1] == 'O') \
      and (spielfeld[2] == 'X' or spielfeld[2] == 'O') \
      and (spielfeld[3] == 'X' or spielfeld[3] == 'O') \
      and (spielfeld[4] == 'X' or spielfeld[4] == 'O') \
      and (spielfeld[5] == 'X' or spielfeld[5] == 'O') \
      and (spielfeld[6] == 'X' or spielfeld[6] == 'O') \
      and (spielfeld[7] == 'X' or spielfeld[7] == 'O') \
      and (spielfeld[8] == 'X' or spielfeld[8] == 'O') \
      and (spielfeld[9] == 'X' or spielfeld[9] == 'O'):
        return ('tie')

#Multiplayer Settings
while True:
    print("Do you want to play locally[1] or online[2]")
    settings = input()
    if settings == "1":
        break
    if settings == "2":
        hosting()
        break
    else:
        print("please enter a valid number")

#Festlegen der Spieler
print("Who is Player one?")
player1 = input()

print("Who is Player two?")
player2 = input()

#Spielmechanik lokal
while(True):
    clear()
    output(spielfeld)
    print()
    print(player1 + ' ist an der Reihe:')
    print("gib eine im Spielfeld gezeigte Zahl ein:")
    symbol = 'X'
    number = input()
    checknumber(number, symbol)
    
    send(spielfeld)

    winning()
    if winning():
        break

    clear()
    output(spielfeld)
    print()
    print(player2 + ' ist an der Reihe:')
    print("gib eine im Spielfeld gezeigte Zahl ein:")
    symbol = 'O'
    number = input()
    checknumber(number, symbol)
    output(spielfeld)

    send(spielfeld)

    winning()
    if winning():
        break

#Spielende
clear()
print()
output(spielfeld)
print()

if(player == 'tie'):
    print ('unentschieden')
else:
    print (player + " hat gewonnen!!!")

print("spiel beendet, danke f??rs mitspielen")