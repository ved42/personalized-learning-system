import streamlit as st
import json
from langchain_groq import ChatGroq
from langchain.prompts import PromptTemplate
from dotenv import load_dotenv
import os

load_dotenv()

# 🔐 Set your API key here
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# 🔧 LLM Setup
llm = ChatGroq(groq_api_key=GROQ_API_KEY, model="llama-3.1-8b-instant")

# Prompt 1: Convert user input to structured profile
profile_prompt = PromptTemplate.from_template("""
A student wants to learn AI. Here's their message:

"{user_input}"

Extract the following fields in JSON:
- goal
- background (math, coding, ai_knowledge)
- learning_style
- time_per_week
Return only the JSON.
""")

# Prompt 2: Generate learning plan from structured profile
plan_prompt = PromptTemplate.from_template("""
You are an expert AI tutor. A student wants to learn Artificial Intelligence. Here's their profile:

{profile}

Generate a 4-week personalized learning plan in **valid JSON only**, in this format:

{{
  "learning_plan": [
    {{
      "week": 1,
      "topics": ["Topic 1", "Topic 2"],
      "resources": ["Resource 1", "Resource 2"],
      "project": "Mini project idea here"
    }},
    ...
  ]
}}

✅ Return ONLY the JSON. Do not include explanations or notes.
""")

# Streamlit UI
st.title("🎓 AI Learning Path Generator")

user_input = st.text_area("Tell me about yourself and your AI learning goals:")

if st.button("Generate Learning Plan"):
    with st.spinner("Analyzing your profile..."):
        # Step 1: Create structured profile
        profile_response = llm.invoke(profile_prompt.format(user_input=user_input))
        try:
            profile_json = json.loads(profile_response.content)
            st.subheader("🧠 Detected Learning Profile")
            st.json(profile_json)
        except:
            st.error("❌ Couldn't parse the profile. Try again or change input.")
            st.stop()

    with st.spinner("Creating your personalized learning plan..."):
        # Step 2: Generate learning plan
        plan_response = llm.invoke(plan_prompt.format(profile=json.dumps(profile_json, indent=2)))
        try:
            plan_json = json.loads(plan_response.content)
            st.subheader("📚 Personalized 4-Week Learning Plan")
            for week in plan_json["learning_plan"]:
                st.markdown(f"### Week {week['week']}")
                st.markdown(f"**Topics:** {', '.join(week['topics'])}")
                st.markdown(f"**Resources:** {', '.join(week['resources'])}")
                st.markdown(f"**Project:** {week['project']}")
                st.markdown("---")
        except:
            st.error("❌ Couldn't parse the learning plan.")
