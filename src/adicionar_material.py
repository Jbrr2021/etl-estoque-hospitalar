from pathlib import Path
from datetime import datetime

import pandas as pd


# Define a pasta base do projeto
BASE_DIR = Path(__file__).resolve().parent.parent

# Caminhos dos arquivos CSV brutos
MATERIAIS_PATH = BASE_DIR / "data" / "raw" / "materiais.csv"
MOVIMENTACOES_PATH = BASE_DIR / "data" / "raw" / "movimentacoes.csv"


def carregar_csv(caminho_arquivo):
    """Carrega um arquivo CSV e retorna um DataFrame."""

    if not caminho_arquivo.exists():
        raise FileNotFoundError(f"Arquivo não encontrado: {caminho_arquivo}")

    return pd.read_csv(caminho_arquivo)


def gerar_proximo_id(df, coluna_id):
    """Gera o próximo ID com base no maior ID existente."""

    if df.empty:
        return 1

    return int(df[coluna_id].max()) + 1


def solicitar_texto(mensagem):
    """Solicita um texto obrigatório ao usuário."""

    while True:
        valor = input(mensagem).strip()

        if valor:
            return valor

        print("[ERRO] Este campo não pode ficar vazio.")


def solicitar_data(mensagem):
    """Solicita uma data no formato AAAA-MM-DD."""

    while True:
        valor = input(mensagem).strip()

        try:
            datetime.strptime(valor, "%Y-%m-%d")
            return valor

        except ValueError:
            print("[ERRO] Data inválida. Use o formato AAAA-MM-DD. Exemplo: 2026-12-31")


def solicitar_numero_inteiro(mensagem):
    """Solicita um número inteiro positivo."""

    while True:
        valor = input(mensagem).strip()

        try:
            numero = int(valor)

            if numero > 0:
                return numero

            print("[ERRO] O número precisa ser maior que zero.")

        except ValueError:
            print("[ERRO] Digite um número inteiro válido.")


def solicitar_categoria():
    """Solicita a categoria do material."""

    categorias_validas = {
        "1": "Medicamento",
        "2": "Soro",
        "3": "Material hospitalar",
        "4": "EPI",
        "5": "Limpeza",
        "6": "Outros",
    }

    print("\nCategorias disponíveis:")
    print("1 - Medicamento")
    print("2 - Soro")
    print("3 - Material hospitalar")
    print("4 - EPI")
    print("5 - Limpeza")
    print("6 - Outros")

    while True:
        opcao = input("Escolha a categoria pelo número: ").strip()

        if opcao in categorias_validas:
            return categorias_validas[opcao]

        print("[ERRO] Opção inválida. Escolha um número da lista.")


def solicitar_tipo_movimentacao():
    """Solicita o tipo de movimentação."""

    tipos_validos = {
        "1": "entrada",
        "2": "saida",
    }

    print("\nTipo de movimentação:")
    print("1 - Entrada")
    print("2 - Saída")

    while True:
        opcao = input("Escolha o tipo pelo número: ").strip()

        if opcao in tipos_validos:
            return tipos_validos[opcao]

        print("[ERRO] Opção inválida. Escolha 1 para entrada ou 2 para saída.")


def cadastrar_material():
    """Cadastra um novo material e uma movimentação inicial nos arquivos CSV."""

    print("\n========================================")
    print(" Cadastro de novo material no estoque")
    print("========================================\n")

    materiais = carregar_csv(MATERIAIS_PATH)
    movimentacoes = carregar_csv(MOVIMENTACOES_PATH)

    novo_id_material = gerar_proximo_id(materiais, "id_material")
    novo_id_movimentacao = gerar_proximo_id(movimentacoes, "id_movimentacao")

    nome = solicitar_texto("Nome do material: ")
    categoria = solicitar_categoria()
    data_validade = solicitar_data("Data de validade (AAAA-MM-DD): ")
    estoque_minimo = solicitar_numero_inteiro("Estoque mínimo: ")

    print("\nAgora informe a movimentação inicial desse material.")

    data_movimentacao = solicitar_data("Data da movimentação (AAAA-MM-DD): ")
    tipo = solicitar_tipo_movimentacao()
    quantidade = solicitar_numero_inteiro("Quantidade movimentada: ")
    setor = solicitar_texto("Setor: ")

    novo_material = pd.DataFrame(
        [
            {
                "id_material": novo_id_material,
                "nome": nome,
                "categoria": categoria,
                "data_validade": data_validade,
                "estoque_minimo": estoque_minimo,
            }
        ]
    )

    nova_movimentacao = pd.DataFrame(
        [
            {
                "id_movimentacao": novo_id_movimentacao,
                "id_material": novo_id_material,
                "data_movimentacao": data_movimentacao,
                "tipo": tipo,
                "quantidade": quantidade,
                "setor": setor,
            }
        ]
    )

    materiais_atualizados = pd.concat(
        [materiais, novo_material],
        ignore_index=True
    )

    movimentacoes_atualizadas = pd.concat(
        [movimentacoes, nova_movimentacao],
        ignore_index=True
    )

    materiais_atualizados.to_csv(
        MATERIAIS_PATH,
        index=False,
        encoding="utf-8-sig"
    )

    movimentacoes_atualizadas.to_csv(
        MOVIMENTACOES_PATH,
        index=False,
        encoding="utf-8-sig"
    )

    print("\n[INFO] Material cadastrado com sucesso!")
    print(f"[INFO] ID do material: {novo_id_material}")
    print(f"[INFO] ID da movimentação inicial: {novo_id_movimentacao}")
    print("\nPróximo passo recomendado:")
    print("python src/pipeline.py")
    print("python src/verificar_banco.py")


if __name__ == "__main__":
    cadastrar_material()