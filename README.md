# processes-and-threads
(1) como  executar  ambos  os  ficheiros  .py:
Para executar os ficheiros colocar na linha de comandos:
	pgrepwc [-a] [-c|-l] [-p n] [-w s] [-o file] {palavras} [-f ficheiros]
				ou
	python3 hpgrepwc.py file

(2) informações pertinentes sobre a implementação do projeto:

Utilizei 2 métodos de distribuição dos ficheiros diferentes:

SE nº de processos >= nº de ficheiros:
Ordenamos a lista de processos do menor para o maior inicialmente
Cada processo fará apenas 1 ficheiro (totalmente ou parcialmente)

exemplo:
nº processos= 15
nº de ficheiros = 4

15/4=    3   (logo 3 processos fazem o file 1)
(15-3)/3=4   (logo 4 processos fazem o file 2)
(12-4)/2=4   (logo 4 processos fazem o file 3)
(8-4/2)   =4 (logo 4 processos fazem o file 4)


---------------------------------------------------------------
SE nº de processos < nº de ficheiros:
Ordenamos a lista de processos do menor para o maior inicialmente
Neste caso, distribuimos os ficheiros pelos processos igualmente, 
se no fim sobrar alguns ficheiros, o ultimo é dividido pelos processos que faltam preencher.
Por isso é importante a ordenacao inicial dos ficheiros por tamanho(menor para maior)
para o ultimo(que será dividido, ser o maior).

exemplo:
nº processos= 5
nº de ficheiros = 23

23/5= 4 (4 files por processo)
4*5= 20 (20 ficheiros que já estão associados a um processo)
23-20 = 3 (3 ficheiros que ainda faltam distribuir)
3-1= 2 (2 ficheiros que não são divididos e são distribuidos pelos 2 primeiros processos)
5-2 = 3 (Dividir o ultimo ficheiro por 3 processos)
