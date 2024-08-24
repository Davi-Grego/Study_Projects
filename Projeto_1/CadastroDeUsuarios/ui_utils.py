from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QPushButton, QFileDialog, QInputDialog, QTableView, QHeaderView,
    QHBoxLayout, QLabel, QFrame, QMessageBox
)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt
import pandas as pd
from data_utils import (
    create_empty_csv, carregar_df, save_df, add_user, delete_user, edit_user, edit_password, clear_table
)
from model import PandasModel

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Gerenciador de Usuários")
        self.setGeometry(300, 100, 1000, 700)
        self.filename = None  # Atributo para armazenar o nome do arquivo
        self.df = pd.DataFrame(columns=['ID', 'USER', 'EMAIL', 'PASSWORD'])
        self.setup_ui()
        self.setStyleSheet("background-color:#1C1C1C ;")

    def setup_ui(self):
        main_layout = QVBoxLayout()

        # Header
        header_label = QLabel("Gerenciador de Usuários")
        header_label.setFont(QFont("Arial", 20, QFont.Bold))
        header_label.setStyleSheet("color:snow;")
        header_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(header_label)

        # Botões de menu
        button_layout = QHBoxLayout()

        self.new_file_button = QPushButton("Criar novo arquivo")
        self.new_file_button.setStyleSheet("background-color:#434343 ; color:snow; font-size: 16px; padding: 10px;")
        self.new_file_button.clicked.connect(self.create_new_file)
        button_layout.addWidget(self.new_file_button)

        self.load_button = QPushButton("Carregar arquivo")
        self.load_button.setStyleSheet("background-color:#434343; color:snow; font-size: 16px; padding: 10px;")
        self.load_button.clicked.connect(self.carregar_arquivo)
        button_layout.addWidget(self.load_button)

        self.add_button = QPushButton("Adicionar usuário")
        self.add_button.setStyleSheet("background-color: #434343; color:snow; font-size: 16px; padding: 10px;")
        self.add_button.clicked.connect(self.add_user_interface)
        button_layout.addWidget(self.add_button)

        self.delete_button = QPushButton("Deletar usuário")
        self.delete_button.setStyleSheet("background-color: #434343; color:snow; font-size: 16px; padding: 10px;")
        self.delete_button.clicked.connect(self.delete_user_interface)
        button_layout.addWidget(self.delete_button)

        self.edit_button = QPushButton("Editar usuário")
        self.edit_button.setStyleSheet("background-color:#434343; color:snow; font-size: 16px; padding: 10px;")
        self.edit_button.clicked.connect(self.edit_user_interface)
        button_layout.addWidget(self.edit_button)

        self.edit_password_button = QPushButton("Editar senha")
        self.edit_password_button.setStyleSheet("background-color:#434343; color:snow; font-size: 16px; padding: 10px;")
        self.edit_password_button.clicked.connect(self.edit_password_interface)
        button_layout.addWidget(self.edit_password_button)

        self.clear_table_button = QPushButton("Limpar Tabela")
        self.clear_table_button.setStyleSheet("background-color:#434343; color:snow; font-size: 16px; padding: 10px;")
        self.clear_table_button.clicked.connect(self.clear_table_interface)
        button_layout.addWidget(self.clear_table_button)

        main_layout.addLayout(button_layout)

        # Tabela de Dados
        self.table = QTableView()
        self.model = PandasModel(self.df)
        self.table.setModel(self.model)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        main_layout.addWidget(self.table)

        self.setLayout(main_layout)

    def create_new_file(self):
        filename, _ = QFileDialog.getSaveFileName(self, "Salvar Arquivo", "", "CSV Files (*.csv)")
        if filename:
            self.filename = filename
            self.df = create_empty_csv(self.filename)
            self.model.update_dataframe(self.df)

    def carregar_arquivo(self):
        filename, _ = QFileDialog.getOpenFileName(self, "Abrir Arquivo", "", "CSV Files (*.csv)")
        if filename:
            self.filename = filename
            self.df = carregar_df(self.filename)
            self.model.update_dataframe(self.df)

    def add_user_interface(self):
        self.df = add_user(self.df)
        self.model.update_dataframe(self.df)

    def delete_user_interface(self):
        self.df = delete_user(self.df)
        self.model.update_dataframe(self.df)

    def edit_user_interface(self):
        self.df = edit_user(self.df)
        self.model.update_dataframe(self.df)

    def edit_password_interface(self):
        self.df = edit_password(self.df)
        self.model.update_dataframe(self.df)

    def clear_table_interface(self):
        self.df = clear_table(self.df)
        self.model.update_dataframe(self.df)

    def closeEvent(self, event):
        if self.filename:
            save_df(self.df, self.filename)
            QMessageBox.information(self, "Sucesso", f"Dados salvos em '{self.filename}' antes de sair.")
        else:
            QMessageBox.warning(self, "Aviso", "Nenhum arquivo carregado. Os dados não foram salvos.")
        event.accept()
