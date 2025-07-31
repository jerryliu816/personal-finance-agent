import chromadb
from chromadb.config import Settings
from sentence_transformers import SentenceTransformer
from typing import List, Dict, Any, Optional
import uuid
from pathlib import Path
import json

class RAGVectorStore:
    def __init__(self, persist_directory: str = "data/chromadb"):
        """
        Initialize the RAG vector store with ChromaDB
        """
        self.persist_directory = Path(persist_directory)
        self.persist_directory.mkdir(parents=True, exist_ok=True)
        
        # Initialize ChromaDB client
        self.client = chromadb.PersistentClient(
            path=str(self.persist_directory),
            settings=Settings(
                anonymized_telemetry=False,
                allow_reset=True
            )
        )
        
        # Initialize embedding model
        self.embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
        
        # Get or create collection
        self.collection = self.client.get_or_create_collection(
            name="financial_documents",
            metadata={"description": "Financial documents for RAG"}
        )
    
    def add_document(self, document_id: str, text: str, metadata: Dict[str, Any] = None) -> List[str]:
        """
        Add a document to the vector store by chunking and embedding it
        """
        chunks = self._chunk_text(text)
        chunk_ids = []
        
        for i, chunk in enumerate(chunks):
            chunk_id = f"{document_id}_chunk_{i}"
            chunk_ids.append(chunk_id)
            
            # Create embedding
            embedding = self.embedding_model.encode(chunk).tolist()
            
            # Prepare metadata
            chunk_metadata = {
                "document_id": document_id,
                "chunk_index": i,
                "total_chunks": len(chunks),
                **(metadata or {})
            }
            
            # Add to collection
            self.collection.add(
                ids=[chunk_id],
                embeddings=[embedding],
                documents=[chunk],
                metadatas=[chunk_metadata]
            )
        
        return chunk_ids
    
    def search(self, query: str, n_results: int = 5) -> List[Dict[str, Any]]:
        """
        Search for relevant document chunks
        """
        # Create query embedding
        query_embedding = self.embedding_model.encode(query).tolist()
        
        # Search the collection
        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=n_results,
            include=['documents', 'metadatas', 'distances']
        )
        
        # Format results
        formatted_results = []
        if results['documents'] and results['documents'][0]:
            for i in range(len(results['documents'][0])):
                formatted_results.append({
                    'document': results['documents'][0][i],
                    'metadata': results['metadatas'][0][i],
                    'distance': results['distances'][0][i],
                    'relevance_score': 1 - results['distances'][0][i]  # Convert distance to similarity
                })
        
        return formatted_results
    
    def delete_document(self, document_id: str) -> bool:
        """
        Delete all chunks for a document
        """
        try:
            # Get all chunks for this document
            results = self.collection.get(
                where={"document_id": document_id},
                include=['ids']
            )
            
            if results['ids']:
                self.collection.delete(ids=results['ids'])
                return True
            return False
        except Exception as e:
            print(f"Error deleting document {document_id}: {e}")
            return False
    
    def get_document_info(self, document_id: str) -> Dict[str, Any]:
        """
        Get information about a document's chunks
        """
        results = self.collection.get(
            where={"document_id": document_id},
            include=['metadatas']
        )
        
        if not results['metadatas']:
            return {"exists": False}
        
        chunk_count = len(results['metadatas'])
        first_metadata = results['metadatas'][0] if results['metadatas'] else {}
        
        return {
            "exists": True,
            "chunk_count": chunk_count,
            "document_id": document_id,
            "metadata": first_metadata
        }
    
    def list_documents(self) -> List[Dict[str, Any]]:
        """
        List all documents in the vector store
        """
        # Get all entries
        results = self.collection.get(include=['metadatas'])
        
        if not results['metadatas']:
            return []
        
        # Group by document_id
        documents = {}
        for metadata in results['metadatas']:
            doc_id = metadata.get('document_id')
            if doc_id:
                if doc_id not in documents:
                    documents[doc_id] = {
                        'document_id': doc_id,
                        'chunk_count': 0,
                        'metadata': metadata
                    }
                documents[doc_id]['chunk_count'] += 1
        
        return list(documents.values())
    
    def _chunk_text(self, text: str, chunk_size: int = 1000, overlap: int = 100) -> List[str]:
        """
        Split text into overlapping chunks
        """
        if len(text) <= chunk_size:
            return [text]
        
        chunks = []
        start = 0
        
        while start < len(text):
            # Find end position
            end = start + chunk_size
            
            # If this is not the last chunk, try to break at a sentence or word boundary
            if end < len(text):
                # Look for sentence boundary
                sentence_end = text.rfind('.', start, end)
                if sentence_end > start + chunk_size // 2:
                    end = sentence_end + 1
                else:
                    # Look for word boundary
                    word_end = text.rfind(' ', start, end)
                    if word_end > start + chunk_size // 2:
                        end = word_end
            
            chunk = text[start:end].strip()
            if chunk:
                chunks.append(chunk)
            
            # Move start position with overlap
            start = end - overlap
            if start >= len(text):
                break
        
        return chunks
    
    def get_context_for_query(self, query: str, max_tokens: int = 2000) -> str:
        """
        Get relevant context for a query, respecting token limits
        """
        results = self.search(query, n_results=10)
        
        context_parts = []
        current_tokens = 0
        
        for result in results:
            # Rough token estimation (1 token ≈ 4 characters)
            chunk_tokens = len(result['document']) // 4
            
            if current_tokens + chunk_tokens > max_tokens:
                break
            
            context_parts.append(f"[Relevance: {result['relevance_score']:.2f}] {result['document']}")
            current_tokens += chunk_tokens
        
        return "\n\n".join(context_parts)
    
    def reset_store(self):
        """
        Reset the entire vector store (useful for testing)
        """
        self.client.reset()
        self.collection = self.client.get_or_create_collection(
            name="financial_documents",
            metadata={"description": "Financial documents for RAG"}
        )