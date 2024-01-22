from typing import Iterable, Set, Tuple
from collections import deque
from queue import PriorityQueue

def troca_char(indice_espaco_vazio:int,indice_vazio_novo:int, estado:str):
    temp_char = estado[indice_vazio_novo]
    novo_estado = list(estado)
    novo_estado[indice_vazio_novo] = "_"
    novo_estado[indice_espaco_vazio] = temp_char
        
    return ''.join(novo_estado)

def executa_movimento(estado:str, indice_espaco_vazio: int, movimento:str) -> str:
    if movimento == "acima":
        indice_vazio_novo = indice_espaco_vazio - 3
        
        if(indice_vazio_novo > -1): 
            return troca_char(indice_espaco_vazio, indice_vazio_novo, estado)
        else:
            return "invalid"
    elif movimento == "esquerda":
        indice_vazio_novo = indice_espaco_vazio - 1   
          
        if(indice_vazio_novo > -1 and indice_vazio_novo // 3 == indice_espaco_vazio // 3): 
            return troca_char(indice_espaco_vazio, indice_vazio_novo, estado)
        else:
            return "invalid"
    elif movimento == "direita":
        indice_vazio_novo = indice_espaco_vazio + 1           
        
        if(indice_vazio_novo < 9 and indice_vazio_novo // 3 == indice_espaco_vazio // 3): 
            return troca_char(indice_espaco_vazio, indice_vazio_novo, estado)
        else:
            return "invalid"
    else:
        indice_vazio_novo = indice_espaco_vazio + 3        
        
        if(indice_vazio_novo < 9): 
            return troca_char(indice_espaco_vazio, indice_vazio_novo, estado)
        else:
            return "invalid"
        
def hamming(estado:str) -> int:
    estado_objetivo = '12345678_'
    acc_atual = 0
    
    for i in range(9):
        if estado[i] != estado_objetivo[i]:
            acc_atual += 1
    
    return acc_atual

def manhattan(estado:str) -> int:
    estado_objetivo = '12345678_'
    acc_atual = 0
    
    acc_atual = acc_atual +abs(estado.find("1") - 0)
    acc_atual = acc_atual +abs(estado.find("2") - 1)
    acc_atual = acc_atual +abs(estado.find("3") - 2)
    acc_atual = acc_atual +abs(estado.find("4") - 3)
    acc_atual = acc_atual +abs(estado.find("5") - 4)
    acc_atual = acc_atual +abs(estado.find("6") - 5)
    acc_atual = acc_atual +abs(estado.find("7") - 6)
    acc_atual = acc_atual +abs(estado.find("8") - 7)
    acc_atual = acc_atual +abs(estado.find("_") - 8)
    
    return acc_atual


class Nodo:
    """
    Implemente a classe Nodo com os atributos descritos na funcao init
    """
    def __init__(self, estado:str, pai, acao:str, custo:int):
        """
        Inicializa o nodo com os atributos recebidos
        :param estado:str, representacao do estado do 8-puzzle
        :param pai:Nodo, referencia ao nodo pai, (None no caso do nó raiz)
        :param acao:str, acao a partir do pai que leva a este nodo (None no caso do nó raiz)
        :param custo:int, custo do caminho da raiz até este nó
        """
        # substitua a linha abaixo pelo seu codigo
        self.estado = estado
        self.acao = acao
        if (pai):
            self.pai = pai
            self.custo = pai.custo + 1
        else:
            self.custo = custo
            self.pai = None
        
    def __hash__(self):
        return hash(self.estado)
    
    def __eq__(self, other):
        return self.estado == other.estado
    
    def __str__(self):
        return f'Nodo: {self.estado},({self.pai}),{self.acao},{self.custo}'
    
    def __lt__(self, other):
        return (hamming(self.estado) < hamming(other.estado)) 

def sucessor(estado:str)->Set[Tuple[str,str]]:
    """
    Recebe um estado (string) e retorna um conjunto de tuplas (ação,estado atingido)
    para cada ação possível no estado recebido.
    Tanto a ação quanto o estado atingido são strings também.
    :param estado:
    :return:
    """
    lista_retorno = []
    movimentos_possiveis = ["acima", "esquerda", "direita", "abaixo"]
    indice_espaco_vazio = estado.find("_")
    
    for movimento in movimentos_possiveis:
        estado_retorno = executa_movimento(estado, indice_espaco_vazio, movimento)
        
        if(estado_retorno != "invalid"):
            lista_retorno.append((movimento,estado_retorno))    
    return lista_retorno


def expande(nodo:Nodo)->Set[Nodo]:
    """
    Recebe um nodo (objeto da classe Nodo) e retorna um conjunto de nodos.
    Cada nodo do conjunto é contém um estado sucessor do nó recebido.
    :param nodo: objeto da classe Nodo
    :return:
    """
    lista_retorno = []
    if(nodo.estado == "12345678_"):
        return lista_retorno
    for item in sucessor(nodo.estado):
        nodo_atual = Nodo(item[1],nodo,item[0],nodo.custo)
        lista_retorno.append(nodo_atual)
    return lista_retorno


def astar_hamming(estado:str)->list[str]:
    """
    Recebe um estado (string), executa a busca A* com h(n) = soma das distâncias de Hamming e
    retorna uma lista de ações que leva do
    estado recebido até o objetivo ("12345678_").
    Caso não haja solução a partir do estado recebido, retorna None
    :param estado: str
    :return:
    """
    estado_objetivo = "12345678_"
    primeiro_nodo = Nodo(estado,None,"abaixo",0)
    x = []    
    f = PriorityQueue()
    f.put((primeiro_nodo.custo, primeiro_nodo))
    i = 0
    while(i < 10000):
        if f.qsize() == 0:
            return None
        estado_atual = f.get()[1]
        if(estado_atual.estado == estado_objetivo):
            lista_acoes = deque()
            nodo_atual = estado_atual
            while(nodo_atual.pai):
                lista_acoes.appendleft(nodo_atual.acao)
                nodo_atual = nodo_atual.pai                
            return list(lista_acoes)
        if(estado_atual not in x):            
            x.append(estado_atual)    
            for u in expande(estado_atual): 
                if(u not in x):
                    custo_total = u.custo + hamming(u.estado)
                    f.put((custo_total, u))
        i = i + 1



def astar_manhattan(estado:str)->list[str]:
    """
    Recebe um estado (string), executa a busca A* com h(n) = soma das distâncias de Manhattan e
    retorna uma lista de ações que leva do
    estado recebido até o objetivo ("12345678_").
    Caso não haja solução a partir do estado recebido, retorna None
    :param estado: str
    :return:
    """
    estado_objetivo = "12345678_"
    primeiro_nodo = Nodo(estado,None,"abaixo",0)
    x = []    
    f = PriorityQueue()
    f.put((primeiro_nodo.custo, primeiro_nodo))
    i = 0
    while(i < 10000):
        if f.qsize() == 0:
            return None
        estado_atual = f.get()[1]
        if(estado_atual.estado == estado_objetivo):
            lista_acoes = deque()
            nodo_atual = estado_atual
            while(nodo_atual.pai):
                lista_acoes.appendleft(nodo_atual.acao)
                nodo_atual = nodo_atual.pai                
            return list(lista_acoes)
        if(estado_atual not in x):            
            x.append(estado_atual)    
            for u in expande(estado_atual): 
                if(u not in x):
                    custo_total = u.custo + manhattan(u.estado)
                    f.put((custo_total, u))
        i = i + 1

#opcional,extra
def bfs(estado:str)->list[str]:
    """
    Recebe um estado (string), executa a busca em LARGURA e
    retorna uma lista de ações que leva do
    estado recebido até o objetivo ("12345678_").
    Caso não haja solução a partir do estado recebido, retorna None
    :param estado: str
    :return:
    """
    # substituir a linha abaixo pelo seu codigo
    raise NotImplementedError

#opcional,extra
def dfs(estado:str)->list[str]:
    """
    Recebe um estado (string), executa a busca em PROFUNDIDADE e
    retorna uma lista de ações que leva do
    estado recebido até o objetivo ("12345678_").
    Caso não haja solução a partir do estado recebido, retorna None
    :param estado: str
    :return:
    """
    # substituir a linha abaixo pelo seu codigo
    raise NotImplementedError

#opcional,extra
def astar_new_heuristic(estado:str)->list[str]:
    """
    Recebe um estado (string), executa a busca A* com h(n) = sua nova heurística e
    retorna uma lista de ações que leva do
    estado recebido até o objetivo ("12345678_").
    Caso não haja solução a partir do estado recebido, retorna None
    :param estado: str
    :return:
    """
    # substituir a linha abaixo pelo seu codigo
    raise NotImplementedError
