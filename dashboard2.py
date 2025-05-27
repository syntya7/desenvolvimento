import streamlit as st
import pandas as pd
import numpy as np
import altair as alt

st.title("Painel de Desempenho Escolar")

# Gerar dados randômicos
alunos = [f"Aluno {i}" for i in range(1, 11)]
disciplinas = ["Matemática", "Português", "História", "Ciências"]

np.random.seed(42)  # para consistência nos dados
dados = {
    "Aluno": np.random.choice(alunos, size=40, replace=True),
    "Nota": np.round(np.random.uniform(0, 10, 40), 1),
    "Disciplina": np.random.choice(disciplinas, size=40, replace=True)
}

df = pd.DataFrame(dados)

# Filtro de disciplina
disciplina_opcao = st.selectbox("Filtrar por disciplina", ["Todas"] + disciplinas)

# Filtragem de dados
if disciplina_opcao != "Todas":
    df_filtrado = df[df["Disciplina"] == disciplina_opcao]
else:
    df_filtrado = df

# Tabela de dados
st.subheader("Tabela de Notas")
st.dataframe(df_filtrado)

# Gráfico de barras
st.subheader("Gráfico de Notas por Aluno")
chart = alt.Chart(df_filtrado).mark_bar().encode(
    x=alt.X('Aluno:N', sort=None),  # Evita sobrecarga de labels no eixo X
    y='Nota:Q',
    color='Disciplina:N',
    tooltip=['Aluno', 'Nota', 'Disciplina']
).properties(
    title="Desempenho dos Alunos",
    width=700
)

st.altair_chart(chart, use_container_width=True)

# Média geral por disciplina
st.subheader("Média Geral por Disciplina")
media_disciplina = df.groupby("Disciplina")["Nota"].mean().round(2)
st.dataframe(media_disciplina.reset_index().rename(columns={"Nota": "Média"}))
