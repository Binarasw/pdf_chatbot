import os
import streamlit as st
import openai
import time

# ✅ Step 1: Load OpenAI API Key Securely from Streamlit Secrets
openai.api_key = st.secrets["OPENAI_API_KEY"]
client = openai.OpenAI(api_key=openai.api_key)

# ✅ Step 2: Hardcoded File IDs (Replace with actual file IDs from OpenAI)
FILE_IDS = [
    "file-TzkdB42kVQVXUYG2H5XySR"  # Replace with your actual file ID(s)
]

# ✅ Step 3: Create an assistant with the File Search tool
assistant = client.beta.assistants.create(
    name="PDF Chat Assistant",
    model="gpt-3.5-turbo",  # ✅ Using GPT-3.5 for cost efficiency
    tools=[{"type": "file_search"}],
    instructions=(
        "You are an AI assistant that answers questions **only** based on the provided PDF documents. "
        "If you do not find relevant information in the uploaded PDFs, simply respond with: "
        "'I do not have information on that in the documents provided.' "
        "Always mention where you get the information from, displaying key sections or summaries. "
        "Do not use any outside knowledge or general information."
    )
)
st.write(f"✅ Assistant created with ID: {assistant.id}")

# ✅ Step 4: Start a new conversation thread
thread = client.beta.threads.create()
st.write(f"✅ Chat session started. Thread ID: {thread.id}")

# ✅ Step 5: Chat Interface (Users Only Ask Questions)
st.title("📄 AI PDF Chatbot")
st.write("Ask questions based on the pre-uploaded PDFs.")

# ✅ Chat Input
user_question = st.text_input("Enter your question:")

if st.button("Get Answer") and user_question:
    with st.spinner("Searching through the PDFs..."):
        # ✅ Step 6: Attach pre-uploaded files to the query
        attachments = [{"file_id": fid, "tools": [{"type": "file_search"}]} for fid in FILE_IDS]

        # ✅ Step 7: Send the user's question to the assistant
        client.beta.threads.messages.create(
            thread_id=thread.id,
            role="user",
            content=user_question,
            attachments=attachments
        )

        # ✅ Step 8: Run the assistant on the thread and wait for a response
        run = client.beta.threads.runs.create(thread_id=thread.id, assistant_id=assistant.id)

        # Wait for completion
        while True:
            run_status = client.beta.threads.runs.retrieve(thread_id=thread.id, run_id=run.id)
            if run_status.status in ["completed", "failed"]:
                break
            time.sleep(2)  # ✅ Added delay to avoid excessive API calls

        # ✅ Step 9: Retrieve and print the assistant's response
        messages = client.beta.threads.messages.list(thread_id=thread.id)
        assistant_response = messages.data[0].content[0].text.value

        # ✅ Step 10: Ensure the assistant only provides responses from the PDFs
        if "source" not in assistant_response.lower():  
            assistant_response = "I do not have information on that in the provided documents."

        # ✅ Step 11: Display the Assistant’s Answer
        st.write("🤖 **Assistant:**", assistant_response)
