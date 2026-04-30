import time

initC=int(input("Digite onde o cavalo vai começar \nComeçando pela coluna e depois a linha:\n"))-1
initL=int(input())-1
pos_atual=[] #sempre ira armazenar onde o cavalo esta naquele momento 
casas_visitadas=[]
movimentos_feitos=0
inicio=time.time()
# validação se os numeros estão corretos 
if(initC >7 or initC <0 or initL>7 or initL<0):
    print("Os valores não são aceitaveis \nDigite apenas numeros entre 1 a 8")
pos_atual=[initC,initL]
print(f"pos atual {pos_atual}")
# movimentos possiveis do cavalo
movimento = [[2,-1], [2,1], [-2,1], [-2,-1], [1,2], [1,-2], [-1,2], [-1,-2]]
cavalo="♞"




def mostrar_posição(posicaoC,posicaoL):
    for l in range(0,8):
        print("\n")
        for c in range(0,8):
            if(c==posicaoC and l==posicaoL):print(f"  {cavalo} ",end="")
            else: print(" ⬜ ",end="")
    print("\n======================================\n")
    return 

mostrar_posição(pos_atual[0],pos_atual[1])


def validar_movimento(movimento):
    
    movimentos_possiveis=[]
    numeros=[]

    for i in range(8):
        
        novoC=pos_atual[0]+movimento[i][0]
        novoL=pos_atual[1]+movimento[i][1]
        
        if(novoC>=0 and novoC<8 and novoL>=0 and novoL<8):
            if([novoC,novoL] not in casas_visitadas):
                movimentos_possiveis.append([movimento[i][0],movimento[i][1]])
                quantidade=numero_movi(movimento[i][0],movimento[i][1],movimento)
                numeros.append(quantidade)
    movimentos_possiveis.sort(key=lambda m: numero_movi(pos_atual[0] + m[0], pos_atual[1] + m[1], movimento))
    return movimentos_possiveis

def numero_movi(pos1,pos2,movimento):
    movimentos_posiveis=[]
    for i in range(8):
        novoC=pos1+movimento[i][0]
        novoL=pos2+movimento[i][1]
        
        if(novoC>=0 and novoC<8 and novoL>=0 and novoL<8):
            if([novoC,novoL] not in casas_visitadas):
                movimentos_posiveis.append([movimento[i][0],movimento[i][1]])
    return len(movimentos_posiveis)

# a função deve pega o novo possivel movimento e ver quantos os possiveis aquela casa vai poder fazer#

def movimentar(movimento_fazer):
    global pos_atual
    global movimentos_feitos
    
    movimentos_feitos+=1

    novoc=movimento_fazer[0]
    novol=movimento_fazer[1]
    nova_pos=[pos_atual[0]+novoc,pos_atual[1]+novol]
    casas_visitadas.append(nova_pos)
    pos_atual[0]=nova_pos[0]
    pos_atual[1]=nova_pos[1]
    mostrar_posição(pos_atual[0],pos_atual[1])
    #time.sleep(0.5)

    
    
    return
     
def executar(movimento_possiveis):
   global pos_atual
   
   if(len(movimento_possiveis)==0):
       return False
   else:
        for i in range(len(movimento_possiveis)):
            pos_anterior=[pos_atual[0],pos_atual[1]]
            movimentar(movimento_possiveis[i])
            if(len(casas_visitadas)==64):return True
            bol=executar(validar_movimento(movimento))    
            if(bol==True):return True
            else:
                pos_atual=pos_anterior
                casas_visitadas.pop()
        return False

executar(validar_movimento(movimento))
fim=time.time()

print(f"A quantidade de movimentos feitos foi: {movimentos_feitos}\nO tempo de duração foi de: {fim-inicio}")
print(casas_visitadas)
