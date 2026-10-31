# @unisenac BFS, DFS, gulosa e Dijkstra no grafo do prédio. Todas devolvem (caminho, custo, visitados)
import heapq
from collections import deque


# @unisenac volta pelas anotações de "de onde cheguei" até a origem e inverte a lista
def montar_caminho(anterior, origem, destino):
    caminho = [destino]
    while caminho[-1] != origem:
        caminho.append(anterior[caminho[-1]])
    caminho.reverse()
    return caminho


# @unisenac o custo não fica no grafo: é a soma dos pesos das arestas do caminho
def calcular_custo(grafo, caminho):
    custo = 0
    for a, b in zip(caminho, caminho[1:]):
        custo += next(peso for vizinho, peso in grafo[a] if vizinho == b)
    return custo


# @unisenac BFS usa fila: explora por camadas, então acha o caminho com menos portas (ignora o peso)
def bfs(grafo, origem, destino):
    if origem == destino:
        return [origem], 0, 1
    anterior = {}
    # @unisenac conjunto de marcadas evita andar em círculo nos ciclos
    marcadas = {origem}
    fila = deque([origem])
    visitados = 0
    while fila:
        atual = fila.popleft()
        visitados += 1
        for vizinho, _ in grafo[atual]:
            if vizinho not in marcadas:
                marcadas.add(vizinho)
                anterior[vizinho] = atual
                if vizinho == destino:
                    visitados += 1
                    caminho = montar_caminho(anterior, origem, destino)
                    return caminho, calcular_custo(grafo, caminho), visitados
                fila.append(vizinho)
    return None, None, visitados


# @unisenac DFS usa pilha: vai fundo no primeiro vizinho; o resultado depende da ordem das arestas no arquivo
def dfs(grafo, origem, destino):
    anterior = {}
    finalizadas = set()
    pilha = [(origem, None)]
    visitados = 0
    while pilha:
        atual, pai = pilha.pop()
        if atual in finalizadas:
            continue
        finalizadas.add(atual)
        if pai is not None:
            anterior[atual] = pai
        visitados += 1
        if atual == destino:
            caminho = montar_caminho(anterior, origem, destino)
            return caminho, calcular_custo(grafo, caminho), visitados
        # @unisenac empilha ao contrário para o primeiro vizinho do arquivo ser o primeiro a sair
        for vizinho, _ in reversed(grafo[atual]):
            if vizinho not in finalizadas:
                pilha.append((vizinho, atual))
    return None, None, visitados


# @unisenac gulosa: em cada porta escolhe a aresta de menor peso; só olha o peso local, então não garante o menor custo
def gulosa(grafo, origem, destino):
    caminho = [origem]
    visitadas = {origem}
    visitados = 1
    while caminho:
        atual = caminho[-1]
        if atual == destino:
            return caminho, calcular_custo(grafo, caminho), visitados
        candidatos = [(peso, viz) for viz, peso in grafo[atual] if viz not in visitadas]
        if candidatos:
            _, proximo = min(candidatos)
            visitadas.add(proximo)
            visitados += 1
            caminho.append(proximo)
        else:
            # @unisenac beco sem saída: volta uma porta
            caminho.pop()
    return None, None, visitados


# @unisenac Dijkstra: sempre finaliza a porta de menor distância acumulada desde a origem (menor custo total)
def dijkstra(grafo, origem, destino):
    distancia = {p: float("inf") for p in grafo}
    anterior = {}
    distancia[origem] = 0
    # @unisenac heapq devolve sempre o menor item
    fila = [(0, origem)]
    finalizadas = set()
    while fila:
        d, atual = heapq.heappop(fila)
        if atual in finalizadas:
            continue
        finalizadas.add(atual)
        if atual == destino:
            break
        for vizinho, peso in grafo[atual]:
            nova = d + peso
            # @unisenac achou um jeito mais curto de chegar no vizinho? atualiza e anota de onde veio
            if nova < distancia[vizinho]:
                distancia[vizinho] = nova
                anterior[vizinho] = atual
                heapq.heappush(fila, (nova, vizinho))
    if distancia[destino] == float("inf"):
        return None, None, len(finalizadas)
    caminho = montar_caminho(anterior, origem, destino)
    return caminho, distancia[destino], len(finalizadas)


# @unisenac nome usado na API -> função
ALGORITMOS = {"bfs": bfs, "dfs": dfs, "gulosa": gulosa, "dijkstra": dijkstra}


# @unisenac tarefa obrigatória: procura o par em que a BFS usa menos portas mas o Dijkstra gasta menos metros
def encontrar_par_divergente(grafo):
    melhor = None
    portas = sorted(grafo)
    for i, origem in enumerate(portas):
        for destino in portas[i + 1:]:
            caminho_bfs, custo_bfs, _ = bfs(grafo, origem, destino)
            caminho_dij, custo_dij, _ = dijkstra(grafo, origem, destino)
            if len(caminho_bfs) < len(caminho_dij) and custo_bfs > custo_dij:
                diferenca = custo_bfs - custo_dij
                if melhor is None or diferenca > melhor[0]:
                    melhor = (diferenca, origem, destino, caminho_bfs, custo_bfs, caminho_dij, custo_dij)
    return melhor
