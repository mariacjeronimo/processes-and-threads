import sys
__author__ = "Maria Jerónimo, nº56887 e Tânia Araújo, nº56959"


def binario_to_ascii(ficheiro):
    """Funcão que recebe um ficheiro em binário, traduz para UTF-8 e imprime-o
    Args:
        ficheiro (file): ficheiro em binário
    """
    with open(ficheiro, "rb") as f:
            for linha in f:
                sys.stdout.write(''.join(chr(int(linha[i*8:i*8+8],2)) for i in range(len(linha)//8)) + '\n')

if __name__ == '__main__':
    for i in range(len(sys.argv)):
        if sys.argv[i] == 'hpgrepwc.py':
            ficheiro = sys.argv[i+1]
    binario_to_ascii(ficheiro)