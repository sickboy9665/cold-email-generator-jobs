# __import__('pysqlite3')
# import sys

# sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')
import streamlit as st
from langchain_community.document_loaders import WebBaseLoader
from chains import Chain
from utils import clean_text
import PyPDF2

def extract_text_from_pdf(file):
    try:
        pdf_reader = PyPDF2.PdfReader(file)
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text()
        return text
    except Exception as e:
        st.error(f"Error extracting text from PDF: {e}")
        return ""

def create_streamlit_app(llm, clean_text):
    st.title("📧 Job Application Generator")

    # Input for user details
    with st.form("input_form"):
        st.subheader("Enter your details")
        full_name = st.text_input("Enter your full name:", value="")
        total_experience = st.text_input("Enter your years of experience", placeholder="e.g. 3.7 Years", value="")
        linkedin_url = st.text_input("Enter your LinkedIn Profile URL:", value="")
        url_input = st.text_input("Enter a Careers Page URL:", value="")
        resume_file = st.file_uploader("Upload your resume (PDF only):", type=["pdf"])
        skills_input = st.text_area(
            "Enter your skills (comma-separated):",
            placeholder="e.g., Python, Angular, AI, SQL, Leave blank if already uploaded resume"
        )
        tone = st.selectbox(
            "Select Email Tone:",
            ["Highly Professional", "Mildly Professional", "Humorous", "Casual"]
        )
        submit_button = st.form_submit_button("Save Details")

    # Store user details in session state
    if submit_button:
        if not full_name:
            st.error("Please enter your full name.")
            return

        skills_list = []
        if resume_file:
            resume_text = extract_text_from_pdf(resume_file)
            if resume_text:
                try:
                    skills_list = llm.extract_skills_from_resume(resume_text)
                    st.success(f"Extracted skills from resume: {', '.join(skills_list)}")
                except Exception as e:
                    st.error(f"Error extracting skills from resume: {e}")
        elif skills_input.strip():
            skills_list = [skill.strip() for skill in skills_input.split(',') if skill.strip()]
        else:
            st.error("Please upload a resume or enter your skills manually.")
            return

        st.session_state.user_data = {
            "full_name": full_name,
            "total_experience": total_experience,
            "linkedin_url": linkedin_url,
            "url_input": url_input,
            "skills": skills_list,
            "tone": tone
        }
        st.success("Details saved successfully!")

    # Ensure data is saved before proceeding
    if "user_data" in st.session_state:
        st.subheader("Generate Output")
        output_type = st.radio("Select Output Type:", ["Cold Email", "Cover Letter"])

        if st.button("Generate"):
            user_data = st.session_state.user_data
            try:
                # Load and clean text from the provided URL
                loader = WebBaseLoader([user_data["url_input"]])
                data = clean_text(loader.load().pop().page_content)
                jobs = llm.extract_jobs(data)

                for job in jobs:
                    if output_type == "Cold Email":
                        email = llm.write_mail(
                            job=job,
                            links=[],
                            skillscsv=user_data["skills"],
                            tone=user_data["tone"],
                            full_name=user_data["full_name"],
                            linkedin=user_data["linkedin_url"],
                            experience=user_data["total_experience"]
                        )
                        st.subheader(f"Cold Email for {job.get('role')}")
                        st.code(email, language='markdown')

                    elif output_type == "Cover Letter":
                        cover_letter = llm.generate_cover_letter(
                            job=job,
                            skillscsv=user_data["skills"],
                            full_name=user_data["full_name"],
                            linkedin=user_data["linkedin_url"],
                            experience=user_data["total_experience"]
                        )
                        st.subheader(f"Cover Letter for {job.get('role')}")
                        st.code(cover_letter, language='markdown')
                        # # Placeholder: Add cover letter generation logic
                        # st.subheader(f"Cover Letter for {job.get('role')}")
                        # st.code("Generated cover letter here...", language='markdown')

            except Exception as e:
                st.error(f"An error occurred: {e}")

if __name__ == "__main__":
    chain = Chain()
    st.set_page_config(layout="wide", page_title="Job Application Generator", page_icon="📧")
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

