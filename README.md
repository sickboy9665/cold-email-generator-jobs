## Cold EMAIL Generator For JobSeekers

You can generate Cold Email to send to the hiring managers using Grok AI and some prompts.

Steps to run in local:

1. Clone the repository.
2. Get your grokAPI key, https://console.groq.com/keys
3. Put the key in .env file.
4. In the portfolio.csv you can enter your skills in techstack and your linkedin profile url in links. ## this is for chromadb integration only, SKIP THIS STEP IF YOU DIRECTLY WANT TO TRY!!
5. Create virtual env, install the requirements.txt file.
6. Run the app with streamlit run main.py
7. In UI enter your name, any job posting URL and all the required details. Enter skills manually or upload your resume, it will extract the skills.
8. Click on generate, you will get the options to generate the cold mail or cover letter. Select as per yoru requirement.

It might be helpful for jobseekers who needs some cold emailing for getting job calls....I know its tough nowadays...

If you want to modify some prompt according to your needs, just go to chain.py file and modify the prompt as required :)
