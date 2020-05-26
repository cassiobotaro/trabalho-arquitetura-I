#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
    Componentes de hardware utilizados pelo procesador MIPS.
'''
from storage import Storage

# Program Counter
PC = Storage(entrada=0, saida=None)

ALUOp = Storage(opcode=None, funct=None, op=None)

# Unidade de controle
# Aqui serão armazenados os sinais de controle
ControlUnit = Storage(
    pc_write_cond=None,
    pc_write=None,
    iord=None,
    memread=None,
    memwrite=None,
    memtoreg=None,
    irwrite=None,
    causewrite=None,
    intcause=None,
    epcwrite=None,
    pcsource=None,
    aluop=ALUOp,
    alusrcb=None,
    alusrca=None,
    regwrite=None,
    regdst=None
)

# ALU Unidade Lógica Aritimética
Alu = Storage(
    entradaa=None,
    entradab=None,
    zero=None,
    overflow=None,
    resultado=None
)
