import streamlit as st
import google.generativeai as genai
from serpapi import GoogleSearch

# Setup API keys from Streamlit secrets
genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
serpapi_api_key = st.secrets["SERPAPI_API_KEY"]

# Initialize Gemini model
model = genai.GenerativeModel('gemini-2.0-flash')

def web_search(query):
    search = GoogleSearch({
        "q": query,
        "api_key": serpapi_api_key
    })
    results = search.get_dict()
    # Extract top 3 organic results
    if "organic_results" in results:
        return "\n".join([f"- {result['title']}: {result['snippet']}" 
                         for result in results["organic_results"][:3]])
    return "No results found"

# Streamlit UI
st.set_page_config(page_title="Live AI Search Agent")
st.title("🔍 Live AI Search with Web Data")

query = st.text_input("Enter your search query:", "")

if st.button("Search"):
    if query:
        with st.spinner("🔎 Thinking..."):
            try:
                # First get web search results
                search_results = web_search(query)
                
                # Create a prompt that combines the query and search results
                prompt = f""" you must go to the web to search only when u r required to ans latest data.
                else u must work as an intelligent chatot.
                please provide answers to the query: "{query}"

                Web Search Results:
                {search_results}

                Please analyze these results and provide a clear, informative response."""
                
                # Get response from Gemini
                response = model.generate_content(prompt)
                
                st.subheader("🌍 Latest Information")
                st.write(response.text)
            except Exception as e:
                st.error(f"An error occurred: {str(e)}")
    else:
        st.warning("❗ Please enter a query to search.")