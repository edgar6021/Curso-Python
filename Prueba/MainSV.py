import sys
import time
import ping3
import threading
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidget, QTableWidgetItem, QDialog, QLabel, QLineEdit, QVBoxLayout, QPushButton, QComboBox
from PyQt5.QtSql import QSqlDatabase, QSqlQuery
from PyQt5.uic import loadUi
from PyQt5.QtGui import QIcon

class MiVentana(QMainWindow):
    def __init__(self):
        super().__init__()
        loadUi('IFC.UI', self)

        self.UPLABEL.setVisible(False)
        self.UPICON.setVisible(False)
        self.DOWNLABEL.setVisible(False)
        self.DOWNICON.setVisible(False)

        self.ping_thread = None
        self.actionAgregar_IP.triggered.connect(self.mostrar_dialogo_agregar_servidor)

        self.iniciar_hilo_ping()

    def iniciar_hilo_ping(self):
        self.ping_thread = threading.Thread(target=self.ping_cada_minuto)
        self.ping_thread.daemon = True
        self.ping_thread.start()

        self.conexiondb()

    def ping_cada_minuto(self):
        ping3.EXCEPTIONS = True

        while True:
            IP = self.IPSV.text()
            try:
                ping3.ping(IP)
                print("exito")

                self.DOWNLABEL.setVisible(False)
                self.DOWNICON.setVisible(False)
                self.UPLABEL.setVisible(True)
                self.UPICON.setVisible(True)
            except ping3.errors.HostUnknown:
                print("La respuesta del host es muy lenta")
            except ping3.errors.PingError:
                print("Host inaccesible")
                self.UPLABEL.setVisible(False)
                self.UPICON.setVisible(False)
                self.DOWNLABEL.setVisible(True)
                self.DOWNICON.setVisible(True)
            time.sleep(60)

    def mostrar_dialogo_agregar_servidor(self):
        dialogo = QDialog(self)
        dialogo.setWindowTitle("Agregar Servidor")

        # Crear widgets para el diálogo
        label_nombre = QLabel("Nombre del Servidor:")
        label_ip = QLabel("Dirección IP:")
        label_estado = QLabel("Estado:")
        self.input_nombre = QLineEdit()
        self.input_ip = QLineEdit()
        self.combo_estado = QComboBox()
        self.combo_estado.addItems(["Online", "Down"])
        boton_agregar = QPushButton("Agregar")
        boton_agregar.clicked.connect(self.agregar_servidor)

        # Layout del diálogo
        layout = QVBoxLayout()
        layout.addWidget(label_nombre)
        layout.addWidget(self.input_nombre)
        layout.addWidget(label_ip)
        layout.addWidget(self.input_ip)
        layout.addWidget(label_estado)
        layout.addWidget(self.combo_estado)
        layout.addWidget(boton_agregar)

        dialogo.setLayout(layout)
        dialogo.exec_()

    def agregar_servidor(self):
        nombre = self.input_nombre.text()
        ip = self.input_ip.text()
        estado = self.combo_estado.currentText()  # Get selected state

        if not nombre or not ip:
            print("Por favor, ingresa el nombre y la dirección IP del servidor.")
            return

        query = QSqlQuery(self.db)
        query.prepare("INSERT INTO SERVIDOR (NOMBRE_SERVIDOR, IP_SERVIDOR, ESTADO) VALUES (?, ?, ?)")
        query.addBindValue(nombre)
        query.addBindValue(ip)
        query.addBindValue(estado)  # Bind the state to the query

        if query.exec_():
            print(f"Servidor '{nombre}' agregado con éxito a la base de datos.")
            self.cargar_servidores()
        else:
            print("Error al agregar el servidor:", query.lastError().text())

        query = QSqlQuery(self.db)
        query.prepare("INSERT INTO SERVIDOR (NOMBRE_SERVIDOR, IP_SERVIDOR) VALUES (?, ?)")
        query.addBindValue(nombre)
        query.addBindValue(ip)

        if query.exec_():
            print(f"Servidor '{nombre}' agregado con éxito a la base de datos.")
            self.cargar_servidores()
        else:
            print("Error al agregar el servidor:", query.lastError().text())

    def conexiondb(self):
        self.db = QSqlDatabase.addDatabase("QSQLITE")
        self.db.setDatabaseName("Servidores.db")

        if not self.db.open():
            print("Error al abrir la base de datos:", self.db.lastError().text())
            return

        query = QSqlQuery(self.db)

        if not query.exec_("CREATE TABLE IF NOT EXISTS SERVIDOR ( NOMBRE_SERVIDOR TEXT, IP_SERVIDOR TEXT)"):
            print("Error al crear la tabla SERVIDOR:", query.lastError().text())
            return

        self.cargar_servidores()

    def cargar_servidores(self):
        self.table_widget.clearContents()
        self.table_widget.setRowCount(0)

        query = QSqlQuery(self.db)

        if not query.exec_("SELECT * FROM SERVIDOR"):
            print("Error al ejecutar la consulta:", query.lastError().text())
            return

        row = 0

        while query.next():
            self.table_widget.insertRow(row)
            self.table_widget.setItem(row, 0, QTableWidgetItem(str(query.value(0))))
            self.table_widget.setItem(row, 1, QTableWidgetItem(query.value(1)))

            ip = str(query.value(1))
            try:
                ping3.ping(ip)
                print("exito")
                status = 1
            except ping3.errors.HostUnknown:
                print("La respuesta del host es muy lenta")
                status = 0
            except ping3.errors.PingError:
                print("Host inaccesible")
                status = 0

            status_item = QTableWidgetItem()
            if status == 1:
                status_item.setIcon(QIcon('check.png'))
                status_item.setText('Online')
            else:
                status_item.setIcon(QIcon('delete.png'))
                status_item.setText('Down')

            self.table_widget.setItem(row, 2, status_item)
            row += 1

def main():
    app = QApplication(sys.argv)
    ventana = MiVentana()
    ventana.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
