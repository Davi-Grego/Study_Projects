import sys
import random
import pandas as pd
import string
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QPushButton, QMessageBox,
    QFileDialog, QInputDialog, QTableView, QHeaderView, QAction, QLineEdit,
    QHBoxLayout, QLabel, QFrame
)
from PyQt5.QtCore import QAbstractTableModel, Qt
from PyQt5.QtGui import QFont, QColor

# Funções de manipulação de dados

def create_empty_csv(filename):
    df = pd.DataFrame(columns=['ID', 'USER', 'EMAIL', 'PASSWORD'])
    df.to_csv(filename, index=False)
    print(f"Arquivo CSV vazio '{filename}' gerado com sucesso!")
    return df

def carregar_df(filename):
    try:
        df = pd.read_csv(filename)
        print("Arquivo CSV carregado com sucesso!")
        return df
    except FileNotFoundError:
        print("O arquivo CSV especificado não foi encontrado.")
        return None

def save_df(df, filename):
    df.to_csv(filename, index=False)
    print(f"Dados salvos no arquivo '{filename}'.")

def generate_id(existing_ids):
    while True:
        random_id = ''.join(random.choices(string.ascii_uppercase + string.digits, k=3))
        if random_id not in existing_ids:
            return random_id

def generate_password():
    return ''.join(random.choices(string.ascii_letters + string.digits, k=8))

def add_user(df):
    user, ok1 = QInputDialog.getText(None, "Adicionar Usuário", "Digite o nome do usuário:")
    email, ok2 = QInputDialog.getText(None, "Adicionar Usuário", "Digite o email do usuário:")
    
    if ok1 and ok2:
        if user.strip() == '' or email.strip() == '':
            QMessageBox.warning(None, "Erro", "Nome de usuário e email não podem estar em branco.")
        else:
            unique_id = generate_id(df['ID'].values)
            password = generate_password()
            df.loc[len(df)] = [unique_id, user, email, password]
            QMessageBox.information(None, "Sucesso", "Usuário adicionado com sucesso!")
    return df

def delete_user(df):
    user_id, ok = QInputDialog.getText(None, "Deletar Usuário", "Digite o ID do usuário que deseja deletar:")
    if ok:
        if user_id in df['ID'].values:
            df = df[df['ID'] != user_id]
            print(f"Usuário com ID '{user_id}' excluído com sucesso.")
            QMessageBox.information(None, "Sucesso", "Usuário deletado com sucesso!")
        else:
            print(f"O ID '{user_id}' não foi encontrado no DataFrame.")
    return df

def edit_user(df):
    user_id_to_edit, ok = QInputDialog.getText(None, "Editar Usuário", "Digite o ID do usuário que deseja editar:")
    if ok and user_id_to_edit in df['ID'].values:
        new_name, ok1 = QInputDialog.getText(None, "Editar Usuário", "Digite o novo nome do usuário:")
        new_email, ok2 = QInputDialog.getText(None, "Editar Usuário", "Digite o novo email do usuário:")
        if ok1 and ok2:
            if new_name.strip() == '' or new_email.strip() == '':
                QMessageBox.warning(None, "Erro", "Nome de usuário e email não podem estar em branco.")
            else:
                df.loc[df['ID'] == user_id_to_edit, 'USER'] = new_name
                df.loc[df['ID'] == user_id_to_edit, 'EMAIL'] = new_email
                print(f"Dados do usuário com ID '{user_id_to_edit}' editados com sucesso.")
                QMessageBox.information(None, "Sucesso", "Usuário editado com sucesso!")
    else:
        QMessageBox.warning(None, "Erro", "O ID não foi encontrado no DataFrame.")
    return df

def edit_password(df):
    user_id_to_edit, ok = QInputDialog.getText(None, "Editar Senha", "Digite o ID do usuário para editar a senha:")
    if ok and user_id_to_edit in df['ID'].values:
        new_password = generate_password()
        df.loc[df['ID'] == user_id_to_edit, 'PASSWORD'] = new_password
        print(f"Senha do usuário com ID '{user_id_to_edit}' editada com sucesso.")
        QMessageBox.information(None, "Sucesso", f"Senha do usuário com ID '{user_id_to_edit}' editada com sucesso.")
    else:
        QMessageBox.warning(None, "Erro", "O ID não foi encontrado no DataFrame.")

def clear_table(df):
    confirmation = QMessageBox.question(None, "Confirmar Limpar Tabela", 
                                        "Tem certeza que deseja limpar todos os dados da tabela?",
                                        QMessageBox.Yes | QMessageBox.No)
    if confirmation == QMessageBox.Yes:
        df = pd.DataFrame(columns=['ID', 'USER', 'EMAIL', 'PASSWORD'])
        QMessageBox.information(None, "Sucesso", "Tabela limpa com sucesso!")
    return df

# Modelo de dados para exibir DataFrame em QTableView

class PandasModel(QAbstractTableModel):
    def __init__(self, df=pd.DataFrame(), parent=None):
        super().__init__(parent)
        self._dataframe = df

    def rowCount(self, parent=None):
        return self._dataframe.shape[0]

    def columnCount(self, parent=None):
        return self._dataframe.shape[1]

    def data(self, index, role=Qt.DisplayRole):
        if index.isValid() and role == Qt.DisplayRole:
            return str(self._dataframe.iloc[index.row(), index.column()])
        return None

    def headerData(self, section, orientation, role=Qt.DisplayRole):
        if role == Qt.DisplayRole:
            if orientation == Qt.Horizontal:
                return str(self._dataframe.columns[section])
            elif orientation == Qt.Vertical:
                return str(self._dataframe.index[section])
        return None

    def update_dataframe(self, df):
        self.beginResetModel()
        self._dataframe = df
        self.endResetModel()

# Funções da Interface Gráfica

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
        self.edit_password_button.setStyleSheet("background-color: #434343; color:snow; font-size: 16px; padding: 10px;")
        self.edit_password_button.clicked.connect(self.edit_password_interface)
        button_layout.addWidget(self.edit_password_button)

        self.clear_table_button = QPushButton("Limpar tabela")
        self.clear_table_button.setStyleSheet("background-color: #434343; color:snow; font-size: 16px; padding: 10px;")
        self.clear_table_button.clicked.connect(self.clear_table_interface)
        button_layout.addWidget(self.clear_table_button)

        self.exit_button = QPushButton
        self.exit_button = QPushButton("Salvar e sair")
        self.exit_button.setStyleSheet("background-color: #434343; color:snow; font-size: 16px; padding: 10px;")
        self.exit_button.clicked.connect(self.save_and_exit)
        button_layout.addWidget(self.exit_button)

        main_layout.addLayout(button_layout)

        # Linha de separação
        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        line.setFrameShadow(QFrame.Sunken)
        main_layout.addWidget(line)

        # Tabela de visualização
        self.table_view = QTableView()
        self.table_model = PandasModel(self.df)
        self.table_view.setModel(self.table_model)
        self.table_view.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table_view.setStyleSheet("font-size: 14px;")
        self.table_view.setStyleSheet("Background-color: #434343;color:snow;")
        main_layout.addWidget(self.table_view)

        self.setLayout(main_layout)

    def create_new_file(self):
        filename, ok = QInputDialog.getText(None, "Criar Novo Arquivo", "Digite o nome do novo arquivo:")
        if ok and filename:
            self.df = create_empty_csv(filename + ".csv")
            self.filename = filename + ".csv"
            self.table_model.update_dataframe(self.df)
            QMessageBox.information(None, "Sucesso", f"Arquivo CSV vazio '{filename}.csv' criado com sucesso!")

    def carregar_arquivo(self):
        options = QFileDialog.Options()
        filename, _ = QFileDialog.getOpenFileName(None, "Selecionar Arquivo CSV", "", "CSV Files (*.csv);;All Files (*)", options=options)
        if filename:
            self.df = carregar_df(filename)
            if self.df is None:
                QMessageBox.critical(None, "Erro", "Falha ao carregar o arquivo CSV.")
            else:
                self.filename = filename
                self.table_model.update_dataframe(self.df)
                QMessageBox.information(None, "Sucesso", "Arquivo CSV carregado com sucesso.")
        else:
            QMessageBox.warning(None, "Atenção", "Nenhum arquivo selecionado.")

    def add_user_interface(self):
        if hasattr(self, 'df'):
            self.df = add_user(self.df)
            if self.df is not None:
                self.table_model.update_dataframe(self.df)
        else:
            QMessageBox.warning(None, "Atenção", "Por favor, carregue um arquivo CSV primeiro.")

    def delete_user_interface(self):
        if hasattr(self, 'df'):
            self.df = delete_user(self.df)
            if self.df is not None:
                self.table_model.update_dataframe(self.df)
        else:
            QMessageBox.warning(None, "Atenção", "Por favor, carregue um arquivo CSV primeiro.")

    def edit_user_interface(self):
        if hasattr(self, 'df'):
            self.df = edit_user(self.df)
            if self.df is not None:
                self.table_model.update_dataframe(self.df)
        else:
            QMessageBox.warning(None, "Atenção", "Por favor, carregue um arquivo CSV primeiro.")

    def edit_password_interface(self):
        if hasattr(self, 'df'):
            edit_password(self.df)
            self.table_model.update_dataframe(self.df)
        else:
            QMessageBox.warning(None, "Atenção", "Por favor, carregue um arquivo CSV primeiro.")

    def clear_table_interface(self):
        if hasattr(self, 'df'):
            self.df = clear_table(self.df)
            if self.df is not None:
                self.table_model.update_dataframe(self.df)
        else:
            QMessageBox.warning(None, "Atenção", "Por favor, carregue um arquivo CSV primeiro.")

    def save_and_exit(self):
        if hasattr(self, 'filename') and hasattr(self, 'df'):
            save_df(self.df, self.filename)
            QMessageBox.information(None, "Sucesso", "Dados salvos. Saindo...")
            app.quit()
        else:
            QMessageBox.warning(None, "Atenção", "Não há dados para salvar ou nenhum arquivo carregado.")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
