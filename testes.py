from buscas import bfs, dfs, dijkstra, gulosa
from grafo import carregar_grafo, conferir_grafo, contar_arestas

g = carregar_grafo("arestas.txt")
assert conferir_grafo(g) == [], "BFS não alcança todas as portas"
print("Portas:", len(g), "| Arestas:", contar_arestas(g))

for nome, f in [("bfs", bfs), ("dfs", dfs), ("gulosa", gulosa), ("dijkstra", dijkstra)]:
    print(nome, f(g, "LABTEC", "LAB203"))

assert bfs(g, "LABTEC", "LAB203") == (["LABTEC", "PATIO", "LAB203"], 48, 4)
assert gulosa(g, "LABTEC", "LAB203")[:2] == (["LABTEC", "PATIO", "LAB203"], 48)
assert dijkstra(g, "LABTEC", "LAB203") == (["LABTEC", "LAB201", "LAB202", "LAB203"], 31, 5)
assert dfs(g, "LABTEC", "LAB203")[1] in (31, 48)
print("Tudo certo.")
