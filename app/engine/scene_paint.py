from PyQt6.QtCore import Qt
from PyQt6.QtGui import QBrush
from PyQt6.QtWidgets import QGraphicsScene, \
    QGraphicsView
from .items_graph import Edge, Node
from .logic import GraphControl
from .GraphVisual import GraphVisual

class MyScene(QGraphicsScene):
    def __init__(self):
        super().__init__()
        self.cntNode = 2
        #self.setSceneRect(-500, -500, 1000, 1000)
        self.setSceneRect(-5000, -5000, 10000, 10000)


class MyView(QGraphicsView):
    """ Видимая зона сцены """
    def __init__(self, scene:MyScene, graph_control:GraphControl, main_window, graph_visual:GraphVisual):
        super().__init__(scene)
        self.my_scene = scene
        self.window = main_window
        self.setBackgroundBrush(QBrush(Qt.GlobalColor.white))
        self.graph_control = graph_control
        self.graph_visual = graph_visual
        self.click = False
        self.add_edges_click = False
        self.first_node = None
        self.color_first_node = None

        self.setTransformationAnchor(QGraphicsView.ViewportAnchor.AnchorUnderMouse)
    """ Обработка кликов на сцене (вершин, ребер()), перенос информации при клике в меню инспектора """
    def mousePressEvent(self, event):
        pos = event.pos()
        item = self.itemAt(pos)
        if item and not isinstance(item, Node):
            parent = item.parentItem()
            if isinstance(parent, Node):
                item = parent
        if self.click:
            if not item:
                self.setDragMode(QGraphicsView.DragMode.NoDrag)
                pos = self.mapToScene(pos) #перевод в координаты сцены, т.к. я сделал цену отсчета от нуля
                self.graph_visual.draw_new_node(pos.x(), pos.y())

        elif self.add_edges_click:
            if not item and self.first_node:
                self.first_node.resetColor()
                self.first_node = None
            if isinstance(item, Node):
                if not self.first_node:
                    self.first_node = item
                    self.first_node.changeColor('#FFFF00')
                elif self.first_node and item:
                    self.first_node.resetColor()
                    self.graph_visual.draw_new_edge(self.first_node.id, item.id)
                    self.first_node = None
                    print(1111)
        else:
            self.setDragMode(QGraphicsView.DragMode.ScrollHandDrag)
        if isinstance(item, Node):
            node_id = item.data(0)
            self.window.update_ui_node(node_id)


        super().mousePressEvent(event)
    """ Кнопка добавить вершину """
    def enable_click_btn(self):
        self.click = not self.click
        if self.click:
            self.add_edges_click = False
    """ Кнопка добавить ребро """
    def click_btn_add_edges(self):
        if self.first_node:
            self.first_node.resetColor()
            self.first_node = None
        self.add_edges_click = not self.add_edges_click
        if self.add_edges_click:
            self.click = False


    """ зум """
    def wheelEvent(self, event):
        factor = 1.1 if event.angleDelta().y() > 0 else 0.9
        self.scale(factor, factor)


