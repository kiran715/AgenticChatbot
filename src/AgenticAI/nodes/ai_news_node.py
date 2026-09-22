from tavily import TavilyClient
from langchain_core.prompts import ChatPromptTemplate

class AINewsNode:
    def __init__(self, llm):
        """
        Initializes the AINewsNode with API keys for tavily and GROQ
        """
        self.tavily = TavilyClient()
        self.llm = llm

        # this is used to capture various steps in this file so that later can be used for steps shown
        self.state = {}

    def fetch_news(self, state: dict) -> dict:
        """
        Fetch Ai news based on the sepcified frequancy 

        Args : 
            state (dict) : The state dictionary containing 'frequancy'
        
        Returns:
            dict Updated state with 'news_data' key containing fetched ones
        """

        frequency = state['messages'][0].content.lower()
        self.state['frequency'] = frequency
        time_range_map = {'daily' : 'd', 'weekly' : 'w', 'monthly' : 'm', 'year' : 'y'}
        days_map = {'daily' : 1, 'weekly' : 7, 'monthly' : 30, 'year' : 366}

        response = self.tavily.search(
            query="Top Artificial Intelligence (AI) Technology News India and Globally",
            topic="news",
            time_range=time_range_map[frequency],
            include_answer="advanced",
            max_results=15,
            days=days_map[frequency]
        )

        state['news_data'] = response.get('results', [])
        self.state['news_data'] = state['news_data']
        return self.state

    def summarize_news(self, state: dict) -> dict:
        """
        Summarize the fetched news using llm

        Args:
            state (dict) : The state dictionary containing 'news_data'
        
        Returns:
            dict: Updated state with 'summary' key containing the summarized ones
        """

        news_items = self.state['news_data']

        prompt_template = ChatPromptTemplate.from_messages([
            ('system', """Summarize the AI news articles into markdown format. for each item include:
            - Date in **YYYY-MM-DD** format in IST timezone
            - Concise sentences summary from latest ones
            - sprt news by date wise (latest first)
            - Source URL as link

            Use format:
            ### [Date]
            - [Summary](URL)
            """),
            ('user' , "Articles: \n{articles}")
        ])

        articles_str = "\n\n".join(
            f"content: {item.get('content', '')}\n URL: {item.get('url', '')}\n Date: {item.get('published_date', '')}"
            for item in news_items
        )

        response = self.llm.invoke(prompt_template.format(articles=articles_str))
        state['summary'] = response.content
        self.state['summary'] = state['summary']
        return self.state

    def save_results(self, state):
        frequency = self.state['frequency']
        summary = self.state['summary']
        filename = f"./AINews/{frequency}_summary.md"
        with open(filename, 'w') as f:
            f.write(f"# {frequency.capitalize()} AI News summary \n\n")
            f.write(summary)
        self.state['filename'] = filename
        return self.state