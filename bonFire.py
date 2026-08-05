import argparse
import os
import time
import random

parser = argparse.ArgumentParser(description="Onda maneira no terminal")
parser.add_argument("-u", "--digitos", default=' .:-=+*#%', help="Digitos que serão mostrados no fogo, de menor para maior temperatura.")
parser.add_argument("-c", "--cor", help='muda a cor do fogo (use hex, sem hashtag (#))')
parser.add_argument("-p", "--vazio", default=' ' ,help='Caractere usado na parte vazia')

args = parser.parse_args()

contador = 0

digitos = args.digitos
tempMaxima = len(digitos) - 1


tamanhoTerminal = {'x': os.get_terminal_size().columns, 'y': os.get_terminal_size().lines}

tela = []

# gerar tela
for i in range(tamanhoTerminal['y']):
    tela.append([])
    for j in range(tamanhoTerminal['x']):
        tela[i].append({'x': j, 'y': i, 'nivel': 0})

def hex_para_ansi(hex_code, texto):
  hex_code = hex_code.lstrip("#")
  r = int(hex_code[0:2], 16)
  g = int(hex_code[2:4], 16)
  b = int(hex_code[4:6], 16)
  return f"\033[38;2;{r};{g};{b}m{texto}\033[0m"
            
def printarTela():
    global tela

    os.system('cls' if os.name == 'nt' else 'clear')
    
    for i in range(tamanhoTerminal['y']):
        linha = ''
        for j in range(tamanhoTerminal['x']):
            linha += digitos[tela[i][j]['nivel']]
        if args.cor:
            print(hex_para_ansi(args.cor, linha))
        else:
            print(linha)

while True:

    for x in range(tamanhoTerminal['x']):
        tela[tamanhoTerminal['y'] - 1][x]['nivel'] = tempMaxima

    for y in range(tamanhoTerminal['y'] - 1):
        for x in range(tamanhoTerminal['x']):

            calor_baixo = tela[y + 1][x]['nivel']

            resfriamento = random.randint(0, 1)

            tela[y][x]['nivel'] = max(0, calor_baixo - resfriamento)

    printarTela()
    contador += 1
    time.sleep(0.1)
