"""Demo: indicadores x meta x gatilho, com fila de relatos (5 porques).

Todos os dados sao FICTICIOS (gerados com semente fixa).
Ideia do sistema real: o dado vem da matriz e ninguem "ajusta" o numero;
quando um indicador estoura o gatilho, a filial precisa justificar (relato).
"""
import numpy as np
import pandas as pd

rng = np.random.default_rng(11)
# nome: (meta, gatilho, maior_e_melhor)
INDICADORES = {
    "Aderencia ao checklist (%)": (95, 85, True),
    "Preventivas no prazo (%)": (90, 80, True),
    "Consumo (km/l)": (3.2, 2.9, True),
    "Manutencao corretiva (R$/km)": (0.35, 0.45, False),
}
FILIAIS = ["Matriz", "Satelite A", "Satelite B"]


def avaliar(valor, meta, gatilho, maior_melhor):
    if maior_melhor:
        return "Gatilho estourado" if valor < gatilho else ("Abaixo da meta" if valor < meta else "OK")
    return "Gatilho estourado" if valor > gatilho else ("Acima da meta" if valor > meta else "OK")


def mes_exemplo():
    linhas = []
    for f in FILIAIS:
        for nome, (meta, gat, mm) in INDICADORES.items():
            ruido = rng.normal(0, 0.09)
            valor = round(meta * (1 + ruido - (0.08 if mm else -0.08) * rng.random()), 2)
            linhas.append((f, nome, valor, meta, gat, avaliar(valor, meta, gat, mm)))
    df = pd.DataFrame(linhas, columns=["filial", "indicador", "resultado", "meta", "gatilho", "status"])
    df["relato"] = np.where(df["status"].eq("Gatilho estourado"), "Sem relato", "")
    return df


if __name__ == "__main__":
    df = mes_exemplo()
    print(df.to_string(index=False))
    print("\nRelatos pendentes por filial:")
    print(df[df["relato"] == "Sem relato"].groupby("filial").size().rename("pendentes"))
