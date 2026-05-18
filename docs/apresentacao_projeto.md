# Apresentação do Projeto: Pipeline ETL de Estoque Hospitalar

Este documento reúne uma explicação prática do projeto, com foco em entrevistas, apresentações técnicas e conversas com recrutadores ou profissionais da área de Dados.

---

## Resumo curto do projeto

Desenvolvi um pipeline ETL em Python para simular um controle de estoque hospitalar.

O projeto extrai dados brutos de arquivos CSV, realiza tratamento e validação com Pandas, salva os dados tratados em uma camada `processed`, carrega as informações em um banco SQLite e registra métricas de execução em um arquivo CSV.

Fluxo principal:

```text
data/raw → Python/Pandas → data/processed → SQLite → logs
```

---

## Explicação em até 30 segundos

Este projeto simula um pipeline ETL para controle de estoque hospitalar.  
Ele extrai dados de arquivos CSV, trata e valida as informações com Python e Pandas, calcula o estoque atual dos materiais, identifica itens abaixo do estoque mínimo, salva os dados tratados, carrega tudo em um banco SQLite e registra métricas de execução em uma pasta de logs.

---

## Explicação em até 1 minuto

Desenvolvi esse projeto para praticar conceitos da área de Dados, principalmente ETL, qualidade de dados, SQL e organização em camadas.

A ideia foi simular um cenário de estoque hospitalar, algo conectado com minha experiência profissional. O pipeline lê arquivos CSV com materiais e movimentações de entrada e saída, padroniza textos, converte datas, remove duplicidades, calcula o estoque atual e identifica materiais abaixo do estoque mínimo.

Depois disso, os dados tratados são salvos em `data/processed`, carregados em um banco SQLite e consultados com SQL. Também adicionei uma camada de métricas em `logs/`, registrando data e hora da execução, quantidade de registros processados, quantidade de materiais abaixo do mínimo e status da execução.

---

## Explicação técnica

O projeto foi organizado em camadas para simular uma estrutura comum em projetos de Dados.

A camada `data/raw` armazena os dados brutos de entrada, sem tratamento.  
A camada `data/processed` armazena os arquivos tratados gerados automaticamente pelo pipeline.  
A pasta `database` armazena o banco SQLite criado pelo processo.  
A pasta `logs` armazena as métricas de execução do pipeline.

O pipeline principal está no arquivo:

```text
src/pipeline.py
```

Ele segue as etapas:

1. Extração dos arquivos CSV.
2. Transformação dos dados com Pandas.
3. Validação da qualidade dos dados.
4. Salvamento dos dados tratados em CSV.
5. Carga dos dados em SQLite.
6. Registro de métricas de execução.

---

## Tecnologias usadas

- Python
- Pandas
- SQL
- SQLite
- Git/GitHub
- VS Code
- PowerShell

---

## Principais conceitos praticados

- ETL
- Extração de dados
- Transformação de dados
- Validação de dados
- Qualidade de dados
- Modelagem simples
- Banco de dados relacional
- Consultas SQL
- Separação entre dados brutos e tratados
- Métricas de execução
- Versionamento com Git/GitHub
- Documentação técnica

---

## Por que escolhi esse tema?

Escolhi o tema de estoque hospitalar porque tenho experiência profissional em ambiente hospitalar, com controle de materiais, conferência, organização de informações, planilhas, validade e apoio operacional.

Com isso, consegui conectar minha experiência prática com meus estudos em Dados, criando um projeto que simula um problema real: acompanhar entradas, saídas, estoque atual e materiais abaixo do mínimo.

---

## Problema simulado

O problema simulado é:

> Como organizar e tratar dados de estoque hospitalar para identificar materiais abaixo do estoque mínimo e apoiar a análise operacional?

O pipeline responde a perguntas como:

- Qual é o estoque atual de cada material?
- Quais materiais estão abaixo do estoque mínimo?
- Qual setor teve maior volume de saídas?
- Quais categorias tiveram mais movimentações?
- O pipeline executou corretamente?
- Quantos registros foram processados?

---

## Dados de entrada

O projeto utiliza dois arquivos CSV principais:

```text
data/raw/materiais.csv
data/raw/movimentacoes.csv
```

O arquivo `materiais.csv` contém o cadastro dos materiais, com nome, categoria, data de validade e estoque mínimo.

O arquivo `movimentacoes.csv` contém as entradas e saídas de materiais, com data, tipo de movimentação, quantidade e setor.

---

## Transformações realizadas

Durante a transformação, o pipeline realiza:

- Padronização de textos.
- Conversão de datas.
- Remoção de duplicidades.
- Tratamento de quantidades inválidas.
- Criação da coluna `quantidade_ajustada`.
- Cálculo do estoque atual.
- Identificação de materiais abaixo do estoque mínimo.

A regra principal é:

```text
entrada = soma no estoque
saida = subtrai do estoque
```

---

## Validações realizadas

O pipeline valida:

- Se existem materiais sem ID.
- Se existem movimentações sem ID de material.
- Se existem quantidades negativas.
- Se existem tipos de movimentação inválidos.
- Se existem movimentações com materiais não cadastrados.
- Se o estoque atual foi calculado corretamente.

Essas validações ajudam a evitar que dados inconsistentes sejam carregados no banco.

---

## Saídas geradas pelo projeto

O projeto gera:

```text
data/processed/materiais_tratados.csv
data/processed/movimentacoes_tratadas.csv
data/processed/estoque_atual.csv
database/estoque.db
logs/metricas_execucao.csv
```

---

## Métricas de execução

O arquivo:

```text
logs/metricas_execucao.csv
```

registra informações sobre cada execução do pipeline.

Campos registrados:

- `data_hora_execucao`
- `qtd_materiais_lidos`
- `qtd_movimentacoes_lidas`
- `qtd_materiais_tratados`
- `qtd_movimentacoes_tratadas`
- `qtd_materiais_abaixo_minimo`
- `status_execucao`

Essa etapa adiciona rastreabilidade básica ao pipeline.

---

## Consultas SQL criadas

As consultas SQL permitem analisar:

- todos os materiais cadastrados;
- todas as movimentações;
- estoque atual;
- materiais abaixo do estoque mínimo;
- total de saídas por setor;
- movimentações por categoria;
- materiais próximos do vencimento.

Arquivo:

```text
sql/consultas.sql
```

---

## O que aprendi com o projeto

Com esse projeto, pratiquei:

- organização de estrutura de pastas;
- criação de pipeline ETL;
- leitura de CSV com Pandas;
- transformação e validação de dados;
- carga de dados em SQLite;
- criação de consultas SQL;
- geração de arquivos tratados;
- criação de métricas de execução;
- documentação de projeto;
- versionamento com Git/GitHub;
- resolução de erros no terminal.

---

## Principais dificuldades encontradas

Durante o desenvolvimento, enfrentei alguns pontos importantes:

1. Teste e configuração do Pandas no ambiente.
2. Problemas com aspas no PowerShell ao usar `python -c`.
3. Ajustes no script de verificação do banco.
4. Entendimento do funcionamento do Git, `git add`, commit e push.
5. Organização da documentação no README.

Essas dificuldades foram importantes para entender melhor o fluxo real de desenvolvimento.

---

## Como eu explicaria para um recrutador

Eu explicaria assim:

> Esse foi um projeto prático que desenvolvi para aplicar meus estudos na área de Dados. Usei Python, Pandas, SQL e SQLite para criar um pipeline ETL de controle de estoque hospitalar. O projeto extrai dados de arquivos CSV, faz tratamento e validação, calcula estoque atual, identifica materiais abaixo do estoque mínimo e carrega os dados em banco. Depois evoluí o projeto adicionando camada de dados tratados e métricas de execução, para ter mais organização e rastreabilidade.

---

## Como eu explicaria para alguém técnico

Eu explicaria assim:

> O pipeline foi estruturado em etapas de extração, transformação, validação, persistência em arquivos tratados, carga em SQLite e registro de métricas. Os dados brutos ficam em `data/raw`, os dados tratados são gerados em `data/processed`, o banco SQLite fica em `database` e as métricas de execução ficam em `logs`. Usei Pandas para manipulação dos dados, SQLite para persistência e SQL para consultas analíticas. Também adicionei validações para garantir consistência antes da carga.

---

## Perguntas que podem surgir em entrevista

### 1. Por que você usou CSV como entrada?

Porque CSV é um formato simples e comum para troca de dados. A ideia foi simular um cenário inicial de ingestão de dados brutos antes de evoluir para fontes mais robustas, como APIs, bancos relacionais ou cloud storage.

---

### 2. Por que usou SQLite?

Usei SQLite por ser leve, simples e adequado para um projeto local de estudos. Ele permite praticar carga em banco e consultas SQL sem precisar configurar um servidor de banco mais complexo.

Em uma evolução futura, o projeto pode ser migrado para PostgreSQL ou BigQuery.

---

### 3. Qual a diferença entre `raw` e `processed`?

A camada `raw` armazena os dados brutos, sem alterações.

A camada `processed` armazena os dados já tratados, padronizados e prontos para análise ou carga em banco.

---

### 4. O que é ETL?

ETL significa Extract, Transform and Load.

No projeto:

- Extract: leitura dos arquivos CSV.
- Transform: limpeza, padronização, cálculo de estoque e validações.
- Load: carga dos dados tratados em banco SQLite.

---

### 5. O que você faria para evoluir esse projeto?

Algumas melhorias seriam:

- migrar de SQLite para PostgreSQL;
- consumir dados de uma API;
- gerar logs em arquivo `.log`;
- criar dashboard em Power BI ou Looker Studio;
- criar versão em Google Cloud com Cloud Storage e BigQuery;
- automatizar o pipeline com agendamento;
- usar Airflow ou Prefect para orquestração;
- criar testes automatizados.

---

## Pontos fortes do projeto

- Tema conectado com experiência profissional real.
- Estrutura organizada em camadas.
- Pipeline funcional de ponta a ponta.
- Uso de Python, Pandas, SQL e SQLite.
- Validações de qualidade dos dados.
- Registro de métricas de execução.
- Documentação no README.
- Versionamento no GitHub.

---

## Resumo final

Este projeto representa um primeiro passo prático na área de Dados, conectando experiência operacional com tecnologia.

Ele demonstra capacidade de estruturar um problema, criar um pipeline funcional, tratar e validar dados, carregar informações em banco, consultar com SQL, registrar métricas e documentar a evolução do projeto.