from random import randint
from time import sleep

tab =   [["-","-","-"],
        ["-","-","-"],
        ["-","-","-"]]

tabValor = {
    "linhas": [0,0,0],
    "colunas": [0,0,0],
    "diagonais": [0,0]
}

def mostrarTabuleiro():
    global tab
    for linha in tab:
        print( " ".join(linha))
            

def checarGanhador():
    if -3 in tabValor:
        print("bot ganhou")
        return True

    if 3 in tabValor:
        print("jogador ganhou")

    return False

while True:
    jogada = (int(x) for x in input("sua jogada: ").split())
    tab[jogada[0]][jogada[1]] = "x"
    
    tabValor["linhas"][jogada[0]] += 1
    
    match jogada[1]:
        0:
            tabValor[
        1:
            tabValor[0] += 1
            tabValor[4] += 1
            tabValor[6] += 1
        2:
            tabValor[0] 
    mostrarTabuleiro()
    print("fazendo a jogada...")
    sleep(1)
    jogadaBot = (randint(0,2),randint(0,2))
    while tab[jogadaBot[0]][jogadaBot[1]] == "x":
        jogadaBot = (randint(0,2),randint(0,2))

    tab[jogadaBot[0]][jogadaBot[1]] = "x"
    mostrarTabuleiro()

    if checarGanhador():
        break



    
