import sys
import random
import pandas as pd
import numpy as np
import string
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QMessageBox, QFileDialog, QInputDialog, QTableView, QHeaderView
from PyQt5.QtCore import QAbstractTableModel, Qt

#-------------------------------------Funções-------------------------------------

def create_empty_csv(filename):
    df = pd.DataFrame(columns=['ID', 'USER', 'EMAIL', 'PASSWORD'])
    df.to_csv(filename, index=False)
    print(f"Arquivo CSV vazio '{filename}' gerado com sucesso!")

def carregar_df(filename):
    try:
        df = pd.read_csv(filename)
        print("Arquivo CSV carregado com sucesso!")
        return df
    except FileNotFoundError:
        print("O arquivo CSV especificado não foi encontrado.")
        return None

def saveDf(df):
    df.to_csv(filename, index=False)

def IdGenerator(df):
    while True:
        randomId = ''.join(random.choices(string.ascii_uppercase + string.digits, k=3))
        if randomId not in df['ID'].values:
            return randomId

def generatePassword():
    return ''.join(random.choices(string.ascii_letters + string.digits, k=8))

def addNewUser(df):
    user, ok1 = QInputDialog.getText(None, "Adicionar Usuário", "Digite o nome do usuário:")
    email, ok2 = QInputDialog.getText(None, "Adicionar Usuário", "Digite o email do usuário:")
    
    if ok1 and ok2:
        unicId = IdGenerator(df)
        password = generatePassword()
        df.loc[len(df)] = [unicId, user, email, password]
        return df

def deleteUser(df, userId):
    while True:
        if userId in df['ID'].values:
            df = df[df['ID'] != userId]
            print(f"Usuário com ID '{userId}' excluído com sucesso.")
            return df
        else:
            print(f"O ID '{userId}' não foi encontrado no DataFrame.")
            userId, ok = QInputDialog.getText(None, "Deletar Usuário", "Digite um ID válido:")
            if not ok:
                break

def editUser(df):
    userIdToEdit, ok = QInputDialog.getText(None, "Editar Usuário", "Digite o ID do usuário que deseja editar:")
    if ok and userIdToEdit in df['ID'].values:
        newName, ok1 = QInputDialog.getText(None, "Editar Usuário", "Digite o novo nome do usuário:")
        newEmail, ok2 = QInputDialog.getText(None, "Editar Usuário", "Digite o novo email do usuário:")
        if ok1 and ok2:
            df.loc[df['ID'] == userIdToEdit, 'USER'] = newName
            df.loc[df['ID'] == userIdToEdit, 'EMAIL'] = newEmail
            print(f"Dados do usuário com ID '{userIdToEdit}' editados com sucesso.")
    else:
        QMessageBox.warning(None, "Erro", "O ID não foi encontrado no DataFrame.")
    return df


#_____________________ Modelo de dados para exibir DataFrame em QTableView__________________________
class PandasModel(QAbstractTableModel):
    def __init__(self, df=pd.DataFrame(), parent=None):
        super().__init__(parent)
        self._dataframe = df

    def rowCount(self, parent=None):
        return self._dataframe.shape[0]

    def columnCount(self, parent=None):
        return self._dataframe.shape[1]

    def data(self, index, role=Qt.DisplayRole):
        if index.isValid():
            if role == Qt.DisplayRole:
                return str(self._dataframe.iloc[index.row(), index.column()])
        return None

    def headerData(self, section, orientation, role=Qt.DisplayRole):
        if role == Qt.DisplayRole:
            if orientation == Qt.Horizontal:
                return str(self._dataframe.columns[section])
            elif orientation == Qt.Vertical:
                return str(self._dataframe.index[section])
        return None

    def updateDataFrame(self, df):
        self.beginResetModel()
        self._dataframe = df
        self.endResetModel()

#_________________________________Funções Da Interface Gráfica______________________________________

def carregar_arquivo():
    global filename
    options = QFileDialog.Options()
    filename, _ = QFileDialog.getOpenFileName(None, "Selecionar Arquivo CSV", "", "CSV Files (*.csv);;All Files (*)", options=options)
    if filename:
        global df
        df = carregar_df(filename)
        if df is None:
            QMessageBox.critical(None, "Erro", "Falha ao carregar o arquivo CSV.")
        else:
            QMessageBox.information(None, "Sucesso", "Arquivo CSV carregado com sucesso.")
            table_model.updateDataFrame(df)
    else:
        QMessageBox.warning(None, "Atenção", "Nenhum arquivo selecionado.")
    return filename

def add_user():
    if 'df' in globals():
        global df
        df = addNewUser(df)
        QMessageBox.information(None, "Sucesso", "Usuário adicionado com sucesso!")
        table_model.updateDataFrame(df)
    else:
        QMessageBox.warning(None, "Atenção", "Por favor, carregue um arquivo CSV primeiro.")

def delete_user():
    if 'df' in globals():
        userId, ok = QInputDialog.getText(None, "Deletar Usuário", "Digite o ID do usuário que deseja deletar:")
        if ok:
            global df
            df = deleteUser(df, userId)
            QMessageBox.information(None, "Sucesso", "Usuário deletado com sucesso!")
            table_model.updateDataFrame(df)
    else:
        QMessageBox.warning(None, "Atenção", "Por favor, carregue um arquivo CSV primeiro.")

def edit_user():
    if 'df' in globals():
        global df
        df = editUser(df)
        QMessageBox.information(None, "Sucesso", "Usuário editado com sucesso!")
        table_model.updateDataFrame(df)
    else:
        QMessageBox.warning(None, "Atenção", "Por favor, carregue um arquivo CSV primeiro.")

def create_new_file():
    filename, ok = QInputDialog.getText(None, "Criar Novo Arquivo", "Digite o nome do novo arquivo:")
    if ok and filename:
        create_empty_csv(filename + ".csv")
        QMessageBox.information(None, "Sucesso", f"Arquivo CSV vazio '{filename}.csv' criado com sucesso!")

def save_and_exit():
    if 'df' in globals():
        global df
        saveDf(df)
        QMessageBox.information(None, "Sucesso", "Dados salvos. Saindo...")
        app.quit()
    else:
        QMessageBox.warning(None, "Atenção", "Não há dados para salvar.")

# Configurações da interface gráfica
app = QApplication(sys.argv)
window = QWidget()
window.setWindowTitle("Menu")
window.setGeometry(300, 100, 800, 600)

layout = QVBoxLayout()

new_file_button = QPushButton("Criar novo arquivo")
new_file_button.clicked.connect(create_new_file)
layout.addWidget(new_file_button)


load_button = QPushButton("Carregar arquivo")
load_button.clicked.connect(carregar_arquivo)
layout.addWidget(load_button)

add_button = QPushButton("Adicionar usuário")
add_button.clicked.connect(add_user)
layout.addWidget(add_button)

delete_button = QPushButton("Deletar usuário")
delete_button.clicked.connect(delete_user)
layout.addWidget(delete_button)

edit_button = QPushButton("Editar usuário")
edit_button.clicked.connect(edit_user)
layout.addWidget(edit_button)

exit_button = QPushButton("Salvar e sair")
exit_button.clicked.connect(save_and_exit)
layout.addWidget(exit_button)

table_view = QTableView()
table_model = PandasModel()
table_view.setModel(table_model)
table_view.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
layout.addWidget(table_view)

window.setLayout(layout)

# Execução da interface gráfica
window.show()
sys.exit(app.exec_())
