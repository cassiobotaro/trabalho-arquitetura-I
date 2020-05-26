addi $1, $0, 1
addi $2, $0, 2
add $3, $2, $1
sub $1, $3, $2
addi $10, $11, -23
add $11, $3, $10
sub $1, $10, $11
mult $8, $3, $2
mult $9, $1, $1
and $7, $1, $2
and $7, $2, $2
or $7, $1, $2
or $7, $2, $2
nor $7, $1, $2
nor $7, $2, $2
slt $0, $2, $7
slt $2, $0, $7
beq $0, $0, 1
j 8
addi $5, $0, 5
beq $0, $2, 10
bne $0, $0, 10
bne $0, $2, 2
j 8
j 8
j 30
j 8
j 8
j 8
# label
nop
add $5, $5, $5
jal 34
j 100
# label
nop
jr $ra





#beq $12, $7, 4
##sb $21, 5($5)
#mult $9, $11, $21
##lb $11, -5($23)
#bne $20, $19, 7
#jr 5
#jal 6
