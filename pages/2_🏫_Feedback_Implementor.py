#Initials
import streamlit as st
import streamlit as st
from streamlit.logger import get_logger
from openai import OpenAI

LOGGER = get_logger(__name__)

#Run
def run():
  
  #CONFIGURE/SET UP PAGE
  st.set_page_config(
        page_title="Essay Grader by Kofi Hair-Ralston",
        page_icon="memo",
        layout="wide",
    )
  st.title("📝 Essay Feedback Implementator")

  #Sidebar Content
  st.sidebar.markdown("# Essay Feedback 📝")
  st.sidebar.markdown("### Academic Integrity Note")
  st.sidebar.markdown("Just a friendly reminder that while my app is here to help you fine-tune your essays, you shouldn’t use it to plagiarize or cut corners. Always get permission from your teacher before using the app, because honesty and academic integrity are super important to me. I'm not responsible for any consequences if the app's misused, but use it right and it can help! :)")
  st.sidebar.markdown("-Kofi")
  
  #GARTHER USER INPUT
  key = st.text_input("What's your OpenAI API key?", placeholder='sk-...')
  essay = st.text_area("Upload your essay")
  level = st.selectbox("Grade", ("Freshman", "Sophomore", "Junior", "Senior"))
  feedback = st.text_area("Upload your Teacher's Feedback", placeholder='My teacher said to...')
  ideas = st.text_area("Upload your Implementing Ideas", placeholder="I think I'll...")
  button = st.button("check")

  #LLM CONFIG
  prompt = f"""Here is the essay to revise:
  {essay}
  </essay>

  Here is the teacher's feedback on the essay:
  <feedback>
  {feedback}
  </feedback>

  The feedback level specified by the teacher is:
  <feedback_level>
  {level}
  </feedback_level>

  Ideas that the user is thinking of implementing:
  <ideas>
  {ideas}
  </ideas>

  Please read the essay and feedback carefully. Then, in a "Brainstorming" heading, brainstorm some ideas for how to implement the teacher's feedback in the essay revision. Make sure to take into account the feedback level - aim for changes that match the specified level, whether that's basic implementation, deeper exploration of the feedback, or going above and beyond.

  Next, lay out a clear, step-by-step plan for revising the essay based on the feedback you analyzed and the ideas you brainstormed. The plan should be thorough and include specific examples of changes to make. Tailor it to the specified feedback level.

  Finally, write out the full guide for implementing the feedback in the essay revision. Format the guide in Markdown (you can use headings, bullet points, bold/italic for emphasis, etc). The guide should expand on each step of your action plan with detailed explanations and concrete examples. Remember to gear the guide towards the specified feedback level throughout.

  To summarize:
  - Carefully analyze the essay, feedback, and feedback level 
  - Brainstorm implementation ideas in Markdown, wih a line above and below
  - Create a step-by-step action plan in Markdown
  - Write out the full Markdown guide, tailored to the feedback level

  Focus on providing a helpful, actionable, and easy-to-follow guide for the essay writer to implement the feedback effectively at the level their teacher specified, with specific examples.
  """
  
  #PLAY
  if button and essay and feedback and level and ideas and key:
      client = OpenAI(api_key=key)
      response = client.chat.completions.create(
      model="gpt-4o",
      messages=[
        {"role": "user", "content": prompt}
      ]
    )
      st.write("### Revision Ideas ⤵️")
      st.toast('Your Ideas are Ready!', icon='👀')
      st.balloons()
      answer = str(response.choices[0].message.content)
      st.write(answer)

if __name__ == "__main__":
    run()
    