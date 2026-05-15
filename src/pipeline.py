import sqlite3
from pathlib import Path

import pandas as pd


BASE_DIR = Path(__file__).resolve().parent.parent

RAW_DIR = BASE_DIR / "data" / "raw"
DATABASE_DIR = BASE_DIR / "database"
DATABASE_DIR.mkdir(exist_ok=True)

DB_PATH = DATABASE_DIR / "estoque.db"


def extract():
    """Extrai os dados brutos dos arquivos CSV."""
    materiais = pd.read_csv(RAW_DIR / "materiais.csv")
    movimentacoes = pd.read_csv(RAW_DIR / "movimentacoes.csv")

    return materiais, movimentacoes


def transform(materiais, movimentacoes):
    """Limpa, padroniza e transforma os dados."""

    materiais = materiais.copy()
    movimentacoes = movimentacoes.copy()

    # Padronização de textos
    materiais["nome"] = materiais["nome"].str.strip()
    materiais["categoria"] = materiais["categoria"].str.strip()

    movimentacoes["tipo"] = movimentacoes["tipo"].str.lower().str.strip()
    movimentacoes["setor"] = movimentacoes["setor"].str.strip()

    # Conversão de datas
    materiais["data_validade"] = pd.to_datetime(materiais["data_validade"])
    movimentacoes["data_movimentacao"] = pd.to_datetime(
        movimentacoes["data_movimentacao"]
    )

    # Remoção de duplicados
    materiais = materiais.drop_duplicates(subset=["id_material"])
    movimentacoes = movimentacoes.drop_duplicates(subset=["id_movimentacao"])

    # Tratamento de quantidades inválidas
    movimentacoes = movimentacoes[movimentacoes["quantidade"] > 0]

    # Criação de coluna de quantidade ajustada
    movimentacoes["quantidade_ajustada"] = movimentacoes.apply(
        lambda linha: linha["quantidade"]
        if linha["tipo"] == "entrada"
        else -linha["quantidade"],
        axis=1,
    )

    # Cálculo do estoque atual por material
    estoque_atual = (
        movimentacoes.groupby("id_material")["quantidade_ajustada"]
        .sum()
        .reset_index()
        .rename(columns={"quantidade_ajustada": "estoque_atual"})
    )

    # Junta o estoque atual com o cadastro de materiais
    estoque_atual = estoque_atual.merge(
        materiais,
        on="id_material",
        how="left"
    )

    # Verifica se o estoque está abaixo do mínimo
    estoque_atual["abaixo_minimo"] = (
        estoque_atual["estoque_atual"] < estoque_atual["estoque_minimo"]
    )

    return materiais, movimentacoes, estoque_atual


def validate(materiais, movimentacoes, estoque_atual):
    """Executa validações simples de qualidade dos dados."""

    if materiais["id_material"].isnull().any():
        raise ValueError("Existem materiais sem ID.")

    if movimentacoes["id_material"].isnull().any():
        raise ValueError("Existem movimentações sem ID de material.")

    if movimentacoes["quantidade"].lt(0).any():
        raise ValueError("Existem quantidades negativas nas movimentações.")

    if estoque_atual["estoque_atual"].isnull().any():
        raise ValueError("Existem materiais sem cálculo de estoque.")

    print("Validação concluída com sucesso.")


def load(materiais, movimentacoes, estoque_atual):
    """Carrega os dados tratados em um banco SQLite."""

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

    print(f"Dados carregados com sucesso em: {DB_PATH}")


def run_pipeline():
    print("Iniciando pipeline ETL...")

    materiais, movimentacoes = extract()
    materiais, movimentacoes, estoque_atual = transform(materiais, movimentacoes)

    validate(materiais, movimentacoes, estoque_atual)
    load(materiais, movimentacoes, estoque_atual)

    print("Pipeline finalizado com sucesso.")


if __name__ == "__main__":
    run_pipeline()


