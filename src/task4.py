from langchain.chains.llm import LLMChain
from langchain_core.prompts import PromptTemplate
from langchain_core.documents.base import Document
import os
from langchain_google_genai import GoogleGenerativeAI
from langchain.chains import LLMChain
from MeetGenius_logger import logger
from config.path_manager import path_manager
from dotenv import load_dotenv
load_dotenv()

"""
task 4 : Post-Meeting Summary
- In this task first of all using summary chain that create overall summary of the meeting 
than consequently discussion chain, key decision chain and action items chain 
using unique prompt for each tasks at last combine all and return the combination of all points.
"""

# prompt template for summary
summary_prompt_template = """
You are an expert summarizer. Given the transcript of the entire meeting, 
provide a comprehensive and clear summary without losing the essential context,
Your summary should be detailed and capture the essence of the discussion,
it must be in a single paragraph:

Meeting Transcript:
"{text}"

"""
#prompt template for what was discussed in meeting.
discussion_template = """
You are an AI assistant specialized in identifying and summarizing all discussions made during meetings. 
Based on the provided meeting transcript, 
your task is to:

1. Identify what was discussed during the meeting.
2. Any questions or concerns raised in the meeting
3. Do not include any information explicitly marked as confidential in the transcript


Meeting Transcript:
{meeting_transcript}.
"""

#prompt template for identify key decisions made during the meeting.
key_decision_template = """

You are an AI assistant specialized in identifying and summarizing key decisions made during meetings.
Based on the provided meeting transcript, 
your task is to:

1. Identify all important decisions made during the meeting
2. For each decision, provide clear and concise statement of the decision.
3. The context or problem that led to this decision.(if mentioned in transcript otheriwse do not mention)
4. If no clear decisions were made state that.
5. Do not include any information explicitly marked as confidential in the transcript

Meeting Transcript:
{meeting_transcript}

"""

# prompt template for extracting action items and responsible participants
action_items_template = """
You are an assistant.
your role is to extract and organize action items and the responsible participants from the meeting transcript. 
Please adhere to the following instructions:

1. Carefully review the entire transcript to identify all mentioned or implied action items.
2. For each action item, provide:
   a. A clear, actionable description of the task.
   b. The name or role of the person/persons/team assigned to the task.
3. If an action item is mentioned without a clear assignee, note this as "Assignee: To be determined".
4. If no clear action items were identified state that.
5. Do not include any information explicitly marked as confidential in the transcript.


Meeting Transcript:
{meeting_transcript}

"""



#configure LLM 
google_api_key = os.getenv("GOOGLE_API_KEY")
llm = GoogleGenerativeAI(model="gemini-1.5-flash", api_key=google_api_key)


# reusable function to create LLM chains
def create_llm_chain(template: str, llm_instance, doc_var_name="meeting_transcript"):
    prompt_template = PromptTemplate(
        input_variables=[doc_var_name], 
        template=template
    )
    return LLMChain(llm=llm_instance, prompt=prompt_template)

# reusable function to load the meeting transcript
def load_meeting_transcript(file_path) -> Document:
  
    with open(file_path, 'r') as file:
        meeting_transcript = file.read()
    logger.info("meeting transcipt loaded")
    return Document(page_content=meeting_transcript)


# function to run LLM chain for different tasks 
def run_llm_task(llm_chain, meeting_transcript):
    return llm_chain.run(meeting_transcript)


# Create the LLM Chains for each task
summary_chain = create_llm_chain(summary_prompt_template, llm, doc_var_name="text")
discussion_chain = create_llm_chain(discussion_template, llm)
decision_chain = create_llm_chain(key_decision_template, llm)
action_items_chain = create_llm_chain(action_items_template, llm)


def generate_meeting_insights(file_path):
    """
    this function invoke each chain in consequently to get response from LLM.
    """
    meeting_transcript = load_meeting_transcript(file_path)

    # Run each chain and get results
    summary = run_llm_task(summary_chain, meeting_transcript)
    discussion_points = run_llm_task(discussion_chain, meeting_transcript)
    key_decisions = run_llm_task(decision_chain, meeting_transcript)
    action_items = run_llm_task(action_items_chain, meeting_transcript)

    logger.info("all components of summary generated")
    return summary, discussion_points, key_decisions, action_items

def generate_detailed_summary():
    """
    Main function to generate summary along with other points and return the comprehensive summary of the meeting.
    """

    meeting_transcript_path = path_manager.meeting_transcript
    summary, discussion_points, key_decisions, action_items = generate_meeting_insights(meeting_transcript_path)
    
    return f"{summary} \n\n {discussion_points} \n\n {key_decisions} \n\n {action_items}"

