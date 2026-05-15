import sqlite3
from pathlib import Path

import pandas as pd


# Define a pasta base do projeto
BASE_DIR = Path(__file__).resolve().parent.parent

# Define os caminhos das pastas utilizadas no projeto
RAW_DIR = BASE_DIR / "data" / "raw"
PROCESSED_DIR = BASE_DIR / "data" / "processed"
DATABASE_DIR = BASE_DIR / "database"

# Garante que as pastas existam antes de salvar arquivos
PROCESSED_DIR.mkdir(exist_ok=True)
DATABASE_DIR.mkdir(exist_ok=True)

# Caminho do banco SQLite
DB_PATH = DATABASE_DIR / "estoque.db"


def extract():
    """Extrai os dados brutos dos arquivos CSV."""

    print("[INFO] Extraindo dados dos arquivos CSV...")

    materiais = pd.read_csv(RAW_DIR / "materiais.csv")
    movimentacoes = pd.read_csv(RAW_DIR / "movimentacoes.csv")

    return materiais, movimentacoes


def transform(materiais, movimentacoes):
    """Limpa, padroniza e transforma os dados."""

    print("[INFO] Transformando dados...")

    materiais = materiais.copy()
    movimentacoes = movimentacoes.copy()

    # Padronização de textos nos dados de materiais
    materiais["nome"] = materiais["nome"].str.strip()
    materiais["categoria"] = materiais["categoria"].str.strip()

    # Padronização de textos nas movimentações
    movimentacoes["tipo"] = movimentacoes["tipo"].str.lower().str.strip()
    movimentacoes["setor"] = movimentacoes["setor"].str.strip()

    # Conversão das colunas de data para o formato datetime
    materiais["data_validade"] = pd.to_datetime(materiais["data_validade"])
    movimentacoes["data_movimentacao"] = pd.to_datetime(
        movimentacoes["data_movimentacao"]
    )

    # Remoção de registros duplicados com base nos IDs
    materiais = materiais.drop_duplicates(subset=["id_material"])
    movimentacoes = movimentacoes.drop_duplicates(subset=["id_movimentacao"])

    # Remove movimentações com quantidade menor ou igual a zero
    movimentacoes = movimentacoes[movimentacoes["quantidade"] > 0]

    # Cria uma coluna auxiliar para calcular o impacto no estoque
    # Entrada soma no estoque, saída subtrai do estoque
    movimentacoes["quantidade_ajustada"] = movimentacoes.apply(
        lambda linha: linha["quantidade"]
        if linha["tipo"] == "entrada"
        else -linha["quantidade"],
        axis=1,
    )

    # Calcula o estoque atual por material
    estoque_atual = (
        movimentacoes.groupby("id_material")["quantidade_ajustada"]
        .sum()
        .reset_index()
        .rename(columns={"quantidade_ajustada": "estoque_atual"})
    )

    # Junta o estoque calculado com os dados cadastrais dos materiais
    estoque_atual = estoque_atual.merge(
        materiais,
        on="id_material",
        how="left"
    )

    # Cria indicador para identificar materiais abaixo do estoque mínimo
    estoque_atual["abaixo_minimo"] = (
        estoque_atual["estoque_atual"] < estoque_atual["estoque_minimo"]
    )

    return materiais, movimentacoes, estoque_atual


def validate(materiais, movimentacoes, estoque_atual):
    """Executa validações simples de qualidade dos dados."""

    print("[INFO] Validando qualidade dos dados...")

    # Verifica se existe material sem ID
    if materiais["id_material"].isnull().any():
        raise ValueError("Existem materiais sem ID.")

    # Verifica se existe movimentação sem ID de material
    if movimentacoes["id_material"].isnull().any():
        raise ValueError("Existem movimentações sem ID de material.")

    # Verifica se existem quantidades negativas
    if movimentacoes["quantidade"].lt(0).any():
        raise ValueError("Existem quantidades negativas nas movimentações.")

    # Verifica se todos os tipos de movimentação são válidos
    tipos_validos = {"entrada", "saida"}
    tipos_encontrados = set(movimentacoes["tipo"].unique())

    if not tipos_encontrados.issubset(tipos_validos):
        raise ValueError("Existem tipos de movimentação inválidos.")

    # Verifica se toda movimentação possui um material cadastrado
    ids_materiais = set(materiais["id_material"])
    ids_movimentacoes = set(movimentacoes["id_material"])

    if not ids_movimentacoes.issubset(ids_materiais):
        raise ValueError("Existem movimentações com materiais não cadastrados.")

    # Verifica se o estoque atual foi calculado corretamente
    if estoque_atual["estoque_atual"].isnull().any():
        raise ValueError("Existem materiais sem cálculo de estoque.")

    print("[INFO] Validação concluída com sucesso.")


def save_processed_files(materiais, movimentacoes, estoque_atual):
    """Salva os dados tratados em arquivos CSV na camada processed."""

    print("[INFO] Salvando dados tratados na pasta data/processed...")

    materiais.to_csv(
        PROCESSED_DIR / "materiais_tratados.csv",
        index=False,
        encoding="utf-8-sig"
    )

    movimentacoes.to_csv(
        PROCESSED_DIR / "movimentacoes_tratadas.csv",
        index=False,
        encoding="utf-8-sig"
    )

    estoque_atual.to_csv(
        PROCESSED_DIR / "estoque_atual.csv",
        index=False,
        encoding="utf-8-sig"
    )

    print("[INFO] Arquivos tratados salvos com sucesso.")


def load(materiais, movimentacoes, estoque_atual):
    """Carrega os dados tratados em um banco SQLite."""

    print("[INFO] Carregando dados no banco SQLite...")

    with sqlite3.connect(DB_PATH) as conn:
        materiais.to_sql(
            "dim_materiais",
            conn,
            if_exists="replace",
            index=False
        )

        movimentacoes.to_sql(
            "fato_movimentacoes",
            conn,
            if_exists="replace",
            index=False
        )

        estoque_atual.to_sql(
            "estoque_atual",
            conn,
            if_exists="replace",
            index=False
        )

    print(f"[INFO] Dados carregados com sucesso em: {DB_PATH}")


def run_pipeline():
    """Executa todas as etapas do pipeline ETL."""

    print("[INFO] Iniciando pipeline ETL...")

    materiais, movimentacoes = extract()

    materiais, movimentacoes, estoque_atual = transform(
        materiais,
        movimentacoes
    )

    validate(materiais, movimentacoes, estoque_atual)

    save_processed_files(
        materiais,
        movimentacoes,
        estoque_atual
    )

    load(
        materiais,
        movimentacoes,
        estoque_atual
    )

    print("[INFO] Pipeline finalizado com sucesso.")


if __name__ == "__main__":
    run_pipeline()


