UNIDADE = "passos"


def carregar_grafo(caminho):
    grafo = {}
    with open(caminho, encoding="utf-8") as arq:
        for linha in arq:
            if not linha.strip():
                continue
            a, b, peso = linha.split()
            peso = int(peso)
            grafo.setdefault(a, []).append((b, peso))
            grafo.setdefault(b, []).append((a, peso))
    return grafo


def contar_arestas(grafo):
    return sum(len(vizinhos) for vizinhos in grafo.values()) // 2


def conferir_grafo(grafo, origem="LABTEC"):
    alcancadas = {origem}
    fila = [origem]
    while fila:
        atual = fila.pop(0)
        for vizinho, _ in grafo[atual]:
            if vizinho not in alcancadas:
                alcancadas.add(vizinho)
                fila.append(vizinho)
    return sorted(set(grafo) - alcancadas)


if __name__ == "__main__":
    g = carregar_grafo("arestas.txt")
    print(f"Portas: {len(g)} | Arestas: {contar_arestas(g)}")
    nao_alcancadas = conferir_grafo(g)
    if nao_alcancadas:
        print("ATENÇÃO, portas não alcançadas a partir do LABTEC:", nao_alcancadas)
    else:
        print("OK: a BFS a partir do LABTEC alcança todas as portas.")
