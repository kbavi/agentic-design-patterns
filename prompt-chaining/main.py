import os

from dotenv import load_dotenv
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

load_dotenv()

llm = ChatOpenAI(temperature=0)

prompt_extract = ChatPromptTemplate.from_template(
    "Extract the technical specifications from the following text:\n\n{text_input}"
)

prompt_transform = ChatPromptTemplate.from_template(
    "Transform the following technical specifications into a JSON object with 'cpu', 'memory', and 'storage' fields:\n\n{specifications}"
)

# This syntax uses the '|' (pipe) operator to compose a sequence of LangChain components into a "chain".
# Each component's output feeds into the next.
# Here, 'prompt_extract' generates a prompt, which is sent to the 'llm' (language model),
# and then the output is parsed by 'StrOutputParser' to ensure a string result.
extraction_chain = prompt_extract | llm | StrOutputParser()

full_chain = (
    {"specifications": extraction_chain} | prompt_transform | llm | StrOutputParser()
)

input_text = "The new laptop model features a 3.5 GHz octa-core processor, 16GB of RAM, and a 1TB NVMe SSD."

final_result = full_chain.invoke({"text_input": input_text})

print("\n --- Final JSON Output --- ")
print(final_result)
