from fastapi import FastAPI, HTTPException

from buscas import ALGORITMOS
from grafo import UNIDADE, carregar_grafo

app = FastAPI(title="Rotas do Prédio")
grafo = carregar_grafo("arestas.txt")


def validar_porta(porta):
    porta = porta.upper()
    if porta not in grafo:
        raise HTTPException(404, f"Porta não encontrada: {porta}")
    return porta


def executar(algoritmo, origem, destino):
    caminho, custo, visitados = ALGORITMOS[algoritmo](grafo, origem, destino)
    return {
        "algoritmo": algoritmo,
        "caminho": caminho,
        "custo": custo,
        "unidade": UNIDADE,
        "visitados": visitados,
    }


@app.get("/portas")
def portas():
    return sorted(grafo)


@app.get("/vizinhos/{porta}")
def vizinhos(porta: str):
    porta = validar_porta(porta)
    return [{"porta": p, "peso": w} for p, w in grafo[porta]]


@app.get("/rota")
def rota(origem: str, destino: str, algoritmo: str = "dijkstra"):
    origem, destino = validar_porta(origem), validar_porta(destino)
    algoritmo = algoritmo.lower()
    if algoritmo not in ALGORITMOS:
        raise HTTPException(400, f"Algoritmo inválido: use {', '.join(ALGORITMOS)}")
    return executar(algoritmo, origem, destino)


@app.get("/comparar")
def comparar(origem: str, destino: str):
    origem, destino = validar_porta(origem), validar_porta(destino)
    return [executar(nome, origem, destino) for nome in ALGORITMOS]
