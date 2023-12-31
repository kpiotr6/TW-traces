import os
import re
from typing import Dict, Tuple,List

RelationGraph = Dict[str,List[str]]

# Czyta pliki zawierające dane w formacie:
# znaki alfabetu oddzielone przecinkiem
# analizowane słowo
# produkcje, każda w osobnych liniach
# Przykład:
# a,b,c,d
# baadcb
# (a) x := x + y
# (b) y := y + 2z
# (c) x := 3x + z
# (d) z := y − z
# 
# Zwraca krotkę składającą się z listy symboli, listy przedstawiającej słowo
# oraz objekt type RelationGraph = Dict[str,List[str]]
def read_file(path: str) -> Tuple[List[str],List[str],RelationGraph]:
  if (not os.path.isfile(path)):
    raise ValueError("No such file.")
  with open(path,"r") as file:
    symbols = file.readline()[:-1].split(",")
    word = file.readline()[:-1]
    line = file.readline()
    all_expressions = []
    while line:
      line = line[:-1]
      span = re.search(r"\(.+\)",line).span()
      expression = []
      expression.append(line[span[0]+1:span[1]-1])
      expression.append(line[span[1]+1:])
      expression[1] = "".join(expression[1].split())
      tmp = expression[1].split(":=")
      expression[1] = tmp[0]
      expression.append(tmp[1])
      expression = tuple(expression)
      all_expressions.append(expression)
      line = file.readline()
  graph = create_relation_graph(all_expressions)
  return symbols, word, graph


# Tworzy graf relacji pomiędzy symbolami.
# Reprezentowany jest przez słownik, którego kluczami są symbole alfabetu,
# a wartościami listy zawierające symbole które są w relacji z kluczami
def create_relation_graph(expressions: [Tuple[str, str, str]]) -> RelationGraph:
  graph = dict()
  for exp in expressions:
    connections = []
    graph[exp[0]] = connections
    for exp2 in expressions:
      if exp[1] in exp2[2] or exp2[1] in exp[2]:
        connections.append(exp2[0])
  return graph
