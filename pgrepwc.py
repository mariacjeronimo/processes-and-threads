# imports
import sys
import os.path
import string #para retirar pontuação
import os, signal, time, sys
from multiprocessing import Process, Array, Lock, Manager
import datetime
__author__ = "Maria Jerónimo, nº56887 e Tânia Araújo, nº56959"

def filtraLinha(linha):
    """Funcão que retira pontuação das palavras das linhas que recebe.

    Args:
        linha (list): lista que contém as palavras de uma linha.

    Returns:
        [list]: lista das palavras filtradas (sem pontuação) da linha.
    """
    aaa = linha
    for i in range(len(aaa)):
        aaa[i]=aaa[i].translate(str.maketrans('', '', string.punctuation)) #string.punctuation returns: !"#$%&'()*+,-./:;<=>?@[\]^_`{|}~
    return aaa



def filtrar_palavras(lista_palavras):
    """Funcão que recebe uma lista de palavras e filtra as mesmas, retirando lhes a pontuação.

    Args:
        lista_palavras (list): lista de palavras que foi inserida pelo utilizador na linha de comandos 

    Returns:
        [list]: lista das palavras filtradas (sem pontuação) da linha.
    """
    for i in range(len(lista_palavras)):
        lista_palavras[i]=lista_palavras[i].translate(str.maketrans('', '', string.punctuation))
        
    return lista_palavras



def check_ficheiro_existe(lista_ficheiros):
    """Funcão que verifica se um ficheiro .txt existe na mesma diretoria deste ficheiro .py

    Args:
        lista_ficheiros (list): lista dos ficheiros a verificar(ficheiros que são inseridos na linha de comandos após a opção -f)

    Returns:
        [bool]: return False se o ficheiro não existir 
    """
    for ficheiro in lista_ficheiros:
        if os.path.exists(ficheiro) == False: #Se der True ou seja o ficheiro existe na diretoria e faz o readfile(função)
            print("O ficheiro "+ ficheiro +" não existe!")
            return False



def somaParaResultado(lista):
    """Funcão que faz a soma global das ocorrencias/nº de linhas (depende da opção escolhida -c ou -l) para uma lista em que cada posição da 
    mesma corresponde a cada palavra da lista de palavras. 
    exemplo: ["ola","adeus"]--->[2,5] existiu 2 ocorrencias da palavra "ola" e 5 da palavra "adeus" (-c ativo)

    Args:
        lista (list): lista com as somas globais de cada palavra 
    """
    global resultado
    for i in range (len(lista)):
        resultado[i]+=lista[i]


def readfile(nome_ficheiro,lista_palavras,arg_a,opcao_escolhida,linha_start,linha_end): #leitura dos ficheiros!
    """Funcão principal que lê os ficheiros e faz print das linhas relevantes. Também verifica a opcao escolhida (-c ou -l) e chama funcoes que efectuam as contagens.
    Se a opção -o estiver ativa, são copiadas para um ficheiro a informação relevante do historico de execução do programa.

    Args:
        nome_ficheiro (str): Nome do ficheiro a analisar.
        lista_palavras (list): lista das palavras a pesquisar no ficheiro 
        arg_a (bool): se a opção -a estiver ativa arg_a=True; caso contrario False
        opcao_escolhida (str): -c ou -l (depende da opção escolhida)
        linha_start (int): nº da linha em que começa a ler o ficheiro
        linha_end (int):nº da linha em que acaba a leitura do ficheiro
    """
    global resultado
    global nome_file_historico
    lista_linhas_all=[]
    lista_linhas_One=[]
    lista_linhas_all_normal=[]
    lista_linhas_One_normal=[]

    if nome_file_historico != 0:
        with open(nome_file_historico,"a") as f:
            f.write(stringToBinary("   ficheiro: "+ str(nome_ficheiro) )+ "\n")


    with open(nome_ficheiro) as f:
        inicio_file=datetime.datetime.now() #inicio de exec do ficheiro
        linhas = f.readlines() #lista de strs das linhas do ficheiro

        for i in range(linha_start, linha_end):
            
            linha_filtrada = linhas[i].rstrip() # retira \n
            linha_filtrada=list(linha_filtrada.split(" ")) #transforma as linhas em lista
            linha_filtrada = filtraLinha(linha_filtrada)
            
            if arg_a: #COM O -A 
                if pesquisaTodasPalavras(lista_palavras,linha_filtrada): #LINHAS COM TODAS AS PALAVRAS
                    lista_linhas_all.append(linha_filtrada) #linha para mandar ao -c/-l
                    lista_linhas_all_normal.append(linhas[i])#linha para output
                    
            else:#SEM O -A  
                if pesquisaUmaPalavra(lista_palavras,linha_filtrada):     #LINHAS COM APENAS UMA PALAVRA
                    lista_linhas_One.append(linha_filtrada)
                    lista_linhas_One_normal.append(linhas[i])
                    
        if arg_a:
            if opcao_escolhida == "-c":
                somaParaResultado(encontra_ocorrencias(lista_linhas_all,lista_palavras))
            if opcao_escolhida == "-l":
                somaParaResultado(ocorrencia_linhas(arg_a,lista_linhas_all,lista_palavras))
            for linha in lista_linhas_all_normal:
                print("[PID: " + str(os.getpid()) + "] [Ficheiro: " + str(nome_ficheiro) + "] Linha: " + linha)

        else:
            if opcao_escolhida == "-c":
                somaParaResultado(encontra_ocorrencias(lista_linhas_One,lista_palavras))
            if opcao_escolhida == "-l":
                somaParaResultado(ocorrencia_linhas(arg_a,lista_linhas_One,lista_palavras))
            for linha in lista_linhas_One_normal:
                print("[PID: " + str(os.getpid()) + "] [Ficheiro: " + str(nome_ficheiro) + "] Linha: " + linha)

        end_file=datetime.datetime.now() #fim da exec do file atual
        tempo_pesquisa = end_file-inicio_file

        
    if nome_file_historico != 0:
        with open(nome_file_historico,"a") as f:
            f.write(stringToBinary("       tempo de pesquisa: " + str(tempo_pesquisa))+ "\n")
            f.write(stringToBinary("       dimensão do ficheiro: " + str(linha_end-linha_start))+ "\n")
            #f.write("       linha start: <" + str(linha_start) + ">" + "\n")
            #f.write("       linha end: <" + str(linha_end) + ">" + "\n")


def tempoParaMicrosegundos(t):
    """Funcão que recebe uma string e converte o tempo descrito da string de formato
    (horas:minutos:segundos.microsegundos) para os seus microsegundos correspondentes.

    Args:
        t (string): String de formato "Horas:minutos:segundos.microsegundos"
    Returns:
        [int]: return total de microsegundos
    """
    # t (string)  => str(tempo_end - tempo_start) horas:minutos:segundos.microsegundos 
    # exemplo '0:00:53.997106' [0,00,53.997106] => [53.997106].split(".") = > [53.997106][-1] = > [997106]
    microsegundos = int( t.split(":")[-1].split(".")[-1] )
    t_split_sem_microsegundos = [x.split(".")[0] for x in t.split(":")] #[0,00,53] sem os micro segundos

    segundos_para_microsegundos = int(t_split_sem_microsegundos[2]) * 1000000
    minutos_para_microsegundos = int(t_split_sem_microsegundos[1]) * 60 * 1000000
    horas_para_microsegundos = int(t_split_sem_microsegundos[0]) * 60 * 60 * 1000000

    microsegundos += horas_para_microsegundos + minutos_para_microsegundos + segundos_para_microsegundos

    return(microsegundos)



def tempo(sig, NULL):
    """Função que é chamada de s em s segundos (se a opção -w estiver ativa). Chama as funções apresentar_resultados, file_completo_incompleto e indica o tempo decorrido
    desde a execução do programa.

    Args:
        sig e NULL: Necessários para a implementação 
    """
    global tempo_start
    global lista_palavras
    global stop
    apresentar_resultados(lista_palavras)
    file_completo_incompleto()
    tempo_end=datetime.datetime.now()
    # quando se faz tempo_end-tempo_start o resultado sao só as horas:minutos:segundos,microsegundos
    print("Tempo decorrido desde o inicio de execução do programa: "+ str(tempoParaMicrosegundos(str((tempo_end-tempo_start))))+ " microsegundos.")
   
    

    

def terminar_processos_CTRLC(sig,NULL): #Quando o CTRL-C é accionado a variavel global stop muda para true e faz break aos processos!
    """Função que é chamada quando o CTRL-C é accionado. Acede a uma variável global (stop) e muda a para True para indicar a necessidade de parar corretamente os processos.

    Args:
        sig e NULL: Necessários para a implementação 
    """
    global stop
    stop = True



def lerVariosFicheiroPorProcesso(lista_ficheiros,lista_palavras,arg_a,opcao_escolhida):#a lista_ficheiros corresponde a 1 processo e contem todos os ficheiros que esse processo vai fazer
    """Funcão que recebe a lista_ficheiros (a lista corresponde a 1 processo e contém todos os ficheiros que esse processo vai fazer) 
    A lista_ficheiros tem o segunte formato [["file1",linha_start,linha_end],["file2",linha_start,linha_end],["file3",linha_start,linha_end]]
    ou seja é uma lista de listas, em que cada sublista contém o filename, linha inicial e linha final desse file.
    Se a opção -o estiver ativa, são copiadas para um ficheiro a informação relevante do historico de execução do programa.

    Args:
        lista_ficheiros (list): lista de listas com os ficheiros que se pretende ler no readfile
        lista_palavras (list): lista das palavras a pesquisar no ficheiro 
        arg_a (bool): se a opção -a estiver ativa arg_a=True; caso contrario False
        opcao_escolhida (str): -c ou -l (depende da opção escolhida)
    """
    mutex.acquire()
    global ocorrencias_ficheiros
    global lista_ficheiros_indice #VAR GLOBAL
    global stop
    global resultado
    global nome_file_historico
    #print("---------------------------------------------------------")
    #print("LISTA FILES" + str(lista_ficheiros)) #VERIFICAR DISTRIBUIÇÂO DOS FICHEIROS POR PROCESSOSS
    #print("\n")
    #lista_informacao_para_file=[]

    #time.sleep(3)

    pid_processo=os.getpid()

    if nome_file_historico != 0:
        with open(nome_file_historico,"a") as f:
            f.write(stringToBinary("Processo: " + str(pid_processo) )+ "\n")

    for ficheiro in lista_ficheiros: # lista_ficheiros é uma lista com sublistas que correposndem ao file [[nomefile,linhaStart,linhaEnd]] logo ficheiro[1]=linha_start e ficheiro[2]=linha_end
        if stop == False:
            readfile(ficheiro[0], lista_palavras,arg_a,opcao_escolhida, ficheiro[1], ficheiro[2])
            for tuplo in lista_ficheiros_indice:
                #print(tuplo)
                if tuplo[1]==ficheiro[0]:    
                    ocorrencias_ficheiros += [tuplo[0]]   #tuplo[1] nome file
                                                         #tuplo[0]= indice correspondente ao file
        
        else:
            break


    mutex.release()
        
        

def obter_n_linhas(ficheiro): 
    """Função que recebe um ficheiro e faz return do nº de linhas do ficheiro

    Args:
        ficheiro (str): Nome do ficheiro que queremos conhecer o nº total de linhas

    Returns:
        [int]: Nº de linhas do ficheiro
    """
    with open(ficheiro) as f:
        i = 0
        for linha in f:
            i += 1
    return i




def file_completo_incompleto(): 
    """Função que indica o nº de ficheiros totalmente processados e o nº de ficheiros em processamento.
    """
    global n_processos_files2 #[(nº de processos, file name)]
    global ocorrencias_ficheiros #lista com todas as ocorrencias dos ficheiros nos processos pelo indice
    global lista_ficheiros_indice#[(i,file name)]

    n_ficheiros_completos=0
    n_ficheiros_incompletos=0
    
    for x in n_processos_files2:
        cont=0
        for y in ocorrencias_ficheiros:
            #ver que file corresponte o tuplo com o indice = y
            nome_file=[tuplo for tuplo in lista_ficheiros_indice if tuplo[0] == y][0][1] #guarda o tuplo correspondente ao ficheiro isto dá [(0, 'file1')] como quero o filename é [0][1]
            #ver se o file desse tuplo é = a x[1]
            if nome_file == x[1]:
                cont+=1

        if cont != x[0]:
            #print("FICHEIRO "+ str(x[1]) +" incompleto!")
            n_ficheiros_incompletos+=1
        else:
            #print("FICHEIRO "+ str(x[1]) +" completo!") 
            n_ficheiros_completos+=1

    print("Número de ficheiros completamente processados: " + str(n_ficheiros_completos))
    print("Número de ficheiros em processamento: " + str(n_ficheiros_incompletos))
    return(n_ficheiros_completos,n_ficheiros_incompletos) #RETURN TUPLO (nº de ficheiros(completos,incompletos))



def secondElement(elem):
    """Esta função foi usada para realizar um sorted de uma lista de tuplos em que a key era o segundo elemento dos tuplosna função criar_processos

    Args:
        elem (tuple): tuplo em que pretendo aceder ao segundo elemento

    Returns:
        [any]: definicao do segundo elemento elem[1]
    """
    return elem[1]



def criar_processos(lista_ficheiros,lista_palavras,arg_a,opcao_escolhida,n):
    """Funcão que reencaminha os ficheiros para os processos correspondentes. A escolha depende do numero de processos e do numero de ficheiros.
    Chama processos filhos e faz os prints no processo pai das somas gerais.
     Se a opção -o estiver ativa, são copiadas para um ficheiro a informação relevante do historico de execução do programa.

    Args:
        lista_ficheiros (list): lista de ficheiros que se pretende ler 
        lista_palavras (list): lista das palavras a pesquisar no ficheiro 
        arg_a (bool): se a opção -a estiver ativa arg_a=True; caso contrario False
        opcao_escolhida (str): -c ou -l (depende da opção escolhida)
        n (int): numero de processos filhos
    """
    global resultado
    global n_processos_files2
    global lista_ficheiros_indice
    global tempo_exec_programa
    global nome_file_historico
    t=[]
    linhas_ficheiros=[]
    
    #ORDENAR FICHEIROS DO MENOR PARA O MAIOR
    for ficheiro in lista_ficheiros:
        total = obter_n_linhas(ficheiro)
        linhas_ficheiros.append((ficheiro,total)) #[("file1",5),("file2",10),("file3",11),("file4",1)] ou seja (FileName, LineCount)
    lista_ficheiros_sort= sorted(linhas_ficheiros, key=secondElement, reverse=False)  #ordenar por ordem crescente
    lista_ficheiros=list(map(lambda x: x[0], lista_ficheiros_sort)) #lista ficheiros ordenados
   
   
    lista_ficheiros_indice = [(x,lista_ficheiros[x]) for x in range(len(lista_ficheiros))] #atribui um indice a cada ficheiro[(i,file name)]

    if nome_file_historico != 0:
        info_inicial_historico()



    if n == 0: #(PROCESSO PAI FAZ TUDO SE nº de processos=0) 
        lista_ficheiros = [ [f, 0, obter_n_linhas(f)] for f in lista_ficheiros ]
        lerVariosFicheiroPorProcesso(lista_ficheiros,lista_palavras,arg_a,opcao_escolhida)
        print("O pid do pai é "+str(os.getpid()))
        apresentar_resultados(lista_palavras)
        return #return para não entrar no ultimo if


    if n >= len(lista_ficheiros): #METODO PARA DISTRIBUIÇÃO EQUITATIVA SE Nº PROCESSOS >= Nº FICHEIROS 
       #Lista com x sublistas (sendo x o numero de ficheiros) [[p1,p2,p3],[p4,p5]]=> 2 ficheiros distribuidos por 5 processos
       #Neste caso cada processo só lê um ficheiro mas há vários processos a ler o mesmo ficheiro!
       # lista_processos_ficheiros = [[0,1], [2,3], [4,5]]
       # lista_ficheiros           = ["f1",  "f2",  "f3"]
        

        lista_processos_ficheiros=[[]]*len(lista_ficheiros) 
        total_processos = n 
        total_ficheiros = len(lista_ficheiros) 
        p_atual = 0

        for i in range(total_ficheiros):
            x = total_processos // total_ficheiros 
            for j in range(p_atual, p_atual+x):
                lista_processos_ficheiros[i] = lista_processos_ficheiros[i] + [j]
            p_atual = p_atual + x
            total_processos=total_processos-x
            total_ficheiros=total_ficheiros-1
      

        
        n_processos_files=[] #LISTA Q VAI CONTER O NUMERO DE PROCESSOS POR FICHEIRO PARA DEPOIS SABER SE OS FICHEIROS FORAM PROCESSADOS TOTALMENTE OU NÃO
        for i in range(len(lista_processos_ficheiros)):
            
            n_sublistas = len(lista_processos_ficheiros[i])
            n_processos_files.append(n_sublistas)

            nome_ficheiro = lista_ficheiros[i]
            
            n_linhas = obter_n_linhas(nome_ficheiro)
            linha_start = 0
            linha_end = n_linhas // n_sublistas
           
            n_processos_files2=[(n_processos_files[i], lista_ficheiros[i]) for i in range(0, len(n_processos_files))]

            for j in range(n_sublistas):
                t.append(Process(target=lerVariosFicheiroPorProcesso,args=([ [nome_ficheiro, linha_start, linha_end]],lista_palavras,arg_a,opcao_escolhida, )))
                linha_start = linha_end

                if(j+2 < n_sublistas):
                    linha_end = linha_end + (n_linhas // n_sublistas)
                else:
                    linha_end = n_linhas
                    


        for i in range(len(t)):
            t[i].start()
        for i in range(len(t)):
            t[i].join()
        
        apresentar_resultados(lista_palavras)
        if s_segundos != 0:
            file_completo_incompleto()
       



    
    if n < len(lista_ficheiros): 
    # lista dos processos, cada sublista representa cada processo e dentro de cada sublista há as listas dos ficheiros  [[['file1',0,50],['file2',0,10]],...]
        lista_processos=[[]]*n   
        n_ficheiros = len(lista_ficheiros) 
        n_processos = n

        ficheiros_completos_por_processo=n_ficheiros//n_processos
        ficheiros_completos_total=ficheiros_completos_por_processo*n_processos
        ficheiros_nao_atribuidos=n_ficheiros-ficheiros_completos_total
        if ficheiros_nao_atribuidos > 1:
            last_file_division=n_processos-(ficheiros_nao_atribuidos-1)
        else:
            last_file_division=n_processos
        
            
                
        
        #TODOS OS FICHEIROS MENOS O ULTIMO(que vai ser dividido)
        i=0
        for ficheiro in lista_ficheiros[:-1]:
            linha_start = 0
            linha_end = obter_n_linhas(ficheiro)
            n_processos_files2.append((1,ficheiro)) #numero de processos por file
            
            if i < n_processos: #se o i do file atual for menor q o numero total de processos 
                lista_processos[i]=lista_processos[i]+[[ficheiro,linha_start,linha_end]]
                i+=1
            else:
                i=0
                lista_processos[i]=lista_processos[i]+[[ficheiro,linha_start,linha_end]]
                i+=1
        
        ultimo_file=lista_ficheiros[-1]
        ultimo_file_linhas=obter_n_linhas(ultimo_file)
        linha_start = 0
        linha_end = ultimo_file_linhas // last_file_division


        n_processos_files2.append((last_file_division,ultimo_file))

        for i in range(len(lista_processos)-last_file_division,len(lista_processos)): #Iterar as ultimas last_file_division sublistas

            lista_processos[i]=lista_processos[i] + [[ultimo_file,linha_start,linha_end]]
            linha_start=linha_end
            if(i+2 < len(lista_processos)):
                linha_end= linha_end + (ultimo_file_linhas // last_file_division)
            else:
                linha_end = ultimo_file_linhas
        
        
            
        for processo in lista_processos:
            t.append(Process(target=lerVariosFicheiroPorProcesso,args=(processo,lista_palavras,arg_a,opcao_escolhida, )))
        

        for i in range(len(t)):
            t[i].start()
        for i in range(len(t)):
            t[i].join()

        apresentar_resultados(lista_palavras)

        if s_segundos != 0:
            file_completo_incompleto()
    
    fim_programa=datetime.datetime.now()
    tempo_exec_programa=fim_programa-tempo_start #PARA O FICHEIRO DO -O

    if nome_file_historico != 0:
        with open(nome_file_historico,"r") as f:
            linhas = f.readlines()
        linhas[1] = stringToBinary("Duração da execução: " + str(tempo_exec_programa))+ "\n"
        with open(nome_file_historico,"w") as f:
            for linha in linhas:
                f.write(str(linha))


def apresentar_resultados(lista_palavras): #o print q o processo pai faz no fim com os resultados finais
    """Função que acede ao array de shared memory e faz print das ocorrencias/linhas das palavras da lista_palavras nos ficheiros.

    Args:
        lista_palavras (list): lista das palavras inseridas na linha de comandos
    """
    for i in range(len(lista_palavras)):
        print(str(lista_palavras[i]) + ": "+ str(resultado[i]) + ";")

def info_inicial_historico(): #Só entra nesta função se o nome_file_historico != 0
    """Função que escreve no ficheiro indicado pela opção -o (opcional) a informação inicial relevante para o historico de execução do programa.
    """
    global nome_file_historico
    global data
    global n_processos 
    global opcao_a_sim_nao
    global s_segundos
  
    with open(nome_file_historico,"w") as f:
        f.write(stringToBinary("Início da execução da pesquisa: " + str(data[0]) + "/" + str(data[1]) + "/" + str(data[2]) + ", " + str(data[3]) + ":" + str(data[4]) + ":" + str(data[5]) + ":" + str(data[6]) )+"\n")
        f.write("Duração da execução: "+"\n")
        f.write(stringToBinary("Número de processos filhos: " + str(n_processos) )+"\n")
        f.write(stringToBinary("Opção -a ativada: " + opcao_a_sim_nao )+"\n")
        f.write(stringToBinary("Emissão de alarmes no intervalo de: " + str(s_segundos) + " segundos ")+"\n")


def stringToBinary(s):
    """Função que converte uma string em binário.
    a função será chamada quando ocorrer um WRITE de alguma informação para o ficheiro indicado pela opção -o

    Args:
        s (str): a string que desejamos converter
    Returns:
        [binario]: faz return do binario correspondente.
    """
    s_binary = ""
    for c in s:
        s_binary += format(ord(c), '08b')
    return(s_binary)


#-a verifica se TODAS as palavras estão na linha!
def pesquisaTodasPalavras(lista_palavras,linha):
    """ funcao que verifica se TODAS as palavras estão na linha (opcao -a ativa)

    Args:
        lista_palavras (list): lista de palavras a verificar
        linha (list): lista das palavras que corresponde a uma linha 

    Returns:
        [bool]: True se TODAS as palavras estão na linha
    """
    for palavra in lista_palavras:
        if palavra not in linha:
            return False
    return True



#-a não ativo
def pesquisaUmaPalavra(lista_palavras,linha):#APENAS UMA DAS PALAVRAS ESTÁ NA LINHA
    """ funcao que verifica se apenas uma das palavras estão na linha (opcao -a não está ativa)

    Args:
        lista_palavras (list): lista de palavras a verificar
        linha (list): lista das palavras que corresponde a uma linha 

    Returns:
        [bool]: True se apenas uma das palavras estão na linha
    """
    count=0
    for palavra in lista_palavras:
        if palavra in linha:
            count+=1
    return (count == 1) 
       


#-c (com -a ativo ou não)
def encontra_ocorrencias(lista_linhas,lista_palavras):
    """ Funcao que encontra as ocorrencias das palavras nas linhas e guarda os valores numa lista.

    Args:
        lista_linhas (list): lista de listas em que cada sublista contem as palavras de cada linha [[linha1],[linha2],[linha3]]
        lista_palavras (list): lista de palavras a pesquisar nas linhas

    Returns:
        [list]: lista com as ocorrencias de cada palavra nas linhas exemplo:[palavra1,palavra2]-----> [3,2] palavra1 = 3 ocorrencias; palavras2 = 2 ocorrencias
    """
    global nome_file_historico
    lista=[0] * len(lista_palavras) #lista com zeros [0] ou [0,0] ou [0,0,0] dependendo do nº de palavras da lista de palavras

    for linha in lista_linhas:
        for i in range(len(lista_palavras)):
            for word in linha:
                if lista_palavras[i] == word:
                    lista[i]+=1
    if nome_file_historico != 0:
        with open(nome_file_historico, "a") as f:

            for i in range(len(lista_palavras)):
                f.write(stringToBinary("       número de ocorrências da palavra " + str(lista_palavras[i]) + ": " + str(lista[i]))+"\n")
    return lista



#-l
def ocorrencia_linhas(arg_a,lista_linhas,lista_palavras):
    """Funcao que conta o numero de linhas em que existe ocorrencia de certas palavras. Se o argumento -a estiver ativo o numero de linhas corresponde ao numero de linhas
    da lista_linhas 

    Args:
        arg_a (bool): se a opção -a estiver ativa arg_a=True; caso contrario False
        lista_linhas (list): lista de listas em que cada sublista contem as palavras de cada linha [[linha1],[linha2],[linha3]]
        lista_palavras (list): lista de palavras a pesquisar nas linhas

    Returns:
        [lista]: numero de linhas em que existe ocorrencia de certas palavras. exemplo:[palavra1,palavra2]-----> [3,2] palavra1 = 3 linhas; palavras2 = 2 linhas
    """
    lista=[0] * len(lista_palavras)
    if arg_a:

        if nome_file_historico != 0:
            with open(nome_file_historico, "a") as f:
                for i in range(len(lista_palavras)):
                    f.write(stringToBinary("       número de ocorrências da palavra " + str(lista_palavras[i]) + ": " + str(len(lista_linhas)))+"\n")


        return [len(lista_linhas)] * len(lista_palavras)
    else:
        for linha in lista_linhas:
            for i in range(len(lista_palavras)):
                if lista_palavras[i] in linha:
                    lista[i]+=1

        if nome_file_historico != 0:
            with open(nome_file_historico, "a") as f:
                for i in range(len(lista_palavras)):
                    f.write(stringToBinary("       número de ocorrências da palavra " + str(lista_palavras[i]) + ": " + str(lista[i]))+"\n")


        return lista
    


#-----------------------------------------------------------------
def main():
    """funcao onde se recebem os argumentos da linha de comandos para a estruturacao do codigo.
    """
    global resultado
    global lista_palavras
    global n_processos
    global opcao_a_sim_nao
    global s_segundos
    global nome_file_historico
    lista_inicial=sys.argv
    lista_inicial= lista_inicial[1:] # remover python3 nome
    lista_argumentos=[]
    
    if "-f" not in sys.argv:
        lista_ficheiros=(input("Insira os ficheiros onde pretende procurar:")).split(" ")


    for i in range(len(sys.argv)): #! -f feito !
            
        if "-f" == sys.argv[i]:
            lista_ficheiros = sys.argv[i+1:] #Lista dos ficheiros introduzidos pelo utilizador
            lista_argumentos += sys.argv[i:] #Retirar da lista de argumentos do comando todos os argumentos até ficar apenas com as palavras
        
        if "-p" == sys.argv[i]:
            n = int(sys.argv[i+1])
            lista_argumentos += sys.argv[i:i+2]
            n_processos = n

        if "-w" == sys.argv[i]: #OPCAO -W s (s=intervalo de tempo)
            s = int(sys.argv[i+1])
            s_segundos = s
            lista_argumentos += sys.argv[i:i+2]
            #signal.alarm(s) #ALARME que acciona apos s segundos
            signal.signal(signal.SIGALRM, tempo)  #quando o alarme for accionado a função tempo executa
            signal.setitimer(signal.ITIMER_REAL, s, s)
        

        if "-o" == sys.argv[i]: #OPCAO -O (historico = file para guardar historico de execução do programa)
            historico = sys.argv[i+1]
            lista_argumentos += sys.argv[i:i+2]
            nome_file_historico= historico
            
 
    

    if "-p" not in sys.argv:
        n = 0
        n_processos = n

    if "-w" not in sys.argv:
        s=0

    if "-o" not in sys.argv:
        historico=0
        nome_file_historico=0
        

    if lista_ficheiros == []:
        lista_ficheiros=(input("Insira os ficheiros onde pretende procurar:")).split(" ") 
    
    if check_ficheiro_existe(lista_ficheiros) == False:
        return #caso a pessoa meta um ficheiro q nao existe


    if "-a" in sys.argv:
        arg_a=True
        opcao_a_sim_nao = "Sim"
        lista_argumentos.append("-a") #assumindo que o -a estaria na primeira posição do comando...
        if "-c" in sys.argv:
            opcao_escolhida="-c"
            lista_argumentos.append(opcao_escolhida)
            lista_palavras=[x for x in lista_inicial if x not in lista_argumentos]
            lista_palavras_filtrada=filtrar_palavras(lista_palavras)
            resultado = Array("i",[0]*len(lista_palavras) )
            criar_processos(lista_ficheiros,lista_palavras_filtrada,arg_a,opcao_escolhida,n)
            
        if "-l" in sys.argv:
            opcao_escolhida="-l"
            lista_argumentos.append(opcao_escolhida)
            lista_palavras=[x for x in lista_inicial if x not in lista_argumentos]
            lista_palavras_filtrada=filtrar_palavras(lista_palavras)
            resultado = Array("i",[0]*len(lista_palavras) )
            criar_processos(lista_ficheiros,lista_palavras_filtrada,arg_a,opcao_escolhida,n)
    else:
        arg_a=False
        opcao_a_sim_nao = "Não"

        if "-c" in sys.argv:
            opcao_escolhida="-c"
            lista_argumentos.append(opcao_escolhida)
            lista_palavras=[x for x in lista_inicial if x not in lista_argumentos]
            lista_palavras_filtrada=filtrar_palavras(lista_palavras)
            resultado = Array("i",[0]*len(lista_palavras) )
            criar_processos(lista_ficheiros,lista_palavras_filtrada,arg_a,opcao_escolhida,n)

        if "-l" in sys.argv:
            opcao_escolhida="-l"
            lista_argumentos.append(opcao_escolhida)
            lista_palavras=[x for x in lista_inicial if x not in lista_argumentos]
            lista_palavras_filtrada=filtrar_palavras(lista_palavras) #retira pontuação das palavras
            resultado = Array("i",[0]*len(lista_palavras) )
            criar_processos(lista_ficheiros,lista_palavras_filtrada,arg_a,opcao_escolhida,n)
            
    
    
if __name__ == "__main__":
    tempo_start=datetime.datetime.now() #2021-12-08 15:21:43.948792
    data=[tempo_start.day,tempo_start.month, tempo_start.year,tempo_start.hour,tempo_start.minute,tempo_start.second,tempo_start.microsecond]
    tempo_exec_programa=0 #inicializar como var global
    resultado = Array("i", [0]) #CRIAR UM ARRAY ACESSIVEL POR SHARED MEMORY!
    stop = False #var global
    n_processos = 0
    opcao_a_sim_nao = ""
    s_segundos = 0
    nome_file_historico = ""
    lista_palavras=[]
    n_processos_files2=[] #var global
    lista_ficheiros_indice=[] #[(FICHEIRO1,0),(FICHEIRO2,1),...]
    ocorrencias_ficheiros=Manager().list() #LISTA SHARED MEMORY!
    mutex = Lock() 
    signal.signal(signal.SIGINT, terminar_processos_CTRLC) #qnd se clica no CTRL-C faz função terminar_processos
    signal.signal(signal.SIGPIPE,signal.SIG_DFL)#Para o erro BROKEN PIPE NÃO OCORRER
    
    main()
    


    
        