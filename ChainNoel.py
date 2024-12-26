from langchain_core.messages import AIMessage, HumanMessage
from langchain_core.prompts import MessagesPlaceholder

from langchain_groq import ChatGroq
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate

from dotenv import load_dotenv
load_dotenv()

def create_chain (temperature):
    llm = ChatGroq(model="llama3-8b-8192",
                   temperature=temperature)
    
    system_prompt = """
    Você é o Papai Noel. Responda como se fosse o Papai Noel, utilizando um tom acolhedor e mágico. 
    Incorpore detalhes natalinos e brinque com o imaginário infantil. 
    Quando solicitado, conte histórias criativas de Natal.
    """

    user_prompt = """{user_input}"""

    prompt_template = ChatPromptTemplate.from_messages([('system', system_prompt),
                                                        MessagesPlaceholder(variable_name="chat_history"),
                                                        ('user', user_prompt)])
    
    return prompt_template | llm | StrOutputParser()

def talk_to_noel (chain, user_input, chat_history):
    return chain.stream({
        "chat_history": chat_history,
        "user_input": user_input
    })

                