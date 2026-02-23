from pathlib import Path

# Navegação entre as pastas src e data
caminho_atual = Path(__file__).resolve()
raiz_projeto = caminho_atual.parent.parent

# Criação do caminho e da pasta
data_dir = raiz_projeto / "data"
data_dir.mkdir(exist_ok=True)

# Local do Banco de Dados
db_path = data_dir / "pojetosite.db"

DATABASE_URI = f"sqlite:///{db_path}"
