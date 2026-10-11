from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel
from typing import List, Optional
from langchain_core.output_parsers import PydanticOutputParser


load_dotenv()
from langchain_google_genai import ChatGoogleGenerativeAI


model = ChatGoogleGenerativeAI(
    model="gemini-3.8-flash"
)



class ResearchPaper(BaseModel):
    title: str
    authors: List[str]
    problem_statement: str
    methodology: List[str]
    algorithms: List[str]
    dataset: Optional[str] = None
    results: Optional[str] = None
    limitations: List[str]
    research_gap: str
    future_work: List[str]



parser = PydanticOutputParser(pydantic_object=ResearchPaper)

prompt = ChatPromptTemplate.from_messages([
    ('system',"""
You are a research paper analysis assistant.

Extract the following information from the provided research paper text:
- Title
- Authors
- Problem statement
- Methodology
- Algorithms
- Dataset
- Results
- Limitations
- Research gap
- Future work

Do not invent information that is not present in the text.


     {format_instructions}
"""),
("human","{paper_text}")
]
)



def analyze_paper(paper_text):

    final_prompt = prompt.invoke({
        "paper_text": paper_text,
        "format_instructions": parser.get_format_instructions()
    })

    response = model.invoke(final_prompt)

    response_text = response.text

    research_data = parser.parse(response_text)

    return research_data