
import os
import streamlit as st
from langchain_groq import ChatGroq

class GroqLLM:
    def __init__(self, user_choices):
        self.user_choices = user_choices

    def get_llm_model(self):
        try:
            groq_api_key = self.user_choices['GROQ_API_KEY']
            selected_groq_model = self.user_choices['selected_groq_model']
            if groq_api_key == '':
                st.error('Please enter the Groq API key')
                return

            llm = ChatGroq(api_key=groq_api_key, model=selected_groq_model)
        except Exception as e:
            raise ValueError(f'Error occured with Exception : {e}')
        return llm