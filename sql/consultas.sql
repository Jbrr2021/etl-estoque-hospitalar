-- 1. Ver todos os materiais cadastrados
SELECT *
FROM dim_materiais;


-- 2. Ver todas as movimentações
SELECT *
FROM fato_movimentacoes;


-- 3. Ver estoque atual
SELECT
    nome,
    categoria,
    estoque_atual,
    estoque_minimo,
    abaixo_minimo
FROM estoque_atual;


-- 4. Materiais abaixo do estoque mínimo
SELECT
    nome,
    categoria,
    estoque_atual,
    estoque_minimo
FROM estoque_atual
WHERE abaixo_minimo = 1;


-- 5. Total de saídas por setor
SELECT
    setor,
    SUM(quantidade) AS total_saida
FROM fato_movimentacoes
WHERE tipo = 'saida'
GROUP BY setor
ORDER BY total_saida DESC;


-- 6. Movimentações por categoria
SELECT
    m.categoria,
    f.tipo,
    SUM(f.quantidade) AS total
FROM fato_movimentacoes f
INNER JOIN dim_materiais m
    ON f.id_material = m.id_material
GROUP BY m.categoria, f.tipo
ORDER BY m.categoria, f.tipo;


-- 7. Materiais próximos do vencimento
SELECT
    nome,
    categoria,
    data_validade,
    estoque_atual
FROM estoque_atual
WHERE data_validade <= DATE('now', '+180 days')
ORDER BY data_validade;
