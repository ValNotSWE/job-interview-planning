import openai
import requests
from bs4 import BeautifulSoup
import streamlit as st

# Extract job details
def extract_job_details(job_url):
    response = requests.get(job_url)
    soup = BeautifulSoup(response.text, 'html.parser')
    job_title = soup.find('h1').text if soup.find('h1') else "Unknown Title"
    job_description = soup.find('div', class_='description')
    job_text = job_description.text.strip() if job_description else "No description available"
    return job_title, job_text

# Generate interview questions
def generate_interview_questions(job_title, job_text, interviewers):
    prompt = f"""
    Based on the following job title and description, generate interview questions for each stage of the hiring process.
    
    **Job Title:** {job_title}
    **Job Description:** {job_text}
    
    **Interview Stages:**
    {interviewers}

    **Greenhouse Scorecard Format:**
    **Core Competencies:**
    - (List questions here)

    **Attributes & Soft Skills:**
    - (List questions here)

    **Technical/Functional Skills (if applicable):**
    - (List questions here)

    **Overall Recommendation:**
    - (List questions here)

    Include follow-up probing questions for deeper assessment.
    """

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are an AI assistant specialized in generating interview questions based on Greenhouse scorecard categories."},
            {"role": "user", "content": prompt}
        ]
    )
    
    return response["choices"][0]["message"]["content"]

# Streamlit UI
def main():
    st.title("Job Interview Planning Tool")
    
    job_url = st.text_input("Enter the job posting URL:")
    interviewers = st.text_area("Enter interviewer details (Name - Stage):")

    if st.button("Generate Interview Questions"):
        if job_url:
            job_title, job_text = extract_job_details(job_url)
            interview_questions = generate_interview_questions(job_title, job_text, interviewers)
            st.subheader("Generated Interview Questions (Greenhouse Format):")
            st.text_area("Questions", value=interview_questions, height=400)
        else:
            st.warning("Please enter a job posting URL.")

if __name__ == "__main__":
    main()
