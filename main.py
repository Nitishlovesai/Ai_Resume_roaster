import streamlit as st
from dotenv import load_dotenv
import io
import os
import PyPDF2
import google.generativeai as genai


load_dotenv()
st.title("AI RESUME ROASTER")
st.divider()
st.badge('Nitish loves ai')
st.markdown('Upload your resume and lets see how AI will roast your resume')
GEMINI_API_KEY=os.getenv("GEMINI_API_KEY")
genai.configure(api_key=GEMINI_API_KEY)

uploaded_file =st.file_uploader("Upload your resume (pdf & txt only)", type=['pdf', 'txt'])
job_role = st.text_input('Enter a job role that you are targetting')

analyze =st.button("Analayse Resume")
print(analyze)

def Extract_text_pdf(file_bytes):
    reader= PyPDF2.PdfReader(file_bytes)
    return "\n".join(page.extract_text() or "" for page in reader.pages)


def Extract_text(uploaded_file):
    """"Extract text from uploaded pdf of text"""
    file_type = uploaded_file.type
    if file_type == "application/pdf":
        with io.BytesIO(uploaded_file.read()) as file_bytes:
            return Extract_text_pdf(file_bytes)
    elif file_type == "text/plain":
        return uploaded_file.read().decode("utf-8")

if analyze and uploaded_file:
    try:
        file_content = Extract_text(uploaded_file)
        if not file_content.strip():
            st.error("file does not have any content")
            st.stop()
        prompt = f""""you are a brutally honest , no non sense HR expert who is  been reviewing  resume for decades Roast this resume like you are on comdey stage but still
         give some use full insights feedback .Don't hold back - be sarcastic ,witty and critical where needed .
          What would make this resume actually land a job in {job_role} for a good company.
          here is the resume go wild:{file_content}
    make it sting and make sure to keep it in 150 words.
           """

        model =genai.GenerativeModel("models/gemini-1.5-flash")
        response =model.generate_content(prompt)
        st.markdown("Analysis Result")
        st.markdown(response.text)



    except Exception as e:
        st.error("An exception Occured")
         


        