import sqlite3
from pathlib import Path

import pandas as pd


BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "database" / "estoque.db"


print("Iniciando verificação do banco...")
print(f"Banco utilizado: {DB_PATH}")


def mostrar_resultado(titulo, query, conexao):
    print("\n" + "=" * 60)
    print(titulo)
    print("=" * 60)

    resultado = pd.read_sql_query(query, conexao)

    if resultado.empty:
        print("Nenhum resultado encontrado.")
    else:
        print(resultado)


with sqlite3.connect(DB_PATH) as conn:
    mostrar_resultado(
        "Tabelas criadas no banco",
        """
        SELECT name AS tabela
        FROM sqlite_master
        WHERE type = 'table';
        """,
        conn,
    )

    mostrar_resultado(
        "Estoque atual dos materiais",
        """
        SELECT
            nome,
            categoria,
            estoque_atual,
            estoque_minimo,
            abaixo_minimo
        FROM estoque_atual;
        """,
        conn,
    )

    mostrar_resultado(
        "Materiais abaixo do estoque mínimo",
        """
        SELECT
            nome,
            categoria,
            estoque_atual,
            estoque_minimo
        FROM estoque_atual
        WHERE abaixo_minimo = 1;
        """,
        conn,
    )

    mostrar_resultado(
        "Total de saídas por setor",
        """
        SELECT
            setor,
            SUM(quantidade) AS total_saida
        FROM fato_movimentacoes
        WHERE tipo = 'saida'
        GROUP BY setor
        ORDER BY total_saida DESC;
        """,
        conn,
    )

    mostrar_resultado(
        "Movimentações por categoria",
        """
        SELECT
            m.categoria,
            f.tipo,
            SUM(f.quantidade) AS total
        FROM fato_movimentacoes f
        INNER JOIN dim_materiais m
            ON f.id_material = m.id_material
        GROUP BY m.categoria, f.tipo
        ORDER BY m.categoria, f.tipo;
        """,
        conn,
    )

print("\nVerificação finalizada.")