from file_reader import read_file, RelationGraph
from typing import Dict, Tuple, List
from graph_node import GraphNode
import queue
import graphviz
import sys

DirectedGraph = List[GraphNode]

# Na podstawie grafu relacji pomiędzy symbolami tworzy
# tablicę wypełnioną relacjami zależności oraz tablicę relacji niezależności
def get_relations(symbols: List[str], relation_graph: Dict[str,List[str]]) -> Tuple[List[Tuple],List[Tuple]]:
  in_rel = []
  not_rel = []
  for s1 in symbols:
    for s2 in symbols:
      if s2 in relation_graph[s1]:
        in_rel.append(tuple([s1,s2]))
      else:
        not_rel.append(tuple([s1,s2]))
  in_rel.sort()
  not_rel.sort()
  return in_rel, not_rel

# Funkcja zwracająca postać normalną Foaty na podstawie grafu skierowanego z czasem odwiedzin
def to_FNF(graph: DirectedGraph) -> str:
  time = 0
  for v in graph:
    time = max(time,v.time)
  divided = [[] for i in range(time+1)]
  for v in graph:
    divided[v.time].append(v.symbol)
  result_string = ""
  for packet in divided:
    result_string = f"{result_string}({''.join(packet)})"
  return result_string

# Funkcja tworząca obiekt graphviz.Diagraph umożliwiający łatwe generowanie 
# zapisu grafu w postaci dot.
def to_Diagraph(graph: DirectedGraph, name: str) -> graphviz.Digraph:
  dot = graphviz.Digraph(name,format="png")
  for v in graph:
    for new_v in v.edges:
      dot.edge(str(v.id),str(new_v))
  for v in graph:
    dot.node(str(v.id),v.symbol)
  return dot

# Na podstawie grafu relacji pomiędzy symbolami oraz słowa z nich utworzonego tworzy
# graf skierowany.
def create_directed_graph(word: str, relation_graph: RelationGraph) -> DirectedGraph:
  directed = []
  for i,letter in enumerate(word):
    node = GraphNode(i,letter,[])
    for j in range(i+1,len(word)):
      letter2 = word[j]
      if letter2 in relation_graph[letter]:
        node.edges.append(j)
    directed.append(node)
  return directed

# Funkcja realizująca przeszukanie grafu za pomocą DFSa, a następnie odrzucająca niepotrzebne krawędzie.
# Każdy wierzchołek A przechowuje w polu current_path wszystkie wierzchołki do których można utworzyć ścieżkę
# z wierzchołka A. Następnie dla każdego wierzchołka B, funkcja sprawdza czy wierzchołki których krawędzie prowadzą do 
# B należą do current_path innych wierzchołków prowadzących do B. Jeśli z wierzchołka C prowadzącego do B da się dojść do innego wierzchołka 
# prowadzącego do B to krawędź (C,B) jest zbędna.
def discarding_DFS(graph: DirectedGraph):
  for node in graph:
    sub_DFS(graph, node)
  for node in graph:
    node.visited = False
  for node in graph:
    nodes_to_check: List[GraphNode] = []
    for node2 in graph:
      if node.id in node2.edges:
        nodes_to_check.append(node2)
    for node_check1 in nodes_to_check:
      for node_check2 in nodes_to_check:
        if node_check1 == node_check2:
          continue
        if node_check1 in node_check2.current_path and node.id in node_check2.edges:
          node_check2.edges.remove(node.id)

# Funkcja pomocnicza realizująca sam podstawowy algorytm DFS. Wypełnia dodatkowo listę w polu current_path każdego wierzchołka
def sub_DFS(graph: DirectedGraph, node: GraphNode) -> List[GraphNode]:
  if node.visited:
    tmp = node.current_path.copy()
    tmp.append(node)
    return tmp
  possible_paths = []
  for new_verticle in node.edges:
    node_tmp = graph[new_verticle]
    possible_paths.extend(sub_DFS(graph, node_tmp))
  node.current_path = possible_paths
  node.visited = True
  tmp = node.current_path.copy()
  tmp.append(node)
  return tmp 
        
# Funkcja realizująca algorytm BFS, który odwiedza także już odwiedzone wierzchołki.
def BFS(graph: DirectedGraph):
  for v in graph:
    if not v.visited:
      q = queue.Queue()
      q.put(v)
      v.time = 0
      while not q.empty():
        current = q.get()
        for verticle in current.edges:
          node = graph[verticle]
          node.visited = True
          node.time = current.time+1
          q.put(node)

if __name__ == "__main__":
  if len(sys.argv) == 1:
    name = "test1.txt"
  else:
    name = sys.argv[1]
  symbols, word, relation_graph = read_file(name)
  in_rel,not_rel = get_relations(symbols, relation_graph)
  directed_graph = create_directed_graph(word,relation_graph)
  discarding_DFS(directed_graph)
  BFS(directed_graph)
  print(f"D={in_rel}")
  print(f"I={not_rel}")
  print(f"Foata: {to_FNF(directed_graph)}")
  dot = to_Diagraph(directed_graph,name.split(".")[0])
  dot.render(directory='graph_output')
  print(dot.source)
    
