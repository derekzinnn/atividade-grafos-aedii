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

`desenho-grafo.png` é o desenho do grupo: as portas numeradas e as ligações traçadas sobre a planta.
`grafo-planta.png` é o mesmo grafo gerado a partir do `arestas.txt`, para conferência.
Portas de sala têm o nome da sala (`LAB201`, `CANTINA1`, `IGREJA2`, ...); as de corredor ou de salas sem nome
na planta mantêm o número da planta (`PORTA11`, `PORTA14`, ...). A porta do LabTec é `LABTEC`.

Os pesos são estimados a partir da escala da planta (as medidas impressas nas paredes), em linha reta entre
portas vizinhas. Não foram medidos andando. Uma aresta só existe se dá para andar entre as duas portas sem
passar por outra porta.

`encontrar_par_divergente` em `buscas.py` varre todos os pares de portas e devolve um par em que a BFS usa menos
portas e o Dijkstra gasta menos metros (diferença de pelo menos 15 m, com o caminho mais curto possível).

## BFS e Dijkstra em caminhos diferentes

CANTINA2 até SALAPROFESSORES:

| Algoritmo | Portas no caminho | Custo |
|---|---|---|
| BFS | 9: CANTINA2, IGREJA1, IGREJA2, BIBLIOTECA2, PORTA29, PORTA28, PORTA27, BIBLIOTECA1, SALAPROFESSORES | 112 m |
| Dijkstra | 10: CANTINA2, CANTINA1, PORTA11, BANHEIROFEM, BANHEIROMASC, PORTA14, PORTA19, COORDENADOR, PORTA23, SALAPROFESSORES | 91 m |

A BFS conta portas: atravessando a Igreja e a Biblioteca são 8 arestas, contra 9 pelo corredor da esquerda,
então ela escolhe o primeiro e ignora o peso. O Dijkstra soma as distâncias: o caminho da BFS tem arestas longas
(PORTA27 a BIBLIOTECA1 com 27 m, IGREJA2 a BIBLIOTECA2 com 18 m, CANTINA2 a IGREJA1 com 16 m) e dá 112 m, enquanto
o corredor tem uma porta a mais, mas arestas de 5 a 16 m, e dá 91 m. Menos portas não significa menos metros, e só
o Dijkstra garante o menor custo.
