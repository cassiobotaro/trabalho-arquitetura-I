from processador import Mips
with open('saida.bin') as arq:
    proc = Mips([line.strip() for line in arq.readlines()])

proc.IF()
proc.ID()
proc.EX()
proc.WR()
assert proc.registradores[1] == '00000000000000000000000000000100'
print 'linha 1 ok'
proc.IF()
proc.ID()
proc.EX()
proc.WR()
assert proc.registradores[2] == '00000000000000000000000000000101'
print 'linha 2 ok'
proc.IF()
proc.ID()
proc.EX()
proc.MEM()
assert proc.memoria[7] == '00000000000000000000000000000101'
print 'linha 3 ok'
proc.IF()
proc.ID()
proc.EX()
proc.MEM()
proc.WR()
assert proc.registradores[3] == '00000000000000000000000000000101'
print 'linha 4 ok'
proc.IF()
proc.ID()
proc.EX()
proc.WR()
assert proc.registradores[2] == '10000000000000000000000010000001'
print 'linha 5 ok'
proc.IF()
proc.ID()
proc.EX()
proc.MEM()
assert proc.memoria[7] == '00000000000000000000000010000001'
print 'linha 6 ok'
proc.IF()
proc.ID()
proc.EX()
proc.MEM()
proc.WR()
assert proc.registradores[3] == '11111111111111111111111110000001'
print 'linha 7 ok'
