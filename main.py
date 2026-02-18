# import streamlit as st 
# import PyPDF2
# import io
# import os
# from openai import OpenAI
# from dotenv import load_dotenv

# load_dotenv()

# st.set_page_config(page_title="at resume checker", page_icon="0", layout="centered")
# st.title("ai resume")
# st.markdown("upload your resume")

# OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

# uploaded_file = st.file_uploader("Upload your resume (pdf or txt)", type=["pdf","txt"])
# job_role = st.text_input("enter the job role that you applied(optional):-- ")
# analyze = st.button("analyze resume")

# def extract_text_from_pdf(pdf_file):
#     pdf_reader = PyPDF2.PdfReader(pdf_file)
#     text = " "
#     for page in pdf_reader.pages:
#         text += page.extract_text() + "\n"
#     return text

# def extract_text_from_file(uploaded_file):
#     if uploaded_file.type == "application/pdf":
#         return extract_text_from_pdf(io.BytesIO(uploaded_file.read()))
#     return uploaded_file.read().decode("utf-8")

# if analyze and uploaded_file:
#     try:
#         file_content = extract_text_from_file(uploaded_file)

#         if not file_content.strip():
#             st.error("files does not have any content")
#             st.stop()
        
#         prompt = f"""Please analyze this resume and provide constructive feedback.
#         Focus on the following aspects:
#         1. Content clarity and impact
#         2. Skills presentation
#         3. Experience descriptions
#         4. Specific improvements for {job_role if job_role else 'general job applications'}
#         Resume content:
#         {file_content}

#         Please provide your analysis in a clear, structured format with specific recommendation"""

#         client = OpenAI(api_key=OpenAI_API_KEY)
#         response = client.chat.completions.create(
#             model="gpt-4o-mini",
#             messages=[
#                 {"role" : "system", "content" : "you are an expert resume reviwe with years of experience in  hr and recuritor"},
#                 {"role" : "user", "content" : prompt}
#              ],
#              temperature=0.7,
#              max_tokens=1000
#         )
#         st.markdown("###analysis results")
#         st.markdown(response.choices[0].message.content)

#     except Exception as e:
#         st.error(f"an error occur:{str(e)}")

import streamlit as st
import PyPDF2
import io
import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(page_title="AI Resume Checker", page_icon="📄", layout="centered")
st.title("AI Resume Checker")
st.markdown("Upload your resume")

# Correct environment variable name
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

uploaded_file = st.file_uploader("Upload your resume (pdf or txt)", type=["pdf", "txt"])
job_role = st.text_input("Enter the job role you applied for (optional):")
analyze = st.button("Analyze Resume")


def extract_text_from_pdf(pdf_file):
    pdf_reader = PyPDF2.PdfReader(pdf_file)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text() or ""
    return text


def extract_text_from_file(uploaded_file):
    if uploaded_file.type == "application/pdf":
        return extract_text_from_pdf(uploaded_file)
    return uploaded_file.read().decode("utf-8")


if analyze and uploaded_file:
    try:
        file_content = extract_text_from_file(uploaded_file)

        if not file_content.strip():
            st.error("File does not contain any content.")
            st.stop()

        prompt = f"""
        Please analyze this resume and provide constructive feedback.

        Focus on:
        1. Content clarity and impact
        2. Skills presentation
        3. Experience descriptions
        4. Specific improvements for {job_role if job_role else 'general job applications'}

        Resume content:
        {file_content}

        Provide analysis in a clear structured format.
        """

        
        client = OpenAI(
            api_key=OPENROUTER_API_KEY,
            base_url="https://openrouter.ai/api/v1"
        )

        response = client.chat.completions.create(
            model="openai/gpt-4o-mini",  
            messages=[
                {"role": "system", "content": "You are an expert resume reviewer with years of HR and recruiting experience."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=1000
        )

        st.markdown("### Analysis Results")
        st.markdown(response.choices[0].message.content)

    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
