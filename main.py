import os
import platform

#Globale Variablen
spielfeld = ["",
            "1", "2", "3",
            "4", "5", "6",
            "7", "8", "9",]

number = ""
symbol = ""
won = ""

#Bildschirm leeren
def clear():
    ostype = platform.system()
    print("ostype")
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
    if(won):
        if(won == 'X'):
            player = player1
        if(won == 'O'):
            player = player2
    return player

#Festlegen der Spieler
print("Who is Player one?")
player1 = input()

print("Who is Player two?")
player2 = input()

#Spielmechanik
while(True):

    clear()
    output(spielfeld)
    print()
    print(player1 + ' ist an der Reihe:')
    print("gib eine im Spielfeld gezeigte Zahl ein:")
    symbol = 'X'
    number = input()
    checknumber(number, symbol)

    won = checkwon()
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

    won = checkwon()
    winning()
    if winning():
        break

#Spielende
clear()
print()
output(spielfeld)
print()
print (player + " hat gewonnen!!!")
print("spiel beendet, danke fürs mitspielen")