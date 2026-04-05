import streamlit as st
import pandas as pd

# =====================================================================
# 1. CONFIGURAÇÃO DA PÁGINA E DO COFRE DE SENHAS
# =====================================================================
st.set_page_config(page_title="Painel ILTB - Nova Iguaçu", page_icon="🏥", layout="wide")

# Você dita as regras aqui. A Unidade não consegue alterar essas senhas.
# Esquerda: A SENHA / Direita: O NOME EXATO DA UNIDADE NA PLANILHA
COFRE_DE_ACESSOS = {
    "maternidade2026": "MATERNIDADE MUNICIPAL MARIANA BULHOES",
    "viga_iltb": "CLINICA DA FAMILIA JARDIM DA VIGA",
    "hgni_123": "HGNI HOSPITAL GERAL DE NOVA IGUACU",
    "heraldo_admin": "TODAS" # Senha mestre para você visualizar a rede inteira
}

# =====================================================================
# 2. MOTOR DE BUSCA (LIGANDO O PYTHON AO GOOGLE DRIVE)
# =====================================================================
@st.cache_data(ttl=300) # O Python guarda os dados por 5 min para não sobrecarregar o Google
def carregar_dados():
    # COLE AQUI O ID DA SUA PLANILHA (O mesmo que usamos no Google Apps Script)
    SHEET_ID = "https://docs.google.com/spreadsheets/d/1A6uPoNNsz-5SzDRvZZfurYxt7NOzv73Dtde-GEsoV6o/edit?gid=0#gid=0"
    
    # O Python usa o link de exportação do Google Sheets para puxar os dados como texto (rápido e invisível)
    url_pacientes = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv&gid=0"
    
    # O Pandas lê os dados
    df = pd.read_csv(url_pacientes)
    
    # Converte a coluna "Data Notificação" para o formato de calendário e ordena da mais recente para a mais antiga
    df['Data Notificação'] = pd.to_datetime(df['Data Notificação'], format='%d/%m/%Y', errors='coerce')
    df = df.sort_values(by='Data Notificação', ascending=False)
    
    # Formata a data de volta para o padrão Brasileiro para a visualização ficar bonita
    df['Data Notificação'] = df['Data Notificação'].dt.strftime('%d/%m/%Y')
    
    return df

# =====================================================================
# 3. TELA DE LOGIN DE SEGURANÇA
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
# 4. PAINEL DE DADOS (VISUALIZAR APENAS)
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
        
        # A MÁGICA DO FILTRO: O Python bloqueia os dados e mostra só os da unidade daquela senha!
        if unidade != "TODAS":
            df_pacientes = df_pacientes[df_pacientes["Unidade de Tratamento"] == unidade]
            
        if df_pacientes.empty:
            st.warning("Nenhum paciente registrado para esta unidade até o momento.")
        else:
            # MÉTRICAS RÁPIDAS (Cards no topo da tela)
            total = len(df_pacientes)
            ativos = len(df_pacientes[df_pacientes["Situação Atual"] == "Em andamento"])
            altas = len(df_pacientes[df_pacientes["Situação Atual"] == "Tratamento Completo"])
            abandonos = len(df_pacientes[df_pacientes["Situação Atual"] == "Interrupção do tratamento"])
            
            c1, c2, c3, c4 = st.columns(4)
            c1.metric("Total de Pacientes", total)
            c2.metric("🟢 Em Andamento", ativos)
            c3.metric("🔵 Altas (Completos)", altas)
            c4.metric("🔴 Interrupções", abandonos)
            
            st.write("---")
            st.write("### 📋 Prontuários Acumulados")
            st.write("*(Modo de Leitura: Você pode pesquisar, clicar nas colunas para ordenar, mas não pode alterar ou apagar dados).*")
            
            # Seleciona as colunas mais importantes para a Unidade enxergar na tela
            colunas_para_mostrar = [
                "Data Notificação", "Nome do Paciente", "CNS", "Esquema TPT", 
                "Data Início", "Dose Orientada", "Situação Atual"
            ]
            
            # Exibe a tabela interativa lindíssima do Streamlit
            st.dataframe(
                df_pacientes[colunas_para_mostrar], 
                use_container_width=True, 
                hide_index=True
            )
            
            st.caption("Criado por Heraldo Maia - Versão 1.0 (Visualização via Python/Streamlit)")

    except Exception as e:
        st.error(f"Erro ao conectar com o Banco Central. Verifique o ID da planilha. Detalhe técnico: {e}")
