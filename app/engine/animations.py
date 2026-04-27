import math
import sys
import random
from PyQt6 import uic
from PyQt6.QtCore import Qt, QRectF, QLine, QLineF, QSize, QTimer
from PyQt6.QtGui import QBrush, QColor, QPen, QIcon, QStandardItemModel, QStandardItem, QAction
from PyQt6.QtWidgets import QMainWindow, QWidget, QHBoxLayout, QApplication, QFrame, QVBoxLayout, QGraphicsScene, \
    QGraphicsView, QGraphicsEllipseItem, QGraphicsItem, QGraphicsLineItem, QGraphicsTextItem, QPushButton, \
    QGraphicsDropShadowEffect, QTableView, QHeaderView, QSplitter, QLabel, QMessageBox, QMenu

class AnimateNodeAndEdges():
    def start_path_animation(self, list_nodes, list_edge, path, time_sec, console, title="Запущен алгоритм", result_data=None):
        self.console = console
        self.console.clear()
        self.console.appendHtml(title)
        self.list_nodes = list_nodes
        self.list_edge = list_edge
        self.title = title
        self.path = path
        self.timer = QTimer()
        self.clearColor(list_nodes, list_edge)
        self.result_data = result_data
        #баг с (0, src/dst) был
        if self.path:
            first = self.path[0]
            start_id = first[1] if first[0] == 0 else first[0]
            if self.list_nodes.get(start_id):
                self.list_nodes.get(start_id).changeColor()

        self.timer.timeout.connect(self.animation_timer)
        self.timer.start(time_sec)
        self.old = -1
        pass

    def animation_timer(self):
        if self.path:
            # source,dst = self.path.pop(0)
            t = self.path.pop(0)
            source, dst = t[0], t[1]
            node = self.list_nodes.get(dst)
            if node:
                node.changeColor()
            if source > 0:
                print(f" {source} - {dst}")
                self.console.appendHtml(f"{source} - {dst}")
                # edge = self.list_edge.get(f"{source}-{dst}")
                edge = self.list_edge.get((source, dst)) or self.list_edge.get((dst, source))
                if edge:
                    edge.changeColor()
        else:
            self.timer.stop()
            self.console.appendHtml("Алгоритм завершен")
            if isinstance(self.result_data, dict):
                for node, dist in self.result_data.items():
                    d_str = "∞" if dist == float('inf') else str(dist)
                    self.console.appendHtml(f"До узла {node}: <b>{d_str}</b>")

    def dfs_animate(self, list_nodes, list_edge, res_dfs, time_sec, console):
        self.start_path_animation(list_nodes, list_edge, res_dfs, time_sec, console, "Запущен алгоритм обхода в глубину ")

    def bfs_animate(self, list_nodes, list_edge, res_bfs, time_sec, console):
        self.start_path_animation(list_nodes, list_edge, res_bfs, time_sec, console,
                                  "Запущен алгоритм обхода в ширину ")

    def tree_ost(self, list_nodes, list_edge, res, time_sec, console):
        self.start_path_animation(list_nodes, list_edge, res, time_sec, console,
                                  "Запущен алгоритм построения оставного дерева ")

    def dijkstra_animate(self, list_nodes, list_edge, res, time_sec, console, distances):
        self.start_path_animation(list_nodes, list_edge, res, time_sec, console, "Поиск кратчайших путей (Дейкстра)", distances)





    def clearColor(self,list_nodes,list_edge):
        nodes = list_nodes.values() if isinstance(list_nodes, dict) else list_nodes
        for x in nodes:
            x.resetColor()
        for x in list_edge.values():
            x.resetColor()

    def coloring_animate(self, list_nodes, coloring_res, time_sec, console):
        palette = [
            "#e74c3c", "#2ecc71", "#3498db", "#f1c40f",
            "#9b59b6", "#e67e22", "#1abc9c", "#34495e",
            "#d35400", "#27ae60", "#2980b9", "#8e44ad"
        ]

        self.console = console
        self.console.clear()
        self.console.appendHtml("<b>Запущен алгоритм раскраски графа</b>")

        self.list_nodes = list_nodes
        # Превращаем результат в список для анимации [(node_id, color_hex), ...]
        self.path = [(node, palette[idx % len(palette)]) for node, idx in coloring_res.items()]

        self.clearColor(list_nodes, {})  # Очищаем только узлы

        self.timer = QTimer()
        self.timer.timeout.connect(self.coloring_timer_step)
        self.timer.start(time_sec)

    def coloring_timer_step(self):
        if self.path:
            node_id, color_hex = self.path.pop(0)
            node = self.list_nodes.get(node_id)
            if node:
                node.changeColor(color_hex)
                self.console.appendHtml(f"Узел {node_id} -> цвет <span style='color:{color_hex}'>■</span>")
        else:
            self.timer.stop()
            self.console.appendHtml("<br><b>Раскраска завершена!</b>")

    #на всякий
    # def dfs_animate(self, list_nodes,list_edge, res_dfs, time_sec, console):
    #     self.console = console
    #     self.console.clear()
    #     self.console.appendHtml("Запущен алгоритм обход в глубину")
    #     self.list_nodes = list_nodes
    #     self.list_edge = list_edge
    #     self.res_dfs = res_dfs
    #     self.timer = QTimer()
    #     self.clearColor(list_nodes,list_edge)
    #     self.timer.timeout.connect(self.animate_dfs_node)
    #     self.timer.start(time_sec)
    #     self.old = -1
    # def animate_dfs_node(self):
    #     if self.res_dfs:
    #         source,dst = self.res_dfs.pop(0)
    #         node = self.list_nodes.get(dst)
    #         if node:
    #             node.changeColor()
    #         if source > 0:
    #             print(f" {source} - {dst}")
    #             self.console.appendHtml(f"{source} - {dst}")
    #             # edge = self.list_edge.get(f"{source}-{dst}")
    #             edge = self.list_edge.get((source, dst)) or self.list_edge.get((dst, source))
    #             if edge:
    #                 edge.changeColor()
    #     else:
    #         self.timer.stop()
    #
    #
    # def bfs_animate(self, list_nodes,list_edge, res_bfs, time_sec, console):
    #     self.console = console
    #     self.console.clear()
    #     self.console.appendHtml("Запущен алгоритм обход в ширину")
    #     self.list_nodes = list_nodes
    #     self.list_edge = list_edge
    #     self.res_bfs = res_bfs
    #     self.timer = QTimer()
    #     self.clearColor(list_nodes,list_edge)
    #     self.timer.timeout.connect(self.animate_bfs_node)
    #     self.timer.start(time_sec)
    #     self.old = -1
    # def animate_bfs_node(self):
    #     if self.res_bfs:
    #         source,dst = self.res_bfs.pop(0)
    #         node = self.list_nodes.get(dst)
    #         if node:
    #             node.changeColor()
    #         if source > 0:
    #             print(f" {source} - {dst}")
    #             self.console.appendHtml(f"{source} - {dst}")
    #             # edge = self.list_edge.get(f"{source}-{dst}")
    #             edge = self.list_edge.get((source, dst)) or self.list_edge.get((dst, source))
    #             if edge:
    #                 edge.changeColor()
    #     else:
    #         self.timer.stop()