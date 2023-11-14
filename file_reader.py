import os
import re
from typing import Dict, Tuple,List

type RelationGraph = Dict[str,List[str]]

# A
# W
# rest
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

def create_relation_graph(expressions: [Tuple[str, str, str]]) -> RelationGraph:
  graph = dict()
  for exp in expressions:
    connections = []
    graph[exp[0]] = connections
    for exp2 in expressions:
      if exp[1] in exp2[2] or exp2[1] in exp[2]:
        connections.append(exp2[0])
  return graph
