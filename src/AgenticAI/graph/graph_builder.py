from langgraph.graph import StateGraph, START, END
from src.AgenticAI.state.state import State
from src.AgenticAI.nodes.basic_chatbot_node import BasicChatbotNode

class GraphBuilder:
    def __init__(self, model):
        self.llm = model
        self.graph_builder = StateGraph(State)

    def basic_chatbot_graph_build(self):
        """
        Builds a basic chatbot graph using LangGraph.
        This method initializes a chatbot node using the BasicChatBotNode class
        and integrates it into the graph. the chatbot node is set as both the entry and exit point of the graph
        """
        basic_chatbot = BasicChatbotNode(self.llm)

        self.graph_builder.add_node("chatbot", basic_chatbot.process)

        #! adding edges
        self.graph_builder.add_edge(START, "chatbot")
        self.graph_builder.add_edge("chatbot", END)


    def setup_graph(self, usecase):
        """
        loads my graph based on the user's usecase
        """
        if usecase.upper() == 'BASIC CHATBOT':
            self.basic_chatbot_graph_build()
        return self.graph_builder.compile()