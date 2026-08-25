# SQL Aplicado à Qualidade — Exercícios Progressivos

Dataset: `portfolio_qualidade.db` (tabelas `nao_conformidades` e `unidades`)
Ferramenta sugerida: DB Browser for SQLite (gratuito) ou `sqlite3` no terminal.

Cada bloco tem: contexto de negócio → pergunta → **tente sozinho antes de olhar o gabarito**.

---

## Nível 1 — SELECT, WHERE, ORDER BY

**1.1** Liste todas as não conformidades de gravidade "Crítica", ordenadas da mais recente para a mais antiga.

```sql
SELECT id_rnc, id_unidade, tipo_desvio, data_abertura, status
FROM nao_conformidades
WHERE gravidade = 'Crítica'
ORDER BY data_abertura DESC;
```

**1.2** Quantas não conformidades estão com status "Aberta" ou "Em tratativa" (ou seja, ainda não resolvidas)?

```sql
SELECT COUNT(*) AS pendentes
FROM nao_conformidades
WHERE status IN ('Aberta', 'Em tratativa');
```

---

## Nível 2 — GROUP BY, agregações

**2.1** Quantas não conformidades existem por tipo de desvio? Ordene do mais frequente para o menos frequente.

```sql
SELECT tipo_desvio, COUNT(*) AS total
FROM nao_conformidades
GROUP BY tipo_desvio
ORDER BY total DESC;
```

**2.2** Qual o tempo médio de fechamento (em dias) por gravidade? (Considere só as fechadas)

```sql
SELECT gravidade, ROUND(AVG(dias_para_fechamento), 1) AS media_dias
FROM nao_conformidades
WHERE dias_para_fechamento IS NOT NULL AND dias_para_fechamento <> ''
GROUP BY gravidade
ORDER BY media_dias;
```

**2.3** Quais os 5 responsáveis com mais RNCs abertas em nome deles?

```sql
SELECT responsavel, COUNT(*) AS total_rncs
FROM nao_conformidades
GROUP BY responsavel
ORDER BY total_rncs DESC
LIMIT 5;
```

---

## Nível 3 — JOIN entre tabelas

**3.1** Traga o nome da unidade, região e bandeira junto com cada não conformidade (mostre 10 linhas).

```sql
SELECT n.id_rnc, u.nome_unidade, u.regiao, u.bandeira, n.tipo_desvio, n.gravidade
FROM nao_conformidades n
JOIN unidades u ON n.id_unidade = u.id_unidade
LIMIT 10;
```

**3.2** Qual região concentra mais não conformidades de gravidade "Alta" ou "Crítica"?

```sql
SELECT u.regiao, COUNT(*) AS total_graves
FROM nao_conformidades n
JOIN unidades u ON n.id_unidade = u.id_unidade
WHERE n.gravidade IN ('Alta', 'Crítica')
GROUP BY u.regiao
ORDER BY total_graves DESC;
```

---

## Nível 4 — Subqueries e HAVING

**4.1** Liste as unidades com mais de 60 não conformidades registradas no total (unidades "problema").

```sql
SELECT id_unidade, COUNT(*) AS total
FROM nao_conformidades
GROUP BY id_unidade
HAVING COUNT(*) > 60
ORDER BY total DESC;
```

**4.2** Quais unidades têm uma taxa de reincidência (status = 'Reincidente') acima da média geral da rede?
*(Este é o tipo de pergunta que aparece em entrevista — pensar em "acima da média" exige subquery.)*

```sql
WITH taxa_por_unidade AS (
    SELECT
        id_unidade,
        COUNT(*) AS total,
        SUM(CASE WHEN status = 'Reincidente' THEN 1 ELSE 0 END) AS reincidentes,
        1.0 * SUM(CASE WHEN status = 'Reincidente' THEN 1 ELSE 0 END) / COUNT(*) AS taxa
    FROM nao_conformidades
    GROUP BY id_unidade
)
SELECT id_unidade, total, reincidentes, ROUND(taxa, 3) AS taxa_reincidencia
FROM taxa_por_unidade
WHERE taxa > (SELECT AVG(taxa) FROM taxa_por_unidade)
ORDER BY taxa_reincidencia DESC;
```

---

## Nível 5 — As métricas que viram o Dashboard (Fase 2)

**5.1** Ranking de unidades por número de não conformidades graves (Alta + Crítica), com nome e região.
*(Vira o "Top unidades críticas" do dashboard.)*

```sql
SELECT
    u.nome_unidade,
    u.regiao,
    COUNT(*) AS rncs_graves
FROM nao_conformidades n
JOIN unidades u ON n.id_unidade = u.id_unidade
WHERE n.gravidade IN ('Alta', 'Crítica')
GROUP BY u.id_unidade
ORDER BY rncs_graves DESC
LIMIT 10;
```

**5.2** Evolução mensal do número de não conformidades abertas (para gráfico de linha no Power BI).

```sql
SELECT
    strftime('%Y-%m', data_abertura) AS mes,
    COUNT(*) AS total_abertas
FROM nao_conformidades
GROUP BY mes
ORDER BY mes;
```

**5.3** Tempo médio de fechamento por tipo de desvio, só considerando quem já fechou — indicador de "quais problemas demoram mais para resolver".

```sql
SELECT
    tipo_desvio,
    COUNT(*) AS total_fechadas,
    ROUND(AVG(dias_para_fechamento), 1) AS media_dias_fechamento
FROM nao_conformidades
WHERE status = 'Fechada' AND dias_para_fechamento IS NOT NULL AND dias_para_fechamento <> ''
GROUP BY tipo_desvio
ORDER BY media_dias_fechamento DESC;
```

---

## Como praticar de verdade (não só ler o gabarito)

1. Abra `portfolio_qualidade.db` no DB Browser for SQLite.
2. Tente escrever a query sozinho antes de olhar a resposta — erre, ajuste, rode de novo.
3. Depois de terminar o Nível 5, você já domina as consultas que vão alimentar o Dashboard da Fase 2.
4. Suba este arquivo + o dataset no GitHub como projeto "SQL Practice — Qualidade de Dados", com um README curto explicando o contexto (fictício, inspirado em experiência real em Qualidade/Segurança dos Alimentos).
