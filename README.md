Depot AI ChatBot – Smart Assistant for Depot Managers
A LangChain + LLaMA3-powered AI assistant that allows Depot Managers to ask questions in natural language and get real-time insights from a MySQL logistics database — all through an intuitive desktop GUI.

✨ Features
  🔐 Login Authentication for depot users

  💬 Natural Language to SQL via LLM

  🧠 Context-aware answers (user + depot-specific)

  📊 Fetches real-time depot data: labour charges, contact info, job sheets, and more

  🖥️ Built with Python Tkinter GUI

  🦙 Uses LLaMA 3.2 via Ollama

🚀 How to Run
   1. ✅ Requirements
       Python 3.10+
    
       Ollama (LLaMA 3.2 model must be installed)
    
       MySQL (database with logistics schema)
    
  2. 📦 Install Dependencies
       pip install langchain langchain-community langchain-ollama mysql-connector-python tkinter
  3. ⚙️ Start LLaMA Model
       ollama run llama3.2
  4. 🧠 Configure MySQL
       Make sure to update your DB URI inside bot.py:
       db = SQLDatabase.from_uri("mysql+mysqlconnector://<user>:<password>@localhost/logistics_ai")
    
       The schema should include these tables with proper relationships:
    
       user (user_id, user_email, user_original_password, user_type)
    
       depot (depot_id, depot_user_id, depot_company_id, depot_contact)
    
       company (company_id, company_user_id)
    
       jobsheet (js_depot_id, js_company_id, labour_charge)
    
  5. ▶️ Run the App
       python ChatBody.py
🧩 Project Structure
  📁 project-root
  ├── bot.py           # LangChain logic, DB connection, prompt, agent setup
  ├── ChatBody.py      # Tkinter GUI logic and user interaction
  └── README.md        # This file
📌 Assumptions
  The chatbot is used only by depot managers (user_type = 'D').
  
  All SQL queries are generated automatically using LangChain's agent tools.
  
  LLaMA3 provides natural-sounding, friendly responses to depot managers.
  
  Final answer is extracted from raw agent output using a summarization chain.

✅ Sample Use Cases
  “What’s the total labour charge for my depot this week?”
  
  “Show me the contact number of our depot.”
  
  “How many jobsheets were created today?”

