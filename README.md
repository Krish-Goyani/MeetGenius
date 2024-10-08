<br />
<p align="center">
	<img src="./assets/logo.jpg" alt="Logo" width="400">
	<h1 align="center">MeetGenius</h1>

  <p align="center">
    Intelligent Meeting Lifecycle Platform
    <br/>
  </p>
</p>

This tool streamlines the process of managing meetings by leveraging generative AI and traditional development methods. It handles pre-meeting document management, organizes discussion points, tracks meeting progress, and generates comprehensive post-meeting summaries. The project utilizes Python, Langchain, Streamlit, and several other components to offer efficient meeting workflows.

<!-- TABLE OF CONTENTS -->
## Table of Contents
<details open="open">
  
  <ol>
    <li>
      <a href="#Setup-Instructionsn">Setup Instructions</a>
    </li>
    <li>
      <a href="#Usage-Guidelines">Usage Guidelines</a>
    </li>
    <li>
      <a href="#System-Architecture">System Architecture</a>
    </li>
    <li>
      <a href="#Dependencies">Dependencies</a>
    </li>
  </ol>
</details>

## Setup Instructions

### Prerequisites
- **Python**: Make sure you have Python 3.11.3 installed on your machine.
- **API Keys**: You need the following API keys:
  - **Gemini LLM**: Get this from [Gemini API](https://ai.google.dev/).
  - **Pinecone Vector Database**: Create an account on [Pinecone](https://www.pinecone.io/) and obtain your API key.

### Environment Setup
1. **Extract the Code**:
  - Download the zip file of the project and extract it to your desired location.
  - Navigate to the project directory :

    ```bash
    cd <extracted-directory>
    ```

2. **Create a Virtual Environment**:
   ```bash
   python3.11 -m venv venv
   source venv/bin/activate    # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up the environment variables**:
   Create a `.env` file in the root directory with the following contents:
   ```bash
   GOOGLE_API_KEY=<your_gemini_api_key>
   PINECONE_API_KEY=<your_pinecone_api_key>
   ```

5. **Run the Application**:
   ```bash
   streamlit run MeetGenius.py
   ```

## Usage Guidelines

**Step 1: Pre-Meeting Document Upload**
- Upload documents such as PDFs, reports, and presentation files.
- Upload the discussion points.

**Step 2: Agenda Creation**
- Without any clicks, wait for a few minutes to receive a comprehensive agenda for the meeting, based on the discussion points and uploaded documents.

**Step 3: Meeting Recording and Tracking**
- You have two options: either upload a meeting video or record the live meeting. Based on this, the system will identify which points have been discussed and which remain unresolved.

**Step 4: Post-Meeting Summary**
- Based on the last uploaded or recorded video, you will receive a summary that includes an overall summary, key decisions made, and action items.


## System Architecture

This tool integrates several AI-powered and traditional components to manage the full lifecycle of meetings. Here's a brief overview:

1. **Pre-Meeting Document Management**:
   - Uploaded documents are converted into text, cleaned, and stored.
   - Discussion points entered by participants are saved in JSON format.

2. **Agenda Creation**:
   - Documents are divided into chunks, converted to embeddings (using `all-MiniLM-L6-v2`), and stored in Pinecone for efficient retrieval.
   - The system finds the top 3 related chunks for each discussion point and uses Gemini LLM to generate an agenda.

3. **Meeting Recording and Tracking**:
   - Audio from uploaded or recorded videos is converted to text using the Whisper model.
   - Langchain stores these transcripts in Pinecone.
   - RAG is used to match discussion points with relevant portions of the transcript, tracking what was discussed and flagging unresolved points.

4. **Post-Meeting Summary**:
   - A summary is created using several chained prompts:
     - **Summary Chain**: Generates the overall meeting summary.
     - **Discussion Chain**: Captures what was discussed.
     - **Key Decision Chain**: Identifies important decisions.
     - **Action Items Chain**: Lists tasks and responsible participants.
   - All outputs are combined into a comprehensive post-meeting report.

## Dependencies

Ensure you have all the required dependencies by installing them through `requirements.txt`. Here's an outline of key packages:
- Python 3.11.3
- Langchain
- Whisper
- Streamlit
- Hugging Face (`all-MiniLM-L6-v2` for embeddings)
- Pinecone for vector database
- Gemini LLM via API

Install dependencies:
```bash
pip install -r requirements.txt
```

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.

---
