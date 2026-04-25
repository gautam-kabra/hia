import os
import streamlit as st
from groq import Groq
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS


class ChatAgent:
    def __init__(self):
        # Set HF token for authenticated downloads
        hf_token = st.secrets.get("HF_TOKEN")
        if hf_token:
            os.environ["HF_TOKEN"] = hf_token
            os.environ["HUGGINGFACE_HUB_TOKEN"] = hf_token
        
        self.embeddings = HuggingFaceEmbeddings(
            model_name="all-MiniLM-L6-v2",
            model_kwargs={'device': 'cpu'}
        )
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000, chunk_overlap=200
        )
        api_key = st.secrets["GROQ_API_KEY"]
        self.client = Groq(api_key=api_key)
        self.model_name = "llama-3.3-70b-versatile"  # Default model for chat

    def initialize_vector_store(self, text_content):
        """Create vector store from text content."""
        if not text_content or text_content.strip() == "":
            text_content = "No report context available."

        texts = self.text_splitter.split_text(text_content)
        if not texts:
            texts = [text_content]

        vectorstore = FAISS.from_texts(texts, self.embeddings)
        return vectorstore

    def _format_chat_history(self, chat_history):
        """Format chat history for API."""
        messages = []
        for msg in chat_history:
            messages.append({"role": msg["role"], "content": msg["content"]})
        return messages

    def _contextualize_query(self, query, chat_history):
        """Reformulate query considering chat history."""
        if not chat_history:
            return query

        recent_history = chat_history[-4:]
        history_text = "\n".join(
            [
                f"{'User' if msg['role'] == 'user' else 'Assistant'}: {msg['content']}"
                for msg in recent_history
            ]
        )

        contextualize_prompt = f"""Given a chat history and the latest user question, formulate a standalone question which can be understood without the chat history. Do NOT answer the question, just reformulate it if needed and otherwise return it as is.

Chat History:
{history_text}

Latest User Question: {query}

Standalone Question:"""

        try:
            response = self.client.chat.completions.create(
                model="llama-3.1-8b-instant",  # Fast model for query reformulation
                messages=[
                    {"role": "system", "content": "You reformulate questions to be standalone."},
                    {"role": "user", "content": contextualize_prompt}
                ],
                temperature=0.1,
                max_tokens=200
            )
            return response.choices[0].message.content.strip()
        except Exception:
            return query

    def get_response(self, query, vectorstore, chat_history=None):
        """Get response using RAG."""
        if chat_history is None:
            chat_history = []

        contextualized_query = self._contextualize_query(query, chat_history)

        try:
            retriever = vectorstore.as_retriever(search_kwargs={"k": 3})
            docs = retriever.get_relevant_documents(contextualized_query)
            context = "\n\n".join([doc.page_content for doc in docs])

            if context.strip() == "No report context available.":
                context = ""
        except Exception:
            context = ""

        qa_system_prompt = (
            "You are a helpful health insights assistant. "
            "Use the retrieved report context AND the chat history to answer the user's question. "
            "If the user asks about their report, refer to the analysis and context provided. "
            "If you don't know the answer, just say that you don't know. "
            "Keep the answer concise but helpful."
        )

        if (
            context
            and context.strip()
            and context.strip() != "No report context available."
        ):
            user_content = f"Report Context:\n{context}\n\nQuestion: {query}"
        else:
            user_content = f"Question: {query}"

        # Build messages list with chat history for conversational memory
        messages = [{"role": "system", "content": qa_system_prompt}]

        # Include recent chat history (skip system messages with report metadata)
        for msg in chat_history[-10:]:
            role = msg.get("role", "user")
            content = msg.get("content", "")
            # Skip system messages (report metadata) and empty messages
            if role == "system" or not content.strip():
                continue
            messages.append({"role": role, "content": content})

        # Add current user question with context
        messages.append({"role": "user", "content": user_content})

        try:
            response = self.client.chat.completions.create(
                model=self.model_name,
                messages=messages,
                temperature=0.7,
                max_tokens=500
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"Error generating response: {str(e)}"
