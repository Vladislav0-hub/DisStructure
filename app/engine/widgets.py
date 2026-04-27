import math
import sys
import random
from PyQt6 import uic
from PyQt6.QtCore import Qt, QRectF, QLine, QLineF, QSize, QTimer
from PyQt6.QtGui import QBrush, QColor, QPen, QIcon, QStandardItemModel, QStandardItem, QAction
from PyQt6.QtWidgets import QMainWindow, QWidget, QHBoxLayout, QApplication, QFrame, QVBoxLayout, QGraphicsScene, \
    QGraphicsView, QGraphicsEllipseItem, QGraphicsItem, QGraphicsLineItem, QGraphicsTextItem, QPushButton, \
    QGraphicsDropShadowEffect, QTableView, QHeaderView, QSplitter, QLabel, QMessageBox, QMenu, QDialog, QPlainTextEdit, QDialogButtonBox


class isAddButton(QPushButton):
    def __init__(self):
        super().__init__()
        self.setIcon(QIcon("icon/add_circle_24dp_FFFFFF_FILL0_wght400_GRAD0_opsz24 (1).svg"))
        self.setIconSize(QSize(24, 24))
        self.setStyleSheet("""
                            QPushButton {
                                background-color: #3498db;
                                color: white;
                                border-radius: 10px;
                                padding: 10px;
                            }
                            QPushButton:pressed {
                                background-color: #2980b9;
                                padding-left: 15px; /* эффект смещения */
                                padding-top: 12px;
                            }
                        """)
        self.menu_add = QMenu(self)

        self.menu_add.setStyleSheet("""
                    QMenu {
                        background-color: #2c3e50;
                        color: white;
                        border: 1px solid #34495e;
                    }
                    QMenu::item:selected {
                        background-color: #3498db;
                    }
                """)

        add_list = QAction("Добавить списком смежности", self)
        add_matrix = QAction("Добавить матрицей", self)
        add_incidence_matrix = QAction("Добавить матрицей инцидентности", self)

        self.menu_add.addAction(add_list)
        self.menu_add.addAction(add_matrix)
        self.menu_add.addAction(add_incidence_matrix)

        self.clicked.connect(self.show_sidebar_menu)
        # self.setMenu(self.menu_add)

    def show_sidebar_menu(self):
        button_rect = self.rect()
        point = button_rect.topRight()
        point.setX(point.x() + 10)
        global_point = self.mapToGlobal(point)
        self.menu_add.exec(global_point)

class isClickButton(QPushButton):
    def __init__(self):
        super().__init__()
        self.setIcon(QIcon("icon/add_click_icon.svg"))
        self.setIconSize(QSize(24, 24))
        self.setStyleSheet("""
                    QPushButton {
                        background-color: #3498db;
                        color: white;
                        border-radius: 10px;
                        padding: 10px;
                    }
                    QPushButton:pressed {
                        background-color: #2980b9;
                        padding-left: 15px; /* эффект смещения */
                        padding-top: 12px;
                    }
                """)
    def enable(self):
        #походу пока не надо
        pass

class isAddEdgeButton(QPushButton):
    def __init__(self):
        super().__init__()
        self.add_edges_click = False
        self.setIcon(QIcon("icon/add_edge.svg"))
        self.setIconSize(QSize(24, 24))
        self.setStyleSheet("""
                            QPushButton {
                                background-color: #3498db;
                                color: white;
                                border-radius: 10px;
                                padding: 10px;
                            }
                            QPushButton:pressed {
                                background-color: #2980b9;
                                padding-left: 15px; /* эффект смещения */
                                padding-top: 12px;
                            }
                        """)


class DeleteButton(QPushButton):
    def __init__(self):
        super().__init__()
        self.delete_click = False
        self.setIcon(QIcon("icon/delete_btn.svg"))
        self.setIconSize(QSize(24, 24))
        self.setStyleSheet("""
                                    QPushButton {
                                        background-color: #3498db;
                                        color: white;
                                        border-radius: 10px;
                                        padding: 10px;
                                    }
                                    QPushButton:pressed {
                                        background-color: #2980b9;
                                        padding-left: 15px; /* эффект смещения */
                                        padding-top: 12px;
                                    }
                                """)
class GraphInput(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Ввод")
        self.setMinimumSize(300, 200)

        layout = QVBoxLayout(self)
        self.text_edit = QPlainTextEdit()
        layout.addWidget(self.text_edit)
        buttons = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)
    def get_text(self):
        return self.text_edit.toPlainText()

