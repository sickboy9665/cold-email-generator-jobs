# __import__('pysqlite3')
# import sys

# sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')
import streamlit as st
from langchain_community.document_loaders import WebBaseLoader
from chains import Chain
from utils import clean_text

def create_streamlit_app(llm, clean_text):
    st.title("📧 Cold Mail Generator")
    
    # Input for full name
    full_name = st.text_input("Enter your full name:", value="")
    
    # Input for LinkedIn Profile URL
    linkedin_url = st.text_input("Enter your LinkedIn Profile URL:", value="")
    
    # Input for URL of careers page
    url_input = st.text_input("Enter a Careers Page URL:", value="")
    
    # Input skills manually
    skills_input = st.text_area(
        "Enter your skills (comma-separated):",
        placeholder="e.g., Python, Angular, AI, SQL",
    )
    
    # Email tone selection
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
        
        if not skills_input.strip():
            st.error("Please enter your skills.")
            return
        
        try:
            # Load and clean text from the provided URL
            loader = WebBaseLoader([url_input])
            data = clean_text(loader.load().pop().page_content)
            
            # Extract jobs from the careers page
            jobs = llm.extract_jobs(data)
            
            # Parse skills from user input
            skills_list = [skill.strip() for skill in skills_input.split(',') if skill.strip()]
            
            for job in jobs:
                # Generate email for each job
                email = llm.write_mail(
                    job=job,
                    links=[],
                    skillscsv=skills_list,
                    tone=tone,
                    full_name=full_name,
                    linkedin=linkedin_url,
                )
                
                # Display the email
                st.subheader(f"Email for {job.get('role')}")
                st.code(email, language='markdown')
        except Exception as e:
            st.error(f"An error occurred: {e}")

if __name__ == "__main__":
    chain = Chain()
    st.set_page_config(layout="wide", page_title="Cold Email Generator", page_icon="📧")
    create_streamlit_app(chain, clean_text)


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

