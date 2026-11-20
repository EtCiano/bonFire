import argparse
import os
import shutil
import subprocess
import time
import random
from rgb_gradient_custom import get_linear_gradient

parser = argparse.ArgumentParser(description="Fogo no terminal")
parser.add_argument("-u", "--digitos", default=' ._,;:!>^*#$&8%@', help="Digitos que serão mostrados no fogo, de menor para maior temperatura.")
parser.add_argument("-c", "--cor", help='muda a cor do fogo (use hex)')
parser.add_argument('-g', '--gradiente', help='adiciona gradiente no fogo (coloque as cores em hex, separadas por espaço)')

args = parser.parse_args()

digitos = args.digitos
tempMaxima = len(digitos) - 1

gradiente = []

if args.gradiente:
    coresIniciais = [f'#{cor.lstrip("#")}' for cor in args.gradiente.split()]
    total_cores = max(tempMaxima + 1, len(coresIniciais))
    gradiente = get_linear_gradient(colors=coresIniciais, nb_colors=total_cores, return_format='hex')


def tamanho_atual():
    t = shutil.get_terminal_size()
    return t.columns, t.lines


def limpar():
    subprocess.run(['cls' if os.name == 'nt' else 'clear'], shell=True)


def hex_para_ansi(hex_code, texto):
    hex_code = hex_code.lstrip("#")
    r = int(hex_code[0:2], 16)
    g = int(hex_code[2:4], 16)
    b = int(hex_code[4:6], 16)
    return f"\033[38;2;{r};{g};{b}m{texto}\033[0m"


def printarTela(tela, colunas, linhas):
    limpar()

    for i in range(linhas):
        linha = ''
        for j in range(colunas):
            nivel = tela[i][j]

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


colunas, linhas = 0, 0
tela = []
peso_sem_resfriar = 0

while True:
    novas_colunas, novas_linhas = tamanho_atual()

    # terminal mudou de tamanho: recria a tela e recalcula tudo que depende dele
    if (novas_colunas, novas_linhas) != (colunas, linhas):
        colunas, linhas = novas_colunas, novas_linhas
        tela = [[0] * colunas for _ in range(linhas)]
        proporcao = 4 / (16 ** (linhas / 63))
        peso_sem_resfriar = colunas / (proporcao * len(digitos) * 18)
        limpar()

    for x in range(colunas):
        tela[linhas - 1][x] = tempMaxima

    for y in range(linhas - 1):
        for x in range(colunas):
            calor_baixo = tela[y + 1][x]
            resfriamento = random.choices([0, 1], weights=[peso_sem_resfriar, 1], k=1)[0]
            tela[y][x] = max(0, calor_baixo - resfriamento)

    printarTela(tela, colunas, linhas)
    time.sleep(0.1)