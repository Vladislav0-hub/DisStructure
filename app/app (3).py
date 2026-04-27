import math
import sys
import random
from PyQt6 import uic
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QMainWindow, QWidget, QHBoxLayout, QApplication, QFrame, QVBoxLayout, QSplitter, \
    QMessageBox, QDialog


from engine.animations import AnimateNodeAndEdges
from engine.items_graph import Edge, Node
from engine.logic import GraphControl, Algoritm
from engine.scene_paint import MyScene, MyView
from engine.widgets import isAddButton, isClickButton, GraphInput, isAddEdgeButton
from engine.GraphVisual import GraphVisual


class Window(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setMinimumSize(1280, 720)
        self.central_widget = QSplitter(Qt.Orientation.Horizontal)
        self.setCentralWidget(self.central_widget)
        self.main_layout = QHBoxLayout(self.central_widget)

        self.sidebar()
        self.scene_w()

        # Сигналы кнопок
        self.addClickBtn.clicked.connect(self.view.enable_click_btn)
        self.addEdgesBtn.clicked.connect(self.view.click_btn_add_edges)

        self.algoritm = Algoritm()
        self.rightMenu()

        # Инициализация плавающей панели мониторинга
        self.init_info_panel()

    def init_info_panel(self):
        """Создает и настраивает маленькую карточку алгоритма"""
        try:
            self.info_panel = QWidget(self)  # Родитель - всё окно
            uic.loadUi('ui/task_monitor.ui', self.info_panel)
            self.info_panel.setFixedWidth(240)  # Фиксируем ширину для красоты
            self.info_panel.hide()  # Скрываем до запуска алгоритма
        except Exception as e:
            print(f"Ошибка загрузки task_monitor.ui: {e}")

    def update_monitor(self, title, p1_name, p1_val, p2_name, p2_val):
        """Обновляет текст в карточке (использует objectName из Designer)"""
        if hasattr(self, 'info_panel'):
            self.info_panel.lblTitle.setText(title)
            self.info_panel.lblParam1Name.setText(p1_name)
            self.info_panel.lblParam1Value.setText(str(p1_val))
            self.info_panel.lblParam2Name.setText(p2_name)
            self.info_panel.lblParam2Value.setText(str(p2_val))
            self.info_panel.show()
            self.reposition_monitor()

    def reposition_monitor(self):
        """Держит панель в левом нижнем углу над сценой"""
        if hasattr(self, 'info_panel') and self.info_panel.isVisible():
            # Позиция: отступ 100px от левого края (чтобы не перекрывать сайдбар)
            # и 40px от нижнего края
            self.info_panel.move(100, self.height() - self.info_panel.height() - 40)

    def resizeEvent(self, event):
        """Срабатывает при растягивании окна пользователем"""
        super().resizeEvent(event)
        self.reposition_monitor()

    def sidebar(self):
        self.bar = QFrame()
        self.bar.setStyleSheet("background-color: #2c3e50;")
        self.bar.setMaximumWidth(80)
        self.addNodesBtn = isAddButton()
        self.addClickBtn = isClickButton()
        self.addEdgesBtn = isAddEdgeButton()
        self.layout_bar = QVBoxLayout(self.bar)
        self.layout_bar.addWidget(self.addNodesBtn)
        self.layout_bar.addWidget(self.addClickBtn)
        self.layout_bar.addWidget(self.addEdgesBtn)
        self.layout_bar.addStretch(1)
        self.addNodesBtn.menu_add.actions()[0].triggered.connect(self.add_list_dialog)
        self.addNodesBtn.menu_add.actions()[1].triggered.connect(self.add_matrix_dialog)
        self.main_layout.addWidget(self.bar)

    def scene_w(self):
        self.graph_control = GraphControl()
        self.scene = MyScene()
        self.graphvisualiser = GraphVisual(self.scene, self.graph_control, self)
        self.view = MyView(self.scene, self.graph_control, self, self.graphvisualiser)
        self.main_layout.addWidget(self.view)

    def rightMenu(self):
        self.RightBar = QWidget()
        uic.loadUi('ui/rightmenunode2.ui', self.RightBar)
        self.main_layout.addWidget(self.RightBar)
        self.RightBar.setFixedWidth(300)
        self.RightBar.btnStartAlgo.clicked.connect(self.click_start_algo)

    def click_start_algo(self):
        text_algo = self.RightBar.algorithm_list.currentText()
        list_graph = self.graph_control.get_graph()

        try:
            start = int(self.RightBar.lineEdit_Node.text())
        except ValueError:
            start = 1

        if "DFS (Обход в глубину)" == text_algo:
            self.res_bfs = self.algoritm.dfs_2path(list_graph, start)

            # Обновляем инфо-панель
            self.update_monitor(
                "📈 Алгоритм DFS",
                "Узлов посещено:", len(self.res_bfs),
                "Статус:", "Выполнено"
            )

            self.k = AnimateNodeAndEdges()
            self.k.bfs_animate(self.graphvisualiser.visual_nodes, self.graphvisualiser.visual_edges, self.res_bfs, 500)

        elif "BFS (Поиск в ширину)" == text_algo:
            # Сюда можно добавить логику для BFS по аналогии
            self.update_monitor("📉 Алгоритм BFS", "Очередь:", "-", "Посещено:", "0")

    # Вспомогательные методы (оставил как в твоем коде)
    def update_ui_node(self, node_id):
        self.RightBar.lineEdit_Node.setText(str(node_id))

    def add_list_dialog(self):
        dialog = GraphInput(self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            print(dialog.get_text())

    def add_matrix_dialog(self):
        dialog = GraphInput(self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            text = dialog.get_text()
            try:
                matrix = [[int(x) for x in line.split()] for line in text.strip().split('\n') if line.strip()]
                self.graphvisualiser.ellipse_xy_draw(matrix)
            except Exception as e:
                QMessageBox.critical(self, "Ошибка", f"Неверный формат - {e}")


class StartMenu(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('ui/menubeta1.ui', self)
        self.cardNewProject = self.findChild(QFrame, 'frame_2')
        self.setStyleSheet("QWidget { background-color: white; color: black; }")
        if self.cardNewProject:
            self.cardNewProject.installEventFilter(self)
            self.cardNewProject.setCursor(Qt.CursorShape.PointingHandCursor)

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
    menu = StartMenu()
    menu.show()
    sys.exit(app.exec())