# __import__('pysqlite3')
# import sys

# sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')
import streamlit as st
from langchain_community.document_loaders import WebBaseLoader

from chains import Chain
from portfolio import Portfolio
from utils import clean_text

def create_streamlit_app(llm, portfolio, clean_text):
    st.title("📧 Cold Mail Generator")
    
    # Input for full name
    full_name = st.text_input("Enter your full name:", value="")
    
    linkedinUrl = st.text_input("Enter your LinkedIn Profile URL:", value="")
    
    # Input for URL
    url_input = st.text_input("Enter a Careers Page URL:", value="")
    
    # Tone selection dropdown
    tone = st.selectbox(
        "Select Email Tone:",
        ["Highly Professional", "Mildly Professional", "Humorous", "Casual"]
    )
    
    # Submit button
    submit_button = st.button("Generate Emails")
    
    if submit_button:
        if not full_name:
            st.error("Please enter your full name.")
            return
        
        try:
            # Load the webpage and clean the text
            loader = WebBaseLoader([url_input])
            data = clean_text(loader.load().pop().page_content)
            
            # Load portfolio and extract jobs
            portfolio.load_portfolio()
            jobs = llm.extract_jobs(data)
            skillsCsv = portfolio.getSkills()
            linkincsv = portfolio.getlinks()
            for job in jobs:
                # Query links and generate email
                skills = job.get('skills', [])
                links = portfolio.query_links(skills)
                email = llm.write_mail(job, linkincsv, skillsCsv, tone, full_name,linkedinUrl)
                
                # Display the email
                st.subheader(f"Email for {job.get('role')}")
                st.code(email, language='markdown')
                
                # Provide editing option
                # edited_email = st.text_area(f"Edit the Email for {job.get('role')}:", value=email, height=300)
                # if st.button(f"Save Email for {job.get('role')}"):
                #     st.success(f"Email for {job.get('role')} saved!")
        except Exception as e:
            st.error(f"An Error Occurred: {e}")

if __name__ == "__main__":
    chain = Chain()
    portfolio = Portfolio()  # Make sure to implement or import Portfolio
    st.set_page_config(layout="wide", page_title="Cold Email Generator", page_icon="📧")
    create_streamlit_app(chain, portfolio, clean_text)

# def create_streamlit_app(llm, portfolio, clean_text):
#     st.title("📧 Cold Mail Generator")
#     url_input = st.text_input("Enter a URL:", value="")
#     submit_button = st.button("Submit")

#     if submit_button:
#         try:
#             loader = WebBaseLoader([url_input])
#             data = clean_text(loader.load().pop().page_content)
#             portfolio.load_portfolio()
#             jobs = llm.extract_jobs(data)
#             skillsCsv = portfolio.getSkills()
#             for job in jobs:
#                 skills = job.get('skills', [])
#                 links = portfolio.query_links(skills)
#                 email = llm.write_mail(job, links,skillsCsv)
#                 st.code(email, language='markdown')
#         except Exception as e:
#             st.error(f"An Error Occurred: {e}")


# if __name__ == "__main__":
#     chain = Chain()
#     portfolio = Portfolio()
#     st.set_page_config(layout="wide", page_title="Cold Email Generator", page_icon="📧")
#     create_streamlit_app(chain, portfolio, clean_text)

