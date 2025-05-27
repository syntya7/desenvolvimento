import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

st.title("Analisador")

# Upload do arquivo CSV
uploaded_file = st.file_uploader("Faça upload do arquivo CSV", type=["csv"])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)

    # Remove espaços em branco dos nomes das colunas
    df.columns = df.columns.str.strip()

    # Mostra os nomes das colunas disponíveis
    st.write("Colunas disponíveis no DataFrame:", df.columns.tolist())

    # Exibe os primeiros registros
    st.subheader("Pré-visualização dos dados")
    st.write(df.head())

    # Estatísticas descritivas
    st.subheader("Estatísticas descritivas")
    st.write(df.describe())

    # Filtro por Tipo (Entrada/Saída)
    if "Tipo" in df.columns:
        tipo_filtro = st.selectbox("Filtrar por Tipo:", options=["Todos", "Entrada", "Saída"])
        if tipo_filtro != "Todos":
            df = df[df["Tipo"] == tipo_filtro]
    else:
        st.warning("A coluna 'Tipo' não está presente no arquivo CSV.")

    # Gráfico por Categoria e Valor
    st.subheader("Gráfico por Categoria e Valor")
    if "Categoria" in df.columns and "Valor" in df.columns:
        fig1, ax1 = plt.subplots()
        sns.barplot(data=df, x="Categoria", y="Valor", ci=None, estimator=sum, ax=ax1)
        plt.xticks(rotation=45)
        st.pyplot(fig1)
    else:
        st.warning("As colunas 'Categoria' e/ou 'Valor' não estão presentes no arquivo CSV.")

    # Gráfico personalizado com seleção de colunas
    st.subheader("Gráfico personalizado")
    colunas_validas = df.select_dtypes(include=['object', 'float64', 'int64']).columns.tolist()
    if len(colunas_validas) >= 2:
        x_col = st.selectbox("Escolha a coluna para o eixo X:", colunas_validas)
        y_col = st.selectbox("Escolha a coluna para o eixo Y:", colunas_validas)

        if st.button("Gerar Gráfico"):
            fig2, ax2 = plt.subplots()
            sns.scatterplot(data=df, x=x_col, y=y_col, ax=ax2)
            st.pyplot(fig2)

            # Correlação e interpretação
            if pd.api.types.is_numeric_dtype(df[x_col]) and pd.api.types.is_numeric_dtype(df[y_col]):
                correlacao = df[x_col].corr(df[y_col])
                st.write(f"Coeficiente de correlação entre {x_col} e {y_col}: *{correlacao:.2f}*")

                # Interpretação simples
                if correlacao > 0.5:
                    interpretacao = "forte e positiva"
                elif correlacao < -0.5:
                    interpretacao = "forte e negativa"
                elif abs(correlacao) < 0.3:
                    interpretacao = "fraca ou inexistente"
                else:
                    interpretacao = "moderada"
                st.write(f"Interpretação: A relação entre {x_col} e {y_col} é {interpretacao}.")
            else:
                st.write("Não é possível calcular correlação entre colunas não numéricas.")
    else:
        st.warning("Não há colunas suficientes (numéricas ou categóricas) para criar o gráfico personalizado.")