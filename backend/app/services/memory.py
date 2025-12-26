from typing import List, Optional
from collections import deque
import chromadb
from chromadb.utils import embedding_functions
from app.core.config import settings

class MockEmbeddingFunction(embedding_functions.EmbeddingFunction):
    _function_name = "mock_embedding"
    
    def __init__(self):
        self._name = self._function_name
    
    def name(self) -> str:
        return self._name
    
    def get_config(self) -> dict:
        return {"name": self._name, "dimension": 1536}
    
    @classmethod
    def build_from_config(cls, config: dict):
        return cls()
    
    def __call__(self, input: List[str]) -> List[List[float]]:
        return [[0.1] * 1536 for _ in input]

class MemorySystem:
    def __init__(self, agent_id: str, use_mock: bool = True):
        self.agent_id = agent_id
        self.short_term_memory = deque(maxlen=20)
        self.chroma_client = chromadb.Client()
        
        if use_mock:
            self.embedding_fn = MockEmbeddingFunction()
        else:
            self.embedding_fn = embedding_functions.OpenAIEmbeddingFunction(
                api_key=settings.LLM_API_KEY,
                model_name=settings.LLM_EMBEDDING_MODEL
            )
            
        self.collection = self.chroma_client.get_or_create_collection(
            name=f"agent_memory_{agent_id}",
            embedding_function=self.embedding_fn
        )

    def add_short_term(self, content: str):
        self.short_term_memory.append(content)

    def recall(self, query: str, k: int = 3) -> List[str]:
        results = self.collection.query(
            query_texts=[query],
            n_results=k
        )
        
        if results["documents"]:
            return results["documents"][0]
        return []

    def consolidate_daily(self, summary: str):
        import uuid
        self.collection.add(
            documents=[summary],
            metadatas=[{"type": "daily_summary", "agent": self.agent_id}],
            ids=[str(uuid.uuid4())]
        )
        
        self.short_term_memory.clear()

    def get_recent_context(self) -> str:
        return "\n".join(list(self.short_term_memory))
