# 🚢 Porto de Santos: Risk Analytics & Operabilidade Predictiva

![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=Streamlit&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Scikit-Learn](https://img.shields.io/badge/scikit--learn-%23F7931E.svg?style=for-the-badge&logo=scikit-learn&logoColor=white)

## 📌 Contexto do Projeto
A logística portuária de granéis vegetais em Santos é extremamente sensível a condições climáticas. Chuva e umidade elevada não apenas interrompem o carregamento, mas geram custos vultosos de *demurrage* (sobre-estadia de navios) e ineficiências na cadeia de suprimentos.

Este projeto combina um **Data Lake em Parquet** com um **Modelo de Machine Learning** para prever riscos operacionais e estimar o impacto financeiro em tempo real baseando-se na cotação do dólar e variáveis climáticas.

## 🚀 Funcionalidades Principais
* **Diagnóstico Predictivo (IA):** Classificação de risco de operabilidade usando Random Forest/XGBoost.
* **Simulador Financeiro Dinâmico:** Ajuste de câmbio em tempo real para cálculo de prejuízos estimados em BRL/USD.
* **Análise de Correlação:** Visualização dispersiva entre umidade relativa e movimentação de carga.
* **Arquitetura de Dados:** Processamento otimizado utilizando formato colunar (Parquet) para alta performance.

## 🛠️ Tech Stack
* **Linguagem:** Python
* **Interface:** Streamlit
* **Visualização:** Plotly Express
* **Data Prep:** Pandas & PyArrow (Data Lake Simulation)
* **Machine Learning:** Joblib (Modelo Serializado)

## 📊 Como Visualizar
O dashboard está disponível online para consulta:
👉 **[https://santos-port-forecast-ebkbtvqettntndgcy2xsjq.streamlit.app/]**

---
*Desenvolvido como um protótipo de suporte à decisão logística para o Porto de Santos.*
