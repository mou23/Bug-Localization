import chromadb
from chromadb import Settings
from chromadb import Documents, EmbeddingFunction, Embeddings
from sentence_transformers import SentenceTransformer

embedding_model = SentenceTransformer('jinaai/jina-embeddings-v3')

class MyJinaEmbeddingFunction(EmbeddingFunction):
    def __call__(self, input: Documents) -> Embeddings:
        try:
            embeddings = embedding_model.encode(input, convert_to_numpy=True)
            return embeddings
        except Exception as e:
            print(e)
            print("problem in embedding!")


def initialize_db():
    global client
    client = chromadb.Client(settings=Settings(allow_reset=True))
    client.reset()


def create_file_collection():
    global client, file_collection
    jina_embedding_function = MyJinaEmbeddingFunction()
    file_collection = client.create_collection(name='java-files', embedding_function= jina_embedding_function, metadata={"hnsw:space": "cosine"}) #, "hnsw:M": 32})

    return file_collection


def delete_file_collection():
    global client
    try:
        client.delete_collection('java-files')
    except:
        print('file collection does not exist')



def get_file_collection():
    global file_collection
    return file_collection