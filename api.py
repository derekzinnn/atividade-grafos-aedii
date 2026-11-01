from fastapi import FastAPI, HTTPException
from fastapi.responses import RedirectResponse

from buscas import ALGORITMOS
from grafo import UNIDADE, carregar_grafo

# @unisenac rodar com: uvicorn api:app --reload (documentação em /docs)
app = FastAPI(title="Rotas do Prédio")
grafo = carregar_grafo("arestas.txt")


# @unisenac porta inexistente devolve 404 com mensagem
def validar_porta(porta):
    porta = porta.upper()
    if porta not in grafo:
        raise HTTPException(404, f"Porta não encontrada: {porta}")
    return porta


# @unisenac roda um algoritmo e monta a resposta no formato pedido no enunciado
def executar(algoritmo, origem, destino):
    caminho, custo, visitados = ALGORITMOS[algoritmo](grafo, origem, destino)
    return {
        "algoritmo": algoritmo,
        "caminho": caminho,
        "custo": custo,
        "unidade": UNIDADE,
        "visitados": visitados,
    }


# @unisenac a raiz não tem conteúdo: manda para a documentação interativa
@app.get("/", include_in_schema=False)
def raiz():
    return RedirectResponse("/docs")


# @unisenac GET /portas: todas as portas
@app.get("/portas")
def portas():
    return sorted(grafo)


# @unisenac GET /vizinhos/{porta}: vizinhos e peso de cada aresta
@app.get("/vizinhos/{porta}")
def vizinhos(porta: str):
    porta = validar_porta(porta)
    return [{"porta": p, "peso": w} for p, w in grafo[porta]]


# @unisenac GET /rota: caminho, custo e visitados de um algoritmo
@app.get("/rota")
def rota(origem: str, destino: str, algoritmo: str = "dijkstra"):
    origem, destino = validar_porta(origem), validar_porta(destino)
    algoritmo = algoritmo.lower()
    if algoritmo not in ALGORITMOS:
        raise HTTPException(400, f"Algoritmo inválido: use {', '.join(ALGORITMOS)}")
    return executar(algoritmo, origem, destino)


# @unisenac GET /comparar: os quatro algoritmos lado a lado
@app.get("/comparar")
def comparar(origem: str, destino: str):
    origem, destino = validar_porta(origem), validar_porta(destino)
    return [executar(nome, origem, destino) for nome in ALGORITMOS]
