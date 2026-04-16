import streamlit as st
import pandas as pd
import time
import unicodedata
import re

# 1. CONFIGURAÇÃO DA PÁGINA
st.set_page_config(page_title="SIG-ILTB - Prontuário Eletrônico", layout="wide", page_icon="🔒")

# 2. FUNÇÕES DE LIMPEZA E BLINDAGEM DE DADOS
def normalizar_texto(texto):
    if pd.isna(texto): return ""
    texto = str(texto).strip().lower()
    return ''.join(c for c in unicodedata.normalize('NFD', texto) if unicodedata.category(c) != 'Mn')

def limpar_id(valor):
    """Remove .0, pontos, traços e espaços para garantir que os IDs dão 100% de 'Match'"""
    if pd.isna(valor): return ""
    val_str = str(valor).strip()
    if val_str.endswith('.0'):
        val_str = val_str[:-2]
    return re.sub(r'[^a-zA-Z0-9]', '', val_str).upper()

# 3. CENTRAL DE ACESSOS
USUARIOS = {
    "heraldo_admin": {"senha": "admin123", "nome_oficial": "TODAS"},
    "ist_hgni": {"senha": "ist_hgni", "nome_oficial": "AMBULATORIO DE IST DO HGNI"},
    "cav_mulher": {"senha": "cav_mulher", "nome_oficial": "CENTRO DE APOIO E VALORIZAÇÃO DA MULHER (CAV MULHER)"},
    "cta_vasco": {"senha": "cta_vasco", "nome_oficial": "CENTRO DE SAÚDE VASCO BARCELOS - CTA"},
    "hgni_pep": {"senha": "hgni_pep", "nome_oficial": "HOSPITAL GERAL DE NOVA IGUAÇU (HGNI) - PEP"},
    "mat_mariana": {"senha": "mat_mariana", "nome_oficial": "MATERNIDADE MARIANA BULHÕES"},
    "cf_carlinhos": {"senha": "cf_carlinhos", "nome_oficial": "CLÍNICA DA FAMÍLIA 24h CARLINHOS DA TINGUÁ (MIGUEL COUTO)"},
    "cf_gisele": {"senha": "cf_gisele", "nome_oficial": "CLÍNICA DA FAMÍLIA 24h GISELE PALHARES (VILA DE CAVA)"},
    "cf_adrianopolis": {"senha": "cf_adrianopolis", "nome_oficial": "CLÍNICA DA FAMÍLIA ADRIANÓPOLIS"},
    "cf_alianca": {"senha": "cf_alianca", "nome_oficial": "CLÍNICA DA FAMÍLIA ALIANÇA"},
    "cf_corumba": {"senha": "cf_corumba", "nome_oficial": "CLÍNICA DA FAMÍLIA CORUMBÁ"},
    "cf_ceramica": {"senha": "cf_ceramica", "nome_oficial": "CLÍNICA DA FAMÍLIA DA CERÂMICA"},
    "cf_dombosco": {"senha": "cf_dombosco", "nome_oficial": "CLÍNICA DA FAMÍLIA DOM BOSCO"},
    "cf_ambai": {"senha": "cf_ambai", "nome_oficial": "CLÍNICA DA FAMÍLIA DR MARCO POLO DE GOUVEIA PEREIRA (AMBAÍ)"},
    "cf_delmo": {"senha": "cf_delmo", "nome_oficial": "CLINICA DA FAMILIA Dr. DELMO MOURA SA"},
    "cf_emilia": {"senha": "cf_emilia", "nome_oficial": "CLÍNICA DA FAMÍLIA EMILIA GOMES - CTA"},
    "cf_cacuia": {"senha": "cf_cacuia", "nome_oficial": "CLÍNICA DA FAMÍLIA ERALDO SARDINHA (CACUIA)"},
    "cf_figueira": {"senha": "cf_figueira", "nome_oficial": "CLÍNICA DA FAMÍLIA FIGUEIRA"},
    "cf_ivo": {"senha": "cf_ivo", "nome_oficial": "CLINICA DA FAMILIA IVO MANOEL LOPES"},
    "cf_jaceruba": {"senha": "cf_jaceruba", "nome_oficial": "CLÍNICA DA FAMÍLIA JACERUBA"},
    "cf_palmares": {"senha": "cf_palmares", "nome_oficial": "CLÍNICA DA FAMÍLIA JARDIM  PALMARES"},
    "cf_viga": {"senha": "cf_viga", "nome_oficial": "CLÍNICA DA FAMÍLIA JARDIM DA VIGA"},
    "cf_iguacu": {"senha": "cf_iguacu", "nome_oficial": "CLÍNICA DA FAMÍLIA JARDIM IGUAÇU"},
    "cf_jasmim": {"senha": "cf_jasmim", "nome_oficial": "CLÍNICA DA FAMÍLIA JARDIM JASMIM"},
    "cf_roma": {"senha": "cf_roma", "nome_oficial": "CLÍNICA DA FAMÍLIA JARDIM ROMA"},
    "cf_caicara": {"senha": "cf_caicara", "nome_oficial": "CLÍNICA DA FAMÍLIA JOSÉ RODRIGUES DA SILVA (CAIÇARA)"},
    "cf_km32": {"senha": "cf_km32", "nome_oficial": "CLÍNICA DA FAMÍLIA KM32"},
    "cf_lagoinha": {"senha": "cf_lagoinha", "nome_oficial": "CLÍNICA DA FAMÍLIA LAGOINHA"},
    "cf_tingua": {"senha": "cf_tingua", "nome_oficial": "CLÍNICA DA FAMÍLIA MANOEL MOREIRA DE OLIVEIRA (TINGUÁ)"},
    "cf_marfel": {"senha": "cf_marfel", "nome_oficial": "CLÍNICA DA FAMÍLIA MARFEL"},
    "cf_boaesperanca": {"senha": "cf_boaesperanca", "nome_oficial": "CLÍNICA DA FAMÍLIA MARIA UMBELINA (BOA ESPERANÇA)"},
    "cf_geneciano": {"senha": "cf_geneciano", "nome_oficial": "CLÍNICA DA FAMÍLIA NÁDIA SILVA DE OLIVEIRA (GENECIANO)"},
    "cf_novaera": {"senha": "cf_novaera", "nome_oficial": "CLÍNICA DA FAMILIA NOVA ERA"},
    "cf_odiceia": {"senha": "cf_odiceia", "nome_oficial": "CLINICA DA FAMÍLIA ODICEIA MORAES"},
    "cf_palmeiras": {"senha": "cf_palmeiras", "nome_oficial": "CLÍNICA DA FAMÍLIA PARQUE DAS PALMEIRAS"},
    "cf_novaamerica": {"senha": "cf_novaamerica", "nome_oficial": "CLÍNICA DA FAMÍLIA PASTOR IRACY MARCELINO (NOVA AMÉRICA)"},
    "cf_grama": {"senha": "cf_grama", "nome_oficial": "CLÍNICA DA FAMÍLIA PEDRO ARUME (GRAMA)"},
    "cf_riodouro": {"senha": "cf_riodouro", "nome_oficial": "CLÍNICA DA FAMÍLIA RIO D'OURO"},
    "cf_vilaoperaria": {"senha": "cf_vilaoperaria", "nome_oficial": "CLÍNICA DA FAMÍLIA VILA OPERÁRIA"},
    "cnr_odiceia": {"senha": "cnr_odiceia", "nome_oficial": "CONSULTORIO NA RUA DA CLINICA ODICEIA MORAES"},
    "poli_santarita": {"senha": "poli_santarita", "nome_oficial": "POLICLÍNICA  SANTA RITA"},
    "poli_dirceu": {"senha": "poli_dirceu", "nome_oficial": "POLICLÍNICA DIRCEU DE AQUINO RAMOS"},
    "poli_domwalmor": {"senha": "poli_domwalmor", "nome_oficial": "POLICLÍNICA GERAL DE NOVA IGUAÇU (DOM WALMOR)"},
    "poli_cabucu": {"senha": "poli_cabucu", "nome_oficial": "POLICLÍNICA MANOEL B. DE ALMEIDA (CABUÇU)"},
    "super_dacyr": {"senha": "super_dacyr", "nome_oficial": "SUPERCLÍNICA DA FAMÍLIA DACYR SOARES - MORRO AGUDO"},
    "ubs_moqueta": {"senha": "ubs_moqueta", "nome_oficial": "UBS ALBERTO SOBRAL (MOQUETÁ)"},
    "ubs_austin": {"senha": "ubs_austin", "nome_oficial": "UBS AUSTIN"},
    "ubs_ceramica": {"senha": "ubs_ceramica", "nome_oficial": "UBS CERÂMICA"},
    "ubs_cobrex": {"senha": "ubs_cobrex", "nome_oficial": "UBS COBREX"},
    "ubs_paraiso": {"senha": "ubs_paraiso", "nome_oficial": "UBS JARDIM PARAÍSO (Antiga Patrícia Marinho)"},
    "ubs_santaeugenia": {"senha": "ubs_santaeugenia", "nome_oficial": "UBS JARDIM SANTA EUGÊNIA"},
    "ubs_julia": {"senha": "ubs_julia", "nome_oficial": "UBS JÚLIA TÁVORA"},
    "ubs_manoel": {"senha": "ubs_manoel", "nome_oficial": "UBS MANOEL REZENDE"},
    "ubs_montelibano": {"senha": "ubs_montelibano", "nome_oficial": "UBS MONTE LÍBANO (PROF° RUTILHES DOS SANTOS)"},
    "ubs_novabrasilia": {"senha": "ubs_novabrasilia", "nome_oficial": "UBS NOVA BRASÍLIA"},
    "ubs_prata": {"senha": "ubs_prata", "nome_oficial": "UBS PRATA"},
    "ubs_ranchofundo": {"senha": "ubs_ranchofundo", "nome_oficial": "UBS RANCHO FUNDO"},
    "ubs_santaclara": {"senha": "ubs_santaclara", "nome_oficial": "UBS SANTA CLARA DE VILA NOVA"},
    "ubs_vilajurema": {"senha": "ubs_vilajurema", "nome_oficial": "UBS VILA JUREMA"},
    "uni_pedreira": {"senha": "uni_pedreira", "nome_oficial": "UNIDADE SHOPPING DA PEDREIRA"},
    "usf_engenho": {"senha": "usf_engenho", "nome_oficial": "USF ENGENHO PEQUENO"},
    "usf_lino": {"senha": "usf_lino", "nome_oficial": "USF LINO VILELA"},
    "usf_k11": {"senha": "usf_k11", "nome_oficial": "USF PADRE MANOEL MONTEIRO (K11)"},
    "usf_palhada": {"senha": "usf_palhada", "nome_oficial": "USF PALHADA"},
    "usf_todos": {"senha": "usf_todos", "nome_oficial": "USF PARQUE TODOS OS SANTOS"},
    "usf_rodilandia": {"senha": "usf_rodilandia", "nome_oficial": "USF RODILÂNDIA"},
    "usf_guandu": {"senha": "usf_guandu", "nome_oficial": "USF SANTA CLARA DO GUANDÚ"},
    "usf_valverde": {"senha": "usf_valverde", "nome_oficial": "USF VALVERDE"},
    "usf_vilatania": {"senha": "usf_vilatania", "nome_oficial": "USF VILA TÂNIA"}
}

# 4. FUNÇÃO DE LOGIN
def tela_login():
    if "autenticado" not in st.session_state:
        st.session_state["autenticado"] = False

    if not st.session_state["autenticado"]:
        st.markdown("<h1 style='text-align: center;'>🔐 Sistema SIG-ILTB</h1>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center;'>Introduza as suas credenciais para aceder ao painel</p>", unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            with st.form("login"):
                usuario = st.text_input("Utilizador (Login da Unidade ou Admin)").lower().strip()
                senha = st.text_input("Senha", type="password").strip()
                botao_entrar = st.form_submit_button("Entrar no Sistema")
                
                if botao_entrar:
                    if usuario in USUARIOS and USUARIOS[usuario]["senha"] == senha:
                        st.session_state["autenticado"] = True
                        st.session_state["usuario_atual"] = usuario
                        st.success("Acesso autorizado! A carregar...")
                        time.sleep(1)
                        st.rerun()
                    else:
                        st.error("Utilizador ou senha incorretos.")
        return False
    return True

# 5. PAINEL PRINCIPAL
if tela_login():
    st.markdown("""<style>.main { background-color: #f4f6f9; }</style>""", unsafe_allow_html=True)

    nome_unidade_atual = USUARIOS[st.session_state['usuario_atual']]["nome_oficial"]
    st.title("🏥 Prontuário Digital SIG-ILTB")
    st.caption(f"Unidade Ativa: {nome_unidade_atual}" if st.session_state['usuario_atual'] != 'heraldo_admin' else "Visão Geral - Administração Central")

    SHEET_ID = "1cG2uey69Vb2nnu_n-m5VTEwKuAnvCs2OkaQIvN7Izs8"
    LINK_FORM_EVOLUCAO = "https://docs.google.com/forms/d/e/COLE_SEU_LINK_AQUI/viewform"

    with st.sidebar:
        st.image("https://cdn-icons-png.flaticon.com/512/1085/1085810.png", width=80)
        st.markdown(f"**Logado como:** {st.session_state['usuario_atual']}")
        if st.button('🔄 ATUALIZAR DADOS', use_container_width=True):
            st.cache_data.clear()
            st.rerun()
        if st.button('🚪 SAIR DO SISTEMA', use_container_width=True):
            st.session_state["autenticado"] = False
            st.rerun()

    @st.cache_data(ttl=15)
    def carregar_dados_oficiais():
        try:
            agora = int(time.time())
            url_p = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&sheet=Pacientes&nocache={agora}"
            url_e = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&sheet=Evolucoes&nocache={agora}"
            
            # Força o sistema a ler tudo como texto bruto
            df_p = pd.read_csv(url_p, on_bad_lines='skip', dtype=str).fillna("")
            df_e = pd.read_csv(url_e, on_bad_lines='skip', dtype=str).fillna("")
            return df_p, df_e
        except Exception as e:
            st.error(f"Erro na ligação: {e}")
            return None, None

    df_pacientes, df_evolucoes = carregar_dados_oficiais()

    if df_pacientes is not None and not df_pacientes.empty:
        
        # Filtro de Unidade dinâmico
        if st.session_state['usuario_atual'] != 'heraldo_admin':
            col_unidade = next((col for col in df_pacientes.columns if 'unidade' in normalizar_texto(col) or 'local' in normalizar_texto(col)), None)
            if col_unidade:
                df_pacientes = df_pacientes[df_pacientes[col_unidade].astype(str).str.contains(nome_unidade_atual, case=False, na=False)]

        tab_prontuario, tab_pacientes, tab_evolucoes = st.tabs(["🩺 Prontuário Longitudinal", "📋 Lista de Pacientes", "📈 Base Global"])
        
        with tab_prontuario:
            st.markdown("### 🔍 Busca de Prontuário")
            
            # Localiza a coluna de nome dinamicamente
            col_nome_p = next((c for c in df_pacientes.columns if 'nome' in normalizar_texto(c) or 'paciente' in normalizar_texto(c)), None)
            
            if col_nome_p:
                nomes_validos = df_pacientes[df_pacientes[col_nome_p] != ""][col_nome_p].astype(str).unique()
                lista_pacientes = ["Selecione um paciente..."] + sorted(nomes_validos.tolist())
                
                paciente_selecionado = st.selectbox("Busque o paciente:", lista_pacientes, label_visibility="collapsed")

                if paciente_selecionado != "Selecione um paciente...":
                    d_pac = df_pacientes[df_pacientes[col_nome_p] == paciente_selecionado].iloc[0]
                    
                    # --- EXTRAÇÃO DINÂMICA DE COLUNAS DA ABA 1 ---
                    col_id_p = next((c for c in df_pacientes.columns if any(x in normalizar_texto(c) for x in ['cns', 'cpf', 'id'])), None)
                    col_sit_p = next((c for c in df_pacientes.columns if any(x in normalizar_texto(c) for x in ['situacao', 'status', 'atual'])), None)
                    col_ini_p = next((c for c in df_pacientes.columns if any(x in normalizar_texto(c) for x in ['inicio', 'tpt'])), None)
                    col_med_p = next((c for c in df_pacientes.columns if any(x in normalizar_texto(c) for x in ['medicamento', 'esquema'])), None)
                    
                    col_gest = next((c for c in df_pacientes.columns if 'gestante' in normalizar_texto(c)), None)
                    col_raca = next((c for c in df_pacientes.columns if 'raca' in normalizar_texto(c) or 'cor' in normalizar_texto(c)), None)
                    col_nac = next((c for c in df_pacientes.columns if 'nacionalidade' in normalizar_texto(c)), None)

                    col_pos = next((c for c in df_pacientes.columns if 'posologia' in normalizar_texto(c) or 'dose' in normalizar_texto(c)), None)
                    col_ter = next((c for c in df_pacientes.columns if 'termino' in normalizar_texto(c) or 'fim' in normalizar_texto(c)), None)
                    
                    # --- A CHAVE DE OURO: ID LIMPO ---
                    paciente_id_sujo = d_pac[col_id_p] if col_id_p else ""
                    paciente_id = limpar_id(paciente_id_sujo)
                    
                    val_cns_cpf = str(paciente_id_sujo) if paciente_id_sujo else "Não informado"
                    val_sit = str(d_pac[col_sit_p]) if col_sit_p and d_pac[col_sit_p] else "Em andamento"
                    val_ini = str(d_pac[col_ini_p]) if col_ini_p and d_pac[col_ini_p] else "-"
                    val_med = str(d_pac[col_med_p]) if col_med_p and d_pac[col_med_p] else "-"
                    
                    val_gest = str(d_pac[col_gest]) if col_gest and d_pac[col_gest] else "Não inf."
                    val_raca = str(d_pac[col_raca]) if col_raca and d_pac[col_raca] else "Não inf."
                    val_nac = str(d_pac[col_nac]) if col_nac and d_pac[col_nac] else "Não inf."
                    
                    # Explicação visual para o utilizador sobre as colunas que não estão no Google Forms dele
                    val_pos = str(d_pac[col_pos]) if col_pos and d_pac[col_pos] else "(Não consta no formulário)"
                    val_ter = str(d_pac[col_ter]) if col_ter and d_pac[col_ter] else "(Cálculo clínico não mapeado)"
                    
                    val_proxima_consulta = "Nenhuma consulta registada ainda"
                    
                    # --- CRUZAMENTO BLINDADO COM A ABA 2 (EVOLUÇÕES) ---
                    hist_pac = pd.DataFrame()
                    if df_evolucoes is not None and not df_evolucoes.empty:
                        # Encontra a coluna de ID nas Evoluções
                        col_id_e = next((c for c in df_evolucoes.columns if any(x in normalizar_texto(c) for x in ['cns', 'cpf', 'id'])), None)
                        
                        if col_id_e:
                            # Aplica a limpeza bruta de ID em todas as linhas da aba de Evolução para cruzar
                            df_evolucoes['ID_LIMPO'] = df_evolucoes[col_id_e].apply(limpar_id)
                            hist_pac = df_evolucoes[df_evolucoes['ID_LIMPO'] == paciente_id]
                            
                            if not hist_pac.empty:
                                ultima_evolucao = hist_pac.iloc[-1]
                                
                                # Puxa Próxima Consulta
                                col_prox = next((c for c in hist_pac.columns if 'proxima' in normalizar_texto(c) or 'retorno' in normalizar_texto(c)), None)
                                if col_prox and ultima_evolucao[col_prox]:
                                    val_proxima_consulta = str(ultima_evolucao[col_prox])
                                
                                # Puxa Nova Situação
                                col_nova_sit = next((c for c in hist_pac.columns if 'situacao' in normalizar_texto(c)), None)
                                if col_nova_sit and ultima_evolucao[col_nova_sit]:
                                    val_sit = str(ultima_evolucao[col_nova_sit])

                    # --- MONTAGEM DO CARTÃO DO PACIENTE ---
                    st.markdown("---")
                    with st.container(border=True):
                        st.markdown(f"### 👤 {paciente_selecionado.upper()}")
                        st.markdown(f"**ID de Ligação (CNS/CPF):** {val_cns_cpf}")
                        st.divider()
                        
                        c1, c2 = st.columns(2)
                        with c1:
                            st.markdown(f"**Início TPT:** {val_ini}")
                            st.markdown(f"**Tratamento (Esquema):** {val_med}")
                            st.markdown(f"**Posologia:** {val_pos}")
                        with c2:
                            st.markdown(f"**Término Previsto:** {val_ter}")
                            st.markdown(f"**Próxima Consulta:** {val_proxima_consulta}")
                            
                            sit_lower = val_sit.lower()
                            if 'óbito' in sit_lower or 'obito' in sit_lower:
                                st.error(f"**Situação:** {val_sit}")
                            elif 'alta' in sit_lower or 'completo' in sit_lower or 'cura' in sit_lower:
                                st.success(f"**Situação:** {val_sit}")
                            elif 'interrup' in sit_lower or 'abandono' in sit_lower or 'adversa' in sit_lower:
                                st.warning(f"**Situação:** {val_sit}")
                            else:
                                st.info(f"**Situação:** {val_sit}")
                                
                        st.divider()
                        c3, c4, c5 = st.columns(3)
                        with c3: st.markdown(f"**Gestante:** {val_gest}")
                        with c4: st.markdown(f"**Raça/Cor:** {val_raca}")
                        with c5: st.markdown(f"**Nacionalidade:** {val_nac}")

                    with st.expander("➕ Adicionar Evolução Diária / Mensal", expanded=False):
                        st.info("Registe o atendimento clicando no botão abaixo.")
                        st.link_button("📝 Preencher Evolução", LINK_FORM_EVOLUCAO, use_container_width=True)

                    # --- HISTÓRICO DE EVOLUÇÕES ---
                    st.markdown("### 🗓️ Histórico Longitudinal de Evoluções")
                    
                    if not hist_pac.empty:
                        # Mostra a consulta mais recente no topo
                        hist_pac = hist_pac.iloc[::-1]
                        
                        col_e_data = next((c for c in hist_pac.columns if 'data' in normalizar_texto(c) or 'carimbo' in normalizar_texto(c)), None)
                        col_e_tipo = next((c for c in hist_pac.columns if 'tipo' in normalizar_texto(c) or 'mes' in normalizar_texto(c)), None)
                        col_e_peso = next((c for c in hist_pac.columns if 'peso' in normalizar_texto(c)), None)
                        col_e_med = next((c for c in hist_pac.columns if 'medicamento' in normalizar_texto(c)), None)
                        col_e_sit = next((c for c in hist_pac.columns if 'situacao' in normalizar_texto(c)), None)
                        col_e_prox = next((c for c in hist_pac.columns if 'proxima' in normalizar_texto(c) or 'ret
