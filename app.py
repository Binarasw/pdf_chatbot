import streamlit as st
import openai
import time

# ✅ Step 1: Initialize OpenAI client
client = openai.OpenAI(api_key="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")  # Replace with your actual OpenAI API key

# ✅ Step 2: Hardcoded File IDs (Replace with actual file IDs from OpenAI)
FILE_IDS = [
"file-TzkdB42kVQVXUYG2H5XySR"
]

# ✅ Step 3: Create an assistant with the File Search tool
assistant = client.beta.assistants.create(
    name="PDF Chat Assistant",
    model="gpt-3.5-turbo",
    tools=[{"type": "file_search"}],
    instructions=(
        "You are an AI assistant that answers questions **only** based on the provided PDF documents. "
        "If you do not find relevant information in the uploaded PDFs, simply respond with: "
        "'I do not have information on that in the documents provided.' "
       "always mention where you get the information from displaying key sections or summaries.." 
        "Do not use any outside knowledge or general information."
    )
)
#st.write(f"✅ Assistant created with ID: {assistant.id}")

# ✅ Step 4: Start a new conversation thread
thread = client.beta.threads.create()
st.write(f"✅ Chat session started.")

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
            time.sleep(2)

        # ✅ Step 9: Retrieve and print the assistant's response
        messages = client.beta.threads.messages.list(thread_id=thread.id)
        assistant_response = messages.data[0].content[0].text.value

        # Ensure the assistant only provides responses from the PDFs
        if "source" not in assistant_response.lower():  
            assistant_response = "I do not have information on that in the provided documents."

        # ✅ Display the Assistant’s Answer
        st.write("🤖 **Assistant:**", assistant_response)
