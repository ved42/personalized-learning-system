import streamlit as st
import json
from langchain_groq import ChatGroq
from langchain.prompts import PromptTemplate
from dotenv import load_dotenv
import os
import yaml

load_dotenv()

# 🔐 Set your API key here
GROQ_API_KEY = os.getenv("GROQ_API_KEY")


# === LOAD PROMPTS FROM YAML ===
def load_prompts(filepath="prompt.yaml"):
    with open(filepath, "r") as f:
        return yaml.safe_load(f)

prompts = load_prompts()

# 🔧 LLM Setup
llm = ChatGroq(groq_api_key=GROQ_API_KEY, model=os.getenv("MODEL"))

# Define templates using prompts from YAML
profile_prompt = PromptTemplate.from_template(prompts["profile_prompt"])
plan_prompt = PromptTemplate.from_template(prompts["plan_prompt"])

# === STREAMLIT UI ===

st.set_page_config(page_title="AI Learning Plan Generator", page_icon="🎓")
st.title("🎓 AI Learning Plan Generator")
st.markdown("Describe yourself, and get a personalized AI learning roadmap!")

user_input = st.text_area("🗣️ Tell me about yourself and your AI learning goals:", height=150)

if st.button("Generate Learning Plan"):
    if not user_input.strip():
        st.warning("Please enter something about yourself.")
        st.stop()

    with st.spinner("🔍 Analyzing your profile..."):
        try:
            profile_response = llm.invoke(profile_prompt.format(user_input=user_input))
            profile_json = json.loads(profile_response.content)
            st.success("✅ Profile extracted!")
            st.subheader("🧠 Your Learning Profile")
            st.json(profile_json)
        except Exception as e:
            st.error(f"❌ Failed to parse profile. Error: {e}")
            st.stop()

    with st.spinner("📚 Creating your personalized learning plan..."):
        try:
            plan_response = llm.invoke(plan_prompt.format(profile=json.dumps(profile_json, indent=2)))
            plan_json = json.loads(plan_response.content)
            st.success("✅ Learning Plan Ready!")
            st.subheader("📅 4-Week Personalized Learning Plan")

            for week in plan_json["learning_plan"]:
                st.markdown(f"### Week {week['week']}")
                st.markdown(f"**Topics:** {', '.join(week['topics'])}")
                st.markdown(f"**Resources:** {', '.join(week['resources'])}")
                st.markdown(f"**Project:** {week['project']}")
                st.markdown("---")

        except Exception as e:
            st.error(f"❌ Failed to parse learning plan. Error: {e}")
