#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
    Interpretador de instruções MIPS.
    Limitado às instruções:
        Aritméticas e Lógicas:
            add, sub, addi, and, or, nor, mult
        Transferência de dados:
            lw, sw, lb, sb
        Desvio Condicional:
            b eq, bne, slt
        Desvio Incondicional:
            jump, jal, jr
'''
import sys

# Tabela de opcode das intruções
opcode = {
    'lw': '100011',
    'sw': '101011',
    'lb': '100000',
    'sb': '101000',
    'beq': '000100',
    'bne': '000101',
    'slt': '000000',
    'j': '000010',
    'jal': '000011',
    'jr': '000000'
}
# Mapeamento dos registradores
reg = {
    '$zero': '00000',
    '$at': '00001',
    '$v0': '00010',
    '$v1': '00011',
    '$a0': '00100',
    '$a1': '00101',
    '$a2': '00110',
    '$a3': '00111',
    '$t0': '01000',
    '$t1': '01001',
    '$t2': '01010',
    '$t3': '01011',
    '$t4': '01100',
    '$t5': '01101',
    '$t6': '01110',
    '$t7': '01111',
    '$s0': '10000',
    '$s1': '10001',
    '$s2': '10010',
    '$s3': '10011',
    '$s4': '10100',
    '$s5': '10101',
    '$s6': '10110',
    '$s7': '10111',
    '$t8': '11000',
    '$t9': '11001',
    '$gp': '11100',
    '$sp': '11101',
    '$fp': '11110',
    '$ra': '11111',
    '$0': '00000',
    '$1': '00001',
    '$2': '00010',
    '$3': '00011',
    '$4': '00100',
    '$5': '00101',
    '$6': '00110',
    '$7': '00111',
    '$8': '01000',
    '$9': '01001',
    '$10': '01010',
    '$11': '01011',
    '$12': '01100',
    '$13': '01101',
    '$14': '01110',
    '$15': '01111',
    '$16': '10000',
    '$17': '10001',
    '$18': '10010',
    '$19': '10011',
    '$20': '10100',
    '$21': '10101',
    '$22': '10110',
    '$23': '10111',
    '$24': '11000',
    '$25': '11001',
    '$28': '11100',
    '$29': '11101',
    '$30': '11110',
    '$31': '11111'
}

# Tabela de valores para funct
funct = {
    'add': '100000',
    'addi': '001000',
    'sub': '100010',
    'and': '100100',
    'or': '100101',
    'nor': '100111',
    'mult': '011000',
    'slt': '101010',
    'jr': '001000'
}

# Separação de instruções por tipo
logicas_aritmeticas = ('add', 'addi', 'sub', 'and', 'or', 'nor', 'mult')
transferencia_dados = ('lb', 'sb', 'lw', 'sw')
desvio_condicional = ('beq', 'bne', 'slt')
desvio_incondicional = ('j', 'jal', 'jr')


def calc_imediato(string):
    '''Função para cálculo de valor imediato em binário.

       Recebe como parâmetro uma string com valor numérico que será
       convertido para inteiro e transformado em binário levando
       em consideração o bit de sinal.
    '''
    binario = int(string)
    if binario > 32766 or binario < -32767:
        raise ValueError()
    if binario >= 0:
        binario = bin(binario)[2:]
        binario = binario.zfill(16)
    else:
        binario = bin(binario)[3:]
        binario = '1' + binario.zfill(15)
    return binario


def calc_endereco(string):
    '''Função para cálculo de valor de endereço em binário.

       Recebe como parâmetro uma string com valor numérico que será
       convertido para inteiro e transformado em binário levando
       em consideração o bit de sinal.
    '''
    binario = int(string)
    if binario < 0 or binario > 67108863:
        raise ValueError()
    binario = bin(binario)[2:]
    binario = binario.zfill(26)
    return binario


try:
    '''
    Para cada instrução do arquivo uma saída binária é escrita em
    um arquivo destino chamado saida.bin.
    EX:
    Entrada:add $16, $5, $15 Saída: 00000000101011111000000000100000
    Caso a compilação falhe u erro é apresentado em tela.
    Obs: o operador nop é utilizado como início de
    desenvolvimento de labels.
    '''
    if len(sys.argv) < 2:
        print 'Para executar o programa digite no seguinte formato:\n'\
            'python arq1.py nomedoarquivo.asm'
        sys.exit()

    nome_arquivo = sys.argv[1]
    with open(nome_arquivo) as src, open('saida.bin', 'w') as dst:

        for line in src.readlines():
            instrucao = line.strip()
            # Ignora comentários
            if (not instrucao) or (instrucao.startswith('#')):
                continue

            instrucao = instrucao.split(' ', 1)
            nome = instrucao[0].strip()
            if nome in logicas_aritmeticas:
                rs = instrucao[1].split(',')[1].strip()
                if nome == 'addi':
                    rt = instrucao[1].split(',')[0].strip()
                    imediato = instrucao[1].split(',')[2].strip()
                    dst.write('001000' + reg[rs] + reg[rt] +
                              calc_imediato(imediato) + '\n')
                else:
                    rd = instrucao[1].split(',')[0].strip()
                    rt = instrucao[1].split(',')[2].strip()
                    dst.write('000000' + reg[rs] + reg[rt] +
                              reg[rd] + '00000' + funct[nome] + '\n')
            elif nome in transferencia_dados:
                instrucao = instrucao[1].replace(
                    '(', ' ').replace(',', ' ').replace(')', '')
                instrucao = instrucao.split()
                rt = instrucao[0].strip()
                rs = instrucao[2].strip()
                imediato = instrucao[1].strip()
                dst.write(opcode[nome] + reg[rs] + reg[rt] +
                          calc_imediato(imediato) + '\n')
            elif nome in desvio_condicional:
                rs = instrucao[1].split(',')[0].strip()
                rt = instrucao[1].split(',')[1].strip()
                if nome == 'slt':
                    rd = instrucao[1].split(',')[2].strip()
                    dst.write(opcode[nome] + reg[rs] + reg[rt] + reg[rd] +
                              '0' * 5 + funct[nome] + '\n')
                else:
                    imediato = instrucao[1].split(',')[2].strip()
                    dst.write(opcode[nome] + reg[rs] + reg[rt] +
                              calc_imediato(imediato) + '\n')
            elif nome in desvio_incondicional:
                if nome == 'jr':
                    registrador = instrucao[1].strip()
                    dst.write(opcode[nome] + reg[registrador] +
                              '000000000000000' + funct[nome] + '\n')
                else:
                    endereco = calc_endereco(instrucao[1].strip())
                    dst.write(opcode[nome] + endereco + '\n')
            elif nome == "nop":
                dst.write(32 * '0' + '\n')
            else:
                raise NotImplementedError('Instrução inválida.')
except IOError:
    print 'Arquivo não encontrado!'
except (IndexError, ValueError) as e:
    print 'Erros ocorreram durante compilação : ' + e.message
