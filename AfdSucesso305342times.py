if __name__ == '__main__':
     #Abertura Arquivo
    #Informe o nome do Arquivo para Leitura do Compilador:
    arq = open("Exemplo.afd", 'r') 
    #Inclui AFD na String
    todo_texto = arq.read()
    arq.close()
    #String list, cada linha 1 item.
    linhas = todo_texto.split("\n")
    FuncaoPrograma = []

    #Acessando todos items da lista por linha.
    for i in range(0,len(linhas)-1):
        if i == 0:
            #Estado Inicial
            EstadoI = linhas[i]                

        if i == 1:
            #Conjunto de Estados
            ConjuntoE = linhas[i].split(" ")
            #Contador Estados
            ContadorE = int(ConjuntoE[0])          
            del(ConjuntoE[0])

        if i == 2:
            #Conjunto EstadoFinal
            EstadoFinal = linhas[i].split(" ")    
            #Contador EstadoFinal
            ContadorEF = int(EstadoFinal[0])          
            del(EstadoFinal[0])

        if i == 3:
            #Conjunto alfabeto
            Alfabeto = linhas[i].split(" ")      
            #Contador Alfabeto
            ContadorAlf = int(Alfabeto[0])            
            del(Alfabeto[0])
        #Contador Transição
        if i == 4:
            ContadorTrans = int(linhas[i])      
        #Função programa:
        if i > 4:                           
            FuncaoPrograma.append(linhas[i].split(" "))
    del(todo_texto)
    del(linhas)

    
    #Congela 5 atributo AFD
    print("DEFINIÇÃO AFD --  M = \n ( Alfabeto > ", Alfabeto,", \n \n Conjuntos > ", ConjuntoE,",  \n \n  FunçãoPrograma(Exibirá abaixo) \n \n  Estado Inicial > ", EstadoI,", \n \n Estado Final > ",EstadoFinal,")")  
    print(" \n \n FunctProgramaExib = {")
    
    #Congela palavra Vazia
    for i in range(0, len(FuncaoPrograma)):                                     
        print("\t", FuncaoPrograma[i])
    print("\t}")

    palavra = input("DIGITE A PALAVRA PARA TESTE ")
    print()

    E_atual = EstadoI
    print("O ESTADO INICIAL É: ",E_atual)
    Resultado = 0
    #Teste palavra vazia:
    if len(palavra) == 0:               
        aux = 0
        for q in EstadoFinal:
            if E_atual == q:
                aux += 1
        if aux > 0:
            Resultado = 1
            print("VAZIA ESTÁ CONTIDA NA LINGUAGEM.")
        else:
            Resultado = 0
            print("VAZIA NAO ESTA NA LINGUAGEM.")
    else:
        aux = 0
        #http://www.pythondiario.com/2015/06/afd-en-python-automata-finito.html
        #Teste todos simbolos da palavra inserida, se esta contida no alfabeto
        for simbolo in palavra:             
            for letra in Alfabeto:
                if simbolo == letra:
                    aux += 1
        #Todos simbolos existentes no alfabeto
        if aux == len(palavra):             
            for i in range(0, len(palavra)):
                simbolo = palavra[i]
                TesteDefinicao = 0
                #http://www.pythondiario.com/2015/06/afd-en-python-automata-finito.html
                #Faz Transição, verifica se cai por indefinição
                for trans in FuncaoPrograma:    
                    if E_atual == trans[0] and simbolo == trans[1]:
                        TesteDefinicao += 1
                        novo_estado = trans[2]
                        print("Esta no estado", E_atual,", le o simbolo '%s' vai para o estado" % simbolo,novo_estado)
                if TesteDefinicao == 0:
                    Resultado = 2
                E_atual = novo_estado
            if Resultado != 2:
                teste_fim = 0
                #Verifica se Estado atual é Estado Final
                for q in EstadoFinal:         
                    if E_atual == q:
                        teste_fim += 1
                if teste_fim > 0:
                    Resultado = 1
                else:
                    Resultado = 0
        else:
            Resultado = 3
    #Testes:
    if Resultado == 0:                  
        print(" PALAVRA NAO PASSA ")
    if Resultado == 1:
        print(" PALAVRA PASSA COM SUCESSO \n ")
    if Resultado == 2:
        print(" CAI POR INDEFINIÇÃO ")
    if Resultado == 3:
        print("  PALAVRA POSSUI UM OU MAIS SIMBOLOS FORA DO ALFABETO [Execute o Programa Novamente] \n")



    #KWARGS - DESCOMPACTA
    print("**Minimiza AFD:**\n")

   #https://github.com/vicmarbe/pytomata/blob/master/pytomata.py                                       
   #Função programa deve ser total para minimização
   #Verifica se função programa é total, se não transforma.
    if ContadorTrans < (ContadorAlf * ContadorE):    
        ConjuntoE.append('')
        aux = 0
        for q in ConjuntoE:
            for simbolo in Alfabeto:
                for trans in FuncaoPrograma:
                    if q == trans[0] and simbolo == trans[1]:
                        aux = 1
                if aux == 0:
                    FuncaoPrograma.append([q, simbolo, ConjuntoE[len(ConjuntoE)-1]])
                aux = 0
        print("CONJUNTO DE ESTADOS:")
        print(ConjuntoE)
        print()
        print("TODAS AS TRANSIÇÕES:")
        print(FuncaoPrograma)
        print()

    #http://www.decom.ufop.br/anderson/BCC242/MinimizacaoDeAFD.pdf
    #https://github.com/vicmarbe/pytomata/blob/master/pytomata.py
    #Step 1/2 : Cria Tabela e Marca estados normalmente não Equivalentes 
    print(" Step 1/2 : CRIA TABELA E MARCA ESTADOS NORMALMENTE NÃO EQUIVALENTES  \n")
    pares_NEq = []
    for i in range(0, len(ConjuntoE)-1):
        for j in range(1, len(ConjuntoE)):
            if(((ConjuntoE[i] in EstadoFinal) and (ConjuntoE[j] not in EstadoFinal)) or ((ConjuntoE[j] in EstadoFinal) and (ConjuntoE[i] not in EstadoFinal))) and i < j:
                pares_NEq.append([ConjuntoE[i],ConjuntoE[j]])
    print(" PARES DE ESTADOS TRIVIAMENTES NÃO EQUIVALENTES: \n")
    print(pares_NEq)
    print()
    #http://www.decom.ufop.br/anderson/BCC242/MinimizacaoDeAFD.pdf
    #https://github.com/vicmarbe/pytomata/blob/master/pytomata.py
    #Step 3: Marca estados não equivalentes 
    print(" Step 3: MARCA ESTADOS NÃO EQUIVALENTES \n ")
    par = []
    p1 = []
    p2 = []
    lista_enc = []
    for i in range(0, len(ConjuntoE)-1):
        for j in range(1, len(ConjuntoE)):
            if ConjuntoE[i] != ConjuntoE[j] and i < j:
                par = [ConjuntoE[i], ConjuntoE[j]]
                #Se par não marca - nos pares não equivalentes.
                if par not in pares_NEq:                        
                    aux1 = 0
                    aux2 = 0
                    for simbolo in Alfabeto:
                        for trans in FuncaoPrograma:
                            if ConjuntoE[i] == trans[0] and simbolo == trans[1]:
                                p1.append(trans[2])
                                aux1 += 1
                            if ConjuntoE[j] == trans[0] and simbolo == trans[1]:
                                p2.append(trans[2])
                                aux2 += 1
                    for k in range(0, len(p1)):
                        #Se pu = pv
                        if p1[k] == p2[k]:                                          
                            continue
                        #Se pu != pv e {pu,pv} Não Marca
                        elif p1[k] != p2[k] and ([p1[k], p2[k]]) not in pares_NEq:   
                            if p1[k] < p2[k] and ([p1[k], p2[k], ConjuntoE[i], ConjuntoE[j]] not in lista_enc):
                                lista_enc.append([p1[k], p2[k], ConjuntoE[i], ConjuntoE[j]])
                            elif ([p1[k], p2[k], ConjuntoE[i], ConjuntoE[j]]) not in lista_enc:
                                lista_enc.append([p2[k], p1[k], ConjuntoE[i], ConjuntoE[j]])
                        #Se pu != pv e {pu,pv} Tem Marcação
                        elif p1[k] != p2[k] and ([p1[k], p2[k]]) in pares_NEq:     
                            if ([ConjuntoE[i], ConjuntoE[j]]) not in pares_NEq:
                                pares_NEq.append([ConjuntoE[i], ConjuntoE[j]])
                    p1.clear()
                    p2.clear()

    for i in range(0, len(lista_enc)):
        for aux in lista_enc:
            if (([aux[0], aux[1]]) or ([aux[1], aux[0]])) in pares_NEq:
                if ([aux[2], aux[3]]) not in pares_NEq:
                    pares_NEq.append([aux[2], aux[3]])
                else:
                    lista_enc.remove(aux)
            elif ([aux[2], aux[3]]) in pares_NEq:
                lista_enc.remove(aux)
    print(" PARES NÃO EQUIVALENTES  OU SEJA NÃO ESTÃO LIGADOS ATRAVÉS DE TRANSIÇÃO")
    print(pares_NEq)
    print()    
    #https://github.com/vicmarbe/pytomata/blob/master/pytomata.py
    #Step 4: Junção estados Equivalentes
    print(" Step 4: JUNÇÃO DOS ESTADOS EQUIVALENTES OU SEJA LIGADOS POR TRANSIÇÕES ")
    pares_todos = []
    #Pega lista de pares possíveis:
    for i in range(0, len(ConjuntoE)-1):               
        for j in range(1, len(ConjuntoE)):
            if i < j:
                pares_todos.append([ConjuntoE[i], ConjuntoE[j]])

    for aux in lista_enc:
        for par in pares_todos:
            if par not in pares_NEq:
                if (([aux[0], aux[1]] not in pares_NEq and par == ([aux[0], aux[1]])) or ([aux[1], aux[0]] not in pares_NEq and par == ([aux[1], aux[0]]))):

                    if((aux[0]+aux[1] or aux[1]+aux[0]) not in ConjuntoE):
                        ConjuntoE.append(aux[0]+aux[1])
                        if((aux[0] and aux[1]) in EstadoFinal):
                            EstadoFinal.append(aux[0]+aux[1])
                    if ((aux[2] + aux[3] or aux[3] + aux[2]) not in ConjuntoE):
                        ConjuntoE.append(aux[2]+aux[3])
                        if((aux[2] and aux[3]) in EstadoFinal):
                            EstadoFinal.append(aux[2] + aux[3])

                    for letra in Alfabeto:
                        if ([aux[0]+aux[1], letra, aux[2]+aux[3]]) not in FuncaoPrograma:
                            FuncaoPrograma.append([aux[0]+aux[1], letra, aux[2]+aux[3]])

                    k = 0
                    #Len Pega tamanho da String
                    j = len(FuncaoPrograma)
                    for i in range(0,j-k):
                        while FuncaoPrograma[i-k][0] == aux[0] or FuncaoPrograma[i-k][0] == aux[1]:
                            del(FuncaoPrograma[i-k])
                            k += 1
                    #if (aux[0] and aux[1]) in ConjuntoE:
                        #ConjuntoE.remove(aux[0])
                        #if(aux[0] in EstadoFinal):
                         #   EstadoFinal.remove(aux[0])
                        #ConjuntoE.remove(aux[1])
                        #if (aux[1] in EstadoFinal):
                         #   EstadoFinal.remove(aux[1])
                            
    print()
    print("NOVO CONJUNTO DE ESTADOS")
    print(ConjuntoE)
    print("NOVA FUNCAO PROGRAMA")
    print(FuncaoPrograma)
    print("RESULTADO DE CONJUNTO FINAIS:")
    print(EstadoFinal)
