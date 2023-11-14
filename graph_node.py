from typing import List

class GraphNode:

  def __init__(self,id: int, symbol: str, edges: List[int]):
    self.id = id
    self.symbol = symbol
    self.visited = False
    self.edges = edges
    self.current_path = []
    self.time = -1
  
  def __repr__(self):
    return f"id={self.id}, visited={self.visited}, edges={self.edges}, path={self.current_path}"