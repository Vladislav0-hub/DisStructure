import random
from collections import deque
import heapq


class Algoritm():
    @staticmethod
    def generate_matrix(size):
        return [[1 if random.random() > 0.8 else 0 for _ in range(size)] for _ in range(size)]

    @staticmethod
    def check_eiler(graph) -> str:
        active_nodes = [node for node, neighbors in graph.items() if neighbors]
        if active_nodes:
            visited = set(Algoritm.dfs(graph, active_nodes[0]))
            if any(node not in visited for node in active_nodes):
                return "граф не Эйлеров"

        cnt = 0
        degrees = Algoritm.degrees_node(graph)
        for i, d in degrees.items():
            if d % 2 != 0:
               cnt += 1
        if cnt == 0:
            return "граф Эйлеров"
        elif cnt == 2:
            return "граф полуэйлеров"
        return "граф не Эйлеров"


    @staticmethod #степень вершины
    def degrees_node(graph) -> dict:
        res = {}
        for id, neighbors in graph.items():
            res[id] = len(neighbors)
            if id in neighbors:
                res[id] += 1
        return res

    @staticmethod
    def is_bipartite(graph) -> tuple:
        colors = {}
        parts = {0: [], 1: []}

        for start in graph:
            if start in colors:
                continue

            colors[start] = 0
            queue = deque([start])

            while queue:
                vertex = queue.popleft()
                for neighbor in graph[vertex]:
                    if neighbor == vertex:
                        return False, ([], [])

                    if neighbor not in colors:
                        colors[neighbor] = 1 - colors[vertex]
                        queue.append(neighbor)
                    elif colors[neighbor] == colors[vertex]:
                        return False, ([], [])

        for node, color in colors.items():
            parts[color].append(node)

        return True, (sorted(parts[0]), sorted(parts[1]))

    @staticmethod
    def is_complete_bipartite(graph) -> bool:
        is_bipartite, parts = Algoritm.is_bipartite(graph)
        if not is_bipartite:
            return False

        left, right = parts
        if not left or not right:
            return False

        right_set = set(right)
        left_set = set(left)

        for node in left:
            if set(graph[node].keys()) != right_set:
                return False
        for node in right:
            if set(graph[node].keys()) != left_set:
                return False

        return True

    @staticmethod
    def components_check(graph):
        visited = set()
        components = 0
        res = {}
        res['cnt'] = 0
        for i in graph.keys():
            if i not in visited:
                res_dfs = Algoritm.dfs(graph, i)
                res[components+1] = res_dfs
                visited.update(res_dfs)
                components += 1
        # return components
        res['cnt'] = components
        return res

    @staticmethod
    def matrix_to_list(graph) -> list:
        length = len(graph)
        res = []
        for i in range(1, length+1):
            s = []
            for x in range(0, length):
                if(graph[i-1][x] > 0):
                    s.append(x+1)
            res.append(s)
        return res

    @staticmethod
    def dfs(graph, start) -> list:
        if start not in graph:
            return []

        visited = set()
        stack = [start]
        node_visit = []
        while stack:
            vertex = stack.pop()
            if vertex not in visited:
                node_visit.append(vertex)
                visited.add(vertex)
                for neighbor in reversed(graph[vertex]):
                    if neighbor not in visited:
                        stack.append(neighbor)
        return node_visit

    @staticmethod
    def dfs_2path(graph, start) -> list:
        visited = set()
        stack = [[0, start]]
        node_visit = [] #для получения путей (откуда, куда)
        while stack:
            source, vertex = stack.pop()
            if vertex not in visited:
                visited.add(vertex)
                node_visit.append([source, vertex])
                # Достаем соседей по ключу (id узла)
                if vertex in graph:
                    for neighbor in reversed(graph[vertex]):
                        if neighbor not in visited:
                            stack.append([vertex, neighbor])
        return node_visit

    @staticmethod
    def bfs(graph, start_node=1) -> list:
        if start_node not in graph:
            return []

        visited = {start_node}
        queue = deque([start_node])
        node_visit = []

        while queue:
            vertex = queue.popleft()
            node_visit.append(vertex)

            # В очереди сортируем соседей по возрастанию
            if vertex in graph:
                for neighbour in sorted(graph[vertex].keys()):
                    if neighbour not in visited:
                        visited.add(neighbour)
                        queue.append(neighbour)

        return node_visit

    @staticmethod
    def bfs_2path(graph, start_node=1) -> list:
        if start_node not in graph:
            return []

        visited = {start_node}
        # храним пары (откуда, куда)
        queue = deque([[0, start_node]])
        node_visit = []

        while queue:
            source, vertex = queue.popleft()
            node_visit.append([source, vertex])

            if vertex in graph:
                for neighbour in sorted(graph[vertex].keys()):
                    if neighbour not in visited:
                        visited.add(neighbour)
                        queue.append([vertex, neighbour])

        return node_visit
    @staticmethod
    def prima(graph, start=None) -> tuple:
        if not graph:
            return ([], 0)

        #берем самую первую ноду
        if start is None:
            start = list(graph.keys())[0]
        if start not in graph:
            return ([], 0)

        total_weight = 0
        tree = []
        visited = set([start])

        edges = [] #формат (вес, откуда, куда) сначало вес т.к. будем использовать кучу

        for node, weight in graph[start].items():
            heapq.heappush(edges, (weight, start, node))

        while edges:
            weight, src, dst = heapq.heappop(edges)

            if dst not in visited:
                visited.add(dst) #отмечаем что вершина в дереве
                tree.append((src, dst, weight))

                total_weight += weight

                # Проходимся по ребрам следующей вершины
                for neighbor_t, weight_t in graph[dst].items():
                    if neighbor_t not in visited:
                        heapq.heappush(edges, (weight_t, dst,neighbor_t))

        return (tree, total_weight)
    @staticmethod
    def prufera(graph) -> list:
        if not graph:
            return []

        edges_cnt = sum(len(neighbors) for neighbors in graph.values()) // 2
        if edges_cnt != len(graph) - 1:
            raise ValueError("Граф должен быть деревом")

        start = next(iter(graph))
        if len(Algoritm.dfs(graph, start)) != len(graph):
            raise ValueError("Граф должен быть связным деревом")

        # словарь списков смежности, т.к. у меня веса были {id: [соседи]}
        lists_nodes = {node_id: list(neighbors.keys()) for node_id, neighbors in graph.items()}
        n = len(lists_nodes)

        if n < 2:
            return []
        res = []

        for _ in range(n - 2):
            # Ищем листья вершины, у которых ровно 1 сосед
            listya = [v for v in lists_nodes if len(lists_nodes[v]) == 1]

            # Выбираем минимальный лист
            l = min(listya)

            # Находим его единственного соседа
            neighbor = lists_nodes[l][0]
            res.append(neighbor)

            # Удаление
            # Сначала вычеркиваем текущий лист из списка соседа
            lists_nodes[neighbor].remove(l)
            # Затем полностью удаляем саму вершину-лист
            del lists_nodes[l]

        return res

    @staticmethod
    def prufera_decode(code) -> list:
        n = len(code) + 2 #число вершин
        # Список всех вершин, которые должны быть в дереве
        nodes = list(range(1, n + 1))
        edges = []
        current_code = list(code)

        for i in range(len(code)):
            # Ищем минимальную вершину v, которой нет в коде
            for v in sorted(nodes):
                if v not in current_code:
                    # Соединяем её с первым элементом кода
                    u = current_code.pop(0)
                    edges.append((v, u))

                    # Удаляем использованную вершину из списка доступных
                    nodes.remove(v)
                    break

        # В конце в vertices останется ровно две вершины, соединяем их
        edges.append((nodes[0], nodes[1]))
        return edges

    @staticmethod
    def dijkstra(graph, start):
        # Инициализируем расстояния: до старта 0, до всех остальных — бесконечность
        distances = {node: float('inf') for node in graph}
        distances[start] = 0

        # Очередь с приоритетом: (расстояние, вершина)
        pq = [(0, start)]

        # Список ребер для анимации (откуда, куда, вес)
        path_edges = []
        # Множество посещенных вершин, чтобы не обрабатывать их дважды
        visited = set()

        while pq:
            current_dist, u = heapq.heappop(pq)

            if u in visited:
                continue
            visited.add(u)

            # Проходим по всем соседям вершины u
            for v, weight in graph[u].items():
                distance = current_dist + weight

                # Если найден путь короче, чем известный ранее
                if distance < distances[v]:
                    distances[v] = distance
                    heapq.heappush(pq, (distance, v))
                    # Запоминаем ребро для визуализации анимации
                    path_edges.append((u, v, weight))

        return distances, path_edges

    @staticmethod
    def coloring(graph) -> dict:
        # сортируем вершины по убыванию степени (Алгоритм Уэлша-Пауэлла)
        nodes = sorted(graph.keys(), key=lambda x: len(graph[x]), reverse=True)

        # Словарь итоговых цветов: {node_id: color_index}
        result = {}

        for node in nodes:
            # Находим цвета, уже занятые соседями
            neighbor_colors = {result[neighbor] for neighbor in graph[node] if neighbor in result}

            # Ищем самый маленький доступный индекс цвета (0, 1, 2...)
            color = 0
            while color in neighbor_colors:
                color += 1

            result[node] = color

        return result

    @staticmethod
    def floyd_warshall(graph):
        # Собираем все ID вершин и сортируем их
        nodes = sorted(graph.keys())
        n = len(nodes)

        # Создаем карту индексов для быстрого доступа к матрице
        node_to_idx = {node: i for i, node in enumerate(nodes)}

        # На диагонали нули, остальные - веса ребер из графа
        dist = [[float('inf')] * n for _ in range(n)]

        for i in range(n):
            dist[i][i] = 0

        for u in graph:
            for v, weight in graph[u].items():
                dist[node_to_idx[u]][node_to_idx[v]] = weight

        for k in range(n):
            for i in range(n):
                for j in range(n):
                    if dist[i][j] > dist[i][k] + dist[k][j]:
                        dist[i][j] = dist[i][k] + dist[k][j]

        return nodes, dist

class GraphControl():
    """списками смежностей """ #было, добавил веса
    def __init__(self):
        self.list_nodes = {} #формат {id_1: {id_2: вес, id_3:вес}, id_2 { } ...}
        self.cnt_node = 0

    def add_node(self, node_id=None) -> int:
        if node_id is None:
            self.cnt_node += 1
            node_id = self.cnt_node
        else:
            if isinstance(node_id, int):
                self.cnt_node = max(self.cnt_node, node_id)
        if node_id not in self.list_nodes:
            self.list_nodes[node_id] = {}
        return node_id

    def add_edge(self, source, dst, weight=1) -> None:
        """в виде id"""
        if source in self.list_nodes and dst in self.list_nodes:
            self.list_nodes[source][dst] = weight
            self.list_nodes[dst][source] = weight
            # if dst not in self.list_nodes[source]:
            #     self.list_nodes[source].append(dst)
            # if source not in self.list_nodes[dst]:
            #     self.list_nodes[dst].append(source)

    def clear(self) -> None:
        self.list_nodes = {}
        self.cnt_node = 0

    def get_graph(self) -> dict:
        """списками смежности"""
        return self.list_nodes

    def load_list(self, list_nodes: dict):
        self.clear()

    def matrix_to_list(self, str_matrix: str):
        matrix = []
        for line in str_matrix.strip().split('\n'):
            if line.strip():
                matrix.append([int(x) for x in line.split()])
        size = len(matrix)
        for x in matrix:
            if (len(x)) != size:
                raise ValueError("Матрица должна быть квадратичная")
        for i in range(size):
            for j in range(size):
                if matrix[i][j] != matrix[j][i]:
                    raise ValueError("Матрица должна быть симметричной для неориентированного графа")
        return matrix

    def update_graph_matrix(self, str_matrix:str):
        matrix = self.matrix_to_list(str_matrix)
        size = len(matrix)
        self.clear()

        for i in range(1, size + 1):
            self.add_node(i)

        for i in range(size):
            for j in range(i, size):
                if matrix[i][j] > 0:
                    weight = matrix[i][j]
                    # self.add_edge(i + 1, j + 1)
                    self.add_edge(i + 1, j + 1, weight)


    def incidence_to_list(self, str_matrix: str):
        matrix = []
        for line in str_matrix.strip().split('\n'):
            if line.strip():
                matrix.append([int(x) for x in line.split()])

        if not matrix:
            raise ValueError("Матрица пустая")

        edges_count = len(matrix[0])
        if edges_count == 0:
            raise ValueError("В матрице нет ребер")

        for row in matrix:
            if len(row) != edges_count:
                raise ValueError("Все строки матрицы инцидентности должны быть одинаковой длины")
            if any(x not in (0, 1, 2) for x in row):
                raise ValueError("Матрица инцидентности может содержать только 0, 1 или 2")

        return matrix

    def update_graph_incidence(self, str_matrix: str):
        matrix = self.incidence_to_list(str_matrix)
        nodes_count = len(matrix)
        edges_count = len(matrix[0])
        self.clear()

        for i in range(1, nodes_count + 1):
            self.add_node(i)

        for edge_col in range(edges_count):
            ones = []
            loop_node = None

            for node_row in range(nodes_count):
                value = matrix[node_row][edge_col]
                node_id = node_row + 1

                if value == 1:
                    ones.append(node_id)
                elif value == 2:
                    if loop_node is not None:
                        raise ValueError("В одном ребре не может быть две петли")
                    loop_node = node_id

            if loop_node is not None:
                if ones:
                    raise ValueError("Петля в матрице инцидентности должна задаваться только числом 2")
                self.add_edge(loop_node, loop_node)
            else:
                if len(ones) != 2:
                    raise ValueError("Каждый столбец должен задавать ровно одно ребро")
                self.add_edge(ones[0], ones[1])


    def update_graph_list(self, text: str):
        parsed = {}
        for line in text.strip().splitlines():
            line = line.strip()
            if not line:
                continue

            if ":" not in line:
                raise ValueError(f"Нет ':' в строке: {line}")

            node_text, neighbors_text = line.split(":", 1)
            node = int(node_text)

            # извлекаем соседей
            neighbors = [int(x) for x in neighbors_text.replace(",", " ").split()]

            # проверяем и саму вершину, и всех её соседей
            if node <= 0 or any(n <= 0 for n in neighbors):
                raise ValueError("Номера вершин должны быть больше 0")

            parsed[node] = neighbors

        if not parsed:
            raise ValueError("Граф пустой")

        self.clear()

        # собираем уникальные вершины через сет
        all_nodes = set(parsed.keys()).union(*parsed.values())

        # вершины
        for node in all_nodes:
            self.add_node(node)

        # ребра
        for node, neighbors in parsed.items():
            for neighbor in neighbors:
                self.add_edge(node, neighbor)


