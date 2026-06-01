import chromadb

chroma_client = chromadb.PersistentClient(path="chroma_stroe")

sop_collection = chroma_client.get_or_create_collection(
    name="telecom_sop_runbooks"
)