import random

initcavaloC =int(input('em qual coluna vai começar: '))
initcavaloL =int(input('em qual linha vai começar: '))
print("PRIMEIRA CASA E A COLUNA E A SEGUNDA A LINHA")
print(f"posiçao inicial: {initcavaloC,initcavaloL}")
# vai armazena os valores iniciais
arm=[initcavaloC,initcavaloL]
# movimentos do cavalo
movimento = [[2,-1], [2,1], [-2,1], [-2,-1], [1,2], [1,-2], [-1,2], [-1,-2]]
#armazena os movimentos possiveis dada a posiçao do cavalo
lista=[]
#vai armazena onde o cavalo estar
onde=[]
onde.append([initcavaloC,initcavaloL])
# vai armazena os movimentos feitos
feito=[]
#valida os movimentos possiveis dada a posiçao do cavalo
def validar(dados):
    for i in range(8):
      moviexecut=dados[i]
      posiC=onde[0][0]
      posiL=onde[0][1]
      novoC = moviexecut[0] + posiC
      novoL = moviexecut[1] + posiL
      if 0< novoC and 0< novoL and 8>=novoC and 8>=novoL:
                novoC = novoC - posiC
                novoL = novoL - posiL
                lista.append([novoC,novoL])
    #print(f"movimento posiveis:{lista}")
    return 
#vai movimentar o cavalo
def movimentar(dados):                                                                                                                                                              #lv
  movimento=random.choice(dados)
  posiC=onde[0][0]
  posiL=onde[0][1]
  novoC=movimento[0] + posiC
  novoL=movimento[1] + posiL
  if 0< novoC and 0< novoL and 8>=novoC and 8>=novoL:
    if [novoC,novoL] not in feito:
     feito.append([novoC,novoL])
     onde.clear()
     onde.append([novoC,novoL])
     lista.clear()
     
    else:
         movimentar(lista)
  return 

#onde o codigo vai rodar
for i in range(10):
    
    validar(movimento)
    movimentar(lista)

    if arm in onde:
      print("CAVALO VOLTOU PARA POSIÇAO INICIAL")  
      break
else:
    print("CAVALO NAO CONSEGUIU VOLTAR")
print(f"movimentos feitos:{feito}")       


#verifica se o cavalo repetiu movimento
for i in range(len(feito)):
  for j in range(i + 1, len(feito)):
    if feito[i] == feito[j]:
      print(f"Listas iguais encontradas nos índices {i} e {j}: {feito[i]}")
else:
  print("NAO REPETIU MOVIMENTO")

                                                                                              