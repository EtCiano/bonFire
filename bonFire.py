import argparse
import os
import time
import random
from rgb_gradient import get_linear_gradient

parser = argparse.ArgumentParser(description="Onda maneira no terminal")
parser.add_argument("-u", "--digitos", default=' ._,;:!>^*#$&8%@', help="Digitos que serão mostrados no fogo, de menor para maior temperatura.")
parser.add_argument("-c", "--cor", help='muda a cor do fogo (use hex)')
# parser.add_argument("-p", "--vazio", default=' ' ,help='Caractere usado na parte vazia')
parser.add_argument("-P", '--proporcao', type=int, default=50, help='proporção da tela ocupada pelo fogo, padrão é 75')
parser.add_argument('-g', '--gradiente', help='adiciona gradiente no fogo (coloque as cores em hex, separadas por espaço)')

args = parser.parse_args()

contador = 0

tamanhoTerminal = {'x': os.get_terminal_size().columns, 'y': os.get_terminal_size().lines}

proporcao = 4/(16**(tamanhoTerminal['y']/63))

digitos = args.digitos
tempMaxima = len(digitos) - 1

tela = []

gradiente = []

if args.gradiente:
    coresIniciais = [f'#{cor.lstrip("#")}' for cor in args.gradiente.split()]
    
    total_cores = max(tempMaxima + 1, len(coresIniciais))
    
    gradiente = get_linear_gradient(colors=coresIniciais, nb_colors=total_cores, return_format='hex')


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
            nivel = tela[i][j]['nivel']
            
            if gradiente:
                if nivel == 0:
                    linha += digitos[nivel]
                else:
                    cor_hex = gradiente[min(nivel, len(gradiente) - 1)]
                    linha += hex_para_ansi(cor_hex, digitos[nivel])
            else:
                linha += digitos[nivel]
                
        if args.cor and not gradiente:
            print(hex_para_ansi(args.cor, linha))
        else:
            print(linha)

while True:

    for x in range(tamanhoTerminal['x']):
        tela[tamanhoTerminal['y'] - 1][x]['nivel'] = tempMaxima

    for y in range(tamanhoTerminal['y'] - 1):
        for x in range(tamanhoTerminal['x']):

            calor_baixo = tela[y + 1][x]['nivel']

            resfriamento = random.choices([0, 1], weights=[tamanhoTerminal['x']/(proporcao*len(digitos)*18), 1], k=1)[0]

            tela[y][x]['nivel'] = max(0, calor_baixo - resfriamento)

    printarTela()
    contador += 1
    time.sleep(0.1)
