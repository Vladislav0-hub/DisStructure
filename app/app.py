import json
import math
import sys
import random
from pathlib import Path
from PyQt6 import uic
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QMainWindow, QWidget, QHBoxLayout, QApplication, QFrame, QVBoxLayout, QSplitter, \
    QMessageBox, \
    QDialog, QPlainTextEdit, QFileDialog, QPushButton

# Управление визуальными эффектами: таймеры, пошаговая перекраска узлов и ребер
from engine.animations import AnimateNodeAndEdges

# Обьекты: классы Node (вершина) и Edge (ребра) QGraphicsItem
from engine.items_graph import Edge, Node

# логика: GraphControl (хранение данных, без учета PyQt), Algoritm (алгоритмы)
from engine.logic import GraphControl, Algoritm

# Сцена и область: MyScene (слой объектов) и MyView (камера, зум, клики)
from engine.scene_paint import MyScene, MyView

# Виджеты: кнопки и боковые меню управления
from engine.widgets import isAddButton, isClickButton, GraphInput, isAddEdgeButton, DeleteButton

from engine.GraphVisual import GraphVisual

from engine.files import Files

class Window(QMainWindow):
    def __init__(self):
        '''Окно редактора'''
        super().__init__()
        self.setMinimumSize(1280, 720)
        self.central_widget = QSplitter(Qt.Orientation.Horizontal) #для смены ширины пользователем, доработать позже

        self.setCentralWidget(self.central_widget)
        self.main_layout = QHBoxLayout(self.central_widget)


        # self.edges_dict = {}


        self.sidebar()
        self.scene_w()

        self.addClickBtn.clicked.connect(self.view.enable_click_btn) #хуйня, переделать после в сайдбар либо в сам класс
        self.addEdgesBtn.clicked.connect(self.view.click_btn_add_edges)

        #self.graphvisualiser = GraphVisual(self.scene, self.graph_control, self)


        self.algoritm = Algoritm()

        self.rightMenu()
        self.Files = Files( self.graphvisualiser, self.graph_control)
        self.btn_save_json()

    def sidebar(self):
        """Сайдбар"""
        self.bar = QFrame()
        self.bar.setStyleSheet("background-color: #2c3e50;")
        self.bar.setMaximumWidth(80)
        self.addNodesBtn = isAddButton()
        self.addClickBtn = isClickButton()
        self.addEdgesBtn = isAddEdgeButton()
        self.deleteBtn = DeleteButton()
        self.layout_bar = QVBoxLayout(self.bar)
        self.layout_bar.addWidget(self.addNodesBtn)
        self.layout_bar.addWidget(self.addClickBtn)
        self.layout_bar.addWidget(self.addEdgesBtn)
        # self.layout_bar.addWidget(self.deleteBtn)
        self.layout_bar.addStretch(1)


        self.addNodesBtn.menu_add.actions()[0].triggered.connect(self.add_list_dialog)
        self.addNodesBtn.menu_add.actions()[1].triggered.connect(self.add_matrix_dialog)
        self.addNodesBtn.menu_add.actions()[2].triggered.connect(self.add_incidence_matrix_dialog)

        self.main_layout.addWidget(self.bar)

    def add_list_dialog(self):
        """Добавление списком смежностей и парс"""
        dialog = GraphInput(self)
        dialog.text_edit.setPlaceholderText("""Введите граф списком, пример:
                1: 2, 3
                2: 1, 3
                3: 1, 2
                """)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            try:
                text = dialog.get_text()
                self.graph_control.update_graph_list(text)
                self.graphvisualiser.draw_circle()
            except Exception as e:
                QMessageBox.critical(self, "Ошибка", f"Неверный формат - {e}")
    def add_matrix_dialog(self):
        """Добавление матрицей смежностей и парс"""
        dialog = GraphInput(self)
        dialog.text_edit.setPlaceholderText("""Введите граф матрице, пример:
        0 1 1
        1 0 1
        1 1 0
        """)
        if dialog.exec() == QDialog.DialogCode.Accepted:

            try:
                # matrix = []
                # for line in text.strip().split('\n'):
                #     if line.strip():
                #         matrix.append([int(x) for x in line.split()])
                #
                # size = len(matrix)
                # for x in matrix:
                #     if(len(x)) != size:
                #         raise ValueError("Матрица должна быть квадратичная")
                text = dialog.get_text()
                self.graph_control.update_graph_matrix(text)
                self.graphvisualiser.draw_circle()
            except Exception as e:
                QMessageBox.critical(self, "Ошибка", f"Неверный формат - {e}")

    def add_incidence_matrix_dialog(self):
        """Добавление матрицей инцидентности и парс"""
        dialog = GraphInput(self)
        dialog.text_edit.setPlaceholderText("""Введите матрицу инцидентности, пример:
        1 1 0
        1 0 1
        0 1 1
        """)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            try:
                text = dialog.get_text()
                self.graph_control.update_graph_incidence(text)
                self.graphvisualiser.draw_circle()
            except Exception as e:
                QMessageBox.critical(self, "Ошибка", f"Неверный формат - {e}")

    def test_algoritm(self, txt:str):
        dialog = GraphInput(self)
        dialog.text_edit.setPlaceholderText(txt)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            try:
                text = dialog.get_text()
                return text
            except Exception as e:
                self.console_print(f"Ошибка при вводе: {e}")
        return None

    def scene_w(self):
        self.graph_control = GraphControl()
        self.scene = MyScene()
        self.graphvisualiser = GraphVisual(self.scene, self.graph_control, self)
        self.view = MyView(self.scene, self.graph_control, self, self.graphvisualiser)

        self.middle_splitter = QSplitter(Qt.Orientation.Vertical)
        self.console = QPlainTextEdit()
        self.console.setReadOnly(True)
        self.console.setStyleSheet(
            "background-color: #1e1e1e; color: #d4d4d4; font-family: Consolas, monospace; font-size: 14px;")

        self.middle_splitter.addWidget(self.view)
        self.middle_splitter.addWidget(self.console)
        self.middle_splitter.setSizes([800, 200])
        self.main_layout.addWidget(self.middle_splitter)

        # self.main_layout.addWidget(self.view)

    def rightMenu(self):
        self.RightBar = QWidget()
        uic.loadUi('ui/rightmenunode5.ui', self.RightBar)
        self.bar.setStyleSheet("background-color: #2c3e50;")
        self.main_layout.addWidget(self.RightBar)
        self.RightBar.setFixedWidth(300)
        self.RightBar.btnStartAlgo.clicked.connect(self.click_start_algo)
    def click_start_algo(self):
        text_algo = self.RightBar.algorithm_list.currentText()
        print(self.graph_control.get_graph())
        if "Анализ графа - 0" == text_algo:
            try:
                graph = self.graph_control.get_graph()
                if not graph:
                    self.console_print("Граф пуст!")
                    return

                degrees = self.algoritm.degrees_node(graph)
                components = self.algoritm.components_check(graph)
                is_bipartite, parts = self.algoritm.is_bipartite(graph)
                is_complete_bipartite = self.algoritm.is_complete_bipartite(graph)

                self.console.clear()
                self.console_print("Анализ графа")
                for node in sorted(degrees):
                    self.console_print(f"Степень вершины {node}: {degrees[node]}")
                self.console_print(f"Количество компонент связности: {components['cnt']}")
                self.console_print(self.algoritm.check_eiler(graph))

                if is_bipartite:
                    left = ' '.join(map(str, parts[0])) if parts[0] else "-"
                    right = ' '.join(map(str, parts[1])) if parts[1] else "-"
                    self.console_print(f"Граф двудольный: да ({left}) и ({right})")
                else:
                    self.console_print("Граф двудольный: нет")

                self.console_print(f"Граф полный двудольный: {'да' if is_complete_bipartite else 'нет'}")
            except Exception as e:
                self.console_print(f"Ошибка - {e}")
        if "DFS (Обход в глубину) - 1" == text_algo:
            try:
                start = int(self.RightBar.lineEdit_Node.text())
            except ValueError:
                start = 1
            list_graph = self.graph_control.get_graph()
            res_dfs = self.algoritm.dfs_2path(list_graph, start)
            res = self.algoritm.dfs(list_graph, start)
            self.k = AnimateNodeAndEdges()
            self.k.dfs_animate(self.graphvisualiser.visual_nodes, self.graphvisualiser.visual_edges, res_dfs, 500, self.console)
            res1 = ' '.join(map(str, res))
            self.console_print("Результат: "+str(res1))
        elif "BFS (Поиск в ширину) - 3" == text_algo:
            try:
                start = int(self.RightBar.lineEdit_Node.text())
            except ValueError:
                start = 1
            list_graph = self.graph_control.get_graph()
            res_bfs = self.algoritm.bfs_2path(list_graph, start)
            self.k = AnimateNodeAndEdges()
            self.k.dfs_animate(self.graphvisualiser.visual_nodes, self.graphvisualiser.visual_edges, res_bfs, 500,
                               self.console)
        elif "Число компонент свзяности - 5" == text_algo:
            res = self.algoritm.components_check(self.graph_control.get_graph())
            if res['cnt'] == 0:
                self.console_print(
                    str(f'Количество компонента связности: 0'))
            else:
                self.console_print(
                    str(f'Количество компонента связности:{str(res["cnt"])}'))

                for x in range(int(res['cnt'])):
                    self.console_print(f"{x+1}: " +
                        str(' '.join(map(str, res[x+1]))))
        elif "Прима для MST - 7" == text_algo:
            try:
                start = int(self.RightBar.lineEdit_Node.text())
            except ValueError:
                start = None
            list_graph = self.graph_control.get_graph()
            res, weight = self.algoritm.prima(list_graph, start)

            self.k = AnimateNodeAndEdges()
            self.k.tree_ost(self.graphvisualiser.visual_nodes, self.graphvisualiser.visual_edges, res, 500,
                               self.console)
        elif "Проверка DFS - 2" == text_algo:
            try:
                start = int(self.RightBar.lineEdit_Node.text())
            except ValueError:
                start = 1
            input_txt = self.test_algoritm("Пример ввода: 1-3 3-2 2-4, либо 1 2 3 4")
            if input_txt is None:
                return
            list_graph = self.graph_control.get_graph()
            res_dfs = self.algoritm.dfs_2path(list_graph, start)
            if '-' in input_txt:
                try:
                    user_edges = []
                    for item in input_txt.split():
                        u, v = map(int, item.split('-'))
                        user_edges.append((u, v))

                    actual_path = self.algoritm.dfs_2path(list_graph, start)
                    actual_edges = [tuple(edge) for edge in actual_path if edge[0] != 0]

                    if user_edges == actual_edges:
                        self.console_print("Верно! Пути обхода совпадают.")
                    else:
                        self.console_print(f"Ошибка!\nВаши ребра: {user_edges}\nПравильные: {actual_edges}")
                except Exception as e:
                    self.console_print(str(e))
            else:
                try:
                    expected_nodes = [int(x) for x in input_txt.split()]
                    actual_nodes = self.algoritm.dfs(list_graph, start)
                    if expected_nodes == actual_nodes:
                        self.console_print("Верно! Последовательность обхода совпадает.")
                    else:
                        self.console_print(f" Ошибка! \nВаш ответ: {expected_nodes}\nПравильный: {actual_nodes}",)
                except Exception as e:
                    self.console_print(f"Ошибка ввода: {e}")

        elif "Проверка BFS - 4" == text_algo:
            try:
                start = int(self.RightBar.lineEdit_Node.text())
            except ValueError:
                start = 1

            input_txt = self.test_algoritm("Введите ожидаемую последовательность BFS (например: 1 2 3 4)")
            if input_txt is None:
                return
            if input_txt:
                list_graph = self.graph_control.get_graph()
                try:
                    expected_nodes = [int(x) for x in input_txt.split()]
                    actual_nodes = self.algoritm.bfs(list_graph, start)

                    if expected_nodes == actual_nodes:
                        self.console_print("Верно! Последовательность BFS совпадает.")
                    else:
                        self.console_print(
                            f"Ошибка в BFS!\nВаш ответ: {expected_nodes}\nПравильный: {actual_nodes}")
                except Exception as e:
                    self.console_print(f"Ошибка парсинга: {e}")
        elif "Проверка компонент связности - 6" == text_algo:
            input_txt = self.test_algoritm("Сколько компонент связности в этом графе? Введите число:")
            if input_txt is None:
                return
            if input_txt:
                try:

                    user_count = int(input_txt.strip())

                    list_graph = self.graph_control.get_graph()
                    actual_res = self.algoritm.components_check(list_graph)
                    actual_count = actual_res.get('cnt', 0)

                    if user_count == actual_count:
                        self.console_print(f"Верно! В графе ровно {actual_count} компонент(ы) связности.")
                    else:
                        self.console_print(f"Ошибка! Вы указали {user_count}, но на самом деле их {actual_count}.")

                except ValueError:
                    self.console_print("Ошибка: нужно ввести целое число!")
        elif "Кодирование Прюфера - 10" == text_algo:
            graph = self.graph_control.get_graph()
            nodes_cnt = len(graph)
            edges_cnt = sum(len(neighbors) for neighbors in graph.values()) // 2

            if nodes_cnt > 1 and edges_cnt == nodes_cnt - 1:
                try:
                    res = self.algoritm.prufera(graph)
                    self.console_print(f"Код Прюфера: {' '.join(map(str, res))}")
                except ValueError as e:
                    self.console_print(f"Ошибка: {e}")
            else:
                self.console_print("Ошибка: Граф должен быть деревом!")


        elif "Декодирование Прюфера - 11" == text_algo:
            input_txt = self.test_algoritm("Введите код через пробел (напр. 4 4 4):")
            if input_txt is None:
                return
            if input_txt:
                try:
                    code = [int(x) for x in input_txt.split()]
                    edges = self.algoritm.prufera_decode(code)
                    adj = {}

                    for u, v in edges:
                        if u not in adj: adj[u] = []
                        if v not in adj: adj[v] = []
                        adj[u].append(str(v))
                        adj[v].append(str(u))

                    lines = [f"{node}: {', '.join(neighbors)}" for node, neighbors in adj.items()]
                    graph_str = "\n".join(lines)

                    self.graph_control.update_graph_list(graph_str)
                    self.graphvisualiser.draw_circle()
                    self.console_print(f"Дерево восстановлено из кода {code}")

                except Exception as e:
                    self.console_print(f"Ошибка декодирования: {e}")

        elif "Алгоритм Дейкстера - 8" == text_algo:
            try:
                # Берем стартовую вершину из lineEdit
                start = int(self.RightBar.lineEdit_Node.text())
            except ValueError:
                start = 1

            list_graph = self.graph_control.get_graph()

            # Проверка наличия вершины
            if start not in list_graph:
                self.console_print(f"Ошибка: Вершины {start} нет в графе")
                return

            distances, path_edges = self.algoritm.dijkstra(list_graph, start)
            self.k = AnimateNodeAndEdges()
            self.k.dijkstra_animate(
                self.graphvisualiser.visual_nodes,
                self.graphvisualiser.visual_edges,
                path_edges,
                500,
                self.console,
                distances
            )

        elif "Раскраска графа - 12" == text_algo:
            list_graph = self.graph_control.get_graph()
            if not list_graph:
                self.console_print("Граф пуст!")
                return

            # Получаем словарь {узел: индекс_цвета}
            colors = self.algoritm.coloring(list_graph)

            # Находим хроматическое число (макс. индекс + 1)
            chromatic_num = max(colors.values()) + 1
            self.console_print(f"Хроматическое число (приблизительно): {chromatic_num}")

            # Запускаем анимацию
            self.k = AnimateNodeAndEdges()
            self.k.coloring_animate(
                self.graphvisualiser.visual_nodes,
                colors,
                500,
                self.console
            )

        elif "Матрицы кратчайших путей - 9" == text_algo:
            list_graph = self.graph_control.get_graph()
            if not list_graph:
                self.console_print("Граф пуст!")
                return

            # Получаем список вершин и матрицу
            nodes, matrix = self.algoritm.floyd_warshall(list_graph)

            self.console.clear()
            self.console.appendHtml("<b>Матрица кратчайших путей (Флойд-Уоршелл):</b><br>")

            # Формируем шапку таблицы
            header = "&nbsp;&nbsp;&nbsp;&nbsp;" + "&nbsp;&nbsp;".join([f"<b>{n}</b>" for n in nodes])
            self.console.appendHtml(header)

            # Выводим строки матрицы
            for i, row_node in enumerate(nodes):
                row_str = f"<b>{row_node}</b>: "
                formatted_row = []
                for val in matrix[i]:
                    if val == float('inf'):
                        formatted_row.append("∞")
                    else:
                        formatted_row.append(str(val))

                row_str += "&nbsp;&nbsp;".join(formatted_row)
                self.console.appendHtml(row_str)

            self.console_print("<br>Расчет завершен.")


    def btn_save_json(self):
        self.btnSave:QPushButton = self.RightBar.pushButton_Export
        self.btnSave.clicked.connect(self.save_json)
    def save_json(self):
        path, _ = QFileDialog.getSaveFileName(
            self, "Выберите папку сохранения", "graph.json", "JSON"
        )
        if not path:
            return
        path = Path(path)
        graph_dict = self.Files.get_nodes_with_xy()
        if path:
            with path.open("w", encoding = 'utf-8') as f:
                json.dump(graph_dict, f, indent=5)
    def update_ui_node(self, node_id):
        self.RightBar.lineEdit_Node.setText(str(node_id))

    def console_print(self, text:str):
        text = f'<span>{text}</span>'
        self.console.appendHtml(text)








class StartMenu(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('ui/menubeta1.ui', self)

        self.cardNewProject = self.findChild(QFrame, 'frame_2')
        self.setStyleSheet("QWidget { background-color: white; color: black; }")

        if self.cardNewProject:
            self.cardNewProject.installEventFilter(self)
            self.cardNewProject.setCursor(Qt.CursorShape.PointingHandCursor)
        else:
            print("Нет такого файла")

    def eventFilter(self, obj, event):
        if obj == self.cardNewProject and event.type() == event.Type.MouseButtonPress:
            if event.button() == Qt.MouseButton.LeftButton:
                self.open_main_program()
                return True
        return super().eventFilter(obj, event)

    def open_main_program(self):
        self.main_window = Window()
        self.main_window.show()
        self.close()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    # window = Window()
    # apply_stylesheet(app, theme='dark_teal.xml')
    # window.show()
    menu = StartMenu()
    menu.setFixedSize(1024, 576)
    menu.show()
    sys.exit(app.exec())
