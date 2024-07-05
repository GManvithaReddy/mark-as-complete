# from extra.crew.agents import agents
# from extra.crew.tasks import tasks
# from langchain_community.agent_toolkits import GmailToolkit
# from langchain_community.tools.gmail.search import GmailSearch
# from langchain_community.tools.gmail.utils import build_resource_service, get_gmail_credentials
# from langchain_core.output_parsers import StrOutputParser
# from langchain_core.output_parsers import JsonOutputParser
# from crewai import Crew
# from langchain_groq import ChatGroq
# from langchain_core.prompts import ChatPromptTemplate

# # UTILS

# def write_markdown_file(content, filename):
#   """Writes the given content as a markdown file to the local directory.

#   Args:
#     content: The string content to write to the file.
#     filename: The filename to save the file as.
#   """
#   with open(f"{filename}.md", "w") as f:
#     f.write(content)

# llm = ChatGroq(
#     model = "llama3-70b-8192",
#     temperature=0
# )


from fastapi import FastAPI
from extra.graph import WorkFlow

app = FastAPI()

 
@app.get("/mark_as_complete")
async def mark_as_complete():
     
    try:
        result = WorkFlow().app.invoke({})
        return {"message": "Workflow invoked successfully", "result": result}
    except Exception as e:
        return {"error": f"Error invoking workflow: {str(e)}"}

