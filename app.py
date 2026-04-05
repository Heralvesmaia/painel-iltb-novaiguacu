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
# 2. MOTOR DE BUSCA (RESILIENTE A ERROS DE CABEÇALHO)
# =====================================================================
@st.cache_data(ttl=60)
def carregar_todos_os_dados():
    # SEU ID DA PLANILHA
    SHEET_ID = "1A6uPoNNsz-5SzDRvZZfurYxt7NOzv73Dtde-GEsoV6o" 
    
    # GIDs das abas (CONFIRME O GID DA ABA EVOLUCOES NO NAVEGADOR)
    GID_PACIENTES = "0"
    GID_EVO = "355108392" # <-- TROQUE PELO NÚMERO APÓS #gid=

    url_pacientes = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv&gid={GID_PACIENTES}"
    url_evolucoes = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv&gid={GID_EVO}"
    
    df_pac = pd.read_csv(url_pacientes)
    df_evo = pd.read_csv(url_evolucoes)
    
    # TRUQUE DE MESTRE: Limpa espaços em branco nos nomes das colunas
    df_pac.columns = df_pac.columns.str.strip()
    df_evo.columns = df_evo.columns.str.strip()
    
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
        
        # Criar identificador único (Nome + CNS)
        df_pacientes["Busca"] = df_pacientes["Nome do Paciente"] + " | " + df_pacientes["CNS"].astype(str)
        
        paciente_selecionado = st.selectbox("Selecione um paciente para ver a evolução completa:", 
                                            ["-- Selecione --"] + list(df_pacientes["Busca"].unique()))

        if paciente_selecionado != "-- Selecione --":
            # Pega o CNS (tudo o que vem depois do '|') e remove espaços
            id_busca = paciente_selecionado.split("|")[1].strip()
            
            # Identifica automaticamente qual é a coluna de ID na aba Evoluções (mesmo que o nome mude um pouco)
            col_id_evo = [c for c in df_evolucoes.columns if "CNS" in c or "CPF" in c][0]
            
            # Filtra as evoluções comparando números limpos
            df_evolucoes[col_id_evo] = df_evolucoes[col_id_evo].astype(str).str.replace(r'\D', '', regex=True)
            id_busca_limpo = "".join(filter(str.isdigit, id_busca))
            
            evolucoes_pac = df_evolucoes[df_evolucoes[col_id_evo] == id_busca_limpo]
            
            if evolucoes_pac.empty:
                st.info("Nenhuma evolução clínica registrada além do cadastro inicial.")
            else:
                st.write(f"#### 📅 Linha do Tempo: {paciente_selecionado.split('|')[0].strip()}")
                
                # Ordenar da evolução mais recente para a mais antiga
                evolucoes_pac = evolucoes_pac.sort_values(by=evolucoes_pac.columns[0], ascending=False)
                
                for _, row in evolucoes_pac.iterrows():
                    # Ajuste dinâmico de nomes de colunas para exibição
                    data_atend = row.get("Data da Evolução", "Data não informada")
                    tipo_mes = row.get("Tipo/Mês", "Evolução")
                    situacao = row.get("Situação", "-")
                    relato = row.get("Relato Clínico", "-")
                    conduta = row.get("Conduta", "-")
                    
                    with st.expander(f"🔹 {data_atend} - {tipo_mes}"):
                        st.write(f"**Situação na data:** {situacao}")
                        st.write(f"**Relato Clínico:** {relato}")
                        st.info(f"**Conduta:** {conduta}")

        st.divider()

        # --- SEÇÃO 3: LISTA GERAL ---
        st.write("### 📋 Lista Geral de Pacientes")
        st.dataframe(df_pacientes[["Data Notificação", "Nome do Paciente", "CNS", "Esquema TPT", "Situação"]], use_container_width=True, hide_index=True)

    except Exception as e:
        st.error(f"Erro ao processar dados: {e}")
