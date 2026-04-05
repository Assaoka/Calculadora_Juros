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
    col_init1, col_init2, col_init3 = st.columns(3)
    with col_init1:
        aporte_inicial = st.number_input("Aporte Inicial (R$)", min_value=0.0, value=21000.0, step=100.0)
    with col_init2:
        data_inicial = st.date_input("Data Inicial", value="today")
    with col_init3:
        taxa_inflacao = st.number_input("Inflação Anual Média (%)", min_value=0.0, value=4.5, step=0.1)

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
    valor_reajustado_lista = []
    
    current_total = aporte_inicial
    current_aplicado = aporte_inicial
    current_reajustado = aporte_inicial
    current_date = pd.to_datetime(data_inicial)
    
    datas.append(current_date)
    valor_total_lista.append(current_total)
    valor_aplicado_lista.append(current_aplicado)
    valor_reajustado_lista.append(current_reajustado)
    
    transition_dates = []
    resumo_periodos = []
    simulacao_interrompida = False
    
    for idx, p in enumerate(period_data):
        if simulacao_interrompida:
            break
            
        inicio_aplicado = current_aplicado
        inicio_total = current_total
        
        meses_no_periodo = p["meses"]
        taxa_mensal = (1 + p["taxa_anual"] / 100) ** (1 / 12) - 1
        taxa_inflacao_mensal = (1 + taxa_inflacao / 100) ** (1 / 12) - 1
        
        for _ in range(meses_no_periodo):
            current_date += pd.DateOffset(months=1)
            
            # Cálculo do próximo valor
            novo_total = current_total * (1 + taxa_mensal) + p["aporte_mensal"]
            current_aplicado += p["aporte_mensal"]
            
            # Cálculo do valor reajustado (poder de compra hoje)
            meses_decorridos = len(valor_total_lista)
            valor_reajustado = novo_total / ((1 + taxa_inflacao_mensal) ** meses_decorridos)
            
            if novo_total <= 0:
                current_total = 0
                datas.append(current_date)
                valor_total_lista.append(current_total)
                valor_aplicado_lista.append(current_aplicado)
                valor_reajustado_lista.append(0)
                simulacao_interrompida = True
                break
                
            current_total = novo_total
            datas.append(current_date)
            valor_total_lista.append(current_total)
            valor_aplicado_lista.append(current_aplicado)
            valor_reajustado_lista.append(valor_reajustado)
            
        transition_dates.append(current_date)
        resumo_periodos.append({
            "Período": f"Período {idx + 1}",
            "Total Investido": current_aplicado - inicio_aplicado,
            "Rendimento do Período": (current_total - inicio_total) - (current_aplicado - inicio_aplicado),
            "Evolução Total (Período)": current_total - inicio_total
        })

            
    df = pd.DataFrame({
        "Data": datas,
        "Valor Investido": valor_aplicado_lista,
        "Patrimônio Bruto (Nominal)": valor_total_lista,
        "Poder de Compra (Real)": valor_reajustado_lista
    })

    
    if simulacao_interrompida:
        st.warning("⚠️ **A simulação foi interrompida antecipadamente:** O montante acumulado chegou a zero devido a resgates superiores ao saldo disponível.")
    
    st.divider()

    
    df_melt = df.melt(id_vars=["Data"], value_vars=["Valor Investido", "Patrimônio Bruto (Nominal)", "Poder de Compra (Real)"], 
                      var_name="Tipo", value_name="Valor (RS)")
    
    fig = px.line(df_melt, x="Data", y="Valor (RS)", color="Tipo",
                  title="Evolução do Patrimônio (Nominal vs Real)",
                  labels={"Valor (RS)": "Montante (R$)", "Data": "Data do Aporte"},
                  color_discrete_map={
                      "Valor Investido": "#909090", 
                      "Patrimônio Bruto (Nominal)": "#27ae60",
                      "Poder de Compra (Real)": "#f39c12"
                  })
    
    # Adicionando linhas tracejadas nas transições (exceto a última se não for relevante)
    for t_date in transition_dates[:-1]:
        fig.add_vline(x=t_date, line_dash="dash", line_color="#e74c3c", opacity=0.7)
        
    # Adicionando marcadores nas transições nos valores exatos
    transition_df = df[df["Data"].isin(transition_dates)]
    fig.add_scatter(x=transition_df["Data"], y=transition_df["Patrimônio Bruto (Nominal)"], mode="markers", 
                    marker=dict(color="#e74c3c", size=8), name="Transição / Fim de Período")
    
    fig.update_layout(hovermode="x unified", legend_title_text="")
    
    cols = st.columns([1.75, 5.0])
    with cols[1]:
        st.plotly_chart(fig, use_container_width=True)
    
    def format_br(val):
        return f"R$ {val:,.2f}".replace(",", "_").replace(".", ",").replace("_", ".")
        
    # Métricas globais
    lucro_total = current_total - current_aplicado
    valor_final_reajustado = valor_reajustado_lista[-1]
    perda_inflacionaria = current_total - valor_final_reajustado
    
    with cols[0].container(border=True):
        st.metric("Total Investido", format_br(current_aplicado))
        st.divider()
        #st.metric("Rendimento Total", format_br(lucro_total))
        #st.divider()
        st.metric("Total Acumulado Final", format_br(current_total))
        st.divider()
        st.metric("Poder de Compra (Hoje)", format_br(valor_final_reajustado), 
                  help="Este é o valor que o montante final teria nos dias de hoje, descontada a inflação.")
        #st.divider()
        #st.metric("Perda p/ Inflação", f"-{format_br(perda_inflacionaria)}", delta_color="inverse",
                  #help="Quanto do seu rendimento 'desapareceu' por conta da desvalorização da moeda.")
        
    # Tabela com resumo por período
    st.markdown("#### Detalhamento de Performance por Período:")
    df_resumo = pd.DataFrame(resumo_periodos)
    for col in ["Total Investido", "Rendimento do Período", "Evolução Total (Período)"]:
        df_resumo[col] = df_resumo[col].apply(format_br)
    
    st.dataframe(df_resumo, use_container_width=True, hide_index=True)
