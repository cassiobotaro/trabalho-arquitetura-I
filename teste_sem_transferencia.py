from processador import Mips
with open('saida.bin') as arq:
    proc = Mips([line.strip() for line in arq.readlines()])

proc.IF()
proc.ID()
proc.EX()
proc.WR()
assert proc.registradores[1] == '00000000000000000000000000000001'
print 'linha 1 ok'
proc.IF()
proc.ID()
proc.EX()
proc.WR()
assert proc.registradores[2] == '00000000000000000000000000000010'
print 'linha 2 ok'
proc.IF()
proc.ID()
proc.EX()
proc.WR()
assert proc.registradores[3] == '00000000000000000000000000000011'
print 'linha 3 ok'
proc.IF()
proc.ID()
proc.EX()
proc.WR()
assert proc.registradores[1] == '00000000000000000000000000000001'
print 'linha 4 ok'
proc.IF()
proc.ID()
proc.EX()
proc.WR()
assert proc.registradores[10] == '10000000000000000000000000010111'
print 'linha 5 ok'
proc.IF()
proc.ID()
proc.EX()
proc.WR()
assert proc.registradores[11] == '10000000000000000000000000010100'
print 'linha 6 ok'
proc.IF()
proc.ID()
proc.EX()
proc.WR()
assert proc.registradores[1] == '10000000000000000000000000000011'
print 'linha 7 ok'
proc.IF()
proc.ID()
proc.EX()
proc.WR()
assert proc.registradores[8] == '00000000000000000000000000000110'
print 'linha 8 ok'
proc.IF()
proc.ID()
proc.EX()
proc.WR()
assert proc.registradores[9] == '00000000000000000000000000001001'
print 'linha 9 ok'
proc.IF()
proc.ID()
proc.EX()
proc.WR()
assert proc.registradores[7] == '00000000000000000000000000000000'
print 'linha 10 ok'
proc.IF()
proc.ID()
proc.EX()
proc.WR()
assert proc.registradores[7] == '00000000000000000000000000000010'
print 'linha 11 ok'
proc.IF()
proc.ID()
proc.EX()
proc.WR()

print proc.alu.entradaa
print proc.alu.entradab
assert proc.registradores[7] == '10000000000000000000000000000001'
print 'linha 12 ok'
proc.IF()
proc.ID()
proc.EX()
proc.WR()
assert proc.registradores[7] == '00000000000000000000000000000010'
print 'linha 13 ok'
proc.IF()
proc.ID()
proc.EX()
proc.WR()
assert proc.registradores[7] == '01111111111111111111111111111110'
print 'linha 14 ok'
proc.IF()
proc.ID()
proc.EX()
proc.WR()
assert proc.registradores[7] == '11111111111111111111111111111101'
print 'linha 15 ok'
proc.IF()
proc.ID()
proc.EX()
proc.WR()
assert proc.registradores[7] == '00000000000000000000000000000001'
print 'linha 16 ok'
proc.IF()
proc.ID()
proc.EX()
proc.WR()
assert proc.registradores[7] == '00000000000000000000000000000000'
print 'linha 17 ok'
proc.IF()
proc.ID()
proc.EX()
assert proc.pc.entrada == 19
print 'linha 18 ok'
proc.IF()
proc.ID()
proc.EX()
proc.WR()
assert proc.registradores[5] == '00000000000000000000000000000101'
print 'linha 20 ok'
proc.IF()
proc.ID()
proc.EX()
assert proc.pc.entrada == 21
print 'linha 21 ok'
proc.IF()
proc.ID()
proc.EX()
assert proc.pc.entrada == 22
print 'linha 22 ok'
proc.IF()
proc.ID()
proc.EX()
assert proc.pc.entrada == 25
print 'linha 23 ok'
proc.IF()
proc.ID()
proc.EX()
assert proc.pc.entrada == 30
print 'linha 26 ok'
proc.IF()
proc.ID()
proc.EX()
proc.WR()
assert proc.registradores[5] == '00000000000000000000000000001010'
print 'linha 31(32) ok'
proc.IF()
proc.ID()
proc.EX()
assert proc.pc.entrada == 34
print 'linha 32(33) ok'
proc.IF()
proc.ID()
proc.EX()
assert proc.pc.entrada == 32
print 'linha 35(37) ok'
proc.IF()
proc.ID()
proc.EX()
assert proc.pc.entrada == 100
print 'linha 33(34) ok'
