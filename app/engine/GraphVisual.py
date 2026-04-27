import math


from .items_graph import Edge, Node
from .logic import GraphControl
#доделать


class GraphVisual():
    def __init__(self, scene, graph_control, window):
        self.scene = scene
        self.graph_control:GraphControl = graph_control
        self.window = window
        self.visual_nodes = {} # {node_id: Node}, словарь всех визуальных узлов (id: адрес)
        self.visual_edges = {} # {"1-2": Edge, "2-1": Edge}, словарь визуальнных ребер, (путь: адрес)

    def draw_new_node(self, x, y, node_id=None) -> Node:
        new_id = self.graph_control.add_node(node_id)
        new_node = Node(new_id, x, y)
        self.visual_nodes[new_id] = new_node
        self.scene.addItem(new_node)

        return new_node

    def draw_new_edge(self, source_id:int | str, dst_id:int | str, weight = 1) -> Edge:
        source = self.visual_nodes.get(source_id)
        dst = self.visual_nodes.get(dst_id)

        if (source_id, dst_id) in self.visual_edges:
            print("дубль")
            return self.visual_edges[(source_id, dst_id)]
        if (dst_id, source_id) in self.visual_edges:
            print("дубль")
            return self.visual_edges[(dst_id, source_id)]


        if source and dst:
            self.graph_control.add_edge(source_id,dst_id,weight)
            new_edge = Edge(source,dst, weight)
            self.scene.addItem(new_edge)
            self.visual_edges[(source_id, dst_id)] = new_edge
            self.visual_edges[(dst_id, source_id)] = new_edge #потом переделать т.к. граф неоринтированый
            source.add_edge(new_edge)
            if dst is not source:
                dst.add_edge(new_edge)
            return new_edge
        else:
            return None

    # def ellipse_xy_draw(self, matrix, radius=200):
    #     self.graph_clear()
    #     size = len(matrix)
    #     if size == 0:
    #         return
    #     nodes = []
    #     for i in range(size):
    #         angle = 2 * math.pi * i / size
    #         x = radius * math.cos(angle)
    #         y = radius * math.sin(angle)
    #         new_node = self.draw_new_node(x, y)
    #         nodes.append(new_node)
    #     for i in range(size):
    #         for j in range(size):
    #             weight = matrix[i][j]
    #             if weight > 0:
    #                 u_node = nodes[i]
    #                 v_node = nodes[j]
    #                     #переделать позже мб, если ориент граф нужен будет
    #                 self.draw_new_edge(u_node.id, v_node.id, weight)
    #списком смежностей
    def draw_circle(self, radius=200):
        self.graph_clear_only_visual()
        graph = self.graph_control.get_graph()

        size = len(graph)
        if size == 0:
            return
        nodes = list(graph.keys())
        for i in range(size):
            id = nodes[i]
            angle = 2 * math.pi * i / size
            x = radius * math.cos(angle)
            y = radius * math.sin(angle)
            print(x, y)
            new_node = self.draw_new_node(x, y, id)
        for j in graph:
            neighbors = graph[j]
            for x, weight in neighbors.items():
                self.draw_new_edge(j, x,weight)



    def graph_clear_only_visual(self):
        self.scene.clear()
        self.visual_nodes = {}
        self.visual_edges = {}
        self.window.RightBar.lineEdit_Node.clear()

    def graph_clear(self):
        self.graph_control.clear()
        self.scene.clear()
        self.visual_nodes = {}

        self.visual_edges = {}
        self.window.RightBar.lineEdit_Node.clear()

    def get_visual_nodes(self):
        return self.visual_nodes

    def get_visual_edges(self):
        return self.visual_edges
