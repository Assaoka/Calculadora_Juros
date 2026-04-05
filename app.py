import streamlit as st
import pandas as pd
import plotly.express as px
import uuid

st.set_page_config(page_title="Calculadora de Juros Compostos", page_icon="📈", layout="wide")

# Initialize session state for periods
if "periodos" not in st.session_state:
    st.session_state.periodos = [{"id": str(uuid.uuid4())}]

def add_period():
    st.session_state.periodos.append({"id": str(uuid.uuid4())})

def remove_period(period_id):
    st.session_state.periodos = [p for p in st.session_state.periodos if p["id"] != period_id]

st.html("<h1 align='center'> Calculadora de Juros Compostos </h1>")

with st.expander("Parâmetros", expanded=True):
    col_init1, col_init2 = st.columns(2)
    with col_init1:
        aporte_inicial = st.number_input("Aporte Inicial (R$)", min_value=0.0, value=21000.0, step=100.0)
    with col_init2:
        data_inicial = st.date_input("Data Inicial", value="today")

    st.divider()

    # Lê os parâmetros dos períodos ativos na UI e guarda num dicionário temporário
    period_data = []

    # Exibe os períodos de forma dinâmica
    for idx, p in enumerate(st.session_state.periodos):
        pid = p["id"]
        with st.container():
            col1, col2, col3, col4, col5 = st.columns([1.5, 1.5, 2, 2, 1])
            
            with col1:
                duracao_valor = st.number_input("Duração", min_value=1, value=2 if idx==0 else 4, step=1, key=f"dur_val_{pid}")
            with col2:
                duracao_tipo = st.selectbox("Unidade", ["Anos", "Meses"], key=f"dur_tipo_{pid}")
            with col3:
                taxa_juros = st.number_input("Taxa de Juros Anual (%)", min_value=0.0, value=10.0 if idx==0 else 11.0, step=0.1, key=f"taxa_{pid}")
            with col4:
                aporte_mensal = st.number_input("Aporte/Resgate Mensal (R$)", value=3200.0 if idx==0 else 5500.0, step=100.0, key=f"aporte_{pid}")
            with col5:
                st.markdown("<br>", unsafe_allow_html=True)
                if st.button("❌", key=f"del_{pid}", help="Remover este período"):
                    remove_period(pid)
                    st.rerun()
                    
            meses_no_periodo = duracao_valor * 12 if duracao_tipo == "Anos" else duracao_valor
            period_data.append({
                "meses": meses_no_periodo,
                "taxa_anual": taxa_juros,
                "aporte_mensal": aporte_mensal
            })

    st.button("➕ Adicionar Período", on_click=add_period, use_container_width=True)

if True:
    if not period_data:
        st.warning("Adicione pelo menos um período para calcular.")
        st.stop()
        
    datas = []
    valor_total_lista = []
    valor_aplicado_lista = []
    
    current_total = aporte_inicial
    current_aplicado = aporte_inicial
    current_date = pd.to_datetime(data_inicial)
    
    datas.append(current_date)
    valor_total_lista.append(current_total)
    valor_aplicado_lista.append(current_aplicado)
    
    transition_dates = []
    resumo_periodos = []
    
    for idx, p in enumerate(period_data):
        inicio_aplicado = current_aplicado
        inicio_total = current_total
        
        meses_no_periodo = p["meses"]
        taxa_mensal = (1 + p["taxa_anual"] / 100) ** (1 / 12) - 1
        
        for _ in range(meses_no_periodo):
            current_date += pd.DateOffset(months=1)
            current_total = current_total * (1 + taxa_mensal) + p["aporte_mensal"]
            current_aplicado = current_aplicado + p["aporte_mensal"]
            
            datas.append(current_date)
            valor_total_lista.append(current_total)
            valor_aplicado_lista.append(current_aplicado)
            
        transition_dates.append(current_date)
        resumo_periodos.append({
            "Período": f"Período {idx + 1}",
            "Total Aplicado": current_aplicado - inicio_aplicado,
            "Rendimento do Período": (current_total - inicio_total) - (current_aplicado - inicio_aplicado),
            "Evolução Total (Período)": current_total - inicio_total
        })
            
    df = pd.DataFrame({
        "Data": datas,
        "Valor Aplicado": valor_aplicado_lista,
        "Valor Total": valor_total_lista
    })

    
    st.divider()
    
    df_melt = df.melt(id_vars=["Data"], value_vars=["Valor Aplicado", "Valor Total"], 
                      var_name="Tipo", value_name="Valor (RS)")
    
    fig = px.line(df_melt, x="Data", y="Valor (RS)", color="Tipo",
                  title="Valor Aplicado vs Valor Total com Juros Compostos",
                  labels={"Valor (RS)": "Montante (R$)", "Data": "Data do Aporte"},
                  color_discrete_map={"Valor Aplicado": "#909090", "Valor Total": "#27ae60"})
    
    # Adicionando linhas tracejadas nas transições (exceto a última se não for relevante)
    for t_date in transition_dates[:-1]:
        fig.add_vline(x=t_date, line_dash="dash", line_color="#e74c3c", opacity=0.7)
        
    # Adicionando marcadores nas transições nos valores exatos
    transition_df = df[df["Data"].isin(transition_dates)]
    fig.add_scatter(x=transition_df["Data"], y=transition_df["Valor Total"], mode="markers", 
                    marker=dict(color="#e74c3c", size=8), name="Transição / Fim de Período")
    
    fig.update_layout(hovermode="x unified", legend_title_text="")
    
    cols = st.columns([1.75, 5.0])
    with cols[1]:
        st.plotly_chart(fig, use_container_width=True)
    
    def format_br(val):
        return f"R$ {val:,.2f}".replace(",", "_").replace(".", ",").replace("_", ".")
        
    # Métricas globais
    lucro_total = current_total - current_aplicado
    with cols[0].container(border=True):
        st.metric("Total Aplicado", format_br(current_aplicado))
        st.divider()
        st.metric("Rendimento Total", format_br(lucro_total))
        st.divider()
        st.metric("Total Acumulado Final", format_br(current_total))
        
    # Tabela com resumo por período
    st.markdown("#### Detalhamento de Performance por Período:")
    df_resumo = pd.DataFrame(resumo_periodos)
    for col in ["Total Aplicado", "Rendimento do Período", "Evolução Total (Período)"]:
        df_resumo[col] = df_resumo[col].apply(format_br)
    
    st.dataframe(df_resumo, use_container_width=True, hide_index=True)
