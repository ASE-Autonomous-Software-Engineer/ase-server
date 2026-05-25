import chromadb

client = chromadb.PersistentClient(
    path="./memory_db"
)

collection = client.get_or_create_collection(
    name="agent_memory"
)

class MemoryStore:

    @staticmethod
    def save_memory(
        memory_id,
        content,
        metadata=None
    ):

        collection.add(
            ids=[memory_id],
            documents=[content],
            metadatas=[metadata or {}]
        )

    @staticmethod
    def retrieve_memory(
        query,
        n_results=5
    ):

        return collection.query(
            query_texts=[query],
            n_results=n_results
        )