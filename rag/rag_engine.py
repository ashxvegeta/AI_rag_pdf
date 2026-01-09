from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
import os

class RAGEngine:

    def  __init__(self, pdf_path: str):

        self.pdf_path = pdf_path
        self.llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
        self.vectorstore = None
        self.chat_history = []
        self._load_and_index_pdf()

    def _load_and_index_pdf(self):
        # load pdf 
        loader = PyPDFLoader(self.pdf_path)
        documents = loader.load()

        # split text
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
        chunks = text_splitter.split_documents(documents)

        # create embeddings
        embeddings = OpenAIEmbeddings()

        # create vector store
        self.vectorstore = FAISS.from_documents(chunks, embeddings)

    def ask(self, query: str) -> str:
        #  Retrieve relevant docs
        relevant_docs = self.vectorstore.similarity_search(query, k=3)

        if not relevant_docs:
            return "The question you are asking is not in document."

        context = "\n\n".join([doc.page_content for doc in relevant_docs])

        #  Build message list
        messages = [
            SystemMessage(
                content="Answer ONLY using the provided context. "
                        "If not found, say 'The question you are asking is not in document.'"
            )
        ]

        #  Add previous memory
        messages.extend(self.chat_history)

        # Add current question WITH context
        messages.append(
            HumanMessage(content=f"Context:\n{context}\n\nQuestion: {query}")
        )

        #  Ask LLM
        response = self.llm.invoke(messages)
        answer = response.content.strip()

        # Save conversation to memory
        self.chat_history.append(HumanMessage(content=query))
        self.chat_history.append(AIMessage(content=answer))

        return answer

        