import streamlit as st
import pandas as pd

# =====================================================================
# 1. CONFIGURAÇÃO DA PÁGINA E COFRE DE SENHAS
# =====================================================================
st.set_page_config(page_title="Painel ILTB - Nova Iguaçu", page_icon="🏥", layout="wide")

COFRE_DE_ACESSOS = {
    # ACESSO MESTRE DA COORDENAÇÃO
    "heraldo_admin": "TODAS",
    
    # HOSPITAIS, MATERNIDADES E CENTROS
    "ist_hgni": "AMBULATORIO DE IST DO HGNI",
    "cav_mulher": "CENTRO DE APOIO E VALORIZAÇÃO DA MULHER (CAV MULHER)",
    "cta_vasco": "CENTRO DE SAÚDE VASCO BARCELOS - CTA",
    "hgni_pep": "HOSPITAL GERAL DE NOVA IGUAÇU (HGNI) - PEP",
    "mat_mariana": "MATERNIDADE MARIANA BULHÕES",
    
    # CLÍNICAS DA FAMÍLIA (CF) E 24H
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
    
    # POLICLÍNICAS E SUPERCLÍNICAS
    "poli_santarita": "POLICLÍNICA  SANTA RITA",
    "poli_dirceu": "POLICLÍNICA DIRCEU DE AQUINO RAMOS",
    "poli_domwalmor": "POLICLÍNICA GERAL DE NOVA IGUAÇU (DOM WALMOR)",
    "poli_cabucu": "POLICLÍNICA MANOEL B. DE ALMEIDA (CABUÇU)",
    "super_dacyr": "SUPERCLÍNICA DA FAMÍLIA DACYR SOARES - MORRO AGUDO",
    
    # UNIDADES BÁSICAS DE SAÚDE (UBS)
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
    
    # UNIDADES DE SAÚDE DA FAMÍLIA (USF)
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
# 2. MOTOR DE BUSCA (RESILIENTE)
# =====================================================================
@st.cache_data(ttl=60)
def carregar_todos_os_dados():
    # =================================================================
    # ATENÇÃO HERALDO: COLOQUE SEUS IDs REAIS AQUI ANTES DE SALVAR!
    # =================================================================
    SHEET_ID = "1A6uPoNNsz-5SzDRvZZfurYxt7NOzv73Dtde-GEsoV6o" 
    GID_PACIENTES = "0"
    GID_EVO = "355108392"
    
    url_pacientes = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv&gid={GID_PACIENTES}"
    url_evolucoes = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv&gid={GID_EVO}"
    
    df_pac = pd.read_csv(url_pacientes)
    df_evo = pd.read_csv(url_evolucoes)
    
    # Limpa espaços em branco nos nomes das colunas para evitar erros
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
    st.write("Digite a senha fornecida pela Coordenação de Vigilância para acessar os prontuários da sua Unidade.")
    
    senha_digitada = st.text_input("Senha de Acesso", type="password")
    
    if st.button("Entrar no Sistema"):
        if senha_digitada in COFRE_DE_ACESSOS:
            st.session_state["unidade_logada"] = COFRE_DE_ACESSOS[senha_digitada]
            st.rerun()
        else:
            st.error("❌ Senha incorreta ou Unidade não encontrada.")

# =====================================================================
# 4. PAINEL PRINCIPAL
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
            df_pacientes, df_evolucoes = carregar_todos_os_dados()
        
        # Filtro de Unidade
        if unidade != "TODAS":
            df_pacientes = df_pacientes[df_pacientes["Unidade de Tratamento"] == unidade]
            
        if df_pacientes.empty:
            st.warning("Nenhum paciente registrado para esta unidade até o momento.")
        else:
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
                id_busca = paciente_selecionado.split("|")[1].strip()
                
                # Identifica coluna de ID automaticamente
                col_id_evo = [c for c in df_evolucoes.columns if "CNS" in c or "CPF" in c][0]
                
                # Filtra evoluções por número limpo (apenas dígitos)
                df_evolucoes[col_id_evo] = df_evolucoes[col_id_evo].astype(str).str.replace(r'\D', '', regex=True)
                id_busca_limpo = "".join(filter(str.isdigit, id_busca))
                
                evolucoes_pac = df_evolucoes[df_evolucoes[col_id_evo] == id_busca_limpo]
                
                if evolucoes_pac.empty:
                    st.info("Nenhuma evolução clínica registrada além do cadastro inicial.")
                else:
                    st.write(f"#### 📅 Linha do Tempo: {paciente_selecionado.split('|')[0].strip()}")
                    
                    evolucoes_pac = evolucoes_pac.sort_values(by=evolucoes_pac.columns[0], ascending=False)
                    
                    for _, row in evolucoes_pac.iterrows():
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
            st.write("*(Modo de Leitura: Você pode pesquisar e clicar nas colunas para ordenar).*")
            
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
