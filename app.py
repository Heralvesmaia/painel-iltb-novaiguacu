import streamlit as st
import pandas as pd

# =====================================================================
# 1. CONFIGURAÇÃO DA PÁGINA E COFRE DE SENHAS
# =====================================================================
st.set_page_config(page_title="Painel ILTB - Nova Iguaçu", page_icon="🏥", layout="wide")

COFRE_DE_ACESSOS = {
    "heraldo_admin": "TODAS",
    "ist_hgni": "AMBULATORIO DE IST DO HGNI",
    "cav_mulher": "CENTRO DE APOIO E VALORIZAÇÃO DA MULHER (CAV MULHER)",
    "cta_vasco": "CENTRO DE SAÚDE VASCO BARCELOS - CTA",
    "hgni_pep": "HOSPITAL GERAL DE NOVA IGUAÇU (HGNI) - PEP",
    "mat_mariana": "MATERNIDADE MARIANA BULHÕES",
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
    "usf_engenho": "USF ENGENHO PEQUENO",
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
    # === ATENÇÃO: COLOQUE SEUS IDs AQUI ===
    SHEET_ID = "1A6uPoNNsz-5SzDRvZZfurYxt7NOzv73Dtde-GEsoV6o" 
    GID_PACIENTES = "0"
    GID_EVO = "355108392" 
    
    url_pacientes = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv&gid={GID_PACIENTES}"
    url_evolucoes = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv&gid={GID_EVO}"
    
    df_pac = pd.read_csv(url_pacientes)
    df_evo = pd.read_csv(url_evolucoes)
    
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
    st.write("Digite a senha fornecida pela Coordenação para acessar os prontuários da sua Unidade.")
    
    senha_digitada = st.text_input("Senha de Acesso", type="password")
    
    if st.button("Entrar no Sistema"):
        if senha_digitada in COFRE_DE_ACESSOS:
            st.session_state["unidade_logada"] = COFRE_DE_ACESSOS[senha_digitada]
            st.rerun()
        else:
            st.error("❌ Senha incorreta ou Unidade não encontrada.")

# =====================================================================
# 4. PAINEL PRINCIPAL E AUDITORIA
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
        with st.spinner('Puxando prontuários e cruzando dados da Nuvem...'):
            df_pacientes, df_evolucoes = carregar_todos_os_dados()
        
        # Filtro de Segurança da Unidade
        if unidade != "TODAS":
            df_pacientes = df_pacientes[df_pacientes["Unidade de Tratamento"] == unidade]
            
        if df_pacientes.empty:
            st.warning("Nenhum paciente registrado para esta unidade até o momento.")
        else:
            # --- TELA DE FILTROS (NOVIDADE) ---
            st.write("### 🔎 Filtros de Busca e Auditoria")
            cf1, cf2 = st.columns(2)

            opcoes_sit = ["Todas as Situações"] + sorted(df_pacientes["Situação"].dropna().unique().tolist())
            filtro_situacao = cf1.selectbox("Filtrar por Status do Tratamento:", opcoes_sit)

            filtro_unidade = "Todas as Unidades"
            if unidade == "TODAS":
                opcoes_uni = ["Todas as Unidades"] + sorted(df_pacientes["Unidade de Tratamento"].dropna().unique().tolist())
                filtro_unidade = cf2.selectbox("Auditar Unidade Específica:", opcoes_uni)

            # Aplicando os filtros dinâmicos
            df_filtrado = df_pacientes.copy()
            if filtro_situacao != "Todas as Situações":
                df_filtrado = df_filtrado[df_filtrado["Situação"] == filtro_situacao]
            if filtro_unidade != "Todas as Unidades":
                df_filtrado = df_filtrado[df_filtrado["Unidade de Tratamento"] == filtro_unidade]

            # --- SEÇÃO 1: MÉTRICAS (Agora são dinâmicas baseadas no filtro) ---
            st.write("---")
            c1, c2, c3, c4 = st.columns(4)
            c1.metric("Total de Pacientes (Filtro)", len(df_filtrado))
            c2.metric("🟢 Em Andamento", len(df_filtrado[df_filtrado["Situação"] == "Em andamento"]))
            c3.metric("🔵 Altas", len(df_filtrado[df_filtrado["Situação"] == "Tratamento Completo"]))
            c4.metric("🔴 Interrupções", len(df_filtrado[df_filtrado["Situação"] == "Interrupção do tratamento"]))

            st.write("---")

            # --- SISTEMA DE ABAS (TABS) ---
            aba1, aba2, aba3 = st.tabs(["📋 1. Lista Geral", "🔍 2. Prontuário Individual", "📑 3. Auditoria de Evoluções"])

            with aba1:
                st.write("*(Dica: Clique no título das colunas para ordenar alfabeticamente ou por data).*")
                # Adicionada a coluna "Unidade de Tratamento" na visualização geral
                colunas_mostrar = ["Data Notificação", "Unidade de Tratamento", "Nome do Paciente", "CNS", "Esquema TPT", "Situação"]
                
                # Para evitar erro se a coluna não existir perfeitamente
                colunas_mostrar = [c for c in colunas_mostrar if c in df_filtrado.columns]
                
                st.dataframe(df_filtrado[colunas_mostrar], use_container_width=True, hide_index=True)

            with aba2:
                st.write("Selecione um paciente para ver a linha do tempo organizada das consultas dele.")
                df_filtrado["Busca"] = df_filtrado["Nome do Paciente"] + " | " + df_filtrado["CNS"].astype(str)
                pac_sel = st.selectbox("Buscar Paciente:", ["-- Selecione --"] + list(df_filtrado["Busca"].unique()))

                if pac_sel != "-- Selecione --":
                    id_busca = pac_sel.split("|")[1].strip()
                    col_id_evo = [c for c in df_evolucoes.columns if "CNS" in c or "CPF" in c][0]
                    df_evolucoes["_id_limpo"] = df_evolucoes[col_id_evo].astype(str).str.replace(r'\D', '', regex=True)
                    id_busca_limpo = "".join(filter(str.isdigit, id_busca))
                    
                    evo_pac = df_evolucoes[df_evolucoes["_id_limpo"] == id_busca_limpo]
                    
                    if evo_pac.empty:
                        st.info("Nenhuma evolução registrada para este paciente.")
                    else:
                        evo_pac = evo_pac.sort_values(by=evo_pac.columns[0], ascending=False)
                        for _, row in evo_pac.iterrows():
                            with st.expander(f"🔹 {row.get('Data da Evolução', '-')} - {row.get('Tipo/Mês', '-')} ({row.get('Situação', '-')})"):
                                st.write(f"**Relato Clínico:** {row.get('Relato Clínico', '-')}")
                                st.info(f"**Conduta:** {row.get('Conduta', '-')}")

            with aba3:
                st.write("### 📑 Relatório Completo de Acompanhamento")
                st.write("Esta tabela cruza os pacientes filtrados acima com **todas as evoluções clínicas** registradas no banco. Ideal para auditoria de andamento e interrupções.")
                
                # Encontrar ID limpo dos pacientes filtrados
                col_id_pac = [c for c in df_filtrado.columns if "CNS" in c or "CPF" in c][0]
                df_filtrado["_id_limpo"] = df_filtrado[col_id_pac].astype(str).str.replace(r'\D', '', regex=True)
                
                # Encontrar ID limpo das evoluções
                col_id_evo = [c for c in df_evolucoes.columns if "CNS" in c or "CPF" in c][0]
                df_evolucoes["_id_limpo"] = df_evolucoes[col_id_evo].astype(str).str.replace(r'\D', '', regex=True)
                
                # Cruzar as duas planilhas usando o ID Limpo
                df_auditoria = pd.merge(
                    df_filtrado[["_id_limpo", "Nome do Paciente", "Unidade de Tratamento"]],
                    df_evolucoes,
                    on="_id_limpo",
                    how="inner"
                )
                
                if df_auditoria.empty:
                    st.info("Não há evoluções clínicas para os pacientes no filtro atual.")
                else:
                    # Organizar as colunas finais do Relatório de Auditoria
                    colunas_audit = [
                        "Unidade de Tratamento", "Nome do Paciente", "Data da Evolução", 
                        "Tipo/Mês", "Situação", "Relato Clínico", "Conduta"
                    ]
                    colunas_audit = [c for c in colunas_audit if c in df_auditoria.columns]
                    
                    # Ordenar por unidade, nome e data
                    df_auditoria = df_auditoria.sort_values(by=["Unidade de Tratamento", "Nome do Paciente"])
                    
                    st.dataframe(df_auditoria[colunas_audit], use_container_width=True, hide_index=True)

    except Exception as e:
        st.error(f"Erro no processamento dos dados. Detalhe técnico: {e}")
