from langgraph.graph import StateGraph, START, END
from src.AgenticAI.state.state import State
from src.AgenticAI.nodes.basic_chatbot_node import BasicChatbotNode
from src.AgenticAI.tools.search_tool import get_tools, create_tool_node
from langgraph.prebuilt import tools_condition
from src.AgenticAI.nodes.chatbot_with_tool_node import ChatBotwithToolNode
from src.AgenticAI.nodes.ai_news_node import AINewsNode

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

    def chatbot_with_tool_build_graph(self):
        """
        Builds an advanced chatbot graph with tool integration. This method creates a chatbot
        that includes both a chatbot and a tool node. It defines tools, initializes the chatbot with tool capabilities,
        and sets up conditional and direct edges between nodes. thw chatbot node is set as the entry point
        """
        tools = get_tools()
        tool_node = create_tool_node(tools)

        # defining the llm
        llm = self.llm

        #defining 
        chatbot_with_tool_node = ChatBotwithToolNode(llm)
        chatbot_tool_node = chatbot_with_tool_node.create_chatbot(tools)

        # Adding nodes
        self.graph_builder.add_node("chatbot", chatbot_tool_node)
        self.graph_builder.add_node("tools", tool_node)

        # creating the edges
        self.graph_builder.add_edge(START, "chatbot")
        self.graph_builder.add_conditional_edges("chatbot", tools_condition)
        self.graph_builder.add_edge("tools", "chatbot")

    def ai_news_builder_graph(self):

        ainewsnode = AINewsNode(self.llm)


        # adding nodes
        self.graph_builder.add_node("fetch_news", ainewsnode.fetch_news)
        self.graph_builder.add_node("summarize_news", ainewsnode.summarize_news)
        self.graph_builder.add_node("save_results", ainewsnode.save_results)

        # adding edges
        self.graph_builder.set_entry_point("fetch_news")
        self.graph_builder.add_edge("fetch_news", "summarize_news")
        self.graph_builder.add_edge("summarize_news", "save_results")
        self.graph_builder.add_edge("save_results", END)

    def setup_graph(self, usecase):
        """
        loads my graph based on the user's usecase
        """
        if usecase.upper() == 'BASIC CHATBOT':
            self.basic_chatbot_graph_build()
        if usecase.upper() == 'CHATBOT WITH WEBSEARCH':
            self.chatbot_with_tool_build_graph()
        if usecase.upper() == 'AI NEWS':
            self.ai_news_builder_graph()
        return self.graph_builder.compile()