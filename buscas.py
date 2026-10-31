import heapq
from collections import deque


def montar_caminho(anterior, origem, destino):
    caminho = [destino]
    while caminho[-1] != origem:
        caminho.append(anterior[caminho[-1]])
    caminho.reverse()
    return caminho


def calcular_custo(grafo, caminho):
    custo = 0
    for a, b in zip(caminho, caminho[1:]):
        custo += next(peso for vizinho, peso in grafo[a] if vizinho == b)
    return custo


def bfs(grafo, origem, destino):
    if origem == destino:
        return [origem], 0, 1
    anterior = {}
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
        for vizinho, _ in reversed(grafo[atual]):
            if vizinho not in finalizadas:
                pilha.append((vizinho, atual))
    return None, None, visitados


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
            caminho.pop()
    return None, None, visitados


def dijkstra(grafo, origem, destino):
    distancia = {p: float("inf") for p in grafo}
    anterior = {}
    distancia[origem] = 0
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
            if nova < distancia[vizinho]:
                distancia[vizinho] = nova
                anterior[vizinho] = atual
                heapq.heappush(fila, (nova, vizinho))
    if distancia[destino] == float("inf"):
        return None, None, len(finalizadas)
    caminho = montar_caminho(anterior, origem, destino)
    return caminho, distancia[destino], len(finalizadas)


ALGORITMOS = {"bfs": bfs, "dfs": dfs, "gulosa": gulosa, "dijkstra": dijkstra}
