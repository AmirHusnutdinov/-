import sys
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QApplication, QTableWidgetItem, QHeaderView
from PyQt5.QtWidgets import QMainWindow, QWidget
from addEditCoffeeForm import Ui_Form
from mainui import Ui_MainWindow
import sqlite3


# Чтобы изменить значение надо кликнуть на ID и нажать на кнопку

class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.ask = False
        self.id = None
        self.load()
        self.tableWidget.itemSelectionChanged.connect(self.on_selct)

    def load(self):
        con = sqlite3.connect('data/coffe.db')
        cur = con.cursor()
        lst = cur.execute(f'''SELECT * FROM coffes''')

        self.tableWidget.setColumnCount(6)
        self.tableWidget.setHorizontalHeaderLabels(['ID', 'Помол', 'Качество',
                                                    'Обжарка', 'Название', 'Цена'])
        self.tableWidget.setRowCount(0)

        for i, row in enumerate(lst):
            self.tableWidget.setRowCount(
                self.tableWidget.rowCount() + 1)

            for j, elem in enumerate(row):
                self.tableWidget.setItem(
                    i, j, QTableWidgetItem(f'{elem}'))

        self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.btn.clicked.connect(self.show_window)

    def show_window(self):
        self.ex1 = NewWindow(self.ask, self.id)
        self.ex1.window_closed.connect(self.load)
        self.ex1.show()
        if self.ex1.ask:
            self.ex1.line_name.setText('')
            self.ex1.line_price.setText('')

    def on_selct(self):
        if self.tableWidget.currentColumn() == 0:
            self.ask = True
            self.id = self.tableWidget.item(self.tableWidget.currentRow(), 0).text()


class NewWindow(QWidget, Ui_Form):
    window_closed = pyqtSignal()

    def __init__(self, ask=None, id=None):
        super().__init__()
        self.setupUi(self)
        self.ask = ask
        self.id = id
        if ask:
            self.con = sqlite3.connect('data/coffe.db')
            self.cur = self.con.cursor()
            lst = self.cur.execute(f'''SELECT *
             from coffes WHERE id == {id}''').fetchall()
            lst = [i for i in lst[0]]
            self.box_griding.setCurrentIndex(self.box_griding.findText(lst[1]))
            self.box_quality.setCurrentIndex(self.box_quality.findText(lst[2]))
            self.box_degrees.setCurrentIndex(self.box_degrees.findText(lst[3]))
            self.line_name.setText(str(lst[4]))
            self.line_price.setText(str(lst[5]))

        self.btn.clicked.connect(self.run)

    def run(self):
        self.con = sqlite3.connect('data/coffe.db')
        self.cur = self.con.cursor()
        if not self.ask:
            self.cur.execute(f'''INSERT INTO coffes(grind, quality,
             degree, name, price)
            VALUES("{self.box_griding.currentText()}", 
            "{self.box_quality.currentText()}",
            "{self.box_degrees.currentText()}",
            "{self.line_name.text()}", 
            "{self.line_price.text()}")''')

        else:
            self.cur.execute(f'''UPDATE coffes
            SET grind = "{self.box_griding.currentText()}", 
            quality = "{self.box_quality.currentText()}", 
            degree = "{self.box_degrees.currentText()}", 
            name = "{self.line_name.text()}", 
            price = "{self.line_price.text()}"
            WHERE id = {self.id}''')

        self.con.commit()
        self.close()
        self.line_name.setText('')
        self.line_price.setText('')

    def closeEvent(self, event):
        self.window_closed.emit()

        event.accept()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MainWindow()
    ex.show()
    sys.exit(app.exec_())
