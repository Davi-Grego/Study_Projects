import pandas as pd
import random
import string
from PyQt5.QtWidgets import QInputDialog, QMessageBox

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
            if new_name.strip() == '':
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
