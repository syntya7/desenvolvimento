import streamlit as st
import pandas as pd
from datetime import date

st.title("Cadastro de Pacientes")

# Inicializa o session_state se ainda não estiver definido
if "pacientes" not in st.session_state:
    st.session_state.pacientes = []

# Formulário de cadastro
with st.form(key="form_paciente"):
    nome = st.text_input("Nome do paciente")
    idade = st.number_input("Idade", min_value=0, max_value=120, step=1)
    sexo = st.selectbox("Sexo", ["Masculino", "Feminino", "Outro"])
    especialidade = st.selectbox(
        "Especialidade médica", ["Clínica Geral", "Cardiologia", "Pediatria", "Dermatologia"]
    )
    data_consulta = st.date_input("Data da consulta", min_value=date.today())

    convenio_check = st.checkbox("Possui convênio?")
    convenio_nome = ""
    if convenio_check:
        convenio_nome = st.text_input("Nome do convênio")

    submitted = st.form_submit_button("Cadastrar Paciente")
    if submitted:
        novo_paciente = {
            "Nome": nome,
            "Idade": idade,
            "Sexo": sexo,
            "Especialidade": especialidade,
            "Data da Consulta": data_consulta,
            "Convênio": convenio_nome if convenio_check else "Não"
        }
        st.session_state.pacientes.append(novo_paciente)
        st.success("Paciente cadastrado com sucesso!")

# Exibe a tabela de pacientes cadastrados
if st.session_state.pacientes:
    df = pd.DataFrame(st.session_state.pacientes)
    st.dataframe(df)

# Botão para limpar os dados
if st.button("Limpar Dados"):
    st.session_state.pacientes = []
    st.success("Dados apagados com sucesso!")