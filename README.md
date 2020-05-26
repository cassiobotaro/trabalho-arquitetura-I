# trabalho-arquitetura-I
Simulação do processador MIPS multiciclo.

## Requisitos do sistema

- Python (3.6+)

## Intruções de utilização

Coloque o arquivo.asm no mesmo diretório onde está o arquivo interpretador.py,
em seguida execute `python interpretador.py nomedoarquivo.asm`.
Um arquivo chamado saida.bin será criado no mesmo diretório. Este arquivo
contém o código na forma binário que o simulador do interpretador mips
irá utilizar.
Para simular a execução do programa, digite:
    `python main.py saida.bin`
ou
    `python main.py saida.bin [tempo_de_parada]`
A segunda opção de execução espera um valor numérico que será utilizado
para atrasar execução do programa, melhorando assim visualização dos ciclos.
