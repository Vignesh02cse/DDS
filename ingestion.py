from langchain_community.document_loaders import TextLoader
from langchain_openai import OpenAIEmbeddings

from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Pinecone
from langchain_community.document_loaders import DirectoryLoader

# def return_urls():
#     urls = []
#     filelist = os.listdir('urls/')
#     for filename in filelist:
#         file = open('urls/' + filename, 'r')
#         for url in file.readlines():
#             urls.append(url)
#
#         file.close()
#     return urls
'''ingestion the documents to the vectorstore'''


def ingest_docs():
    # urls = return_urls()
    # loader_web = WebBaseLoader(urls)
    loader_text = DirectoryLoader('documents/', glob='**/*.txt', loader_cls=TextLoader)

    '''load the multiple loaders into a single loader'''

    '''csv loader'''
    # loader = CSVLoader(file_path='./csv/combined.csv')
    # csv_data = loader.load()
    '''json loader'''
    # def metadata_func(record: dict, metadata: dict) -> dict:
    #     metadata["sender_name"] = record.get("sender_name")
    #     metadata["timestamp_ms"] = record.get("timestamp_ms")
    #
    #     if "source" in metadata:
    #         source = metadata["source"].split("/")
    #         source = source[source.index("langchain"):]
    #         metadata["source"] = "/".join(source)
    #
    #     return metadata
    '''json loader from directory'''
    # loader = JSONLoader(
    #     file_path='./json/intents.json',
    #     jq_schema='.messages[]',
    #     content_key="content",
    #     metadata_func=metadata_func
    # )
    #
    # json_data = loader.load()
    # loader_all = MergedDataLoader(loaders=[loader_text,loader_web])
    # print (loader_all)
    # print (json_data)
    # docs_all = loader_all.load()
    # Define the metadata extraction function.

    docs_all = loader_text.load()
    # print (docs_all)

    '''length of the documents'''
    print(f"loaded {len(docs_all)} site documents")

    '''split the documents into chunks'''
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=400, chunk_overlap=50, separators=["\n\n", "\n", " ", ""]
    )
    '''split the documents into chunks and add to the vectorstore'''
    documents = text_splitter.split_documents(docs_all)
    '''create embeddings and add to the vectorstore'''
    embeddings = OpenAIEmbeddings()
    '''length of the documents'''
    print(f"Going to add {len(documents)} to Pinecone")
    '''add the documents to the vectorstore'''
    Pinecone.from_documents(documents, embeddings, index_name='mental')
    '''after adding the documents to the vectorstore'''
    print("****Loading to vectorestore done ***")


if __name__ == "__main__":
    ingest_docs()
