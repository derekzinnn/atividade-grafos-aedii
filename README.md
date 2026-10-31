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

`grafo-planta.png` mostra as 47 portas numeradas sobre a planta e as ligações entre portas vizinhas.
Os números são os da planta numerada pelo grupo (`PORTA01` a `PORTA47`); a porta do LabTec é `LABTEC` e a do Lab201 é `LAB201`.

## BFS e Dijkstra em caminhos diferentes

LABTEC até PORTA23:

| Algoritmo | Portas no caminho | Custo |
|---|---|---|
| BFS | 11: LABTEC, PORTA06, PORTA36, PORTA35, PORTA34, PORTA33, PORTA32, PORTA26, PORTA25, PORTA24, PORTA23 | 130 m |
| Dijkstra | 13: LABTEC, LAB201, PORTA09, PORTA10, PORTA11, PORTA12, PORTA13, PORTA14, PORTA19, PORTA20, PORTA21, PORTA22, PORTA23 | 118 m |

A BFS conta portas: o caminho pelo pátio e pela biblioteca tem 10 arestas, contra 12 pelo corredor da esquerda,
então ela escolhe o primeiro e ignora o peso. O Dijkstra soma as distâncias: o caminho da BFS tem arestas longas
(LABTEC a PORTA06 com 21 m, PORTA32 a PORTA26 com 20 m, PORTA33 a PORTA32 com 18 m) e dá 130 m, enquanto o do
corredor tem mais portas, mas arestas curtas, e dá 118 m. Menos portas não significa menos metros, e só o
Dijkstra garante o menor custo.
