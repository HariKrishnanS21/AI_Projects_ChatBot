from langchain.prompts import PromptTemplate
from langchain_community.agent_toolkits.sql.base import create_sql_agent
from langchain_community.utilities import SQLDatabase
from langchain_community.chat_models import ChatOllama
from langchain_community.tools.sql_database.tool import QuerySQLDataBaseTool, InfoSQLDatabaseTool
from langchain.agents import AgentExecutor

# DB connection
db = SQLDatabase.from_uri("mysql+mysqlconnector://root:Hari%402139@localhost/logistics_ai")

# LLM
llm = ChatOllama(model="llama3.2", temperature=0)

# Custom SQL Agent Prompt
custom_sql_prompt = PromptTemplate(
    input_variables=[
        "input", "table_info", "dialect", "top_k",
        "tool_names", "tools", "agent_scratchpad",
        "user_id", "depot_id","table_names"
    ],
    template="""
You are a helpful logistics assistant for a depot manager who can easily convert any natural language into simple SQL queries and find its answer.
You have to check the response from the {table_names} and these tables are with the schema {table_info}. 
You have to understand the schema and the names of the columns and their tables.
Then understand the relationship between each tables mentioned as below 
Relationships:
- user.user_id = depot.depot_user_id AND user.user_type = 'D'
- depot.depot_company_id = company.company_id
- user.user_id = company.company_user_id AND user.user_type = 'C'
- jobsheet.js_depot_id = depot.depot_id
- jobsheet.js_company_id = company.company_id

The query would be filtered strictly with respect of the user_id: {user_id} and depot_id: {depot_id} .Don't inter change them, strictly use in the exact format.
 
SQL Dialect: {dialect}

You should act as a sql expert who can Understand the table names, schema, columns names and relations and can make the best query out of the user question.
Only join necessary tables and avoid unwanted table joins.
Avoid making mistakes in the column name spelling every letter should be same as that in the schema.
Avoid using any columns not listed in the schema. Always return a friendly, natural-language response.
Respond in a way that makes sense to a depot manager. Use rupees for money. Dont mention SQL, databases, or queries.

Use one of the following tools: {tool_names}

Format:
---
Question: the original user question  
Thought: reasoning behind the next step  
Action: the tool to use  
ActionInput: SQL query for the selected tool  
Observation: result of the tool  
Thought: Now I know the final answer  
Final Answer: plain-language answer  
---

Begin!

Question: {input}
{agent_scratchpad}
"""
)

# Tools
tools = [QuerySQLDataBaseTool(db=db), InfoSQLDatabaseTool(db=db)]

# Agent Executor
agent_executor = create_sql_agent(
    llm=llm,
    db=db,
    prompt=custom_sql_prompt,
    tools=tools,
    verbose=True,
    handle_parsing_errors=True,
    agent_type="openai-tools"  
)

# Login function
def login(username: str, password: str):
    from sqlalchemy import text
    with db._engine.connect() as connection:
        query = text("""
            SELECT depot.*, user.*
            FROM user
            JOIN depot ON user.user_id = depot.depot_user_id
            WHERE user.user_email = :username AND user.user_original_password = :password AND user.user_type = 'D'
        """)
        result = connection.execute(query, {"username": username, "password": password}).fetchone()
        return dict(result._mapping) if result else None

# User-aware query
def query_user_specific(question: str, user_context: dict):
    return agent_executor.invoke({
        "input": question,
        "table_info": db.get_table_info(),
        "table_names":db.get_usable_table_names(),
        "dialect": db.dialect,
        "top_k": 10,
        "tool_names": ", ".join([tool.name for tool in tools]),
        "tools": "\n".join([tool.name for tool in tools]),
        "agent_scratchpad": "",
        "user_id": user_context.get("user_id"),
        "depot_id": user_context.get("depot_id")
    })
