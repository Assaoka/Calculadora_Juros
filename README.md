# 📈 Calculadora de Juros Compostos

Uma ferramenta que pode ser usada para simular investimentos consecutivos com condições diferentes, permitindo visualizar o impacto dos juros compostos e aportes / retiradas mensais ao longo do tempo.

O site está disponível no [Streamlit Cloud](https://calculadora-de-juros-compostos.streamlit.app/)

## 📝 Descrição

Esta aplicação foi desenvolvida com **Streamlit** e **Python** para ajudar investidores a planejarem sua evolução patrimonial. Diferente das calculadoras convencionais, esta permite a criação de **múltiplos períodos** de investimento, cada um com sua própria duração, taxa de juros e valor de aporte, refletindo melhor a realidade de mudanças na vida financeira.

### ✨ Principais Funcionalidades
- **Múltiplos Períodos:** Configure fases distintas de investimento (ex: 2 anos com taxa X, seguidos de 5 anos com taxa Y).
- **Gráfico Interativo:** Visualização clara da diferença entre o **capital aplicado** e o **montante total** (com juros).
- **Detalhamento por Período:** Tabela detalhada mostrando o rendimento e a evolução em cada fase configurada.
- **Métricas Globais:** Resumo instantâneo do Total Aplicado, Rendimento Total e Saldo Final.

## 🚀 Como Rodar Localmente

Certifique-se de ter o Python (versão 3.8+) instalado em sua máquina.

### 1. Preparação do Ambiente
Recomenda-se o uso de um ambiente virtual:
```bash
python -m venv venv
# No Windows:
venv\Scripts\activate
# No Linux/Mac:
source venv/bin/activate
```

### 2. Instalação das Dependências
Instale todos os pacotes necessários listados no `requirements.txt`:
```bash
pip install -r requirements.txt
```

### 3. Execução
Inicie a aplicação utilizando o Streamlit:
```bash
streamlit run app.py
```

Alternativamente, você pode usar os arquivos `run_hidden.vbs` para iniciar a aplicação sem o terminal aberto. Para encerrar a aplicação, execute o arquivo `stop_app.bat`.

## 🛠️ Tecnologias Utilizadas

- **[Streamlit](https://streamlit.io/):** Para a interface web e interatividade.
- **[Pandas](https://pandas.pydata.org/):** Para processamento e estruturação dos dados financeiros.
- **[Plotly Express](https://plotly.com/python/):** Para a geração dos gráficos dinâmicos.
- **[Python](https://www.python.org/):** Linguagem de programação robusta para os cálculos.
