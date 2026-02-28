import os
from typing import List, Dict, Optional
from SvdpGrantAgent.factories.llm_factory import get_llm_provider
from SvdpGrantAgent.factories.db_factory import get_vector_store
from langchain.prompts import ChatPromptTemplate
from SvdpGrantAgent.schema import GrantRecord, GrantStatus

class WriterAgent:
    def __init__(self):
        self.vectorstore = get_vector_store()
        self.llm = get_llm_provider(temperature=0)

    def _query_knowledge_base(self, query: str) -> str:
        """
        Retrieves context from the vector database with citations.
        """
        docs = self.vectorstore.similarity_search(query, k=3)
        context_parts = []
        for i, doc in enumerate(docs):
            source = doc.metadata.get("source", "Unknown Source")
            context_parts.append(f"[Source {i+1}: {source}]\n{doc.page_content}")
        return "\n\n".join(context_parts)

    def draft_application_section(self, section_name: str, requirements: str, feedback: Optional[str] = None) -> Dict[str, str]:
        """
        Drafts a specific section of the grant application following strict RAG confinement.
        """
        context = self._query_knowledge_base(f"Information about SVdP Pasco: {section_name} {requirements}")
        
        system_prompt = """You are the SVdP Grant Writer Agent. 
        Your task is to draft a grant application section based STRICTLY on the provided context.
        
        RULES:
        1. STRICT RAG CONFINEMENT: If the answer is not in the context, leave the field BLANK and flag it.
        2. CITATION MANDATE: Every claim, metric, or fact must be followed by a citation like [Source X].
        3. Do not use your internal knowledge about Saint Vincent de Paul; only use the provided context.
        4. If the context is insufficient, return "INSUFFICIENT_DATA".
        """
        
        prompt_messages = [
            ("system", system_prompt),
            ("human", "Context:\n{context}\n\nSection to Draft: {section_name}\nRequirements: {requirements}")
        ]
        
        if feedback:
            prompt_messages.append(("human", f"HUMAN FEEDBACK FOR REWRITE: {feedback}"))
            
        prompt = ChatPromptTemplate.from_messages(prompt_messages)
        
        chain = prompt | self.llm
        response = chain.invoke({"context": context, "section_name": section_name, "requirements": requirements})
        
        content = response.content
        return {
            "section": section_name,
            "content": content,
            "status": "DRAFTED" if "INSUFFICIENT_DATA" not in content else "FLAGGED"
        }

    def generate_full_draft(self, grant: GrantRecord, feedback: Optional[str] = None) -> Dict[str, str]:
        """
        Iterates through requirements and generates a full draft payload.
        """
        draft_results = {}
        for req in grant.extracted_requirements:
            result = self.draft_application_section(req, "Please provide a detailed response for this grant requirement.", feedback=feedback)
            draft_results[req] = result["content"]
        
        return draft_results

if __name__ == "__main__":
    # Example usage (requires environment variables and DB setup)
    # writer = WriterAgent()
    # sample_grant = GrantRecord(grant_id="test", grant_source_url="http://example.com", extracted_requirements=["Mission Statement", "Financial Need"])
    # print(writer.generate_full_draft(sample_grant))
    pass

