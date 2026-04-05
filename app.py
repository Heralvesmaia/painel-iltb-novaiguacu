import streamlit as st
import pandas as pd

# =====================================================================
# 1. CONFIGURAÇÃO E SENHAS
# =====================================================================
st.set_page_config(page_title="Painel ILTB - Nova Iguaçu", page_icon="🏥", layout="wide")

COFRE_DE_ACESSOS = {
    "maternidade2026": "MATERNIDADE MUNICIPAL MARIANA BULHOES",
    "viga_iltb": "CLINICA DA FAMILIA JARDIM DA VIGA",
    "hgni_123": "HGNI HOSPITAL GERAL DE NOVA IGUACU",
    "heraldo_admin": "TODAS"
}

# =====================================================================
# 2. MOTOR DE BUSCA (DUPLO: PACIENTES E EVOLUÇÕES)
# =====================================================================
@st.cache_data(ttl=60) # Atualiza a cada 1 minuto
def carregar_todos_os_dados():
    # SUBSTITUA PELO SEU ID REAL
    SHEET_ID = "1A6uPoNNsz-5SzDRvZZfurYxt7NOzv73Dtde-GEsoV6o" 
    
    # GIDs das abas (AJUSTE O GID_EVO COM O NÚMERO QUE VOCÊ PEGOU)
    GID_PACIENTES = "0"
    GID_EVO = "355108392" 

    url_pacientes = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv&gid={GID_PACIENTES}"
    url_evolucoes = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv&gid={GID_EVO}"
    
    df_pac = pd.read_csv(url_pacientes)
    df_evo = pd.read_csv(url_evolucoes)
    
    return df_pac, df_evo

# =====================================================================
# 3. LOGIN
# =====================================================================
if "unidade_logada" not in st.session_state:
    st.session_state["unidade_logada"] = None

if st.session_state["unidade_logada"] is None:
    st.title("🔒 Acesso Restrito - Monitoramento ILTB")
    senha = st.text_input("Senha de Acesso", type="password")
    if st.button("Entrar"):
        if senha in COFRE_DE_ACESSOS:
            st.session_state["unidade_logada"] = COFRE_DE_ACESSOS[senha]
            st.rerun()
        else:
            st.error("Senha incorreta.")

# =====================================================================
# 4. PAINEL PRINCIPAL
# =====================================================================
else:
    unidade = st.session_state["unidade_logada"]
    st.title(f"🏥 Gestão de Prontuários - {unidade}")
    
    if st.sidebar.button("Sair (Logout)"):
        st.session_state["unidade_logada"] = None
        st.rerun()

    try:
        df_pacientes, df_evolucoes = carregar_todos_os_dados()
        
        # Filtro de Unidade
        if unidade != "TODAS":
            df_pacientes = df_pacientes[df_pacientes["Unidade de Tratamento"] == unidade]

        # --- SEÇÃO 1: MÉTRICAS ---
        st.write("### 📊 Indicadores da Unidade")
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Total", len(df_pacientes))
        c2.metric("🟢 Ativos", len(df_pacientes[df_pacientes["Situação"] == "Em andamento"]))
        c3.metric("🔵 Altas", len(df_pacientes[df_pacientes["Situação"] == "Tratamento Completo"]))
        c4.metric("🔴 Interrupções", len(df_pacientes[df_pacientes["Situação"] == "Interrupção do tratamento"]))

        st.divider()

        # --- SEÇÃO 2: CONSULTA DE PRONTUÁRIO ELETRÔNICO ---
        st.write("### 🔍 Consultar Histórico Clínico (Prontuário)")
        
        # Criar lista para busca: "Nome do Paciente | CNS"
        df_pacientes["Busca"] = df_pacientes["Nome do Paciente"] + " | " + df_pacientes["CNS"].astype(str)
        paciente_selecionado = st.selectbox("Selecione um paciente para ver a evolução completa:", ["-- Selecione --"] + list(df_pacientes["Busca"].unique()))

        if paciente_selecionado != "-- Selecione --":
            cns_busca = paciente_selecionado.split(" | ")[1]
            
            # Puxar Evoluções do paciente (Comparando com a coluna CNS/CPF do Paciente na aba Evoluções)
            # Nota: O nome da coluna na aba Evolucoes deve ser exatamente "CNS/CPF do Paciente"
            evolucoes_pac = df_evolucoes[df_evolucoes["CNS/CPF do Paciente"].astype(str).str.contains(cns_busca)]
            
            if evolucoes_pac.empty:
                st.info("Nenhuma evolução clínica registrada além do cadastro inicial.")
            else:
                st.write(f"#### 📅 Linha do Tempo: {paciente_selecionado.split(' | ')[0]}")
                for i, row in evolucoes_pac.sort_values(by="Data da Evolução", ascending=False).iterrows():
                    with st.expander(f"🔹 {row['Data da Evolução']} - {row['Tipo/Mês']}"):
                        st.write(f"**Situação na data:** {row['Situação']}")
                        st.write(f"**Relato Clínico:** {row['Relato Clínico']}")
                        st.success(f"**Conduta:** {row['Conduta']}")

        st.divider()

        # --- SEÇÃO 3: LISTA GERAL ---
        st.write("### 📋 Lista Geral de Pacientes")
        st.dataframe(df_pacientes[["Data Notificação", "Nome do Paciente", "CNS", "Esquema TPT", "Situação"]], use_container_width=True, hide_index=True)

    except Exception as e:
        st.error(f"Erro ao processar dados: {e}")
