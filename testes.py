from buscas import ALGORITMOS, bfs, dijkstra
from grafo import carregar_grafo, conferir_grafo, contar_arestas

g = carregar_grafo("arestas.txt")
assert conferir_grafo(g) == [], "BFS não alcança todas as portas"
print("Portas:", len(g), "| Arestas:", contar_arestas(g))

for origem in g:
    for vizinho, peso in g[origem]:
        assert (origem, peso) in g[vizinho], "aresta sem volta"

for destino in g:
    menor = dijkstra(g, "LABTEC", destino)[1]
    for nome, busca in ALGORITMOS.items():
        caminho, custo, visitados = busca(g, "LABTEC", destino)
        assert caminho[0] == "LABTEC" and caminho[-1] == destino
        assert custo >= menor, nome

print("BFS", bfs(g, "LABTEC", "PORTA24"))
print("Dijkstra", dijkstra(g, "LABTEC", "PORTA24"))
print("Tudo certo.")
