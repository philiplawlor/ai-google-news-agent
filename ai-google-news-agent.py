from dotenv import load_dotenv
import requests
import json
import openai
import streamlit as st
import os



# Load environment variables
# load_dotenv()

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

            st.write("Search Results")
            st.write(display_text, unsafe_allow_html=True)

            return ""
            # return response.json().get('items', [])
        else:
            return {"error": f"Failed to fetch data: {response.status_code}"}

    def news_search(self, query, num_results=5):
        url = f"https://newsapi.org/v2/everything?q={query}&apiKey={self.news_api_key}&pageSize={num_results}"
        response = requests.get(url)

        if response.status_code == 200:
            for item in response.json().get('articles', []):
                search_items = []
                for item in response.json().get('articles', []):
                    search_items.append([item['title'], item['url'], item['description']])
            
            display_text = ""
            for item in search_items:
                display_text += f"<h3><a href='{item[1]}'>{item[0]}</a></h3>"
                display_text += f"<p>{item[2]}</p>"

            st.write("News Results")
            st.write(display_text, unsafe_allow_html=True)

            # st.write(search_items, unsafe_allow_html=True)
            return "" 
            # return response.json().get("articles", [])
        else:
            return {"error": f"Failed to fetch news: {response.status_code}"}
    
    def query_llama(self, prompt):
        headers = {'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6IjY1ODk5ZDY1LTkxZmItNGFhNi1hNjllLWU0YjNlMTA5NmJjMCJ9.nKsR0D-78laZ6FI5JxAloVzE9uS89yPTFs9fa5pXFSg',
                    'Content-Type': 'application/json'}
        # data = json.dumps({"prompt": prompt, "max_tokens": 100})
        payload = json.dumps({
                    "model": "gpt-4-turbo",
                    "messages": [
                        {
                        "role": "user",
                        "content": f"{prompt}"
                        }
                    ]
                    })

        response = requests.post(self.llama_endpoint, headers=headers, data=payload)
        if response.status_code == 200:
            # print(response.json().get('choices',[]))
            for item in response.json().get('choices', []):
                search_items = item['message']['content']

            return search_items
        else:
            return {"error": f"Failed to query LLaMA: {response.status_code}"}

# Streamlit UI
st.title("Live Data Agent")
query = st.text_input("Enter your query:")

if st.button("Clear Search"):
    st.write("")

if st.button("Search Google"):
    agent = LiveDataAgent(google_api_key=st.secrets["GOOGLE_API_KEY"], google_cx=st.secrets["GOOGLE_CX"], news_api_key=st.secrets["NEWS_API_KEY"], llama_endpoint="http://localhost:3000/api/chat/completions")
    results = agent.google_search(query)
    st.write(results)

if st.button("Clear News"):
    st.write("")

if st.button("Search News"):
    agent = LiveDataAgent(google_api_key=st.secrets["GOOGLE_API_KEY"], google_cx=st.secrets["GOOGLE_CX"], news_api_key=st.secrets["NEWS_API_KEY"], llama_endpoint="http://localhost:3000/api/chat/completions")
    results = agent.news_search(query)
    st.write(results)

if st.button("clear"):
    st.write("")

if st.button("Query LLaMA"):
    agent = LiveDataAgent(google_api_key=st.secrets["GOOGLE_API_KEY"], google_cx=st.secrets["GOOGLE_CX"], news_api_key=st.secrets["NEWS_API_KEY"], llama_endpoint="http://localhost:3000/api/chat/completions")
    results = agent.query_llama(query)
    st.write(results)
