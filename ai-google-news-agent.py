from dotenv import load_dotenv
import requests
import json
import openai
import streamlit as st
import os


st.write("DB username:", st.secrets["google_api_key"])
st.write("DB password:", st.secrets["google_cx"])

st.write(
    "Has environment variables been set:",
    os.environ["db_username"] == st.secrets["news_api_key"], st.secrets['llama_endpoint']
)

# Load environment variables
load_dotenv()

class LiveDataAgent:
    def __init__(self, google_api_key, google_cx, news_api_key, llama_endpoint):
        self.google_api_key = google_api_key
        self.google_cx = google_cx
        self.news_api_key = news_api_key
        self.llama_endpoint = llama_endpoint

    def google_search(self, query, num_results=5):
        url = f"https://www.googleapis.com/customsearch/v1?q={query}&key={self.google_api_key}&cx={self.google_cx}&num={num_results}"
        response = requests.get(url)
        # print(response.text)
        if response.status_code == 200:
            for item in response.json().get('items', []):
                search_items = []
                for item in response.json().get('items', []):
                    search_items.append([item['title'], item['link'], item['htmlSnippet']])
            # search_item = [item['title'] for item in response.json().get('items', [])]

            #format the search items into html so that it can be displayed in the streamlit app
            display_text = ""
            for item in search_items:
                display_text += f"<h3><a href='{item[1]}'>{item[0]}</a></h3>"
                display_text += f"<p>{item[2]}</p>"
            st.write(display_text, unsafe_allow_html=True)

            return ""
            # return response.json().get('items', [])
        else:
            return {"error": f"Failed to fetch data: {response.status_code}"}

    def news_search(self, query, num_results=5):
        url = f"https://newsapi.org/v2/everything?q={query}&apiKey={self.news_api_key}&pageSize={num_results}"
        response = requests.get(url)
        if response.status_code == 200:
            return response.json().get("articles", [])
        else:
            return {"error": f"Failed to fetch news: {response.status_code}"}
    
    def query_llama(self, prompt):
        headers = {'Content-Type': 'application/json'}
        data = json.dumps({"prompt": prompt, "max_tokens": 100})
        response = requests.post(self.llama_endpoint, headers=headers, data=data)
        if response.status_code == 200:
            return response.json()
        else:
            return {"error": f"Failed to query LLaMA: {response.status_code}"}

# Streamlit UI
st.title("Live Data Agent")
query = st.text_input("Enter your query:")

if st.button("Search Google"):
    agent = LiveDataAgent(google_api_key="AIzaSyAf83nRkbTkH7kvjtEwdmHGWskxD8RHQq0", google_cx="8470d3ed300cf4a11", news_api_key="e5b5c7db95c340c081b725f187c54b84", llama_endpoint="http://localhost:3000/generate")
    results = agent.google_search(query)
    st.write(results)

if st.button("Search News"):
    agent = LiveDataAgent(google_api_key="AIzaSyAf83nRkbTkH7kvjtEwdmHGWskxD8RHQq0", google_cx="8470d3ed300cf4a11", news_api_key="e5b5c7db95c340c081b725f187c54b84", llama_endpoint="http://localhost:3000/generate")
    results = agent.news_search(query)
    st.write(results)

if st.button("Query LLaMA"):
    agent = LiveDataAgent(google_api_key="AIzaSyAf83nRkbTkH7kvjtEwdmHGWskxD8RHQq0", google_cx="8470d3ed300cf4a11", news_api_key="e5b5c7db95c340c081b725f187c54b84", llama_endpoint="http://localhost:3000/generate")
    results = agent.query_llama(query)
    st.write(results)
