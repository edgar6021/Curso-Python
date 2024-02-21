import sys, time, ping3
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidget, QTableWidgetItem
from PyQt5.QtSql import QSqlDatabase, QSqlQueryModel, QSqlDatabase, QSqlQuery
from PyQt5.uic import loadUi
import iconos_rc
import threading
import sqlite3
from PyQt5.QtGui import QIcon



class MiVentana(QMainWindow):
    def __init__(self):
        super().__init__()
        loadUi('IFC.UI', self)


        self.UPLABEL.setVisible(False)
        self.UPICON.setVisible(False)
        self.DOWNLABEL.setVisible(False)
        self.DOWNICON.setVisible(False)
        #self.ping_every_minute()
        IP = self.IPSV.text()

        #para ejecutar la función en segundo plano
        self.ping_thread = threading.Thread(target=self.ping_every_minute)
        self.ping_thread.daemon = True  #para que se detenga cuando la aplicacion se cierre.
        self.ping_thread.start()
        self.conexiondb()

    def ping_every_minute(self):
        ping3.EXCEPTIONS = True
        #IP = self.IPSV.text()
        IP= "8.8.8.8"
        while True:
            try:
                ping3.ping(IP)
                print("exito")

                self.DOWNLABEL.setVisible(False)
                self.DOWNICON.setVisible(False)
                self.UPLABEL.setVisible(True)
                self.UPICON.setVisible(True)
            except ping3.errors.HostUnknown: # error en especifico
                print("La respuesta del host es muy lenta")
            except ping3.errors.PingError: # si el host no responde f `PingError`.
                print("Host inaccesible")
                self.UPLABEL.setVisible(False)
                self.UPICON.setVisible(False)
                self.DOWNLABEL.setVisible(True)
                self.DOWNICON.setVisible(True)
            time.sleep(60)

    def conexiondb(self):
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

            status_item = QTableWidgetItem()
            #status = query.value(2)

            ###########################################
            column_1_value = query.value(1)
            print(column_1_value)
            ##########################################
            status = 1
            #funcion para la 2 columna
            if status == 1:
                status_item.setIcon(QIcon('check.png'))  # Ruta a tu icono de conexión online
                status_item.setText('Online')
            else:
                status_item.setIcon(QIcon('delete.png'))  # Ruta a tu icono de conexión offline
                status_item.setText('Down')

            self.table_widget.setItem(row, 2, status_item)
            row += 1

            #print(f"Columna 2: {query.value(1)}")

def main():
    app = QApplication(sys.argv)
    ventana = MiVentana()
    ventana.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()