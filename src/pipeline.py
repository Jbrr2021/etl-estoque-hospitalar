import sqlite3
from pathlib import Path
from datetime import datetime

import pandas as pd


# Define a pasta base do projeto
BASE_DIR = Path(__file__).resolve().parent.parent

# Define os caminhos das pastas utilizadas no projeto
RAW_DIR = BASE_DIR / "data" / "raw"
PROCESSED_DIR = BASE_DIR / "data" / "processed"
DATABASE_DIR = BASE_DIR / "database"
LOGS_DIR = BASE_DIR / "logs"

# Garante que as pastas existam antes de salvar arquivos
PROCESSED_DIR.mkdir(exist_ok=True)
DATABASE_DIR.mkdir(exist_ok=True)
LOGS_DIR.mkdir(exist_ok=True)

# Caminhos dos arquivos gerados
DB_PATH = DATABASE_DIR / "estoque.db"
METRICS_PATH = LOGS_DIR / "metricas_execucao.csv"


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


def save_metrics(
    data_hora_execucao,
    qtd_materiais_lidos,
    qtd_movimentacoes_lidas,
    qtd_materiais_tratados,
    qtd_movimentacoes_tratadas,
    qtd_materiais_abaixo_minimo,
    status_execucao
):
    """Salva métricas de execução do pipeline em um arquivo CSV."""

    print("[INFO] Salvando métricas de execução...")

    # Cria um DataFrame com as métricas da execução atual
    metricas = pd.DataFrame(
        [
            {
                "data_hora_execucao": data_hora_execucao,
                "qtd_materiais_lidos": qtd_materiais_lidos,
                "qtd_movimentacoes_lidas": qtd_movimentacoes_lidas,
                "qtd_materiais_tratados": qtd_materiais_tratados,
                "qtd_movimentacoes_tratadas": qtd_movimentacoes_tratadas,
                "qtd_materiais_abaixo_minimo": qtd_materiais_abaixo_minimo,
                "status_execucao": status_execucao,
            }
        ]
    )

    # Se o arquivo já existir, adiciona a nova execução ao final
    if METRICS_PATH.exists():
        metricas.to_csv(
            METRICS_PATH,
            mode="a",
            header=False,
            index=False,
            encoding="utf-8-sig"
        )
    else:
        metricas.to_csv(
            METRICS_PATH,
            index=False,
            encoding="utf-8-sig"
        )

    print(f"[INFO] Métricas salvas com sucesso em: {METRICS_PATH}")


def run_pipeline():
    """Executa todas as etapas do pipeline ETL."""

    print("[INFO] Iniciando pipeline ETL...")

    # Registra a data e hora da execução
    data_hora_execucao = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    status_execucao = "SUCESSO"

    try:
        # Extração
        materiais_raw, movimentacoes_raw = extract()

        qtd_materiais_lidos = len(materiais_raw)
        qtd_movimentacoes_lidas = len(movimentacoes_raw)

        # Transformação
        materiais, movimentacoes, estoque_atual = transform(
            materiais_raw,
            movimentacoes_raw
        )

        qtd_materiais_tratados = len(materiais)
        qtd_movimentacoes_tratadas = len(movimentacoes)

        qtd_materiais_abaixo_minimo = int(
            estoque_atual["abaixo_minimo"].sum()
        )

        # Validação
        validate(materiais, movimentacoes, estoque_atual)

        # Salvamento dos arquivos tratados
        save_processed_files(
            materiais,
            movimentacoes,
            estoque_atual
        )

        # Carga no banco
        load(
            materiais,
            movimentacoes,
            estoque_atual
        )

    except Exception as erro:
        status_execucao = f"ERRO: {erro}"

        # Caso ocorra erro, tenta salvar o máximo de informação possível
        qtd_materiais_lidos = 0
        qtd_movimentacoes_lidas = 0
        qtd_materiais_tratados = 0
        qtd_movimentacoes_tratadas = 0
        qtd_materiais_abaixo_minimo = 0

        print(f"[ERRO] O pipeline falhou: {erro}")

    # Salva as métricas mesmo se houver erro
    save_metrics(
        data_hora_execucao,
        qtd_materiais_lidos,
        qtd_movimentacoes_lidas,
        qtd_materiais_tratados,
        qtd_movimentacoes_tratadas,
        qtd_materiais_abaixo_minimo,
        status_execucao
    )

    print("[INFO] Pipeline finalizado.")


if __name__ == "__main__":
    run_pipeline()