class Config:
    SQLALCHEMY_DATABASE_URI = 'sqlite:///expenses.db'  # Caminho para o banco de dados SQLite
    SQLALCHEMY_TRACK_MODIFICATIONS = False  # Desabilitar o rastreamento de modificações para evitar warnings
    SECRET_KEY = '240225'  # Para segurança das sessões no Flask
