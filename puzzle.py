import copy
import time

class No:
    def __init__(self, estado, noPai, acao, profundidade = 1):
        self.estado = estado
        self.noPai = noPai
        self.acao = acao
        if profundidade == 0:
            self.profundidade = 0
        else:
            self.profundidade = noPai.profundidade + 1

class Puzzle:

    def achaEspacoVazio(self, estado):
        for i in range(len(estado)):
            if estado[i] == 0:
                return i
            
    def irDireita(self, estado, noAtual):
        i = self.achaEspacoVazio(estado)
        novoEstado = copy.deepcopy(estado)

        if i != 2 and i != 5 and i != 8:
            novoEstado[i] = novoEstado[i + 1]
            novoEstado[i + 1] = 0

        novoNo = No(novoEstado, noAtual, 'Direita')

        return novoNo
    
    def irEsquerda(self, estado, noAtual):
        i = self.achaEspacoVazio(estado)
        novoEstado = copy.deepcopy(estado)

        if i != 0 and i != 3 and i != 6:
            novoEstado[i] = novoEstado[i - 1]
            novoEstado[i - 1] = 0

        novoNo = No(novoEstado, noAtual, 'Esquerda')
        
        return novoNo
    
    def irCima(self, estado, noAtual):
        i = self.achaEspacoVazio(estado)
        novoEstado = copy.deepcopy(estado)

        if i > 2:
            novoEstado[i] = novoEstado[i - 3]
            novoEstado[i - 3] = 0

        novoNo = No(novoEstado, noAtual, 'Cima')
        
        return novoNo
    
    def irBaixo(self, estado, noAtual):
        i = self.achaEspacoVazio(estado)
        novoEstado = copy.deepcopy(estado)

        if i < 6:
            novoEstado[i] = novoEstado[i + 3]
            novoEstado[i + 3] = 0

        novoNo = No(novoEstado, noAtual, 'Baixo')

        return novoNo

    def buscaResultado(self, noAtual):
        resultado = []
        no = noAtual
        i = 0
        while no.acao:
            resultado.append(no.acao)
            no = no.noPai
            i += 1
        
        resultado.reverse()
        return resultado
    
    def expandir(self, estado, noAtual):
        acoes = []
        acoes.append(self.irCima(estado, noAtual))
        acoes.append(self.irBaixo(estado, noAtual))
        acoes.append(self.irDireita(estado, noAtual))
        acoes.append(self.irEsquerda(estado, noAtual))
        
        return acoes
    
def printResultados(resultado, tempo):
    if resultado:
        print(f'Caminho para o objetivo: {resultado}')
        print(f'Custo: {len(resultado)}')
        print(f'Nos explorados: {estadosExplorados}')
        print(f'Tempo total: {tempo}')

    else:
        print('Solucao nao encontrada')
    
def bfs(estadoIni, estadoAlvo):
    fila = []
    alcancado = {}
    aberto = {}
    puzzle = Puzzle()
    noRaiz = No(estadoIni, None, None, 0)
    profund = 0

    fila.append(noRaiz)
    aberto[str(noRaiz.estado)] = noRaiz.estado

    while len(fila) > 0:
        global estadosExplorados
        estadosExplorados += 1

        noAtual = fila.pop(0)

        estado = noAtual.estado
        alcancado[str(estado)] = estado
        aberto.pop(str(estado))

        if estadoAlvo == estado:
            return puzzle.buscaResultado(noAtual)
        
        acoes = puzzle.expandir(estado, noAtual)

        for i in acoes:
            if str(i.estado) not in alcancado and str(i.estado) not in aberto:
                fila.append(i)
                aberto[str(i.estado)] = i.estado

def dfs(estadoIni, estadoAlvo, limPassos = 30):
    
    def dfs_recusivo(noAtual, estadoAlvo, limPassos):
        global estadosExplorados
        estadosExplorados += 1

        if estadoAlvo == noAtual.estado:
            return puzzle.buscaResultado(noAtual)
        
        if noAtual.profundidade == limPassos:
            return False
        
        alcancado.append(noAtual.estado)

        for sucessor in reversed(puzzle.expandir(noAtual.estado, noAtual)):
            if sucessor.estado not in alcancado:
                resultado = dfs_recusivo(sucessor, estadoAlvo, limPassos)

                if resultado:
                    return resultado
                
        alcancado.pop()
        return False
        
    puzzle = Puzzle()
    noRaiz = No(estadoIni, None, None, 0)
    alcancado = []
    
    return dfs_recusivo(noRaiz, estadoAlvo, limPassos)

def idfs(estadoIni, estadoAlvo):

    i = 0
    while True:
        resultado = dfs(estadoIni, estadoAlvo, i)

        if resultado:
            return resultado
        
        i += 1
        
exemploInicial = [3,5,8,1,6,2,4,0,7]

estadoInicial2 = [0,8,7,6,5,4,3,2,1]

estadoAlvo = [0,1,2,3,4,5,6,7,8]

estadosExplorados = 0

tempo_inicio = time.time()
resultado = bfs(exemploInicial, estadoAlvo)
tempo_fim = time.time()

printResultados(resultado, tempo_fim - tempo_inicio)
    