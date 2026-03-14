import streamlit as st
import requests


st.title("Career Recommendation System")
st.write("Enter your skills to get career suggestions")

skills_input = st.text_input(
    "Enter skills (comma separated)",
    "Programming, Mathematics"
)

if st.button("Get Recommendations"):

    skills = [skill.strip() for skill in skills_input.split(",")]

    response = requests.post(
        "http://16.112.59.48:8000/recommend",
        json={"skills": skills}
    )

    if response.status_code == 200:

        careers = response.json()["recommended_careers"]

        st.subheader("Recommended Careers")

        for career in careers:
            st.write("•", career)