# from dotenv import load_dotenv
# load_dotenv()

# from langchain_openai import ChatOpenAI, OpenAIEmbeddings
# from langchain_text_splitters import RecursiveCharacterTextSplitter
# from langchain_community.document_loaders import PyPDFLoader
# from langchain_community.vectorstores import FAISS
# from langchain_core.messages import SystemMessage, HumanMessage

# # load pdf 
# loader = PyPDFLoader("sample.pdf")
# documents = loader.load()

# # split text
# text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
# chunks = text_splitter.split_documents(documents)

# # create embeddings
# embeddings = OpenAIEmbeddings()

# # create vector store
# vectorstore = FAISS.from_documents(chunks, embeddings)

# # initialize chat model

# llm = ChatOpenAI(model="gpt-4", temperature=0)

# print("\nAsk questions from your PDF (type 'exit' to quit)\n")

# while True:
#     query = input("You: ")
#     if query.lower() == 'exit':
#         break

#     # retrieve relevant documents
#     relevant_docs = vectorstore.similarity_search(query, k=3)
#     context = "\n\n".join([doc.page_content for doc in relevant_docs])

#     # prompt LLm with context
#     messgae = [
#         SystemMessage(content="Answer ONLY using the provided context. If not found, say 'The question you are asking is not in document.."),
#         HumanMessage(content=f"Context:\n{context}\n\nQuestion: {query}")
#     ]
    
#     response = llm.invoke(messgae)
#     print("\nAI:", response.content)