import sqlite3
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidget, QTableWidgetItem
from PyQt5.QtSql import QSqlDatabase, QSqlQuery

class ServerWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Tabla de Servidores")
        self.setGeometry(100, 100, 600, 400)

        self.create_table_widget()

    def create_table_widget(self):
        self.table_widget = QTableWidget(self)
        self.setCentralWidget(self.table_widget)

        # Configurar la tabla
        self.table_widget.setColumnCount(3)
        self.table_widget.setHorizontalHeaderLabels(['Nombre de Servidor', 'IP', 'Estado'])

        # Conectar a la base de datos
        self.db = QSqlDatabase.addDatabase("QSQLITE")
        self.db.setDatabaseName("Servidores")  # Nombre de tu base de datos SQLite

        if not self.db.open():
            print("No se pudo abrir la base de datos")
            return

        query = QSqlQuery()
        query.exec_("SELECT * FROM SERVIDOR")

        row = 0
        while query.next():
            self.table_widget.insertRow(row)
            self.table_widget.setItem(row, 0, QTableWidgetItem(query.value(0)))
            self.table_widget.setItem(row, 1, QTableWidgetItem(query.value(1)))
            self.table_widget.setItem(row, 2, QTableWidgetItem(query.value(2)))
            row += 1

def main():
    app = QApplication(sys.argv)
    window = ServerWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()