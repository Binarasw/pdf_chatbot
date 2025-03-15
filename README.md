# 📄 AI PDF Chatbot

A Streamlit-based chatbot that answers user questions **only** from pre-uploaded PDFs using OpenAI's Assistants API.

## 🔹 Features
✅ Uses OpenAI's `file_search` tool for document-based retrieval.  
✅ Prevents responses based on general knowledge (strict PDF-based answers).  
✅ Optimized for cost efficiency using GPT-3.5.  
✅ Simple UI for users to ask questions.  

## 🔹 Setup & Installation

1. **Clone the repository:**
   ```sh
   git clone https://github.com/your-username/pdf_chatbot.git
   cd pdf_chatbot
   ```

2. **Create a virtual environment:**
   ```sh
   python3 -m venv venv
   source venv/bin/activate  # On macOS/Linux
   venv\Scripts\activate    # On Windows
   ```

3. **Install dependencies:**
   ```sh
   pip install -r requirements.txt
   ```

4. **Set up your OpenAI API key:**
   - Replace `"your-api-key-here"` in `app.py` with your actual OpenAI API key.

5. **Run the Streamlit app:**
   ```sh
   streamlit run app.py
   ```


