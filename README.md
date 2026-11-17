# Frota Analytics Demo

Demos em Python/Pandas de três sistemas internos que desenvolvi para gestão de frota em uma distribuidora de bebidas. **Todos os dados aqui são fictícios** (gerados com semente fixa): nenhuma placa, filial, colaborador ou número real da empresa.

*English: Python/Pandas demos of three fleet-management systems I built at work, rebuilt here with 100% synthetic data.*

## O que cada demo mostra

| Arquivo | Problema de negócio | Técnicas |
|---|---|---|
| `nok_ans_demo.py` | Motoristas reapontam o mesmo defeito a cada saída. Como transformar apontamentos repetidos em uma ocorrência e medir se o conserto saiu dentro do prazo (ANS)? | `groupby`, `diff`, `cumsum` para agrupar eventos; cálculo de prazo por criticidade e filial |
| `dto_demo.py` | Quem deveria registrar o checklist no mês e não registrou? | `merge` (incl. `cross`), exclusão de férias do denominador, cobertura por mês e filial |
| `gatilhos_demo.py` | Quais indicadores estouraram meta ou gatilho e ainda não têm relato de causa? | Regras de status por indicador, fila de pendências por filial |

## Como rodar

```bash
pip install pandas numpy
python nok_ans_demo.py
python dto_demo.py
python gatilhos_demo.py
```

## Exemplo de saída (`nok_ans_demo.py`)

```
90 ocorrencias | 13 em aberto | 3 abertas vencidas
            ocorrencias  aderencia_ans
filial
Matriz               23           65.2
Satelite A           26           57.7
Satelite B           41           78.0
```

## Sobre os sistemas reais

Os sistemas originais rodam na operação (Python/SQLite, HTML/JS e importação de planilhas do ERP) e acompanham checklist de motoristas, itens reprovados, manutenções preventivas e indicadores mensais por filial. Aqui estão apenas as regras de análise, reescritas com dados sintéticos.

**Autor:** Eder Joe · [LinkedIn](https://www.linkedin.com/in/eder-joe-960798431/)
