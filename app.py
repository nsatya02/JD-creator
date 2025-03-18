import streamlit as st
from groq import Groq
from datetime import datetime

client = Groq(api_key=st.secrets["api_key"])

# Custom CSS for better styling
st.markdown("""
<style>
    .header {
        font-size: 24px !important;
        color: #2E86C1;
        margin-bottom: 20px;
    }
    .stTextInput>div>div>input, .stTextArea>div>div>textarea {
        background-color: #FBFCFC;
        border: 1px solid #AED6F1;
    }
    .stButton>button {
        background-color: #2E86C1 !important;
        color: white !important;
        border: none;
        padding: 10px 24px;
        border-radius: 5px;
    }
</style>
""", unsafe_allow_html=True)

def generate_job_description(role, skills, experience_level, years_experience=None, company_name=None, location=None):
    """Generate JD using GPT with structured prompt engineering"""

    exp_section = ""
    if experience_level == "Experienced" and years_experience:
        exp_section = f"Require {years_experience}+ years of relevant experience\n"
    
    base_prompt = f"""
    Create a professional job description for a {role} position with these requirements:
    
    1. Target Experience Level: {experience_level}
    {f"2. Minimum Experience Required: {years_experience}+ years" if years_experience else ""}
    3. Key Skills Required: {skills}
    {f"4. Company Name: {company_name}" if company_name else ""}
    {f"5. Location: {location}" if location else ""}

    Structure with these sections:
    - Job Title (include seniority based on experience)
    - Company Overview
    BeamX TechLabs Pvt Ltd. is a leading technology company specialised in software development and IT
    solutions. With a focus on innovation and cutting-edge technologies, we strive to provide exceptional
    solutions to our clients across various industries. Join our dynamic team and contribute to the
    development of groundbreaking software applications
    - Position Summary
    - Key Responsibilities (include experience-specific tasks if applicable)
    - Required Skills and Qualifications ({exp_section}include specific experience requirements)
    - Preferred Qualifications
    - Education Requirements
    - Compensation and Benefits (adjust based on experience level)
    - How to Apply

    Make it professional but modern. Use bullet points for lists.
    Include industry-specific terminology for {role}.
    """
    
    try:
        response = client.chat.completions.create(
            model="gemma2-9b-it",
            messages=[
                {"role": "system", "content": "You are a professional HR manager with 20 years of experience in creating job descriptions."},
                {"role": "user", "content": base_prompt}
            ],
            temperature=0.7,
            max_tokens=1000
        )
        return response.choices[0].message.content
    except Exception as e:
        st.error(f"Error generating job description: {str(e)}")
        return None

def main():
    st.markdown("""
    <style>
        .header {
            font-size: 24px !important;
            color: #2E86C1;
            margin-bottom: 20px;
        }
    </style>
    """, unsafe_allow_html=True)
    
    st.markdown('<div class="header">🚀 Job Description Creator</div>', unsafe_allow_html=True)
    
    # Initialize session state
    if 'experience_level' not in st.session_state:
        st.session_state.experience_level = "Fresher"
    
    # Experience selector outside the form for immediate update
    st.session_state.experience_level = st.radio(
        "Experience Level*",
        ("Fresher", "Experienced"),
        horizontal=True,
        key="exp_radio"
    )
    
    with st.form(key='jd_form'):
        col1, col2 = st.columns(2)
        with col1:
            role = st.text_input("Job Role/Title*", placeholder="e.g., Software Engineer")
            company_name = st.text_input("Company Name (optional)", placeholder="Acme Corp")
            
        with col2:
            # Show slider only for experienced candidates
            if st.session_state.experience_level == "Experienced":
                years_experience = st.slider(
                    "Years of Experience Required",
                    min_value=1, 
                    max_value=20,
                    value=5,
                    help="Select minimum years of experience required"
                )
            else:
                years_experience = None
                
            location = st.text_input("Location (optional)", placeholder="New York, NY")
        
        skills = st.text_area(
            "Required Skills*", 
            placeholder="List key skills separated by commas\n"
                      "Example: Python, Machine Learning, SQL, Data Analysis",
            height=100
        )
        
        submitted = st.form_submit_button("Generate Job Description")
    
    if submitted:
        # Rest of the code remains the same...
        if not role or not skills:
            st.warning("Please fill required fields (Role and Skills)")
            return
        
        with st.spinner(f"Creating {st.session_state.experience_level} JD..."):
            jd = generate_job_description(
                role=role,
                skills=skills,
                experience_level=st.session_state.experience_level,
                years_experience=years_experience,
                company_name=company_name,
                location=location
            )
        
        if jd:
            st.success("✅ Professional Job Description Created")
            st.markdown("---")
            st.markdown(jd)
            
            # Download functionality
            timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
            exp_suffix = f"_{years_experience}yoe" if years_experience else ""
            filename = f"{role.replace(' ', '_')}{exp_suffix}_{timestamp}.txt"
            
            st.download_button(
                label="Download JD",
                data=jd,
                file_name=filename,
                mime="text/plain"
            )

if __name__ == "__main__":
    main()


# "---------------"
# '''
# Advanced Improvements You Can Add:

# Add tone selection (Formal/Casual/Startup-style)

# Include salary range suggestions

# Add multilingual support

# Implement JD quality scoring

# Add company branding options (logo upload)

# Include diversity and inclusion statements

# Add equal opportunity employer sections

# Implement rate limiting for API calls
# '''
