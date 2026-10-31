from buscas import ALGORITMOS, bfs, dijkstra, encontrar_par_divergente
from grafo import carregar_grafo, conferir_grafo, contar_arestas

# @unisenac testes rápidos: python testes.py
g = carregar_grafo("arestas.txt")
assert conferir_grafo(g) == [], "BFS não alcança todas as portas"
print("Portas:", len(g), "| Arestas:", contar_arestas(g))

# @unisenac toda aresta precisa ter a volta
for origem in g:
    for vizinho, peso in g[origem]:
        assert (origem, peso) in g[vizinho], "aresta sem volta"

# @unisenac nenhum algoritmo pode achar custo menor que o Dijkstra
for destino in g:
    menor = dijkstra(g, "LABTEC", destino)[1]
    for nome, busca in ALGORITMOS.items():
        caminho, custo, visitados = busca(g, "LABTEC", destino)
        assert caminho[0] == "LABTEC" and caminho[-1] == destino
        assert custo >= menor, nome

print("Par divergente:", encontrar_par_divergente(g))
print("Tudo certo.")
