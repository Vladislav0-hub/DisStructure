import math
import sys
import random
from PyQt6 import uic
from PyQt6.QtCore import Qt, QRectF, QLine, QLineF, QSize, QTimer
from PyQt6.QtGui import QBrush, QColor, QPen, QIcon, QStandardItemModel, QStandardItem, QAction, QPainterPath
from PyQt6.QtWidgets import QMainWindow, QWidget, QHBoxLayout, QApplication, QFrame, QVBoxLayout, QGraphicsScene, \
    QGraphicsView, QGraphicsEllipseItem, QGraphicsItem, QGraphicsLineItem, QGraphicsPathItem, QGraphicsTextItem, QPushButton, \
    QGraphicsDropShadowEffect, QTableView, QHeaderView, QSplitter, QLabel, QMessageBox, QMenu


class Edge(QGraphicsPathItem):
    def __init__(self, source, dst,weight=1):
        super().__init__()
        self.source = source
        self.dst = dst
        self.weight = weight
        self.is_loop = source == dst
        self.setPen(QPen(QColor("#94A3B8"), 2))
        self.text_item = QGraphicsTextItem(str(weight), self)
        self.text_item.setDefaultTextColor(Qt.GlobalColor.black)
        self.update_pos()
        self.setZValue(-2)


    def update_pos(self):
        pos_source = self.source.pos()
        pos_dst = self.dst.pos()
        path = QPainterPath()
        if self.is_loop:
            x = pos_source.x()
            y = pos_source.y()
            path.moveTo(x + 10, y - 10)
            path.cubicTo(x + 30, y - 34, x - 30, y - 34, x - 10, y - 10)
            path.cubicTo(x - 28, y + 8, x + 28, y + 8, x + 10, y - 10)
        else:
            path.moveTo(pos_source.x(), pos_source.y())
            path.lineTo(pos_dst.x(), pos_dst.y())
        self.setPath(path)
        self.center_text()

    def center_text(self):
       if self.is_loop:
           k = self.source.pos()
           self.text_item.setPos(k.x() - self.text_item.boundingRect().width() / 2, k.y() - 40)
       else:
           pos_source = self.source.pos()
           pos_dst = self.dst.pos()
           x = (pos_source.x() + pos_dst.x()) / 2
           y = (pos_source.y() + pos_dst.y()) / 2
           self.text_item.setPos(x, y)

    def changeColor(self):
        self.setPen(QPen(QColor("#10b981"), 2))
        self.setZValue(-1)

    def resetColor(self):
        self.setPen(QPen(QColor("#94A3B8"), 2))




class Node(QGraphicsEllipseItem):
    def __init__(self,node_id ,x,y):
        super().__init__(-15,-15,30,30)
        self.setCacheMode(QGraphicsItem.CacheMode.DeviceCoordinateCache)
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(15)
        shadow.setOffset(5, 5)  # смещение тени (x, y)
        shadow.setColor(QColor(0, 0, 0, 60))
        self.id = node_id
        self.setData(0, node_id)
        self.setGraphicsEffect(shadow)
        self.edges = []
        self.color = "#94A3B8"
        self.setPos(x, y)
        self.setPen(QPen(QColor(self.color), 2))

        self.setBrush(QBrush(QColor(Qt.GlobalColor.white)))

        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsMovable)
        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsSelectable)
        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemSendsGeometryChanges)

        self.text_item = QGraphicsTextItem(str(node_id), self)
        self.text_item.setDefaultTextColor(Qt.GlobalColor.black)
        self.center_text()

    @property
    def get_edge(self, dst_node):
        for edge in self.edges:
            if edge.dst == dst_node:
                return edge
        return None
    def center_text(self):
        center = self.text_item.boundingRect()
        self.text_item.setPos(-center.width()/2,-center.height()/2)

    def add_edge(self, edgesss):
        self.edges.append(edgesss)

    def itemChange(self, change, value):
        if change == QGraphicsItem.GraphicsItemChange.ItemPositionHasChanged:
            for edge in self.edges:
                edge.update_pos()
        return super().itemChange(change, value)
    def changeColor(self, color="#10b981"):
        self.color = color
        self.setBrush(QBrush(QColor(color)))
        self.setPen(QPen(QColor(color), 2))

    def resetColor(self):
        self.color = "#94A3B8"
        self.setPen(QPen(QColor(self.color), 2))
        self.setBrush(QBrush(QColor(Qt.GlobalColor.white)))
    @property
    def get_color(self):
        return self.color
