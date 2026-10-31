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

`grafo-planta.png` mostra as 47 portas sobre a planta e as ligações entre portas vizinhas.
Portas de sala têm o nome da sala (`LAB201`, `CANTINA1`, `IGREJA2`, ...); as de corredor ou de salas sem nome
na planta mantêm o número da planta numerada pelo grupo (`PORTA11`, `PORTA14`, ...). A porta do LabTec é `LABTEC`.

Os pesos são estimados a partir da escala da planta (as medidas impressas nas paredes), em linha reta entre
portas vizinhas. Não foram medidos andando.

`encontrar_par_divergente` em `buscas.py` varre todos os pares de portas e devolve o par em que a BFS acha menos
portas e o Dijkstra acha menos metros, com a maior diferença.

## BFS e Dijkstra em caminhos diferentes

BANHEIROFEM até BIBLIOTECA1:

| Algoritmo | Portas no caminho | Custo |
|---|---|---|
| BFS | 7: BANHEIROFEM, PORTA11, CANTINA1, IGREJA1, IGREJA2, BIBLIOTECA2, BIBLIOTECA1 | 92 m |
| Dijkstra | 8: BANHEIROFEM, BANHEIROMASC, PORTA14, PORTA19, COORDENADOR, PORTA23, SALAPROFESSORES, BIBLIOTECA1 | 58 m |

A BFS conta portas: pelo pátio são 6 arestas, contra 7 pelo corredor de cima, então ela escolhe o primeiro e
ignora o peso. O Dijkstra soma as distâncias: o caminho da BFS tem arestas longas (BIBLIOTECA2 a BIBLIOTECA1
com 20 m, IGREJA2 a BIBLIOTECA2 com 18 m, CANTINA1 a IGREJA1 com 16 m) e dá 92 m, enquanto o corredor de cima
tem uma porta a mais, mas arestas de 5 a 11 m, e dá 58 m. Menos portas não significa menos metros, e só o
Dijkstra garante o menor custo.
