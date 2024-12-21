import os
import streamlit as st
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.exceptions import OutputParserException
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Chain:
    def __init__(self):
        self.llm = ChatGroq(
            temperature=0,
            groq_api_key=os.getenv("GROQ_API_KEY"),
            model_name="llama-3.1-70b-versatile"
        )

    def extract_jobs(self, cleaned_text):
        prompt_extract = PromptTemplate.from_template(
            """
            ### SCRAPED TEXT FROM WEBSITE:
            {page_data}
            ### INSTRUCTION:
            The scraped text is from the careers page of a website.
            Your job is to extract the job postings and return them in JSON format containing the following keys: `role`, `experience`, `skills`, and `description`.
            Only return the valid JSON.
            ### VALID JSON (NO PREAMBLE):
            """
        )
        chain_extract = prompt_extract | self.llm
        res = chain_extract.invoke(input={"page_data": cleaned_text})
        try:
            json_parser = JsonOutputParser()
            res = json_parser.parse(res.content)
        except OutputParserException:
            raise OutputParserException("Context too big. Unable to parse jobs.")
        return res if isinstance(res, list) else [res]

    def write_mail(self, job, links, skillscsv, tone, full_name):
        prompt_tone_mapping = {
            "Highly Professional": "Maintain a formal tone, emphasizing professionalism and precision.",
            "Mildly Professional": "Use a friendly and approachable tone while staying professional.",
            "Humorous": "Add a light touch of humor to make the email stand out while remaining appropriate.",
            "Casual": "Adopt a conversational and relaxed tone to make the email feel personal."
        }

        selected_tone_instruction = prompt_tone_mapping.get(tone, "Maintain a formal tone.")

        prompt_email = PromptTemplate.from_template(
            f"""
            ### JOB DESCRIPTION:
            {{job_description}}
            
            ### INSTRUCTION:
            You are a job seeker with 3.6 years of experience in your field, writing an email in the following tone: {selected_tone_instruction}.
            Highlight your relevant skills: {{skillscsv}}, and experiences that directly align with the job description, showcasing your ability to contribute effectively to the company's goals. 
            Mention that you can be reached on LinkedIn: {{link_list}}.
            Conclude the email with one sign-off, either "Best regards" or "Thanks and regards," followed by: "{{full_name}}".
            Avoid using multiple sign-offs in the email.
            ### EMAIL (NO PREAMBLE):
            """
        )

        chain_email = prompt_email | self.llm
        res = chain_email.invoke({
            "job_description": str(job),
            "link_list": links,
            "skillscsv": skillscsv,
            "full_name": full_name
        })
        return res.content



# import os
# from langchain_groq import ChatGroq
# from langchain_core.prompts import PromptTemplate
# from langchain_core.output_parsers import JsonOutputParser
# from langchain_core.exceptions import OutputParserException
# from dotenv import load_dotenv

# load_dotenv()
# print(os.getenv("GROQ_API_KEY"))
# class Chain:
#     def __init__(self):
#         self.llm = ChatGroq(temperature=0, groq_api_key=os.getenv("GROQ_API_KEY"), model_name="llama-3.1-70b-versatile")

#     def extract_jobs(self, cleaned_text):
#         prompt_extract = PromptTemplate.from_template(
#             """
#             ### SCRAPED TEXT FROM WEBSITE:
#             {page_data}
#             ### INSTRUCTION:
#             The scraped text is from the career's page of a website.
#             Your job is to extract the job postings and return them in JSON format containing the following keys: `role`, `experience`, `skills` and `description`.
#             Only return the valid JSON.
#             ### VALID JSON (NO PREAMBLE):
#             """
#         )
#         chain_extract = prompt_extract | self.llm
#         res = chain_extract.invoke(input={"page_data": cleaned_text})
#         try:
#             json_parser = JsonOutputParser()
#             res = json_parser.parse(res.content)
#         except OutputParserException:
#             raise OutputParserException("Context too big. Unable to parse jobs.")
#         return res if isinstance(res, list) else [res]

#     def write_mail(self, job, links, skillscsv):
#         prompt_email = PromptTemplate.from_template(
#         """
#         ### JOB DESCRIPTION:
#         {job_description}
        
#         ### INSTRUCTION:
#         You are a job seeker with 3.6 years of experience in your field, writing a professional yet personable email to the hiring manager for the above-mentioned position. 
#         Highlight your relevant skills: {skillscsv}, and experiences that directly align with the job description, showcasing your ability to contribute effectively to the company's goals. 
#         Be concise and professional, while maintaining a friendly tone. Mention that you can be reached on LinkedIn: {link_list}.
#         The email should feel genuine, focusing on how your skills can meet the organization's needs without over-exaggerating.
#         ### EMAIL (NO PREAMBLE):
#         """
#         )

        
#         chain_email = prompt_email | self.llm
#         res = chain_email.invoke({"job_description": str(job), "link_list": links, "skillscsv": skillscsv})
#         return res.content

# if __name__ == "__main__":
#     print(os.getenv("GROQ_API_KEY"))