# 📊 Análise de Vendas e Segmentação de Clientes (RFM)

![Status Concluído](https://img.shields.io/badge/STATUS-CONCLUÍDO-GREEN?style=for-the-badge)
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-150458?style=for-the-badge&logo=pandas&logoColor=white)
![Tkinter](https://img.shields.io/badge/Tkinter-GUI-blue?style=for-the-badge)

Este projeto implementa uma **Análise RFM (Recência, Frequência e Monetarização)** completa em Python, processando um histórico de vendas (2018-2023) para segmentar clientes e sugerir ações estratégicas de marketing automaticamente.

O diferencial deste script é o uso de uma **Interface Gráfica (Tkinter)** que apresenta visualmente cada etapa do tratamento de dados ao usuário final, além de exportar o relatório conclusivo.

## 🎯 O que é Análise RFM?

A técnica RFM classifica os clientes com base em três pilares comportamentais:
* **R (Recência):** Há quanto tempo o cliente fez a última compra?
* **F (Frequência):** Quantas vezes ele comprou no período?
* **M (Monetarização):** Qual o valor total gasto?

## 📂 Estrutura do Repositório

Aqui está a descrição de cada arquivo presente neste projeto:

| Arquivo | Descrição |
| :--- | :--- |
| `analise_vendas_2018_2023.py` | **Código Principal:** Script Python contendo toda a lógica de ETL, cálculos estatísticos e a interface gráfica (Tkinter). |
| `vendas2018_2023.csv` | **Input (Entrada):** Base de dados bruta com o histórico de vendas necessário para iniciar a análise. |
| `df_agregado_cliente.csv` | **Output (Saída):** Arquivo gerado automaticamente pelo script contendo a segmentação final e as ações sugeridas. |
| `README.md` | Documentação oficial do projeto com instruções de uso. |

## 📋 Funcionalidades do Projeto

1.  **Interface Interativa:** Janelas pop-up (Tkinter) mostram os dados sendo transformados em tempo real (Carregamento -> Limpeza -> Agregação -> Segmentação).
2.  **Cálculo Automático de Scores:**
    * Criação de quartis para classificar Recência e Frequência.
    * Definição de faixas personalizadas para o valor Monetário.
3.  **Segmentação de Clientes:**
    * Classificação em grupos como: *Campeões, Clientes Fiéis, Potenciais, Novos, Em Risco* e *Perdidos*.
4.  **Motor de Decisão:**
    * Gera automaticamente uma **"Ação Recomendada"** para cada cliente (ex: *"Priorizar: Oferecer benefícios exclusivos..."* ou *"Reativar: Campanhas de win-back..."*).
5.  **Exportação de Dados:** Gera um arquivo `.csv` final pronto para ser consumido por times de Marketing ou ferramentas de BI (Power BI/Tableau).

## 🚀 Tecnologias Utilizadas

* **Python 3.x**
* **Pandas:** Manipulação e agregação de dados (`groupby`, `qcut`, `cut`).
* **Tkinter:** Construção da interface gráfica para visualização das tabelas.
* **DateTime:** Manipulação temporal para cálculo de recência.

## 📦 Pré-requisitos e Como Executar

### 1. Preparação do Arquivo
Para que o script funcione, certifique-se de que o arquivo `vendas2018_2023.csv` está na mesma pasta do script `analise_vendas_2018_2023.py`.

### 2. Executando o Código
Certifique-se de ter as bibliotecas instaladas (`pandas`, `tkinter`) e rode o script:

```bash
# Clone o repositório
git clone [https://github.com/brenaspessoa-sys/Analise-RFM-Vendas.git](https://github.com/brenaspessoa-sys/Analise-RFM-Vendas.git)

# Execute o script
python analise_vendas_2018_2023.py
