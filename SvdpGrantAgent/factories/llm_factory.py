import os
from langchain_openai import ChatOpenAI
from langchain_community.chat_models import ChatAnthropic

def get_llm_provider(model_type: str = "primary", temperature: float = 0):
    """
    Fetches the LLM provider configured in environment variables.
    Standardizes output to a LangChain model interface.
    """
    provider = os.getenv("LLM_PROVIDER", "openai").lower()
    
    if provider == "openai":
        return ChatOpenAI(
            model=os.getenv("OPENAI_MODEL", "gpt-4-turbo-preview"),
            temperature=temperature
        )
    elif provider == "anthropic":
        return ChatAnthropic(
            model=os.getenv("ANTHROPIC_MODEL", "claude-3-opus-20240229"),
            temperature=temperature
        )
    elif provider == "google":
        from langchain_google_genai import ChatGoogleGenerativeAI
        return ChatGoogleGenerativeAI(
            model=os.getenv("GOOGLE_MODEL", "gemini-1.5-pro"),
            temperature=temperature
        )
    
    # Default to OpenAI if nothing else is specified correctly
    return ChatOpenAI(model="gpt-4-turbo-preview", temperature=temperature)
