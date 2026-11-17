"""Demo: itens NOK de checklist -> ocorrencias -> aderencia ao ANS.

Todos os dados sao FICTICIOS (gerados com semente fixa).
Regras espelham a logica de um sistema real de manutencao de frota:
  1. O motorista reaponta o mesmo defeito a cada saida ate o conserto.
     Apontamentos da mesma placa e item viram UMA ocorrencia.
  2. Sem novo apontamento por 48h, a ocorrencia conta como resolvida (presumido).
  3. prazo = observacao + deslocamento + oficina (por criticidade);
     filiais satelite mandam o servico para a matriz: deslocamento em dobro.
"""
import numpy as np
import pandas as pd

rng = np.random.default_rng(42)
AGORA = pd.Timestamp("2026-11-16 08:00")
ITENS = ["Pneus", "Freios", "Farol", "Nivel de oleo", "Para-brisa", "Cinto de seguranca"]
FILIAIS = {"Matriz": 1, "Satelite A": 2, "Satelite B": 2}  # fator de deslocamento
# horas: observacao, deslocamento, oficina
PRAZOS = {"Emergencial": (4, 2, 24), "Imediata": (8, 4, 48), "Alta": (24, 4, 72), "Media": (48, 4, 120)}


def gerar_apontamentos(n_placas=60):
    linhas = []
    for i in range(n_placas):
        placa = f"FKE{i:04d}"
        filial = rng.choice(list(FILIAIS))
        for item in rng.choice(ITENS, size=rng.integers(1, 3), replace=False):
            crit = rng.choice(list(PRAZOS), p=[0.3, 0.2, 0.3, 0.2])
            inicio = AGORA - pd.Timedelta(hours=int(rng.integers(6, 24 * 30)))
            # reaponta a cada ~12h por alguns dias, ate "o conserto"
            dias = int(rng.integers(1, 6)) * 2
            for k in range(dias):
                linhas.append((placa, filial, item, crit, inicio + pd.Timedelta(hours=12 * k)))
    return pd.DataFrame(linhas, columns=["placa", "filial", "item", "criticidade", "apontado_em"])


def virar_ocorrencias(ap):
    ap = ap.sort_values(["placa", "item", "apontado_em"]).copy()
    gap = ap.groupby(["placa", "item"])["apontado_em"].diff()
    ap["ocorrencia"] = (gap.isna() | (gap > pd.Timedelta(hours=48))).cumsum()
    oc = ap.groupby("ocorrencia").agg(
        placa=("placa", "first"), filial=("filial", "first"), item=("item", "first"),
        criticidade=("criticidade", "first"), inicio=("apontado_em", "min"),
        ultimo=("apontado_em", "max"), apontamentos=("apontado_em", "count"))
    oc["aberta"] = oc["ultimo"] + pd.Timedelta(hours=48) > AGORA
    oc["fim"] = oc["ultimo"].where(~oc["aberta"])  # resolvida em: ultimo apontamento
    return oc.reset_index()


def aplicar_ans(oc):
    obs, desl, ofi = (oc["criticidade"].map(lambda c: PRAZOS[c][i]) for i in range(3))
    oc["prazo_h"] = obs + desl * oc["filial"].map(FILIAIS) + ofi
    decorrido = (oc["fim"].fillna(AGORA) - oc["inicio"]).dt.total_seconds() / 3600
    oc["no_prazo"] = decorrido <= oc["prazo_h"]
    return oc


if __name__ == "__main__":
    oc = aplicar_ans(virar_ocorrencias(gerar_apontamentos()))
    print(f"{len(oc)} ocorrencias | {oc['aberta'].sum()} em aberto | "
          f"{(~oc.loc[oc['aberta'], 'no_prazo']).sum()} abertas vencidas")
    tab = oc.groupby("filial")["no_prazo"].agg(["count", "mean"]).rename(
        columns={"count": "ocorrencias", "mean": "aderencia_ans"})
    tab["aderencia_ans"] = (tab["aderencia_ans"] * 100).round(1)
    print(tab)
    print(oc.groupby("criticidade")["no_prazo"].mean().mul(100).round(1).rename("aderencia_%"))
    oc.to_csv("ocorrencias_demo.csv", index=False)
