import streamlit as st
import pandas as pd
import joblib
import json
import plotly.express as px
from datetime import datetime

# --- 1. CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="Porto de Santos - Risk Analytics", layout="wide")

# --- 2. FUNÇÃO DE CARREGAMENTO ---
@st.cache_resource
def load_assets():
    # Carrega o Parquet
    df = pd.read_parquet("final_santos_data_lake.parquet")
    # CORREÇÃO: Forçar datetime
    df['data'] = pd.to_datetime(df['data'])
    
    # Carrega o Modelo
    modelo = joblib.load('modelo_porto_realista.pkl')
    
    # Carrega o JSON de Configuração
    with open('config_projeto.json', 'r') as f:
        config_data = json.load(f)
        
    return df, modelo, config_data

# --- 3. EXECUÇÃO DO CARREGAMENTO ---
df, modelo, config = load_assets()

# --- 4. SIDEBAR ---
st.sidebar.header("⚙️ Parâmetros Financeiros")
cotacao_input = st.sidebar.slider(
    "Cotação Dólar (R$)", 
    min_value=4.0, max_value=7.0, 
    value=float(config['ultima_cotacao']), 
    step=0.01
)

# --- CÁLCULOS DINÂMICOS ---
df['prejuizo_brl_dinamico'] = df['prejuizo_usd'] * cotacao_input
total_usd = df['prejuizo_usd'].sum()
total_brl = df['prejuizo_brl_dinamico'].sum()

# --- TÍTULO ---
st.title("🚢 Logística Portuária vs. Clima: Santos")
st.markdown(f"**Última atualização dos parâmetros:** {config['data_atualizacao']}")

# --- KPIs PRINCIPAIS ---
col1, col2, col3 = st.columns(3)
col1.metric("Prejuízo Estimado (USD)", f"US$ {total_usd:,.2f}")
col2.metric("Prejuízo Estimado (BRL)", f"R$ {total_brl:,.2f}", delta=f"Câmbio: {cotacao_input}")
col3.metric("Toneladas Perdidas", f"{df['toneladas_perdidas'].sum():,.0f} t")

st.markdown("---")

# --- GRÁFICOS ---
c1, c2 = st.columns(2)

with c1:
    st.subheader("📊 Impacto Financeiro Mensal")
    df_mensal = df.resample('M', on='data')['prejuizo_brl_dinamico'].sum().reset_index()
    fig_mensal = px.bar(df_mensal, x='data', y='prejuizo_brl_dinamico', 
                        title="Prejuízo Acumulado por Mês (R$)", color_discrete_sequence=['#E63946'])
    st.plotly_chart(fig_mensal, use_container_width=True)

with c2:
    st.subheader("📉 Correlação: Umidade vs. Movimentação")
    fig_scatter = px.scatter(df, x='umidade_relativa', y='VLPesoCargaBruta', 
                             color='chuva', size='prejuizo_usd',
                             title="Dispersão: Onde a ineficiência acontece?",
                             labels={'VLPesoCargaBruta': 'Carga (t)', 'umidade_relativa': 'Umidade (%)'})
    st.plotly_chart(fig_scatter, use_container_width=True)

# --- ÁREA DE PREVISÃO (IA) ---
st.markdown("---")
st.subheader("🤖 Diagnóstico de Operabilidade (Machine Learning)")

st.info("Simule as condições climáticas atuais para prever o risco de paralisação.")

# --- CORREÇÃO: Criação dos inputs que estavam faltando ---
col_ia1, col_ia2 = st.columns(2)

with col_ia1:
    input_umidade = st.slider("Umidade Relativa Atual (%)", 0, 100, 70)
    input_chuva = st.slider("Precipitação Atual (mm)", 0.0, 100.0, 5.0)

with col_ia2:
    # Para o modelo funcionar, ele espera 'umidade_ontem' e 'chuva_ontem'. 
    # Vou sugerir usar os mesmos valores ou permitir ajuste fino:
    input_umidade_ontem = st.number_input("Umidade Ontem (%)", 0, 100, input_umidade)
    input_chuva_ontem = st.number_input("Precipitação Ontem (mm)", 0.0, 100.0, input_chuva)

# Organização dos dados para o Modelo
entrada_ia = pd.DataFrame([[input_umidade, input_chuva, input_umidade_ontem, input_chuva_ontem]], 
                          columns=['umidade_relativa', 'chuva', 'umidade_ontem', 'chuva_ontem'])

# Execução da Predição
if st.button("Executar Diagnóstico"):
    predicao = modelo.predict(entrada_ia)[0]
    probabilidade = modelo.predict_proba(entrada_ia).max() * 100

    if predicao == 1:
        st.error(f"⚠️ **RISCO DE INEFICIÊNCIA ALTO** ({probabilidade:.1f}% de confiança)")
        st.write("**Recomendação:** Avaliar retenção de fluxo interior-porto para evitar custos extras de Demurrage.")
    else:
        st.success(f"✅ **OPERAÇÃO NORMAL** ({probabilidade:.1f}% de confiança)")
        st.write("**Condição:** Clima favorável para o carregamento de grãos e operações de pátio.")