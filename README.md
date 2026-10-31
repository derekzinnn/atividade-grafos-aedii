# Rotas do Prédio com Grafos

Trabalho de Algoritmos e Estruturas de Dados II, Unisenac Campus Pelotas (Prof. Pablo De Chiaro).

## Integrantes

- Derek Cavalcanti

## Unidade do peso

Passos. O peso de cada aresta é a distância entre duas portas vizinhas, não a distância acumulada desde o LabTec.

## Como rodar

```bash
pip install -r requirements.txt
python testes.py
uvicorn api:app --reload
```

Depois abra http://127.0.0.1:8000/docs.

| Endpoint | Devolve |
|---|---|
| `GET /portas` | Todas as portas |
| `GET /vizinhos/{porta}` | Vizinhos e peso de cada aresta |
| `GET /rota?origem=&destino=&algoritmo=` | Caminho, custo e visitados (`bfs`, `dfs`, `gulosa` ou `dijkstra`) |
| `GET /comparar?origem=&destino=` | Os quatro algoritmos lado a lado |

Porta inexistente devolve 404 com mensagem.

## Arquivos

- `arestas.txt`: uma aresta por linha (`PORTA PORTA PESO`), cada aresta uma única vez.
- `grafo.py`: monta a lista de adjacência nos dois sentidos.
- `buscas.py`: BFS, DFS, gulosa e Dijkstra.
- `api.py`: API FastAPI.

## BFS e Dijkstra em caminhos diferentes

LABTEC até LAB203:

| Algoritmo | Caminho | Custo |
|---|---|---|
| BFS | LABTEC, PATIO, LAB203 | 48 |
| Dijkstra | LABTEC, LAB201, LAB202, LAB203 | 31 |

A BFS conta portas: o caminho pelo PATIO tem 2 arestas contra 3 do outro, então ela o escolhe e ignora o peso.
O Dijkstra soma os pesos: pelo PATIO são 8 + 40 = 48, e pelo outro lado são 12 + 10 + 9 = 31. Menos portas não
significa menos passos, e só o Dijkstra garante o menor custo.
