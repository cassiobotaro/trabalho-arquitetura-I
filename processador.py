#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
    Módulo contendo processador MIPS.
'''
from componentes import PC, ControlUnit, Alu
from sys import exit


class Mips(object):

    """
        Classe que representa o processador multiciclo MIPS.
    """

    def __init__(self, instrucoes):
        """
            Inicializa a instância com seu 'hardware'.
        """
        self.pc = PC
        self.alu = Alu
        self.control_unit = ControlUnit
        self.instrucoes = instrucoes
        self.instrucao = None
        self.registradores = ['0' * 32] * 32
        self.rs = None
        self.rt = None
        self.rd = None
        self.sign_extend = None
        self.memoria = ['0' * 32] * 64000
        self.write_data = None

    def imprimirIF(self):
        """
            Imprime o contador de programa.
        """
        print(('IF \n  PC -> {pc}\n'.format(pc=self.pc.saida)))

    def imprimirID(self):
        """
            Imprime os valores dos sinais de controle.
        """
        print((
            'ID\n'
            '  PCWriteCond -> {pc_write_cond}\n'
            '  PCWrite -> {pc_write}\n'
            '  IorD -> {iord}\n'
            '  MemRead -> {memread}\n'
            '  MemWrite -> {memwrite}\n'
            '  MemtoReg -> {memtoreg}\n'
            '  IRWrite -> {irwrite}\n'
            '  CauseWrite -> {causewrite}\n'
            '  IntCause -> {intcause}\n'
            '  EPCWrite -> {epcwrite}\n'
            '  PCSource -> {pcsource}\n'
            '  AluOP -> {op}\n'
            '  ALUSrcB -> {alusrcb}\n'
            '  ALUSrcA -> {alusrca}\n'
            '  RegWrite -> {regwrite}\n'
            '  RegDst -> {regdst}\n'.format(
                op=self.control_unit.aluop.op,
                **self.control_unit
            )
        ))

    def imprimirEX(self):
        """
            Imprime a saída da Alu e flag de Zero
        """
        print((
            'EX\n'
            '  AluOut -> {resultado}\n'
            '  Zero -> {zero}\n'.format(**self.alu)
        ))

    def imprimirMEM(self):
        """
            Imprime o endereço de memória e o dado.
        """
        print((
            'MEM\n'
            '  Endereço -> {saida}\n'
            '  Dado -> {rt}\n'.format(
                saida=self.alu.resultado,
                rt=self.registradores[int(self.rt, 2)]
            )
        ))

    def imprimirWR(self):
        """
            Imprime o valor a ser escrito e o registrador de destino.
        """
        print((
            'WR\n'
            '  WriteData -> {write_data}\n'
            '  RegDst -> {regdst}\n'.format(
                write_data=self.write_data,
                regdst=self.control_unit.regdst
            )
        ))

    def imprimirRegistradores(self):
        '''
            Imprime o banco de registradores.
        '''
        print('Número do registrador -> valor')
        for indice, registrador in enumerate(self.registradores):
            print(('{indice:02} -> {registrador}\n'.format(**locals())))

    def IF(self):
        """
            Busca a instrução e incrmenta o PC.

            Caso o pc saia dos limites da memória reservada para
            instruções do programa, o processamento é encerrado.
        """
        if self.pc.entrada >= len(self.instrucoes) or self.pc.entrada < 0:
            self.imprimirRegistradores()
            exit()
        self.pc.saida = self.pc.entrada
        self.pc.entrada += 1
        self.instrucao = self.instrucoes[self.pc.saida]
        self.imprimirIF()

    def _setControlSignals(self):
        """
            Atribui os sinais de controle de acordo com decodificação
            da instrução.
        """
        opcode = self.control_unit.aluop.opcode
        funct = self.control_unit.aluop.funct

        if opcode == '000000' and funct != '001000':
            # instrução do tipo R
            self.control_unit.pc_write_cond = 'x'
            self.control_unit.pc_write = 'x'
            self.control_unit.iord = '0'
            self.control_unit.memread = 'x'
            self.control_unit.memwrite = 'x'
            self.control_unit.memtoreg = '0'
            self.control_unit.irwrite = 'x'
            self.control_unit.causewrite = 'x'
            self.control_unit.intcause = 'x'
            self.control_unit.epcwrite = 'x'
            self.control_unit.pcsource = '00'
            self.control_unit.aluop.op = '10'
            self.control_unit.alusrcb = '00'
            self.control_unit.alusrca = '1'
            self.control_unit.regwrite = '1'
            self.control_unit.regdst = '1'

        elif opcode in ('101011', '101000'):
            # instrução store
            self.control_unit.pc_write_cond = 'x'
            self.control_unit.pc_write = 'x'
            self.control_unit.iord = '1'
            self.control_unit.memread = 'x'
            self.control_unit.memwrite = '1'
            self.control_unit.memtoreg = 'x'
            self.control_unit.irwrite = 'x'
            self.control_unit.causewrite = 'x'
            self.control_unit.intcause = 'x'
            self.control_unit.epcwrite = 'x'
            self.control_unit.pcsource = '00'
            self.control_unit.aluop.op = '00'
            self.control_unit.alusrcb = '10'
            self.control_unit.alusrca = '1'
            self.control_unit.regwrite = 'x'
            self.control_unit.regdst = 'x'

        elif opcode in ('100011', '100000'):
            # instrução load
            self.control_unit.pc_write_cond = 'x'
            self.control_unit.pc_write = 'x'
            self.control_unit.iord = '1'
            self.control_unit.memread = '1'
            self.control_unit.memwrite = 'x'
            self.control_unit.memtoreg = '1'
            self.control_unit.irwrite = 'x'
            self.control_unit.causewrite = 'x'
            self.control_unit.intcause = 'x'
            self.control_unit.epcwrite = 'x'
            self.control_unit.pcsource = '00'
            self.control_unit.aluop.op = '00'
            self.control_unit.alusrcb = '10'
            self.control_unit.alusrca = '1'
            self.control_unit.regwrite = '1'
            self.control_unit.regdst = '0'

        elif opcode in ('000010', '000011') or (opcode == '000000' and
                                                funct == '001000'):
            # instrução de desvio incondicional
            self.control_unit.pc_write_cond = 'x'
            self.control_unit.pc_write = 'x'
            self.control_unit.iord = '0'
            self.control_unit.memread = 'x'
            self.control_unit.memwrite = 'x'
            self.control_unit.memtoreg = 'x'
            self.control_unit.irwrite = 'x'
            self.control_unit.causewrite = 'x'
            self.control_unit.intcause = 'x'
            self.control_unit.epcwrite = 'x'
            self.control_unit.pcsource = '10'
            self.control_unit.aluop.op = '00'
            self.control_unit.alusrcb = '11'
            self.control_unit.alusrca = '0'
            self.control_unit.regwrite = 'x'
            self.control_unit.regdst = 'x'

        elif opcode in ('000100', '000101'):
            # instrução de desvio condicional
            self.control_unit.pc_write_cond = 'x'
            self.control_unit.pc_write = 'x'
            self.control_unit.iord = '0'
            self.control_unit.memread = 'x'
            self.control_unit.memwrite = 'x'
            self.control_unit.memtoreg = 'x'
            self.control_unit.irwrite = 'x'
            self.control_unit.causewrite = 'x'
            self.control_unit.intcause = 'x'
            self.control_unit.epcwrite = 'x'
            self.control_unit.pcsource = '01'
            self.control_unit.aluop.op = '01'
            self.control_unit.alusrcb = '00'
            self.control_unit.alusrca = '1'
            self.control_unit.regwrite = 'x'
            self.control_unit.regdst = 'x'

        else:
            # instrução do tipo I
            self.control_unit.pc_write_cond = 'x'
            self.control_unit.pc_write = 'x'
            self.control_unit.iord = '0'
            self.control_unit.memread = 'x'
            self.control_unit.memwrite = 'x'
            self.control_unit.memtoreg = '0'
            self.control_unit.irwrite = 'x'
            self.control_unit.causewrite = 'x'
            self.control_unit.intcause = 'x'
            self.control_unit.epcwrite = 'x'
            self.control_unit.pcsource = '00'
            self.control_unit.aluop.op = '10'
            self.control_unit.alusrcb = '10'
            self.control_unit.alusrca = '1'
            self.control_unit.regwrite = '1'
            self.control_unit.regdst = '0'

    def ID(self):
        """
            A instrução é decodificada e os sinais de controle
            definidos.
        """
        self.rs = self.instrucao[6:11:]
        self.rt = self.instrucao[11:16:]
        self.rd = self.instrucao[16:21:]
        self.control_unit.aluop.opcode = self.instrucao[:6:]
        self.control_unit.aluop.funct = self.instrucao[-6::]
        self._setControlSignals()
        self.imprimirID()

    def _soma(self):
        """
            Instrução que soma as entradas da ALU
        """
        soma = int(self.alu.entradaa, 2) + int(self.alu.entradab, 2)
        self.alu.resultado = bin(soma).replace('0b', '').zfill(32)

    def _sub(self):
        """
            Instrução que subtrai o valor das entradas da ALU
        """
        sub = int(self.alu.entradaa, 2) - int(self.alu.entradab, 2)
        self.alu.resultado = bin(sub).replace('0b', '').zfill(32)

    def _mult(self):
        """
            Instrução que multiplica o valor das entradas da ALU
        """
        mult = int(self.alu.entradaa, 2) * int(self.alu.entradab, 2)
        self.alu.resultado = bin(mult).replace('0b', '').zfill(32)

    def _and(self):
        """
            Instrução que realiza a operação AND das entradas da ALU
        """
        andbb = int(self.alu.entradaa, 2) & int(self.alu.entradab, 2)
        self.alu.resultado = bin(andbb).replace('0b', '').zfill(32)

    def _or(self):
        """
            Instrução que realiza a operação OR das entradas da ALU
        """
        orbb = int(self.alu.entradaa, 2) | int(self.alu.entradab, 2)
        self.alu.resultado = bin(orbb).replace('0b', '').zfill(32)

    def _nor(self):
        """
            Instrução que realiza a operação NOR das entradas da ALU
        """
        norbb = int(self.alu.entradaa, 2) | int(self.alu.entradab, 2)
        norbb = bin(norbb).replace('0b', '').zfill(32)
        self.alu.resultado = norbb.translate(str.maketrans('-01', '010'))

    def _j(self):
        """
            Instrução j
        """
        self.pc.entrada = int(self.instrucao[6::], 2)
        self.alu.resultado = '0' * 32

    def _jal(self):
        """
            Instrução jal
        """
        self.registradores[31] = bin(self.pc.entrada)[2::].zfill(32)
        self.pc.entrada = int(self.instrucao[6::], 2)
        self.alu.resultado = '0' * 32

    def _jr(self):
        """
            Instrução jr
        """
        self.pc.entrada = int(self.registradores[int(self.rs, 2)], 2)
        self.alu.resultado = '0' * 32

    def _beq(self):
        """
            Instrução beq
        """
        if self.alu.entradaa.zfill(32) == self.alu.entradab.zfill(32):
            self.alu.zero = '1'
            self.pc.entrada += int(self.instrucao[-16::], 2)
        else:
            self.alu.zero = '0'
        self.alu.resultado = '0' * 32

    def _bne(self):
        """
            Instrução bne
        """
        if self.alu.entradaa.zfill(32) != self.alu.entradab.zfill(32):
            self.alu.zero = '1'
            self.pc.entrada += int(self.instrucao[-16::], 2)
        else:
            self.alu.zero = '0'
        self.alu.resultado = '0' * 32

    def _slt(self):
        """
            Instrução slt
        """
        if int(self.alu.entradaa, 2) < int(self.alu.entradab, 2):
            self.alu.resultado = 31 * '0' + '1'
        else:
            self.alu.resultado = 32 * '0'

    def _overflow(self):
        """
            Calcula a quantidade de bits de overflow e remove os bits
            excedentes do resultado da ALU.
        """
        if len(self.alu.resultado) < 32:
            self.alu.ovfl = 0
        else:
            self.alu.ovfl = len(self.alu.resultado) - 32
            self.control_unit.pc_write = 'x'
            self.control_unit.causewrite = 'x'
            self.control_unit.intcause = '1'
            self.control_unit.epcwrite = 'x'
            self.control_unit.pcsource = '11'
            self.control_unit.aluop.op = '01'
            self.control_unit.alusrcb = '01'
            self.control_unit.alusrca = '0'

        self.alu.resultado = self.alu.resultado[self.alu.ovfl::]

    def EX(self):
        """
            Execução da instrução.
            Verifica os sinais de controle(src A e src B da ALU)
             e executa a instrução.
        """
        # Entrada A
        if self.control_unit.alusrca == '0':
            self.alu.entradaa = bin(self.pc.saida).replace('0b', '').zfill(32)
        else:
            self.alu.entradaa = self.registradores[int(self.rs, 2)]

        if self.control_unit.alusrcb == '00':
            # Entrada B
            self.alu.entradab = self.registradores[int(self.rt, 2)]
        elif self.control_unit.alusrcb == '01':
            # 4
            self.alu.entradab = '00000000000000000000000000000100'
        elif self.control_unit.alusrcb == '10':
            # Sign Extend
            self.alu.entradab = self.instrucao[-16::]
        elif self.control_unit.alusrcb == '11':
            # Sign Extend com shift left 2
            aux = self.instrucao[-16::]
            if aux.startswith('1'):
                aux = '-' + self.instrucao[-15::]
            self.alu.entradab = bin(int(aux, 2) << 2).replace('0b',
                                                              '').zfill(32)
        self.alu.zero = 'x'

        # tratamento necessario para negativos
        if self.alu.entradaa.startswith('1'):
            self.alu.entradaa = self.alu.entradaa.replace('1', '-', 1)
        if self.alu.entradab.startswith('1'):
            self.alu.entradab = self.alu.entradab.replace('1', '-', 1)

        # executa a instrução
        if self.control_unit.regdst == '1':
            # instrução do tipo R
            if self.control_unit.aluop.funct == '100000':
                self._soma()
            elif self.control_unit.aluop.funct == '100010':
                self._sub()
            elif self.control_unit.aluop.funct == '100100':
                self._and()
            elif self.control_unit.aluop.funct == '100101':
                self._or()
            elif self.control_unit.aluop.funct == '100111':
                self._nor()
            elif self.control_unit.aluop.funct == '011000':
                self._mult()

        elif (self.control_unit.memread == '1' or
              self.control_unit.memwrite == '1'):
            # instrução de transferência de dados
            self._soma()

        if self.control_unit.pcsource == '10':
            # instrução de desvio incondicional
            if self.control_unit.aluop.opcode == '000010':
                self._j()
            elif self.control_unit.aluop.opcode == '000011':
                self._jal()
            else:
                self._jr()

        elif self.control_unit.pcsource == '01':
            # instrução de desvio condicional
            if self.control_unit.aluop.opcode == '000100':
                self._beq()
            elif self.control_unit.aluop.opcode == '000101':
                self._bne()
        elif (self.control_unit.aluop.opcode == '000000' and
              self.control_unit.aluop.funct == '101010'):
            self._slt()
        else:
            # instrução do tipo I
            if self.control_unit.aluop.opcode == '001000':
                # addi
                self._soma()

        # trata sinal, overflow e imprime EX
        self.alu.resultado = self.alu.resultado.replace('-', '1')
        self._overflow()
        self.imprimirEX()

    def MEM(self):
        """
            Operações de leitura e escrita da memória.
        """
        if self.control_unit.memread == '1':
            # LW
            if self.control_unit.aluop.opcode == '100011':
                self.write_data = self.memoria[int(self.alu.resultado, 2)]
            # LB
            elif self.control_unit.aluop.opcode == '100000':
                dado = self.memoria[int(self.alu.resultado, 2)][-8::]
                self.write_data = dado[0] * 24 + dado

        elif self.control_unit.memwrite == '1':
            # SW
            if self.control_unit.aluop.opcode == '101011':
                self.memoria[int(self.alu.resultado,
                                 2)] = self.registradores[int(self.rt, 2)]
            # SB
            elif self.control_unit.aluop.opcode == '101000':
                dado = self.registradores[int(self.rt, 2)][-8::].zfill(32)
                self.memoria[int(self.alu.resultado, 2)] = dado

        self.imprimirMEM()

    def WR(self):
        """
            Escrita nos registradores.
        """
        if self.control_unit.memtoreg == '0':
            self.write_data = self.alu.resultado

        if self.control_unit.regdst == '0':
            self.registradores[int(self.rt, 2)] = self.write_data
        elif self.control_unit.regdst == '1':
            self.registradores[int(self.rd, 2)] = self.write_data

        self.imprimirWR()
