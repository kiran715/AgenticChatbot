import streamlit as st

from src.AgenticAI.ui.streamlitui.loadui import LoadStreamlitUI
from src.AgenticAI.llms.groqllm import GroqLLM
from src.AgenticAI.graph.graph_builder import GraphBuilder
from src.AgenticAI.ui.streamlitui.display_result import DisplayResultStreamlit

def load_agenticai_app():
    """
    Loads and runs the LanGraph AgenticAI application with Streamlit UI. This function initializes the UI, handles user input, configures
    the LLM model, sets up the graph based on the selected use case, and displays the output whilw implementing
    exceptions handling for robustness
    """

    # Load UI
    ui = LoadStreamlitUI()
    user_input = ui.load_streamlit_ui()

    if not user_input:
        st.error('Error: Failed to load user input from the UI')
        return

    if st.session_state['IsButtonClicked']:
        user_message = st.session_state['timeframe']
    else:
        user_message = st.chat_input("Enter your message")

    if user_message:
        try:
            obj_llm_config = GroqLLM(user_choices=user_input)
            model = obj_llm_config.get_llm_model()
            if not model:
                st.error("Error: LLM Model could not be initialized")
                return

            usecase = user_input['selected_usecase']

            if not usecase:
                st.error("Error: no use case selected")
                return

            graphBuilder = GraphBuilder(model=model)

            try:
                graph = graphBuilder.setup_graph(usecase=usecase)
                DisplayResultStreamlit(usecase, graph, user_message).display_result_ui()
            except Exception as e:
                st.error(f"Error: Graph setup failed - {e}")
                return

        except Exception as e:
            st.error(f"Error : user message is not given - {e}")
            return
