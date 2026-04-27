import math
import sys
import random
from PyQt6 import uic
from PyQt6.QtCore import Qt, QRectF, QLine, QLineF, QSize, QTimer
from PyQt6.QtGui import QBrush, QColor, QPen, QIcon, QStandardItemModel, QStandardItem, QAction
from PyQt6.QtWidgets import QMainWindow, QWidget, QHBoxLayout, QApplication, QFrame, QVBoxLayout, QGraphicsScene, \
    QGraphicsView, QGraphicsEllipseItem, QGraphicsItem, QGraphicsLineItem, QGraphicsTextItem, QPushButton, \
    QGraphicsDropShadowEffect, QTableView, QHeaderView, QSplitter, QLabel, QMessageBox, QMenu


from .GraphVisual import GraphVisual
from .logic import GraphControl

class Files:
    def __init__(self, graph_visual:GraphVisual, graph_control:GraphControl):
        self.graph_visual = graph_visual
        self.graph_control = graph_control
    def get_nodes_with_xy(self) -> dict:
        json_graph = {}
        graph = self.graph_control.get_graph()
        nodes = [ {"id":x} for x in graph.keys()]
        json_graph['nodes'] = nodes
        t = []
        for i, neighbors in graph.items():
            for dst, weight in neighbors.items():
                d = {"source": i, "dst":dst, "weight":weight}
                t.append(d)
        json_graph['edges'] = t
        return json_graph

