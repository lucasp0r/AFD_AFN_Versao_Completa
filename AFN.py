if __name__ == '__main__':

    #Abrindo arquivo tipo .afn em modo leitura:
    arq = open("Exemplo.afn", 'r')
    #Passando todos o conteudo do arquivo pra uma unica string:
    todo_texto = arq.read()
    arq.close()
    #Lista de string onde cada linha é um item da lista:
    linhas = todo_texto.split("\n")
    F_prog = []

    #Acessando cada item da lista "linhas": linhas[0] = primeira linha...
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

        if i > 4:                           # F_prog = Função programa:
            F_prog.append(linhas[i].split(" "))

    del(todo_texto)
    del(linhas)

    
    Q = Conj_E              # Q = Conjunto de todos os possíveis novos estados
    F = E_fim               # F = CoConjunto de todos os possíveis novos estados finais

    for i in range(0, num_E):
        for j in range(1, num_E):
            if i < j:
                Q.append(Conj_E[i]+Conj_E[j])
                if ((Conj_E[i] or Conj_E[j]) in F):
                    F.append(Conj_E[i]+Conj_E[j])

                k = j + 1
                while k < num_E:
                    Q.append(Q[len(Q)-1]+Conj_E[k])
                    if ((Q[len(Q)-2] or Conj_E[k]) in F):
                        F.append(Q[len(Q)-2]+Conj_E[k])
                    k += 1
    print()
    print(Q)
    print(F)


    F_Prog_new = []     # Nova Função Programa
    Prog = {}           # Dicionário do tipo Prog[Sq1] = {S, q1}

    #Primeira transição: Estado Inicial lendo {a,b} = conjunto de novos estados
    E_atual = E_in
    Prog[E_atual] = E_atual
    for letra in Alf:
        aux = []
        for trans in F_prog:
            if E_atual == trans[0] and letra == trans[1]:
                aux.append(trans[2])
        if len(aux) >= 1:
            aux.sort()
            q_uniao = ''.join(aux)
            Prog[q_uniao] = aux
            F_Prog_new.append([E_atual, letra, q_uniao])


    for i in range(0, qtd_trans):
        abrev = list(Prog.keys())
        if (i <= len(abrev)):
            for q in abrev:
                for E_atual in Prog[q]:
                    for letra in Alf:
                        aux = []
                        for trans in F_prog:
                            if E_atual == trans[0] and letra == trans[1]:
                                aux.append(trans[2])
                        if len(aux) >= 1:
                            aux.sort()
                            q_uniao = ''.join(aux)

                            if (q_uniao not in Prog):
                                Prog[q_uniao] = aux
                            resultado = 0
                            for tr in F_Prog_new:
                                if q == tr[0] and letra == tr[1]:
                                    resultado = 1
                            if resultado == 0:
                                if (aux == Prog[q]):
                                    F_Prog_new.append([q, letra, q])
                                elif (len(aux) < len(Prog[q])):
                                    if (q_uniao not in Prog[q]):
                                        F_Prog_new.append([q, letra, q_uniao])
                                    else:
                                        F_Prog_new.append([q, letra, E_atual+q_uniao])
                                else:
                                    F_Prog_new.append([q, letra, q_uniao])


 #Exclusão dos estados Inúteis
    print("Exclusao dos estados Inuteis")
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




                

    F_prog = F_Prog_new
    del(F_Prog_new)
    Conj_E_new = []
    E_fim_new = []
    abrev = list(Prog.keys())
    for q in abrev:
        Conj_E_new.append(q)
        for aux in Prog[q]:
            if aux in E_fim:
                E_fim_new.append(q)

    Conj_E_new.sort()
    Conj_E = Conj_E_new
    del (Conj_E_new)
    E_fim_new.sort()
    E_fim = E_fim_new
    del (E_fim_new)

    print()
    print("Novo conjunto de estados")
    print(Conj_E)
    print("Nova funcao programa")
    print(F_prog)
    print("Conjunto Estados finais:")
    print(E_fim)


    AFD = open("AFN_p_AFD.afd", "w")

    AFD.write("%s\n" % E_in)

    AFD.write("%d " % len(Conj_E))
    for q in Conj_E:
        AFD.write("%s " % q)

    AFD.write("\n%d " % len(E_fim))
    for q in E_fim:
        AFD.write("%s " % q)

    AFD.write("\n%d " % len(Alf))
    for letra in Alf:
        AFD.write("%s " % letra)

    AFD.write("\n%d\n" % len(F_prog))
    for trans in F_prog:
        AFD.write("%s %s %s\n" % (trans[0], trans[1], trans[2]))

    AFD.close()

