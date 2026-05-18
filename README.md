# Pipeline ETL de Estoque Hospitalar

Este projeto simula um pipeline ETL para controle de estoque hospitalar, utilizando Python, Pandas, SQLite e SQL.

A ideia do projeto é praticar conceitos fundamentais da área de Dados, como extração, transformação, validação, organização em camadas, carga em banco de dados e consultas SQL para análise.

O tema foi escolhido com base em uma experiência prática real em ambiente hospitalar, envolvendo controle de estoque, conferência de materiais, validade, entradas, saídas, organização de informações e apoio operacional.

---

## Objetivo do projeto

Criar um pipeline ETL simples e funcional utilizando Python, Pandas, SQLite e SQL.

O pipeline realiza as seguintes etapas:

1. Extrai dados brutos de arquivos CSV.
2. Trata e padroniza os dados com Python/Pandas.
3. Valida a qualidade das informações.
4. Calcula o estoque atual dos materiais.
5. Identifica materiais abaixo do estoque mínimo.
6. Salva os dados tratados na camada `data/processed/`.
7. Carrega os dados tratados em um banco SQLite.
8. Executa consultas SQL para análise dos dados.

---

## Tecnologias utilizadas

- Python
- Pandas
- SQL
- SQLite
- VS Code
- PowerShell
- Git/GitHub

---

## Estrutura do projeto

```text
etl-estoque-hospitalar/
├── data/
│   ├── raw/
│   │   ├── materiais.csv
│   │   └── movimentacoes.csv
│   └── processed/
│       ├── estoque_atual.csv
│       ├── materiais_tratados.csv
│       └── movimentacoes_tratadas.csv
├── database/
│   └── estoque.db
├── sql/
│   └── consultas.sql
├── src/
│   ├── pipeline.py
│   └── verificar_banco.py
├── .gitignore
├── README.md
├── requirements.txt
└── teste_pandas.py
```

---

## Descrição das pastas e arquivos

### `data/raw/`

Contém os arquivos CSV com os dados brutos do projeto.

Arquivos utilizados:

- `materiais.csv`
- `movimentacoes.csv`

Esses arquivos representam os dados originais antes de qualquer tratamento.

---

### `data/processed/`

Contém os arquivos tratados gerados automaticamente pelo pipeline após a etapa de transformação.

Arquivos gerados:

- `materiais_tratados.csv`
- `movimentacoes_tratadas.csv`
- `estoque_atual.csv`

Essa camada representa os dados após padronização, validação, cálculo de estoque atual e preparação para análise.

---

### `database/`

Pasta onde o banco SQLite é criado após a execução do pipeline.

Arquivo gerado:

- `estoque.db`

O banco contém as tabelas criadas pelo pipeline para consulta e análise dos dados.

---

### `sql/`

Contém consultas SQL utilizadas para análise dos dados carregados no banco.

Arquivo:

- `consultas.sql`

---

### `src/`

Contém os scripts Python do projeto.

Arquivos:

- `pipeline.py`: executa o pipeline ETL completo.
- `verificar_banco.py`: consulta o banco SQLite e exibe os resultados no terminal.

---

### `requirements.txt`

Lista as dependências necessárias para executar o projeto.

Conteúdo:

```text
pandas
```

---

### `teste_pandas.py`

Arquivo criado para testar se o Pandas estava instalado e funcionando corretamente no ambiente.

---

## Dados utilizados

### Arquivo `materiais.csv`

Este arquivo representa o cadastro dos materiais hospitalares.

Colunas:

- `id_material`
- `nome`
- `categoria`
- `data_validade`
- `estoque_minimo`

Exemplo:

```csv
id_material,nome,categoria,data_validade,estoque_minimo
1,Luva descartável,EPI,2026-08-10,100
2,Seringa 10ml,Material hospitalar,2026-03-15,200
3,Álcool 70,Limpeza,2025-12-20,50
4,Máscara cirúrgica,EPI,2026-06-30,150
5,Compressa estéril,Material hospitalar,2025-11-05,80
```

---

### Arquivo `movimentacoes.csv`

Este arquivo representa as entradas e saídas de materiais.

Colunas:

- `id_movimentacao`
- `id_material`
- `data_movimentacao`
- `tipo`
- `quantidade`
- `setor`

Exemplo:

```csv
id_movimentacao,id_material,data_movimentacao,tipo,quantidade,setor
1,1,2026-01-05,entrada,300,Almoxarifado
2,1,2026-01-10,saida,80,Enfermaria
3,2,2026-01-06,entrada,500,Almoxarifado
4,2,2026-01-15,saida,350,Emergência
5,3,2026-01-07,entrada,100,Almoxarifado
6,3,2026-01-18,saida,70,Higienização
7,4,2026-01-08,entrada,250,Almoxarifado
8,4,2026-01-20,saida,120,Centro Cirúrgico
9,5,2026-01-09,entrada,150,Almoxarifado
10,5,2026-01-22,saida,90,Enfermaria
```

---

## Etapas do pipeline ETL

## 1. Extração

O pipeline lê os arquivos CSV localizados em:

```text
data/raw/materiais.csv
data/raw/movimentacoes.csv
```

A extração é feita com Pandas:

```python
pd.read_csv()
```

---

## 2. Transformação

Durante a transformação dos dados, o pipeline realiza:

- Padronização de textos.
- Conversão de campos de data.
- Remoção de registros duplicados.
- Tratamento de quantidades inválidas.
- Criação da coluna `quantidade_ajustada`.
- Cálculo do estoque atual por material.
- Identificação de materiais abaixo do estoque mínimo.

A regra principal é:

- Entrada aumenta o estoque.
- Saída reduz o estoque.

Exemplo da lógica:

```python
if tipo == "entrada":
    quantidade_ajustada = quantidade
else:
    quantidade_ajustada = -quantidade
```

---

## 3. Validação

O pipeline valida se existem problemas básicos nos dados, como:

- Materiais sem ID.
- Movimentações sem ID de material.
- Quantidades negativas.
- Tipos de movimentação inválidos.
- Movimentações com materiais não cadastrados.
- Estoque atual sem cálculo.

Caso alguma validação falhe, o pipeline exibe um erro e interrompe a execução.

Caso esteja tudo correto, aparece a mensagem:

```text
[INFO] Validação concluída com sucesso.
```

---

## 4. Salvamento dos dados tratados

Após a transformação e validação, o pipeline salva os dados tratados em arquivos CSV na camada `data/processed/`.

Arquivos gerados:

```text
data/processed/materiais_tratados.csv
data/processed/movimentacoes_tratadas.csv
data/processed/estoque_atual.csv
```

Essa etapa permite visualizar os dados já tratados antes da carga no banco SQLite.

---

## 5. Carga

Após a transformação, validação e geração dos arquivos tratados, os dados são carregados em um banco SQLite.

Banco gerado:

```text
database/estoque.db
```

Tabelas criadas:

```text
dim_materiais
fato_movimentacoes
estoque_atual
```

---

## Tabelas criadas no banco

### `dim_materiais`

Tabela de dimensão com o cadastro dos materiais.

Contém:

- ID do material
- Nome
- Categoria
- Data de validade
- Estoque mínimo

---

### `fato_movimentacoes`

Tabela fato com o histórico de movimentações.

Contém:

- ID da movimentação
- ID do material
- Data da movimentação
- Tipo da movimentação
- Quantidade
- Setor
- Quantidade ajustada

---

### `estoque_atual`

Tabela consolidada com o estoque atual calculado.

Contém:

- ID do material
- Estoque atual
- Nome
- Categoria
- Data de validade
- Estoque mínimo
- Indicador de estoque abaixo do mínimo

---

## Como executar o projeto

## 1. Clonar ou abrir o projeto

Abra a pasta do projeto no VS Code:

```text
etl-estoque-hospitalar
```

---

## 2. Verificar se o Python está instalado

No terminal, rode:

```bash
python --version
```

---

## 3. Instalar as dependências

No terminal, dentro da pasta do projeto, execute:

```bash
pip install -r requirements.txt
```

Caso o comando `pip` apresente erro, use:

```bash
python -m pip install -r requirements.txt
```

---

## 4. Testar o Pandas

Foi criado um arquivo chamado `teste_pandas.py` para confirmar se o Pandas está funcionando.

Execute:

```bash
python teste_pandas.py
```

Resultado esperado:

```text
Pandas OK: 2.2.3
```

A versão pode mudar dependendo do ambiente.

---

## 5. Executar o pipeline ETL

Execute:

```bash
python src/pipeline.py
```

Resultado esperado:

```text
[INFO] Iniciando pipeline ETL...
[INFO] Extraindo dados dos arquivos CSV...
[INFO] Transformando dados...
[INFO] Validando qualidade dos dados...
[INFO] Validação concluída com sucesso.
[INFO] Salvando dados tratados na pasta data/processed...
[INFO] Arquivos tratados salvos com sucesso.
[INFO] Carregando dados no banco SQLite...
[INFO] Dados carregados com sucesso em: C:\Users\User\Documents\etl-estoque-hospitalar\database\estoque.db
[INFO] Pipeline finalizado com sucesso.
```

Após essa execução, os arquivos tratados serão gerados na pasta `data/processed/` e o banco `estoque.db` será criado ou atualizado dentro da pasta `database/`.

---

## 6. Verificar os dados carregados

Execute:

```bash
python src/verificar_banco.py
```

Esse script consulta o banco e exibe os resultados no terminal.

---

## Resultado obtido

Após executar o pipeline e verificar o banco, foram criadas as seguintes tabelas:

```text
dim_materiais
fato_movimentacoes
estoque_atual
```

Resultado da tabela de estoque atual:

```text
nome                 categoria             estoque_atual   estoque_minimo   abaixo_minimo
Luva descartável      EPI                  220             100              0
Seringa 10ml          Material hospitalar  150             200              1
Álcool 70             Limpeza              30              50               1
Máscara cirúrgica     EPI                  130             150              1
Compressa estéril     Material hospitalar  60              80               1
```

Materiais identificados abaixo do estoque mínimo:

```text
Seringa 10ml
Álcool 70
Máscara cirúrgica
Compressa estéril
```

Total de saídas por setor:

```text
setor               total_saida
Emergência          350
Enfermaria          170
Centro Cirúrgico    120
Higienização        70
```

Movimentações por categoria:

```text
categoria             tipo      total
EPI                   entrada   550
EPI                   saida     200
Limpeza               entrada   100
Limpeza               saida     70
Material hospitalar   entrada   650
Material hospitalar   saida     440
```

---

## Consultas SQL utilizadas

As consultas SQL estão no arquivo:

```text
sql/consultas.sql
```

Principais análises disponíveis:

1. Ver todos os materiais cadastrados.
2. Ver todas as movimentações.
3. Ver o estoque atual.
4. Identificar materiais abaixo do estoque mínimo.
5. Calcular o total de saídas por setor.
6. Analisar movimentações por categoria.
7. Identificar materiais próximos do vencimento.

Exemplo de consulta:

```sql
SELECT
    nome,
    categoria,
    estoque_atual,
    estoque_minimo
FROM estoque_atual
WHERE abaixo_minimo = 1;
```

---

## Erros encontrados durante o desenvolvimento

Durante o desenvolvimento do projeto, alguns erros aconteceram. Eles foram importantes para entender melhor o ambiente, o terminal e a execução dos scripts.

---

## 1. Pandas já estava instalado

Ao rodar:

```bash
pip install -r requirements.txt
```

O terminal retornou que o Pandas já estava instalado:

```text
Requirement already satisfied: pandas
```

Isso não era um erro. Significava apenas que a biblioteca já existia no ambiente Python.

---

## 2. Interrupção ao importar Pandas

Ao rodar o pipeline pela primeira vez, apareceu um erro terminando com:

```text
KeyboardInterrupt
```

Isso indicava que a execução foi interrompida enquanto o Python carregava o Pandas.

Solução aplicada:

- Rodar novamente com calma.
- Testar o Pandas separadamente.
- Criar o arquivo `teste_pandas.py`.

---

## 3. Problema com aspas no PowerShell

Ao tentar rodar o comando:

```bash
python -c 'import pandas as pd; print("Pandas OK:", pd.__version__)'
```

O PowerShell interpretou as aspas de forma incorreta e gerou:

```text
SyntaxError: '(' was never closed
```

Solução aplicada:

Em vez de testar direto pelo terminal, foi criado o arquivo:

```text
teste_pandas.py
```

Com o conteúdo:

```python
import pandas as pd

print("Pandas OK:", pd.__version__)
```

Depois foi executado:

```bash
python teste_pandas.py
```

Resultado:

```text
Pandas OK: 2.2.3
```

---

## 4. Script de verificação não exibiu resultado

Ao executar:

```bash
python src/verificar_banco.py
```

Nada apareceu no terminal inicialmente.

Possíveis causas:

- Arquivo vazio.
- Código não salvo.
- Ausência de comandos `print`.
- Funções criadas, mas não executadas.

Solução aplicada:

O arquivo `verificar_banco.py` foi refeito com mensagens de início, consultas SQL e exibição dos resultados.

Depois disso, o script funcionou corretamente.

---

## Acertos do projeto

Durante o desenvolvimento, foram concluídas com sucesso as seguintes etapas:

- Criação da estrutura de pastas.
- Criação dos arquivos CSV.
- Criação do script `pipeline.py`.
- Instalação e validação do Pandas.
- Execução do pipeline ETL.
- Criação do banco SQLite.
- Criação das tabelas analíticas.
- Execução de consultas SQL.
- Validação dos resultados no terminal.
- Documentação do projeto no README.
- Criação da camada `data/processed/`.
- Geração automática de arquivos CSV tratados.
- Melhoria das mensagens de execução do pipeline com logs informativos.
- Inclusão de validações adicionais, como tipos de movimentação inválidos e materiais não cadastrados.

---

## O que este projeto demonstra

Este projeto demonstra conhecimentos iniciais e práticos em:

- Área de Dados
- ETL
- Python
- Pandas
- SQL
- SQLite
- Modelagem simples de dados
- Qualidade de dados
- Organização de projeto
- Análise de dados
- Resolução de problemas
- Documentação técnica
- Versionamento com Git/GitHub

---

## Como explicar este projeto em uma entrevista

Uma forma simples de apresentar o projeto:

```text
Desenvolvi um pipeline ETL em Python para simular um controle de estoque hospitalar.
O processo extrai dados brutos de arquivos CSV, realiza transformações com Pandas,
como padronização de textos, conversão de datas, remoção de duplicidades e cálculo
de estoque atual. Depois, os dados são validados, salvos em uma camada de dados
tratados e carregados em um banco SQLite. Também criei consultas SQL para analisar
materiais abaixo do estoque mínimo, saídas por setor e movimentações por categoria.
```

---

## Aprendizados

Com este projeto, foi possível praticar:

- Como organizar um projeto de dados.
- Como criar uma estrutura de pastas profissional.
- Como separar dados brutos e dados tratados.
- Como ler arquivos CSV com Pandas.
- Como transformar dados usando Python.
- Como validar informações antes da carga.
- Como salvar arquivos tratados em CSV.
- Como salvar dados em banco SQLite.
- Como consultar dados com SQL.
- Como interpretar erros no terminal.
- Como documentar um projeto para portfólio.
- Como versionar melhorias com Git/GitHub.

---

## Próximas melhorias possíveis

Possíveis evoluções para este projeto:

1. Adicionar mais dados ao CSV.
2. Criar novas validações de qualidade.
3. Criar métricas de execução do pipeline.
4. Gerar logs em arquivo `.log`.
5. Migrar o banco de SQLite para PostgreSQL.
6. Criar dashboard no Power BI ou Looker Studio.
7. Criar versão em cloud usando Google Cloud.
8. Usar BigQuery como destino dos dados.
9. Automatizar a execução do pipeline.
10. Criar testes automatizados.

---

## Status do projeto

Pipeline executado com sucesso:

```text
CSV bruto → Python/Pandas → Transformação → Validação → CSV tratado → SQLite → SQL
```

Fluxo organizado em camadas:

```text
data/raw → data/processed → database
```

---

## Autor

João Batista Rodrigues Ribeiro

Estudante de Engenharia da Computação, com interesse em Dados, Cloud, Automação, IA, SQL, Python e soluções voltadas para organização e melhoria de processos.