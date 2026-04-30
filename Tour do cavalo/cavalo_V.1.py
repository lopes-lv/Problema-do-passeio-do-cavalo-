#falta adicionar para ele nao volta para as casas que ja foi
# e resolver bug de as vezes ele nao voltar para a casa inicial 

initcavaloC =1 #int(input('em qual coluna vai começar: '))
initcavaloL =3 #int(input('em qual linha vai começar: '))

# vai armazena os valores iniciais
arm=[initcavaloC,initcavaloL]




# movimentos possiveis 
movimento = [[2,-1], [2,1], [-2,1], [-2,-1], [1,2], [1,-2], [-1,2], [-1,-2]]
movimento1=movimento[::-1]

# vai armazena os movimentos feitos
lista=[]
fase=[]
erro=[]
# faz todos os moimentos que tem na lista e valida se sao possiveis e executa ate voltar a possiçao inicial
for i in range(8):
    moviexecut = movimento1[i]
    novoC = moviexecut[0] + initcavaloC
    novoL = moviexecut[1] + initcavaloL
    novoM=[novoC,novoL]
    erro.append(novoM)
    if 0< novoC and 0< novoL and 8>=novoC and 8>=novoL:
            initcavaloC= novoC
            initcavaloL= novoL
            lista.append([novoC,novoL])
            fase.append(f"fase{i}")
            # se o cavalo voltar para possiçao inicial ele para o codigo
            if arm in lista:
              break
print(lista)
print(fase)
print(erro)