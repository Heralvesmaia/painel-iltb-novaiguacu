import streamlit as st
import pandas as pd

# =====================================================================
# 1. CONFIGURAÇÃO DA PÁGINA E COFRE DE SENHAS
# =====================================================================
st.set_page_config(page_title="Painel ILTB - Nova Iguaçu", page_icon="🏥", layout="wide")

# Lista completa de unidades fornecida
COFRE_DE_ACESSOS = {
    "heraldo_admin": "TODAS",
    "ist_hgni": "AMBULATORIO DE IST DO HGNI",
    "cav_mulher": "CENTRO DE APOIO E VALORIZAÇÃO DA MULHER (CAV MULHER)",
    "cta_vasco": "CENTRO DE SAÚDE VASCO BARCELOS - CTA",
    "cf_carlinhos": "CLÍNICA DA FAMÍLIA 24h CARLINHOS DA TINGUÁ (MIGUEL COUTO)",
    "cf_gisele": "CLÍNICA DA FAMÍLIA 24h GISELE PALHARES (VILA DE CAVA)",
    "cf_adrianopolis": "CLÍNICA DA FAMÍLIA ADRIANÓPOLIS",
    "cf_alianca": "CLÍNICA DA FAMÍLIA ALIANÇA",
    "cf_corumba": "CLÍNICA DA FAMÍLIA CORUMBÁ",
    "cf_ceramica": "CLÍNICA DA FAMÍLIA DA CERÂMICA",
    "cf_dombosco": "CLÍNICA DA FAMÍLIA DOM BOSCO",
    "cf_ambai": "CLÍNICA DA FAMÍLIA DR MARCO POLO DE GOUVEIA PEREIRA (AMBAÍ)",
    "cf_delmo": "CLINICA DA FAMILIA Dr. DELMO MOURA SA",
    "cf_emilia": "CLÍNICA DA FAMÍLIA EMILIA GOMES - CTA",
    "cf_cacuia": "CLÍNICA DA FAMÍLIA ERALDO SARDINHA (CACUIA)",
    "cf_figueira": "CLÍNICA DA FAMÍLIA FIGUEIRA",
    "cf_ivo": "CLINICA DA FAMILIA IVO MANOEL LOPES",
    "cf_jaceruba": "CLÍNICA DA FAMÍLIA JACERUBA",
    "cf_palmares": "CLÍNICA DA FAMÍLIA JARDIM  PALMARES",
    "cf_viga": "CLÍNICA DA FAMÍLIA JARDIM DA VIGA",
    "cf_iguacu": "CLÍNICA DA FAMÍLIA JARDIM IGUAÇU",
    "cf_jasmim": "CLÍNICA DA FAMÍLIA JARDIM JASMIM",
    "cf_roma": "CLÍNICA DA FAMÍLIA JARDIM ROMA",
    "cf_caicara": "CLÍNICA DA FAMÍLIA JOSÉ RODRIGUES DA SILVA (CAIÇARA)",
    "cf_km32": "CLÍNICA DA FAMÍLIA KM32",
    "cf_lagoinha": "CLÍNICA DA FAMÍLIA LAGOINHA",
    "cf_tingua": "CLÍNICA DA FAMÍLIA MANOEL MOREIRA DE OLIVEIRA (TINGUÁ)",
    "cf_marfel": "CLÍNICA DA FAMÍLIA MARFEL",
    "cf_boaesperanca": "CLÍNICA DA FAMÍLIA MARIA UMBELINA (BOA ESPERANÇA)",
    "cf_geneciano": "CLÍNICA DA FAMÍLIA NÁDIA SILVA DE OLIVEIRA (GENECIANO)",
    "cf_novaera": "CLÍNICA DA FAMILIA NOVA ERA",
    "cf_odiceia": "CLINICA DA FAMÍLIA ODICEIA MORAES",
    "cf_palmeiras": "CLÍNICA DA FAMÍLIA PARQUE DAS PALMEIRAS",
    "cf_novaamerica": "CLÍNICA DA FAMÍLIA PASTOR IRACY MARCELINO (NOVA AMÉRICA)",
    "cf_grama": "CLÍNICA DA FAMÍLIA PEDRO ARUME (GRAMA)",
    "cf_riodouro": "CLÍNICA DA FAMÍLIA RIO D'OURO",
    "cf_vilaoperaria": "CLÍNICA DA FAMÍLIA VILA OPERÁRIA",
    "cnr_odiceia": "CONSULTORIO NA RUA DA CLINICA ODICEIA MORAES",
    "hgni_pep": "HOSPITAL GERAL DE NOVA IGUAÇU (HGNI) - PEP",
    "mat_mariana": "MATERNIDADE MARIANA BULHÕES",
    "poli_santarita": "POLICLÍNICA  SANTA RITA",
    "poli_dirceu": "POLICLÍNICA DIRCEU DE AQUINO RAMOS",
    "poli_domwalmor": "POLICLÍNICA GERAL DE NOVA IGUAÇU (DOM WALMOR)",
    "poli_cabucu": "POLICLÍNICA MANOEL B. DE ALMEIDA (CABUÇU)",
    "super_dacyr": "SUPERCLÍNICA DA FAMÍLIA DACYR SOARES - MORRO AGUDO",
    "ubs_moqueta": "UBS ALBERTO SOBRAL (MOQUETÁ)",
    "ubs_austin": "UBS AUSTIN",
    "ubs_ceramica": "UBS CERÂMICA",
    "ubs_cobrex": "UBS COBREX",
    "ubs_paraiso": "UBS JARDIM PARAÍSO (Antiga Patrícia Marinho)",
    "ubs_santaeugenia": "UBS JARDIM SANTA EUGÊNIA",
    "ubs_julia": "UBS JÚLIA TÁVORA",
    "ubs_manoel": "UBS MANOEL REZENDE",
    "ubs_montelibano": "UBS MONTE LÍBANO (PROF° RUTILHES DOS SANTOS)",
    "ubs_novabrasilia": "UBS NOVA BRASÍLIA",
    "ubs_prata": "UBS PRATA",
    "ubs_ranchofundo": "UBS RANCHO FUNDO",
    "ubs_santaclara": "UBS SANTA CLARA DE VILA NOVA",
    "ubs_vilajurema": "UBS VILA JUREMA",
    "uni_pedreira": "UNIDADE SHOPPING DA PEDREIRA",
    "usf_engenho": "USF ENGENHO Pequeno",
    "usf_lino": "USF LINO VILELA",
    "usf_k11": "USF PADRE MANOEL MONTEIRO (K11)",
    "usf_palhada": "USF PALHADA",
    "usf_todos": "USF PARQUE TODOS OS SANTOS",
    "usf_rodilandia": "USF RODILÂNDIA",
    "usf_guandu": "USF SANTA CLARA DO GUANDÚ",
    "usf_valverde": "USF VALVERDE",
    "usf_vilatania": "USF VILA TÂNIA"
}

# =====================================================================
# 2. MOTOR DE BUSCA
# =====================================================================
@st.cache_data(ttl=60)
def carregar_todos_os_dados():
    # IDs DA PLANILHA (Verifique se estão corretos)
    SHEET_ID = "1A6uPoNNsz-5SzDRvZZfurYxt7NOzv73Dtde-GEsoV6o" 
    GID_PACIENTES = "0"
    GID_EVO = "355108392" # <-- COLOQUE O SEU GID AQUI!
    
    url_pacientes = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv&gid={GID_PACIENTES}"
    url_evolucoes = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv&gid={GID_EVO}"
    
    df_pac = pd.read_csv(url_pacientes)
    df_evo = pd.read_csv(url_evolucoes)
    
    df_pac.columns = df_pac.columns.str.strip()
    df_evo.columns = df_evo.columns.str.strip()
    
    # Criar ID limpo para cruzamento (apenas números do CNS/CPF)
    col_id_pac = [c for c in df_pac.columns if "CNS" in c or "CPF" in c][0]
    df_pac["_id_limpo"] = df_pac[col_id_pac].astype(str).str.replace(r'\D', '', regex=True)
    
    col_id_evo = [c for c in df_evo.columns if "CNS" in c or "CPF" in c][0]
    df_evo["_id_limpo"] = df_evo[col_id_evo].astype(str).str.replace(r'\D', '', regex=True)
    
    return df_pac, df_evo

# =====================================================================
# 3. TELA DE LOGIN
# =====================================================================
if "unidade_logada" not in st.session_state:
    st.session_state["unidade_logada"] = None

if st.session_state["unidade_logada"] is None:
    st.title("🔒 Acesso Restrito - Monitoramento ILTB")
    senha = st.text_input("Digite sua senha de acesso:", type="password")
    if st.button("Entrar no Sistema"):
        if senha in COFRE_DE_ACESSOS:
            st.session_state["unidade_logada"] = COFRE_DE_ACESSOS[senha]
            st.rerun()
        else:
            st.error("❌ Senha inválida.")

# =====================================================================
# 4. PAINEL DE CONTROLE
# =====================================================================
else:
    unidade = st.session_state["unidade_logada"]
    
    st.title("🏥 Gestão Municipal de Prontuários ILTB")
    st.subheader(f"Perfil: {unidade}")
    
    if st.sidebar.button("Sair / Logout"):
        st.session_state["unidade_logada"] = None
        st.rerun()

    try:
        df_pacientes, df_evolucoes = carregar_todos_os_dados()
        
        # Filtro por unidade (se não for admin)
        if unidade != "TODAS":
            df_pacientes = df_pacientes[df_pacientes["Unidade de Tratamento"] == unidade]

        # --- FILTROS SUPERIORES ---
        st.write("### 🔎 Filtros de Auditoria")
        cf1, cf2 = st.columns(2)
        opcoes_sit = ["Todas"] + sorted(df_pacientes["Situação"].unique().tolist())
        filtro_sit = cf1.selectbox("Situação do Tratamento:", opcoes_sit)
        
        df_filtrado = df_pacientes.copy()
        if filtro_sit != "Todas":
            df_filtrado = df_filtrado[df_filtrado["Situação"] == filtro_sit]

        # --- ABAS ---
        aba1, aba2, aba3 = st.tabs(["📋 Lista Geral", "🔍 Prontuário Detalhado", "📑 Auditoria Geral"])

        with aba1:
            st.metric("Pacientes no Filtro", len(df_filtrado))
            colunas_ver = ["Data Notificação", "Unidade de Tratamento", "Nome do Paciente", "CNS", "Esquema TPT", "Situação"]
            st.dataframe(df_filtrado[colunas_ver], use_container_width=True, hide_index=True)

        with aba2:
            st.write("### Pesquisa Individual")
            df_filtrado["Busca"] = df_filtrado["Nome do Paciente"] + " | " + df_filtrado["CNS"].astype(str)
            pac_sel = st.selectbox("Selecione o Paciente:", ["-- Selecione --"] + list(df_filtrado["Busca"].unique()))

            if pac_sel != "-- Selecione --":
                id_limpo_busca = "".join(filter(str.isdigit, pac_sel.split("|")[1]))
                
                # --- NOVIDADE: CABEÇALHO COM UNIDADE ---
                info_pac = df_pacientes[df_pacientes["_id_limpo"] == id_limpo_busca].iloc[0]
                
                st.info(f"📍 **Unidade de Notificação:** {info_pac['Unidade de Tratamento']}")
                
                c_a, c_b, c_c = st.columns(3)
                c_a.write(f"**Paciente:** {info_pac['Nome do Paciente']}")
                c_b.write(f"**Data de Início:** {info_pac['Data Notificação']}")
                c_c.write(f"**Status Atual:** {info_pac['Situação']}")
                
                st.write("---")
                # Evoluções
                evos = df_evolucoes[df_evolucoes["_id_limpo"] == id_limpo_busca]
                if evos.empty:
                    st.warning("Sem evoluções registradas.")
                else:
                    for _, row in evos.sort_values(by=evos.columns[0], ascending=False).iterrows():
                        with st.expander(f"🔹 {row.get('Data da Evolução', 'S/D')} - {row.get('Tipo/Mês', 'Evolução')}"):
                            st.write(f"**Relato:** {row.get('Relato Clínico', '-')}")
                            st.info(f"**Conduta:** {row.get('Conduta', '-')}")

        with aba3:
            st.write("### Relatório Cruzado de Evoluções")
            # Une Pacientes com Evoluções para auditoria completa
            df_audit = pd.merge(
                df_filtrado[["_id_limpo", "Nome do Paciente", "Unidade de Tratamento"]],
                df_evolucoes,
                on="_id_limpo",
                how="inner"
            )
            st.dataframe(df_audit.drop(columns=["_id_limpo"]), use_container_width=True, hide_index=True)

    except Exception as e:
        st.error(f"Erro ao carregar dados: {e}")
