#    st.session_state.openai_key = "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"  # Hard-coded OpenAI key
import streamlit as st
import pandas as pd
from pandasai import PandasAI
from pandasai.llm.openai import OpenAI
import matplotlib.pyplot as plt

st.write("Dan's Streamlit [PandasAI](https://github.com/gventuri/pandas-ai)")

if "openai_key" not in st.session_state:
    with st.form("API key"):
        key = st.text_input("OpenAI Key", value="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")
        if st.form_submit_button("Submit"):
            st.session_state.openai_key = key
            st.session_state.prompt_history = []
            st.session_state.df = None

if "openai_key" in st.session_state:
    if st.session_state.df is None:
        uploaded_file = st.file_uploader(
            "Choose CSV...",
            type="csv",
        )
        if uploaded_file is not None:
            df = pd.read_csv(uploaded_file)
            st.session_state.df = df

    with st.form("Question"):
        question = st.text_input("Question", value="How many rows?")
        submitted = st.form_submit_button("Submit")
        if submitted:
            with st.spinner():
                llm = OpenAI(api_token=st.session_state.openai_key)
                pandas_ai = PandasAI(llm)
                x = pandas_ai.run(st.session_state.df, prompt=question)

                fig = plt.gcf()
                if fig.get_axes():
                    st.pyplot(fig)
                st.write(x)
                st.session_state.prompt_history.append(question)

    if st.session_state.df is not None:
        #st.subheader("Dataframe:")
        st.write(st.session_state.df)

    #st.subheader("History:")
    st.write(st.session_state.prompt_history)

if st.button("Clear"):
    st.session_state.prompt_history = []
    st.session_state.df = None