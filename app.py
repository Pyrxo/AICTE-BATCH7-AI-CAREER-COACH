import streamlit as st
import os
from openai import OpenAI # Import the OpenAI class

st.title('AI Career Roadmap Generator')

st.header('Enter Your Career Details:')

current_role = st.text_input('Current Role', 'Data Analyst')
desired_role = st.text_input('Desired Role', 'AI/ML Engineer')
experience_level = st.selectbox(
    'Experience Level',
    ('Entry-Level', 'Junior', 'Mid-Level', 'Senior', 'Lead/Principal')
)

generate_button_clicked = st.button('Generate Roadmap')

if generate_button_clicked:
    st.write("Generating your personalized AI career roadmap...")

    # Construct the prompt for the AI model with structured output request
    prompt = f"""
    Generate a personalized AI career roadmap, weekly plan, and skill gap analysis
    for an individual with the following details:
    - Current Role: {current_role}
    - Desired Role: {desired_role}
    - Experience Level: {experience_level}

    Please provide the output in the following structured markdown format, with each section clearly delimited:

    ### Career Roadmap
    [Content for comprehensive career roadmap with key milestones and recommended resources]

    ### Weekly Plan
    [Content for a sample weekly learning plan]

    ### Skill Gap Analysis
    [Content for a detailed skill gap analysis, highlighting essential skills for the desired role and suggesting ways to acquire them]
    """

    # Initialize OpenAI client
    openai_api_key = os.environ.get("AIzaSyCobo49evfptqhMlXGWjFZyMVDvbRaN5tw")
    if not openai_api_key:
        st.error("OpenAI API key not found. Please set the OPENAI_API_KEY environment variable.")
        print("Error: OPENAI_API_KEY environment variable is not set. Please set it before running this cell if you intend to generate a roadmap.")
    else:
        client = OpenAI(api_key=openai_api_key)

        try:
            # Call the OpenAI API
            response = client.chat.completions.create(
                model="gpt-3.5-turbo", # Or "gpt-4" if available and preferred
                messages=[
                    {"role": "system", "content": "You are a helpful AI career coach that provides structured advice."},
                    {"role": "user", "content": prompt}
                ]
            )

            ai_response_content = response.choices[0].message.content

            # Parse the content into sections
            # Define the headers expected in the LLM response
            roadmap_header = "### Career Roadmap"
            weekly_plan_header = "### Weekly Plan"
            skill_gap_header = "### Skill Gap Analysis"

            career_roadmap_content = ""
            weekly_plan_content = ""
            skill_gap_analysis_content = ""

            # Split the response content by headers
            parts = ai_response_content.split(roadmap_header)
            if len(parts) > 1:
                roadmap_and_rest = parts[1]
                parts_wp = roadmap_and_rest.split(weekly_plan_header)
                career_roadmap_content = parts_wp[0].strip()

                if len(parts_wp) > 1:
                    weekly_plan_and_rest = parts_wp[1]
                    parts_sg = weekly_plan_and_rest.split(skill_gap_header)
                    weekly_plan_content = parts_sg[0].strip()

                    if len(parts_sg) > 1:
                        skill_gap_analysis_content = parts_sg[1].strip()

            # Display the parsed sections
            if career_roadmap_content:
                st.subheader("Career Roadmap")
                st.markdown(career_roadmap_content)

            if weekly_plan_content:
                st.subheader("Weekly Plan")
                st.markdown(weekly_plan_content)

            if skill_gap_analysis_content:
                st.subheader("Skill Gap Analysis")
                st.markdown(skill_gap_analysis_content)

            if not (career_roadmap_content or weekly_plan_content or skill_gap_analysis_content):
                st.warning("Could not parse the AI response into distinct sections. Displaying raw response:")
                st.markdown(ai_response_content)

        except Exception as e:
            st.error(f"An error occurred while generating the roadmap: {e}")
            st.info("Please ensure your OpenAI API key is correctly set.")

else:
    st.write("Enter your details and click 'Generate Roadmap' to get started!")
