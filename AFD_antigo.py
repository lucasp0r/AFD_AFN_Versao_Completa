if __name__ == '__main__':

    # Abrindo arquivo tipo .afd em modo leitura:
    arq = open("Exemplo.afd", 'r') # <<< INSIRA AQUI O NOME DO ARQUIVO QUE SE DESEJA LER:
    # passando todoS o conteudo do arquivo pra uma unica string:
    todo_texto = arq.read()
    arq.close()
    # lista de string onde cada linha é um item da lista:
    linhas = todo_texto.split("\n")
    F_prog = []

    # Acessando cada item da lista "linhas": linhas[0] = primeira linha...
    for i in range(0,len(linhas)-1):
        if i == 0:
            E_in = linhas[i]                # Estado Inicial

        if i == 1:
            Conj_E = linhas[i].split(" ")   # Conjunto de estados
            num_E = int(Conj_E[0])          # Numero de estados
            del(Conj_E[0])

        if i == 2:
            E_fim = linhas[i].split(" ")    # Conjunto estados finais
            num_Ef = int(E_fim[0])          # Numero de estados finais
            del(E_fim[0])

        if i == 3:
            Alf = linhas[i].split(" ")      # Conjunto alfabeto
            tam_Af = int(Alf[0])            # Tamanho alfabeto
            del(Alf[0])

        if i == 4:
            qtd_trans = int(linhas[i])      # Quantidade transiçoes

        if i > 4:                           # Função programa:
            F_prog.append(linhas[i].split(" "))

    del(todo_texto)
    del(linhas)

    print("AFD M = (", Alf,",",Conj_E,", Fc_Prog,",E_in,",",E_fim,")")  # Printando a 5-upla do Autômato
    print("Fc_Prog = {")
    for i in range(0, len(F_prog)):                                     # Printando a Fç Programa
        print("\t", F_prog[i])
    print("\t}")

    palavra = input("Digite a palavra que deseja testar: ")
    print()

    E_atual = E_in
    print("O estado inicial eh:",E_atual)
    Resultado = 0

    if len(palavra) == 0:               # Testando se a palavra vazia faz parte da linguagem:
        aux = 0
        for q in E_fim:
            if E_atual == q:
                aux += 1
        if aux > 0:
            Resultado = 1
            print("A palavra vazia faz parte dessa linguagem.")
        else:
            Resultado = 0
            print("A palavra vazia nao faz parte dessa linguagem.")
    else:
        aux = 0
        for simbolo in palavra:             # Testa se todos os simbolos da palavra pertencem ao alfabeto
            for letra in Alf:
                if simbolo == letra:
                    aux += 1
        if aux == len(palavra):             # Todos os simbolos da palavra pertencem ao alfabeto de fato
            for i in range(0, len(palavra)):
                simbolo = palavra[i]
                teste_def = 0
                for trans in F_prog:    # Realizando as transições e verificando se o automato nao morre por indefinição
                    if E_atual == trans[0] and simbolo == trans[1]:
                        teste_def += 1
                        novo_estado = trans[2]
                        print("Esta no estado", E_atual,", le o simbolo '%s' vai para o estado" % simbolo,novo_estado)
                if teste_def == 0:
                    Resultado = 2
                E_atual = novo_estado
            if Resultado != 2:
                teste_fim = 0
                for q in E_fim:         # Testando se o estado de chegada após ler toda a palavra é um estado final
                    if E_atual == q:
                        teste_fim += 1
                if teste_fim > 0:
                    Resultado = 1
                else:
                    Resultado = 0
        else:
            Resultado = 3

    if Resultado == 0:                  # Possíveis Resultados para o teste:
        print("Palavra Rejeitada.\n")
    elif Resultado == 1:
        print("Palavra aceita.\n")
    elif Resultado == 2:
        print("Morte por indefinicao.\n")
    elif Resultado == 3:
        print("A palavra possui pelo menos um simbolo que nao pertence ao alfabeto.\n")

    print("**Minimizacao do Automato:**\n")
                                        # Pré-requisito para minimização: a função programa deve ser total
    if qtd_trans < (tam_Af * num_E):    # Verificando se Fç programa é total, caso não seja, fazer com que se torne um:
        Conj_E.append('d')
        aux = 0
        for q in Conj_E:
            for simbolo in Alf:
                for trans in F_prog:
                    if q == trans[0] and simbolo == trans[1]:
                        aux = 1
                if aux == 0:
                    F_prog.append([q, simbolo, Conj_E[len(Conj_E)-1]])
                aux = 0
        print("Novo conjunto de estados:")
        print(Conj_E)
        print()
        print("Funcao programa total:")
        print(F_prog)
        print()

    # Minimização:

    # Etapa 1 e Etapa 2: Construção tabela e Marcação dos estados triviamente não-equivalentes
    print("Etapa 1 e 2:")
    pares_NEq = []
    for i in range(0, len(Conj_E)-1):
        for j in range(1, len(Conj_E)):
            if(((Conj_E[i] in E_fim) and (Conj_E[j] not in E_fim)) or ((Conj_E[j] in E_fim) and (Conj_E[i] not in E_fim))) and i < j:
                pares_NEq.append([Conj_E[i],Conj_E[j]])
    print("Pares de Estados triviamente nao equivalentes:")
    print(pares_NEq)
    print()

    # Etapa 3: Marcação dos estados não-equivalentes
    print("Etapa 3: Marcacao dos estados nao-equivalentes")
    par = []
    p1 = []
    p2 = []
    lista_enc = []
    for i in range(0, len(Conj_E)-1):
        for j in range(1, len(Conj_E)):
            if Conj_E[i] != Conj_E[j] and i < j:
                par = [Conj_E[i], Conj_E[j]]
                if par not in pares_NEq:                        # Se o par não está marcado...
                    aux1 = 0
                    aux2 = 0
                    for simbolo in Alf:
                        for trans in F_prog:
                            if Conj_E[i] == trans[0] and simbolo == trans[1]:
                                p1.append(trans[2])
                                aux1 += 1
                            if Conj_E[j] == trans[0] and simbolo == trans[1]:
                                p2.append(trans[2])
                                aux2 += 1
                    for k in range(0, len(p1)):
                        if p1[k] == p2[k]:                                          # Se pu = pv
                            continue
                        elif p1[k] != p2[k] and ([p1[k], p2[k]]) not in pares_NEq:   # Se pu != pv e {pu,pv} nao esta marcado
                            if p1[k] < p2[k] and ([p1[k], p2[k], Conj_E[i], Conj_E[j]] not in lista_enc):
                                lista_enc.append([p1[k], p2[k], Conj_E[i], Conj_E[j]])
                            elif ([p1[k], p2[k], Conj_E[i], Conj_E[j]]) not in lista_enc:
                                lista_enc.append([p2[k], p1[k], Conj_E[i], Conj_E[j]])
                        elif p1[k] != p2[k] and ([p1[k], p2[k]]) in pares_NEq:      # Se pu != pv e {pu,pv} esta marcado
                            if ([Conj_E[i], Conj_E[j]]) not in pares_NEq:
                                pares_NEq.append([Conj_E[i], Conj_E[j]])
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

    print("Pares nao equivalentes")
    print(pares_NEq)
    print()
    for i in range(0, len(lista_enc)):
        print(lista_enc[i][0], lista_enc[i][1], "Ecabeca: ", lista_enc[i][2], lista_enc[i][3])
    print()

    # Etapa 4: Unificação dos estados Equivalentes
    print("Etapa 4: Unificacao dos estados Equivalentes\n")
    pares_todos = []
    for i in range(0, len(Conj_E)-1):               # Inclui todos os pares possíveis na lista:
        for j in range(1, len(Conj_E)):
            if i < j:
                pares_todos.append([Conj_E[i], Conj_E[j]])

    for aux in lista_enc:
        for par in pares_todos:
            if par not in pares_NEq:
                if (([aux[0], aux[1]] not in pares_NEq and par == ([aux[0], aux[1]])) or ([aux[1], aux[0]] not in pares_NEq and par == ([aux[1], aux[0]]))):

                    if((aux[0]+aux[1] or aux[1]+aux[0]) not in Conj_E):
                        Conj_E.append(aux[0]+aux[1])
                        if((aux[0] and aux[1]) in E_fim):
                            E_fim.append(aux[0]+aux[1])
                    if ((aux[2] + aux[3] or aux[3] + aux[2]) not in Conj_E):
                        Conj_E.append(aux[2]+aux[3])
                        if((aux[2] and aux[3]) in E_fim):
                            E_fim.append(aux[2] + aux[3])

                    for letra in Alf:
                        if ([aux[0]+aux[1], letra, aux[2]+aux[3]]) not in F_prog:
                            F_prog.append([aux[0]+aux[1], letra, aux[2]+aux[3]])

                    k = 0
                    j = len(F_prog)
                    for i in range(0,j-k):
                        while F_prog[i-k][0] == aux[0] or F_prog[i-k][0] == aux[1]:
                            del(F_prog[i-k])
                            k += 1
                    if (aux[0] and aux[1]) in Conj_E:
                        Conj_E.remove(aux[0])
                        if(aux[0] in E_fim):
                            E_fim.remove(aux[0])
                        Conj_E.remove(aux[1])
                        if (aux[1] in E_fim):
                            E_fim.remove(aux[1])

    # Etapa 5: Exclusão dos estados Inúteis
    print("Etapa 5: Exclusao dos estados Inuteis")
    for q in Conj_E:
        if q not in E_fim:
            Resultado = 0
            E_atual = q

            for i in range(0, len(F_prog)):
                if (E_atual == F_prog[i][0]):
                    for trans in F_prog:
                        if (E_atual == trans[0]):
                            for letra in Alf:
                                if E_atual == trans[0] and letra == trans[1]:
                                    E_atual = trans[2]
                                    if E_atual in E_fim:
                                        Resultado = 1

            if Resultado == 0:
                j = len(F_prog)
                m = 0
                for k in range(0, j):
                    if (q == F_prog[k-m][0] or q == F_prog[k-m][2]):
                        del (F_prog[k-m])
                        m += 1
                Conj_E.remove(q)

    print()
    print("Novo conjunto de estados")
    print(Conj_E)
    print("Nova funcao programa")
    print(F_prog)
    print("Conjunto Estados finais:")
    print(E_fim)
    
    A_min = open("AFD_min.afd", "w")

    A_min.write("%s\n" %E_in)

    A_min.write("%d " %len(Conj_E))
    for q in Conj_E:
        A_min.write("%s " %q)

    A_min.write("\n%d " %len(E_fim))
    for q in E_fim:
        A_min.write("%s " %q)

    A_min.write("\n%d " %len(Alf))
    for letra in Alf:
        A_min.write("%s " %letra)

    A_min.write("\n%d\n" %len(F_prog))
    for trans in F_prog:
        A_min.write("%s %s %s\n" %(trans[0], trans[1], trans[2]))

    A_min.close()
