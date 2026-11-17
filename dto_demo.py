"""Demo: cobertura mensal de um checklist obrigatorio por colaborador e filial.

Todos os dados sao FICTICIOS (gerados com semente fixa).
Ideia do sistema real: quem entra no controle precisa registrar o checklist
todo mes; quem esta de ferias no mes sai do calculo (nao conta como pendente).
"""
import numpy as np
import pandas as pd

rng = np.random.default_rng(7)
MESES = pd.period_range("2026-08", "2026-10", freq="M")
FILIAIS = ["Matriz", "Satelite A", "Satelite B"]


def gerar():
    colab = pd.DataFrame({
        "id": range(1, 61),
        "filial": rng.choice(FILIAIS, 60, p=[0.5, 0.3, 0.2]),
        "funcao": rng.choice(["Motorista", "Operador de empilhadeira"], 60, p=[0.7, 0.3]),
    })
    registros = pd.DataFrame(
        [(i, m) for i in colab["id"] for m in MESES if rng.random() < 0.8],
        columns=["id", "mes"])
    ferias = pd.DataFrame(
        [(i, m) for i in colab["id"] for m in MESES if rng.random() < 0.08],
        columns=["id", "mes"])
    return colab, registros, ferias


def cobertura(colab, registros, ferias):
    base = colab.merge(pd.DataFrame({"mes": MESES}), how="cross")
    base = base.merge(ferias.assign(ferias=True), on=["id", "mes"], how="left")
    base = base[base["ferias"].isna()]  # ferias saem do calculo
    base = base.merge(registros.assign(feito=True), on=["id", "mes"], how="left")
    base["feito"] = base["feito"].fillna(False).astype(bool)
    return base.groupby(["mes", "filial"])["feito"].agg(["sum", "count"]).assign(
        cobertura_pct=lambda d: (d["sum"] / d["count"] * 100).round(1))


if __name__ == "__main__":
    colab, registros, ferias = gerar()
    cob = cobertura(colab, registros, ferias)
    print(cob.rename(columns={"sum": "com_registro", "count": "no_controle"}))
    pend = colab.merge(registros[registros["mes"] == MESES[-1]], on="id", how="left")
    print("\nPendentes em", MESES[-1], ":", int(pend["mes"].isna().sum()), "colaboradores")
