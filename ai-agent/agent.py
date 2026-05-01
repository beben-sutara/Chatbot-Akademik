"""
AI Agent untuk Chatbot Akademik
Menggunakan LangChain dan OpenAI untuk pemrosesan bahasa alami
"""
import os
from typing import List, Dict, Any
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-3.5-turbo")

SYSTEM_PROMPT = """Anda adalah asisten akademik yang membantu mahasiswa dan staff kampus.
Nama Anda adalah "Akad" - Asisten Akademik Digital.

Tugas Anda:
1. Menjawab pertanyaan tentang jadwal kuliah, nilai, dan kalender akademik
2. Membantu proses registrasi dan pendaftaran mata kuliah
3. Memberikan informasi layanan mahasiswa
4. Menjawab FAQ akademik
5. Memberikan konsultasi akademik secara ramah dan profesional

Gunakan bahasa Indonesia yang sopan dan mudah dipahami.
Jika Anda tidak memiliki informasi yang diminta, arahkan mahasiswa untuk menghubungi bagian akademik langsung.
"""


def create_agent(tools: List = None):
    """Create a LangChain agent with academic tools."""
    if not OPENAI_API_KEY:
        raise ValueError("OPENAI_API_KEY is not set")

    from langchain_openai import ChatOpenAI
    from langchain.agents import AgentExecutor, create_openai_tools_agent
    from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
    from langchain.schema import SystemMessage

    llm = ChatOpenAI(model=OPENAI_MODEL, openai_api_key=OPENAI_API_KEY, temperature=0.7)
    tools = tools or []

    prompt = ChatPromptTemplate.from_messages([
        ("system", SYSTEM_PROMPT),
        MessagesPlaceholder(variable_name="chat_history"),
        ("human", "{input}"),
        MessagesPlaceholder(variable_name="agent_scratchpad"),
    ])

    agent = create_openai_tools_agent(llm, tools, prompt)
    return AgentExecutor(agent=agent, tools=tools, verbose=True)


def get_simple_response(message: str, history: List[Dict[str, str]] = None) -> str:
    """Get a simple LLM response without tools."""
    if not OPENAI_API_KEY:
        return "OpenAI API key tidak dikonfigurasi. Silakan atur OPENAI_API_KEY."

    from langchain_openai import ChatOpenAI
    from langchain.schema import SystemMessage, HumanMessage, AIMessage

    llm = ChatOpenAI(model=OPENAI_MODEL, openai_api_key=OPENAI_API_KEY, temperature=0.7)
    messages = [SystemMessage(content=SYSTEM_PROMPT)]

    for h in (history or []):
        if h["role"] == "user":
            messages.append(HumanMessage(content=h["content"]))
        elif h["role"] == "assistant":
            messages.append(AIMessage(content=h["content"]))

    messages.append(HumanMessage(content=message))
    response = llm.invoke(messages)
    return response.content


if __name__ == "__main__":
    print("Chatbot Akademik AI Agent")
    print("=" * 40)
    history = []
    while True:
        user_input = input("\nAnda: ").strip()
        if user_input.lower() in ["exit", "quit", "keluar"]:
            print("Terima kasih! Sampai jumpa.")
            break
        response = get_simple_response(user_input, history)
        print(f"\nAkad: {response}")
        history.append({"role": "user", "content": user_input})
        history.append({"role": "assistant", "content": response})
