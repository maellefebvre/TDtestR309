#Lien vers le repository github : 

import sys
import socket
import threading
from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QPushButton, QTextEdit, QWidget, QLineEdit, QLabel

"""Je n'ai pas mis les valeurs pour le socket, l'address et le port du serveur ici mais dans les fonctions
 car je l'ai fait dans la SAE et que pour aller plus vite j'ai repris ce code là et l'ai modifié"""

class ServerGraphique(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.server_socket = None
        self.server_thread = None
        self.clients = []
        self.server_running = False

    def initUI(self):
        self.setWindowTitle('Le serveur de Chat')
        self.setGeometry(600, 600, 600, 600)

        """Affichage de l'interface graphique. Dans l'ordre : Adresse, Port, Nombre maximum de clients, Démarrer le serveur, Affichage des clients connectés, Quitter."""

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout(central_widget)


        self.address_input = QLineEdit('0.0.0.0')
        layout.addWidget(QLabel('Adresse:'))
        layout.addWidget(self.address_input)

        self.port_input = QLineEdit('10000')
        layout.addWidget(QLabel('Port:'))
        layout.addWidget(self.port_input)

        self.max_clients_input = QLineEdit('5')
        layout.addWidget(QLabel('Nombre maximum de clients:'))
        layout.addWidget(self.max_clients_input)

        self.start_button = QPushButton('Démarrer le serveur')
        self.start_button.clicked.connect(self.__demarrage)
        layout.addWidget(self.start_button)

        self.client_display = QTextEdit()
        self.client_display.setReadOnly(True)
        layout.addWidget(self.client_display)

        self.quit_button = QPushButton('Quit')
        self.quit_button.clicked.connect(self.__Arret_app)
        layout.addWidget(self.quit_button)

    def __demarrage(self):
        if self.server_running:
            self.__stop_server()

            """Demarrage du serveur. Si le serveur est déjà en cours de fonctionnement, il est arrêté. Sinon, il est démarré avec les paramètres spécifiés."""
        else:
            try:
                address = self.address_input.text()
                port = int(self.port_input.text())
                max_clients = int(self.max_clients_input.text())
                self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.server_socket.bind((address, port))
                self.server_socket.listen(max_clients)
                self.server_running = True
                self.start_button.setText('Arrêter le serveur')
                self.server_thread = threading.Thread(target=self.__accept)
                self.server_thread.start()
            except ValueError:
                self.client_display.append('Erreur: Le port et le nombre de clients doivent être des nombres entiers.')
            except Exception as e:
                self.client_display.append(f'Erreur: {e}')

    def __accept(self):
        while self.server_running:
            try:
                """Accepter les clients. Si un client se connecte, un thread est créé pour gérer la réception des messages."""
                client_socket, client_address = self.server_socket.accept()
                self.clients.append(client_socket)
                self.client_display.append(f'Client connecté: {client_address}')
                threading.Thread(target=self.__reception, args=(client_socket,)).start()
            except Exception as e:
                self.client_display.append(f'Erreur: {e}')

    def __reception(self, client_socket):
        while self.server_running:
            try:
                """Reception des messages des clients. Si un client envoie un message, il est affiché dans l'interface graphique."""
                message = client_socket.recv(1024).decode()
                if message == 'deco-server':
                    break
                self.client_display.append(f'Message reçu: {message}')
            except Exception as e:
                self.client_display.append(f'Erreur: {e}')
                break
        client_socket.close()

    def __stop_server(self):
        """Arrêt du serveur. Les clients sont déconnectés et le socket du serveur est fermé."""

        self.server_running = False
        self.start_button.setText('Démarrer le serveur')
        for client in self.clients:
            client.close()
        self.server_socket.close()
        self.clients = []

    def __Arret_app(self):
        """
        Quitter l'application.
        """
        self.close()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    server_gui = ServerGraphique()
    server_gui.show()
    sys.exit(app.exec())



