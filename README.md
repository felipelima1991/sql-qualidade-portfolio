# SQL Aplicado à Qualidade — Projeto de Estudo

## Contexto

Depois de anos atuando com Qualidade e Segurança dos Alimentos (auditorias, não conformidades, indicadores) em redes como Assaí Atacadista e Habib's, decidi estruturar esse conhecimento em um projeto de dados: um dataset simulado de **não conformidades (RNCs)**, inspirado em situações reais do dia a dia de campo, usado para praticar SQL do básico ao avançado.

Este repositório é o primeiro passo de uma trilha de portfólio em Análise de Dados — o próximo projeto (dashboard em Power BI) reaproveita este mesmo dataset.

## Estrutura

```
├── gerar_dataset.py       # script que gera os dados simulados
├── nao_conformidades.csv  # tabela fato: 1.400 registros de RNCs
├── unidades.csv           # tabela dimensão: 25 unidades fictícias
├── portfolio_qualidade.db # banco SQLite pronto para consultas
└── exercicios_sql.md      # exercícios progressivos com gabarito
```

## Sobre os dados

Os dados são **simulados**, mas o desenho segue a lógica real de gestão de qualidade no varejo alimentar/indústria: tipo de desvio (BPF, rotulagem, temperatura, praga, etc.), gravidade, status de tratativa e tempo de fechamento — as mesmas variáveis que eu acompanhava presencialmente em auditorias.

## O que este projeto demonstra

- Modelagem simples de dados relacionais (tabela fato + dimensão)
- Consultas SQL: `SELECT`, `WHERE`, `GROUP BY`, `JOIN`, subqueries com `HAVING`, CTEs (`WITH`)
- Tradução de indicadores de negócio (taxa de reincidência, tempo médio de fechamento, ranking de unidades críticas) em queries

## Como rodar

```bash
python3 gerar_dataset.py
sqlite3 portfolio_qualidade.db
```

## Próximos passos da trilha

1. ✅ SQL aplicado (este repositório)
2. 🔜 Dashboard de Não Conformidades em Power BI
3. 🔜 Réplica analítica do projeto "Desperdício Zero"
4. 🔜 Python (pandas) cruzando as bases anteriores

---
*Projeto de portfólio de Felipe Oliveira de Lima — em transição de carreira para Análise de Dados.*
