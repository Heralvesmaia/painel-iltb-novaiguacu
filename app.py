import streamlit as st
import pandas as pd

# =====================================================================
# 1. CONFIGURAÇÃO DA PÁGINA E DO COFRE DE SENHAS
# =====================================================================
st.set_page_config(page_title="Painel ILTB - Nova Iguaçu", page_icon="🏥", layout="wide")

COFRE_DE_ACESSOS = {
    "maternidade2026": "MATERNIDADE MUNICIPAL MARIANA BULHOES",
    "viga_iltb": "CLINICA DA FAMILIA JARDIM DA VIGA",
    "hgni_123": "HGNI HOSPITAL GERAL DE NOVA IGUACU",
    "heraldo_admin": "TODAS"
}

# =====================================================================
# 2. MOTOR DE BUSCA
# =====================================================================
@st.cache_data(ttl=300)
def carregar_dados():
    # COLE O SEU ID VERDADEIRO ABAIXO
    SHEET_ID = "1A6uPoNNsz-5SzDRvZZfurYxt7NOzv73Dtde-GEsoV6o"
    
    url_pacientes = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv&gid=0"
    
    df = pd.read_csv(url_pacientes)
    
    df['Data Notificação'] = pd.to_datetime(df['Data Notificação'], format='%d/%m/%Y', errors='coerce')
    df = df.sort_values(by='Data Notificação', ascending=False)
    df['Data Notificação'] = df['Data Notificação'].dt.strftime('%d/%m/%Y')
    
    return df

# =====================================================================
# 3. TELA DE LOGIN
# =====================================================================
if "unidade_logada" not in st.session_state:
    st.session_state["unidade_logada"] = None

if st.session_state["unidade_logada"] is None:
    st.title("🔒 Acesso Restrito - Monitoramento ILTB")
    st.write("Digite a senha fornecida pela Coordenação de Vigilância para acessar os prontuários da sua Unidade.")
    
    senha_digitada = st.text_input("Senha de Acesso", type="password")
    
    if st.button("Entrar no Sistema"):
        if senha_digitada in COFRE_DE_ACESSOS:
            st.session_state["unidade_logada"] = COFRE_DE_ACESSOS[senha_digitada]
            st.rerun()
        else:
            st.error("❌ Senha incorreta ou Unidade não autorizada.")

# =====================================================================
# 4. PAINEL DE DADOS
# =====================================================================
else:
    unidade = st.session_state["unidade_logada"]
    
    col1, col2 = st.columns([0.8, 0.2])
    col1.title("🏥 Painel de Prontuários ILTB")
    col1.subheader(f"Unidade Referência: {unidade}")
    
    if col2.button("Sair (Logout)"):
        st.session_state["unidade_logada"] = None
        st.rerun()

    st.divider()

    try:
        with st.spinner('Puxando prontuários da Nuvem...'):
            df_pacientes = carregar_dados()
        
        if unidade != "TODAS":
            df_pacientes = df_pacientes[df_pacientes["Unidade de Tratamento"] == unidade]
            
        if df_pacientes.empty:
            st.warning("Nenhum paciente registrado para esta unidade até o momento.")
        else:
            total = len(df_pacientes)
            # CORREÇÃO APLICADA AQUI: Mudamos de "Situação Atual" para "Situação"
            ativos = len(df_pacientes[df_pacientes["Situação"] == "Em andamento"])
            altas = len(df_pacientes[df_pacientes["Situação"] == "Tratamento Completo"])
            abandonos = len(df_pacientes[df_pacientes["Situação"] == "Interrupção do tratamento"])
            
            c1, c2, c3, c4 = st.columns(4)
            c1.metric("Total de Pacientes", total)
            c2.metric("🟢 Em Andamento", ativos)
            c3.metric("🔵 Altas (Completos)", altas)
            c4.metric("🔴 Interrupções", abandonos)
            
            st.write("---")
            st.write("### 📋 Prontuários Acumulados")
            st.write("*(Modo de Leitura: Você pode pesquisar, clicar nas colunas para ordenar, mas não pode alterar ou apagar dados).*")
            
            # CORREÇÃO APLICADA AQUI TAMBÉM:
            colunas_para_mostrar = [
                "Data Notificação", "Nome do Paciente", "CNS", "Esquema TPT", 
                "Data Início", "Dose Orientada", "Situação"
            ]
            
            st.dataframe(
                df_pacientes[colunas_para_mostrar], 
                use_container_width=True, 
                hide_index=True
            )
            
            st.caption("Criado por Heraldo Maia - Versão 1.0 (Visualização via Python/Streamlit)")

    except Exception as e:
        st.error(f"Erro ao conectar com o Banco Central. Detalhe técnico: {e}")
