"""
Gera um dataset simulado de Não Conformidades (RNCs) e Unidades,
inspirado na experiência real de Felipe em Qualidade/Segurança dos Alimentos
(Assaí Atacadista, Habib's, Betel Consultoria).

Uso: python3 gerar_dataset.py
Saída: nao_conformidades.csv, unidades.csv, portfolio_qualidade.db
"""

import csv
import random
import sqlite3
from datetime import date, timedelta

random.seed(42)

# ---------- Dimensão: Unidades ----------
REGIOES = ["Sudeste", "Sul", "Nordeste", "Centro-Oeste"]
BANDEIRAS = ["Varejo Alimentar", "Food Service", "Indústria"]

unidades = []
for i in range(1, 26):  # 25 unidades
    unidades.append({
        "id_unidade": f"U{i:03d}",
        "nome_unidade": f"Unidade {i:03d}",
        "regiao": random.choice(REGIOES),
        "bandeira": random.choice(BANDEIRAS),
        "num_refeicoes_dia": random.choice([0, 250, 500, 800, 1000, 1250]),
    })

# ---------- Fato: Não Conformidades ----------
TIPOS_DESVIO = [
    "Temperatura inadequada",
    "Rotulagem incorreta",
    "Falha em BPF",
    "Documentação incompleta (APPCC/HACCP)",
    "Praga/vetor identificado",
    "Higienização inadequada",
    "Cross contamination",
    "Fornecedor não homologado",
    "Validade vencida",
    "EPI/uniforme não conforme",
]

GRAVIDADE = ["Baixa", "Média", "Alta", "Crítica"]
GRAVIDADE_PESOS = [0.35, 0.35, 0.22, 0.08]

STATUS = ["Aberta", "Em tratativa", "Fechada", "Reincidente"]
RESPONSAVEIS = [
    "Ana Souza", "Bruno Lima", "Carla Mendes", "Diego Alves",
    "Elaine Rocha", "Felipe Oliveira", "Gustavo Reis", "Helena Dias",
    "Igor Santos", "Julia Nogueira",
]

start = date(2023, 10, 1)
end = date(2025, 8, 1)
days_range = (end - start).days

rows = []
rnc_id = 1
for _ in range(1400):
    unidade = random.choice(unidades)
    data_abertura = start + timedelta(days=random.randint(0, days_range))
    gravidade = random.choices(GRAVIDADE, weights=GRAVIDADE_PESOS, k=1)[0]

    # Tempo de fechamento correlacionado com gravidade (críticas fecham mais rápido, viram prioridade)
    base_dias = {"Baixa": 12, "Média": 8, "Alta": 5, "Crítica": 3}[gravidade]
    dias_fechamento = max(0, int(random.gauss(base_dias, base_dias * 0.5)))

    status = random.choices(STATUS, weights=[0.10, 0.15, 0.65, 0.10], k=1)[0]
    data_fechamento = ""
    if status in ("Fechada", "Reincidente"):
        data_fechamento = (data_abertura + timedelta(days=dias_fechamento)).isoformat()

    rows.append({
        "id_rnc": f"RNC{rnc_id:05d}",
        "id_unidade": unidade["id_unidade"],
        "data_abertura": data_abertura.isoformat(),
        "tipo_desvio": random.choice(TIPOS_DESVIO),
        "gravidade": gravidade,
        "status": status,
        "data_fechamento": data_fechamento,
        "dias_para_fechamento": dias_fechamento if data_fechamento else "",
        "responsavel": random.choice(RESPONSAVEIS),
    })
    rnc_id += 1

# ---------- Salvar CSVs ----------
with open("unidades.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=unidades[0].keys())
    writer.writeheader()
    writer.writerows(unidades)

with open("nao_conformidades.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=rows[0].keys())
    writer.writeheader()
    writer.writerows(rows)

# ---------- Carregar em SQLite ----------
conn = sqlite3.connect("portfolio_qualidade.db")
cur = conn.cursor()

cur.execute("DROP TABLE IF EXISTS unidades")
cur.execute("""
    CREATE TABLE unidades (
        id_unidade TEXT PRIMARY KEY,
        nome_unidade TEXT,
        regiao TEXT,
        bandeira TEXT,
        num_refeicoes_dia INTEGER
    )
""")
cur.executemany(
    "INSERT INTO unidades VALUES (:id_unidade, :nome_unidade, :regiao, :bandeira, :num_refeicoes_dia)",
    unidades
)

cur.execute("DROP TABLE IF EXISTS nao_conformidades")
cur.execute("""
    CREATE TABLE nao_conformidades (
        id_rnc TEXT PRIMARY KEY,
        id_unidade TEXT,
        data_abertura TEXT,
        tipo_desvio TEXT,
        gravidade TEXT,
        status TEXT,
        data_fechamento TEXT,
        dias_para_fechamento INTEGER,
        responsavel TEXT,
        FOREIGN KEY (id_unidade) REFERENCES unidades(id_unidade)
    )
""")
cur.executemany(
    """INSERT INTO nao_conformidades VALUES
       (:id_rnc, :id_unidade, :data_abertura, :tipo_desvio, :gravidade,
        :status, :data_fechamento, :dias_para_fechamento, :responsavel)""",
    rows
)

conn.commit()
conn.close()

print(f"OK: {len(unidades)} unidades, {len(rows)} não conformidades geradas.")
print("Arquivos: unidades.csv, nao_conformidades.csv, portfolio_qualidade.db")
