#!/usr/bin/env python
# -*- coding: utf-8 -*-

from processador import Mips
from time import sleep
import sys
"""
    Simula execução das instruções de um programa no processador Mips
    multicilo.

    Inicializa um processador MIPS, e executa as instruções de um arquivo
    respeitando seus ciclos para cada etapa(IF, ID, EX, MEM, WR)
    Um tempo de parada entre cada ciclo pode ser definido para melhorar
    a visualização de cada ciclo.
    Para executar o programa digite no seguinte formato:
    python main.py nomedoarquivo.bin [tempo_parada]
"""


def main():
    if len(sys.argv) < 2:
        print 'Para executar o programa digite no seguinte formato:\n'\
            'python main.py nomedoarquivo.bin [tempo_parada]'
        sys.exit()
    ciclo = int(sys.argv[2]) if len(sys.argv) == 3 else 1
    try:
        with open(sys.argv[1]) as arquivo:
            instrucoes = [linha.strip(' \r\n')
                          for linha in arquivo.readlines()]
        # intancia o processador
        processador = Mips(instrucoes)
        while True:
            processador.IF()
            sleep(ciclo)
            processador.ID()
            sleep(ciclo)
            processador.EX()
            sleep(ciclo)
            if (processador.control_unit.memread == '1' or
                    processador.control_unit.memwrite == '1'):
                processador.MEM()
                sleep(ciclo)

            if processador.control_unit.regwrite == '1':
                processador.WR()
                sleep(ciclo)

    except IOError:
        print 'Arquivo não encontrado!'

    return 0

if __name__ == '__main__':
    main()
