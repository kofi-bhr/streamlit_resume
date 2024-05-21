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
  st.title("📝 Essay Grader")

  #Sidebar Content
  st.sidebar.markdown("# Essay Grader 📝")
  st.sidebar.markdown("### Academic Integrity Note")
  st.sidebar.markdown("Just a friendly reminder that while my app is here to help you proofread and fine-tune your essays, you shouldn’t use it to plagiarize or cut corners. Always get permission from your teacher before using the app, because honesty and academic integrity are super important to me. I'm not responsible for any consequences if the app's misused, but use it right and it can help! :)")
  st.sidebar.markdown("-Kofi")
  
  #GARTHER USER INPUT
  key = st.text_input("What's your OpenAI API key?", placeholder='sk-...')
  essay = st.text_area("Upload your essay")
  assignment_sheet = st.text_area("Upload the assignment sheet")
  exemplar = st.text_area("Upload an exemplar essay")
  desired = st.text_input("What's your desired grade?", placeholder="I want at least a B+, or 88")
  harshness = st.select_slider("Select a hashness level", options=["Easy Grader", "Average Grader", "Slightly Hard Grader", "Extremely Hard Grader", "Impossibly Hard Grader"])
  type = st.selectbox("What type of essay is it?", ("Argumentative (Persuasive)", "Narrative (Personal)", "Descriptive", "Expository"))
  level = st.selectbox("Grade", ("Freshman", "Sophomore", "Junior", "Senior"))
  
  button = st.button("check")

  #LLM CONFIG
  prompt = f"""Please carefully review the following {type} essay (with a harshness level of {harshness}%), which I will provide here: [{essay}]

  Also take into account the following information, if provided:

  Desired Grade: [{desired}]
  Exemplar Essay: [{exemplar}]
  Assignment Sheet: [{assignment_sheet}]

  Remember to grade it like a {type} essay, at the level of a {level} Honors English class.

  First, go through the essay and grade it strictly and granularly according to the rubric or assignment sheet. Provide detailed notes on each sentence and word choice, commenting on how they affect the rubric criteria positively or negatively. 

  Based on this analysis, assign an appropriate letter grade with modifiers if applicable (plus, minus, etc.) and a numerical grade out of 100. Provide a detailed justification referencing specific rubric criteria. Write this rubric-based grade in a “Rubric Grade” section.

  Next, evaluate the essay qualitatively, focusing on the ideas presented, the structure and flow, the maturity of the writing voice, sentence structure, and the overall impression it makes. Assign one of the following grade categories, from best to worst: Outstanding, Exceeds Expectations, Meets Expectations, Approaching Expectations, Acceptable, Poor, Dreadful. Justify your grade with a detailed explanation of your assessment. Put this inside a “Qualitative Grade” section.

  Then, determine the maximum grade the essay could receive if all small mistakes (spelling, grammar, punctuation, etc.) were corrected, without making major changes to the content. Provide this as a letter grade with modifiers and a percentage inside a “Maximum Grade” section.

  Finally, give a detailed line-by-line breakdown of the essay. Quote the original text in a block quote, interspersing your comments every few sentences as an unordered list. Remark on the rubric criteria, qualitative aspects, and correctable errors throughout the essay.

  Format your overall response in markdown like this:

  # Grading

  ## Quantitative Grade

  *Numerical Grade:* [NUMBER GRADE] ([LETTER GRADE])

  [JUSTIFICATION]

  ## Qualitative Grade

  *Qualitative Grade:* [GRADE]

  [JUSTIFICATION]

  ## Maximum Grade

  *Maximum Current Grade:* [GRADE]

  [JUSTIFICATION]

  *Expected Grade After Following Advice:* [GRADE]

  [JUSTIFICATION]

  # Breakdown

  > [LINE FROM ESSAY]
  —--
  - :green[positive comment 1]
  - :green[positive comment 2]
  - :red[constructive comment 1]
  - :red[constructive comment 2]
  - :red[constructive comment 3]
  ```
  Revision
  ```

  > [ANOTHER LINE FROM ESSAY]
  —--
  - :green[positive comment 1]
  - :green[positive comment 2]
  - :red[constructive comment 1]
  - :red[constructive comment 2]
  - :red[constructive comment 3]
  ```
  Revision
  ```

  Remember, be detailed, strict, and harsh in your grading and feedback. Point out every flaw and weakness to help the writer improve. Try to employ about 3 critical comments for every complimentary one, with about 5 comments per section. Be thorough and analytical rather than complimentary. You should also make sure to prioritize useful, specific, actionable feedback in the comments relating back to the exemplar and assignment sheet/rubric.
  
  As for the revisions, make sure to continue using the author's original voice and style, MAKING SURE not to use ANY of the words in the //BAN LIST//. Your revisions should not be shortned or condensed versions of the original text and should maintain all of the elements possible to keep while making as few changes as possible while still employing the advice. Your advice should fall in the "above and beyond" category in grading, and the notes should make the teacher impressed. Be picky and specific.

  BAN LIST:

  //BAN LIST//
  Before generating any text, examine the list below and avoid all cases of these words and phrases: "Informed decisions", "blueprint", "realm", "holistic", "fosters", "informed investment decisions", "informed", "more than just", "it’s about" "navigating", "beacon", "bustling", "treasure trove", "landscape", "tailored", "tailor", “roadmap” , “are more than just”, "tailoring", "dive in", "delving", “streamlining” "dynamic", "robust", "stay tuned", "in conclusion", seamless, bustling, “isn't just”, “not just a”, “isn't merely an”, “cornerstone” “bridge”, “whopping”, “testament”, “paramount” “diving into”, “delve into”, “pivotal” “navigating” “This isn't a”, “isn't just about“ “dives deep”, "It's not just about", “delve”, “harness”, journey”, “elevate”, “maze”, “puzzle”, “overwhelmed", "foster”, and other robotic cliches”
  //BAN LIST//
  """


  #ARI
  def ari(essay):
    words = essay.split()
    sentences = essay.split('. ') + essay.split('! ') + essay.split('? ')
    words_length = sum(len(word.strip('.,!?')) for word in words) / len(words)
    sentences_length = len(words) / len(sentences)
    ari = 4.71 * words_length + 0.5 * sentences_length - 21.43
    return int(ari)
  
  #PLAY
  if button and essay and assignment_sheet and exemplar and desired and key:
      client = OpenAI(api_key=key)
      response = client.chat.completions.create(
      model="gpt-4o",
      messages=[
        {"role": "user", "content": prompt}
      ]
    )
      st.write("### Answer")
      st.write("## Grade: " + str(ari(essay)))
      st.toast('Your Essay is Ready!', icon='👀')
      st.balloons()
      answer = str(response.choices[0].message.content)
      st.write(answer)

if __name__ == "__main__":
    run()
    