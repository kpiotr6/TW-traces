from file_reader import read_file, RelationGraph
from typing import Dict, Tuple, List
from graph_node import GraphNode
import queue
import graphviz
import sys

type DirectedGraph = List[GraphNode]

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

def sub_BFS(graph: DirectedGraph,start: GraphNode):
  q = queue.Queue()
  q.put(start)
  start.time = 0
  while not q.empty():
    current = q.get()
    for verticle in current.edges:
      node = graph[verticle]
      node.visited = True
      node.time = current.time+1
      q.put(node)
        

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
  
def to_FNF(graph: DirectedGraph) -> str:
  time = 0
  for v in graph:
    time = max(time,v.time)
  divided = [[] for i in range(time+1)]
  for v in graph:
    divided[v.time].append(v.symbol)
  result_string = ""
  for packet in divided:
    result_string = f"{result_string}({"".join(packet)})"
  return result_string

def to_Diagraph(graph: DirectedGraph, name: str):
  dot = graphviz.Digraph(name)
  for v in graph:
    for new_v in v.edges:
      dot.edge(str(v.id),str(new_v))
  for v in graph:
    dot.node(str(v.id),v.symbol)
  return dot

if __name__ == "__main__":
  if len(sys.argv) == 0:
    name = "test.txt"
  else:
    name = sys.argv[1]
  symbols, word, relation_graph = read_file(name)
  directed_graph = create_directed_graph(word,relation_graph)
  discarding_DFS(directed_graph)
  BFS(directed_graph)
  dot = to_Diagraph(directed_graph,name.split(".")[0])
  dot.render(directory='graph_output')
  in_rel,not_rel = get_relations(symbols, relation_graph)
  print(f"D={in_rel}")
  print(f"I={not_rel}")
  print(f"Foata: {to_FNF(directed_graph)}")
  print(dot.source)
    
