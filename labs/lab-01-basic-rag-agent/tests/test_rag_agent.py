"""
Test suite for RAG Agent Lab 1.

This module contains validation tests for the RAG agent implementation.
Run with: python test_rag_agent.py
"""

import sys
import os
import time
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "starter-code"))

try:
    from rag_agent import RAGAgent
    from document_processor import DocumentProcessor
    from embeddings import EmbeddingModel
    from retriever import VectorRetriever
    from generator import AnswerGenerator
except ImportError as e:
    print(f"Error importing modules: {e}")
    print("Make sure all starter code files are implemented")
    sys.exit(1)


class TestRAGAgent:
    """Test suite for RAG Agent"""
    
    def __init__(self):
        self.test_data_path = str(Path(__file__).parent.parent / "test-data")
        self.agent = None
        self.passed_tests = 0
        self.total_tests = 0
    
    def run_test(self, test_name, test_func):
        """Run a single test and track results"""
        self.total_tests += 1
        print(f"\n{'='*60}")
        print(f"Test {self.total_tests}: {test_name}")
        print(f"{'='*60}")
        
        try:
            test_func()
            print(f"✓ {test_name} PASSED")
            self.passed_tests += 1
            return True
        except Exception as e:
            print(f"✗ {test_name} FAILED")
            print(f"Error: {e}")
            return False
    
    def test_document_processing(self):
        """Test document loading and chunking"""
        processor = DocumentProcessor(chunk_size=800, chunk_overlap=150)
        
        # Test document loading
        chunks = processor.process_documents(self.test_data_path)
        
        assert len(chunks) > 0, "No chunks created"
        assert len(chunks) >= 5, f"Expected at least 5 chunks, got {len(chunks)}"
        
        # Test chunk metadata
        for chunk in chunks[:3]:
            assert hasattr(chunk, 'page_content'), "Chunk missing page_content"
            assert hasattr(chunk, 'metadata'), "Chunk missing metadata"
            assert 'source' in chunk.metadata, "Chunk missing source metadata"
        
        # Test chunk statistics
        stats = processor.get_chunk_statistics(chunks)
        assert stats['total_chunks'] == len(chunks)
        assert stats['avg_chunk_length'] > 0
        
        print(f"  - Processed {stats['total_chunks']} chunks")
        print(f"  - Average chunk length: {stats['avg_chunk_length']:.0f} characters")
        print(f"  - Unique sources: {stats['unique_sources']}")
    
    def test_embedding_generation(self):
        """Test embedding model"""
        model = EmbeddingModel()
        
        # Test single text encoding
        text = "What are transformers?"
        embedding = model.encode_query(text)
        
        assert embedding is not None, "Embedding is None"
        assert len(embedding.shape) == 1, "Embedding should be 1D array"
        assert embedding.shape[0] == model.get_embedding_dimension()
        
        # Test batch encoding
        texts = [
            "What are transformers?",
            "How do RAG systems work?",
            "Compare vector databases"
        ]
        embeddings = model.encode(texts)
        
        assert embeddings.shape[0] == len(texts)
        assert embeddings.shape[1] == model.get_embedding_dimension()
        
        # Test similarity
        similarity = model.compute_similarity(embeddings[0], embeddings[1])
        assert 0 <= similarity <= 1, f"Similarity should be between 0 and 1, got {similarity}"
        
        print(f"  - Embedding dimension: {model.get_embedding_dimension()}")
        print(f"  - Encoded {len(texts)} texts successfully")
        print(f"  - Sample similarity score: {similarity:.3f}")
    
    def test_vector_retrieval(self):
        """Test vector database and retrieval"""
        # Create test data
        processor = DocumentProcessor()
        chunks = processor.process_documents(self.test_data_path)
        
        model = EmbeddingModel()
        texts = [chunk.page_content for chunk in chunks]
        embeddings = model.encode_documents(texts)
        
        # Test retrieval
        retriever = VectorRetriever(embedding_dimension=model.get_embedding_dimension())
        retriever.add_documents(chunks, embeddings)
        
        # Test search
        query = "What are transformers?"
        query_embedding = model.encode_query(query)
        results = retriever.search(query_embedding, k=3)
        
        assert len(results) > 0, "No results returned"
        assert len(results) <= 3, f"Expected at most 3 results, got {len(results)}"
        
        # Check result format
        for doc, score in results:
            assert hasattr(doc, 'page_content'), "Result missing page_content"
            assert isinstance(score, float), "Score should be float"
            assert score >= 0, "Score should be non-negative"
        
        # Test index stats
        stats = retriever.get_index_stats()
        assert stats['total_documents'] == len(chunks)
        
        print(f"  - Indexed {stats['total_documents']} documents")
        print(f"  - Retrieved {len(results)} results")
        print(f"  - Top result score: {results[0][1]:.3f}")
    
    def test_answer_generation(self):
        """Test answer generation (requires API key)"""
        if not os.getenv("OPENAI_API_KEY"):
            print("  - Skipping (OPENAI_API_KEY not set)")
            print("  - Set OPENAI_API_KEY environment variable to test generation")
            return
        
        # Create mock documents
        from langchain.docstore.document import Document
        
        docs = [
            Document(
                page_content="Transformers use self-attention mechanisms to process sequences in parallel.",
                metadata={"source": "paper_01.txt", "chunk_id": 1}
            ),
            Document(
                page_content="The attention mechanism computes Query, Key, and Value vectors.",
                metadata={"source": "paper_01.txt", "chunk_id": 2}
            )
        ]
        
        generator = AnswerGenerator()
        response = generator.generate(
            query="What are transformers?",
            context_documents=docs
        )
        
        assert 'answer' in response, "Response missing answer"
        assert 'sources' in response, "Response missing sources"
        assert len(response['answer']) > 0, "Answer is empty"
        
        print(f"  - Generated answer: {response['answer'][:100]}...")
        print(f"  - Number of sources: {response['num_sources']}")
    
    def test_rag_agent_integration(self):
        """Test complete RAG agent"""
        # Initialize agent
        self.agent = RAGAgent(top_k=3)
        
        # Test ingestion
        print("  - Testing document ingestion...")
        stats = self.agent.ingest(self.test_data_path)
        
        assert stats['ingestion_successful'], "Ingestion failed"
        assert stats['chunks_created'] > 0, "No chunks created"
        
        print(f"    ✓ Ingested {stats['documents_processed']} documents")
        print(f"    ✓ Created {stats['chunks_created']} chunks")
        
        # Test query (skip if no API key)
        if not os.getenv("OPENAI_API_KEY"):
            print("  - Skipping query test (OPENAI_API_KEY not set)")
            return
        
        print("  - Testing query processing...")
        response = self.agent.query("What are transformers?")
        
        assert response['query_successful'], "Query failed"
        assert len(response['answer']) > 0, "Answer is empty"
        assert response['num_sources_retrieved'] > 0, "No sources retrieved"
        
        print(f"    ✓ Query processed successfully")
        print(f"    ✓ Retrieved {response['num_sources_retrieved']} sources")
    
    def test_error_handling(self):
        """Test error handling"""
        # Test invalid directory
        processor = DocumentProcessor()
        try:
            processor.load_documents("/nonexistent/path")
            assert False, "Should have raised error for invalid path"
        except (ValueError, FileNotFoundError):
            print("  - ✓ Handles invalid directory path")
        
        # Test empty query
        model = EmbeddingModel()
        try:
            model.encode_query("")
            assert False, "Should have raised error for empty query"
        except ValueError:
            print("  - ✓ Handles empty query")
        
        # Test search on empty index
        retriever = VectorRetriever()
        try:
            import numpy as np
            retriever.search(np.zeros(384), k=3)
            assert False, "Should have raised error for empty index"
        except ValueError:
            print("  - ✓ Handles empty index search")
    
    def test_performance(self):
        """Test performance requirements"""
        if not os.getenv("OPENAI_API_KEY"):
            print("  - Skipping (OPENAI_API_KEY not set)")
            return
        
        # Initialize agent if not already done
        if self.agent is None:
            self.agent = RAGAgent()
            self.agent.ingest(self.test_data_path)
        
        # Test query latency
        query = "What are the key components of RAG systems?"
        
        start_time = time.time()
        response = self.agent.query(query)
        end_time = time.time()
        
        latency = end_time - start_time
        
        print(f"  - Query latency: {latency:.2f} seconds")
        
        if latency < 5.0:
            print(f"  - ✓ Meets latency requirement (< 5 seconds)")
        else:
            print(f"  - ⚠ Exceeds latency requirement (< 5 seconds)")
    
    def run_all_tests(self):
        """Run all tests"""
        print("\n" + "="*60)
        print("RAG AGENT TEST SUITE")
        print("="*60)
        
        # Run tests
        self.run_test("Document Processing", self.test_document_processing)
        self.run_test("Embedding Generation", self.test_embedding_generation)
        self.run_test("Vector Retrieval", self.test_vector_retrieval)
        self.run_test("Answer Generation", self.test_answer_generation)
        self.run_test("RAG Agent Integration", self.test_rag_agent_integration)
        self.run_test("Error Handling", self.test_error_handling)
        self.run_test("Performance", self.test_performance)
        
        # Print summary
        print("\n" + "="*60)
        print("TEST SUMMARY")
        print("="*60)
        print(f"Passed: {self.passed_tests}/{self.total_tests}")
        print(f"Success Rate: {(self.passed_tests/self.total_tests)*100:.1f}%")
        
        if self.passed_tests == self.total_tests:
            print("\n🎉 All tests passed! Your RAG agent is working correctly.")
        else:
            print(f"\n⚠ {self.total_tests - self.passed_tests} test(s) failed. Review the errors above.")
        
        return self.passed_tests == self.total_tests


if __name__ == "__main__":
    tester = TestRAGAgent()
    success = tester.run_all_tests()
    sys.exit(0 if success else 1)
