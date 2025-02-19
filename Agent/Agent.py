from sqlalchemy import text
import json
import google.generativeai as genai
from llama_index.core import (
    VectorStoreIndex,
    StorageContext,
    SQLDatabase,
    Document
)
from llama_index.llms.gemini import Gemini
from llama_index.embeddings.gemini import GeminiEmbedding
from llama_index.core.query_engine import RetrieverQueryEngine
from llama_index.core.retrievers import VectorIndexRetriever
from llama_index.core.vector_stores import SimpleVectorStore
from llama_index.core.settings import Settings
from .query import QueryHandler

class Agent:
    def __init__(self, database_url: str, gemini_api_key: str):
        self.handlers = QueryHandler(DATABASE_URL=database_url)
        self.sql_database = SQLDatabase(engine=self.handlers.get_engine())
        genai.configure(api_key=gemini_api_key)

        self.embedding_model = GeminiEmbedding(model_name="models/embedding-001", api_key=gemini_api_key, dimension=768)
        Settings.embed_model = self.embedding_model

        self.llm = Gemini(model="models/gemini-1.5-flash", api_key=gemini_api_key, temperature=1.0)
        Settings.llm = self.llm 

        self.vector_store = SimpleVectorStore()
        self.storage_context = StorageContext.from_defaults(vector_store=self.vector_store)

        self.schema_index = self._create_schema_index()

    def _create_schema_index(self) -> VectorStoreIndex:
        documents = [
            Document(text=self._get_table_context(table), metadata={"table": table})
            for table in self.handlers.models.keys()
        ]
        return VectorStoreIndex.from_documents(
            documents,
            storage_context=self.storage_context,
            embed_model=self.embedding_model,
        )

    def _get_table_context(self, table_name: str) -> str:
        table_info = self.sql_database.get_single_table_info(table_name)
        query = f"SELECT * FROM {table_name}"
        result = self.handlers.db.execute(text(query))
        sample_data = [dict(row) for row in result.mappings().all()]
        return f"## Schema của bảng {table_name} ##\n{table_info}\n\n-- Dữ liệu mẫu --\n{json.dumps(sample_data, ensure_ascii=False, default=str)}"

    def response(self, question: str) -> str:
        query_engine = RetrieverQueryEngine(retriever=VectorIndexRetriever(index=self.schema_index, similarity_top_k=5))
        response = query_engine.query(question)
        context = "\n".join([node.text for node in response.source_nodes])

        final_prompt = f"""
        Context database:
        {context}
        
        Hãy trả lời câu hỏi bằng tiếng Việt tự nhiên dựa trên dữ liệu trên database đã được cung cấp
        Câu hỏi: {question}
        """
        
        response = self.llm.complete(final_prompt)
        return response.text

    def __del__(self):
        if hasattr(self, "handlers"):
            self.handlers.close()
