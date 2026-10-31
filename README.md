# Rotas do Prédio com Grafos

Trabalho de Algoritmos e Estruturas de Dados II, Unisenac Campus Pelotas (Prof. Pablo De Chiaro).

## Integrantes

- Derek Cavalcanti
- Julia Alsina

## Unidade do peso

Metros. O peso de cada aresta é a distância em linha reta entre duas portas vizinhas, calculada a partir das medidas da planta (corredores não entram na conta). Não é a distância acumulada desde o LabTec.

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

## Grafo

`grafo-planta.png` mostra as 49 portas marcadas sobre a planta e as ligações entre portas vizinhas.
As portas sem nome na planta foram numeradas (`PORTA01` a `PORTA49`); `LABTEC` e `LAB201` mantêm o nome.

## BFS e Dijkstra em caminhos diferentes

LABTEC até PORTA24:

| Algoritmo | Portas no caminho | Custo |
|---|---|---|
| BFS | 10 (LABTEC, LAB201, PORTA08, PORTA07, PORTA09, PORTA12, PORTA15, PORTA16, PORTA28, PORTA24) | 124 m |
| Dijkstra | 11 (LABTEC, LAB201, PORTA08, PORTA07, PORTA09, PORTA17, PORTA18, PORTA19, PORTA21, PORTA22, PORTA24) | 114 m |

Os dois caminhos saem iguais até a PORTA09 e depois se separam. A BFS conta portas: pelo caminho do meio
(PORTA12, PORTA15, PORTA16, PORTA28) são 4 portas até a PORTA24, contra 5 pelo corredor de cima
(PORTA17, PORTA18, PORTA19, PORTA21, PORTA22), então ela escolhe o primeiro e ignora o peso.
O Dijkstra soma as distâncias: o caminho do meio tem arestas longas (PORTA16 a PORTA28 e PORTA28 a PORTA24
têm 18 m e 19 m) e dá 124 m, enquanto o de cima tem arestas curtas e dá 114 m. Menos portas não significa
menos metros, e só o Dijkstra garante o menor custo.
