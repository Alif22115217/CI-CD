import streamlit as st
import pandas as pd
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate


# Load API key
path_file = "C:\KULIAH\KAMPUS MERDEKA CELERATES DATA SCIENCE\master_keys.xlsx"
API_KEY = pd.read_excel(path_file)["api_key"][1]


# Define chat function
def chat(contexts, history, question, persona):
    llm = ChatGoogleGenerativeAI(
        model="gemini-1.5-flash",
        temperature=0.7,
        api_key=API_KEY
    )
    
    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                f"You are a {persona}. Use the provided data and chat history to answer user questions intelligently.",
            ),
            ("human", "This is the data: {contexts}\nChat history for context: {history}\nUser question: {question}"),
        ]
    )
    
    chain = prompt | llm
    completion = chain.invoke(
        {
            "contexts": contexts,
            "history": history,
            "question": question,
        }
    )

    answer = completion.content
    input_tokens = completion.usage_metadata['input_tokens']
    completion_tokens = completion.usage_metadata['output_tokens']

    return {
        "answer": answer,
        "input_tokens": input_tokens,
        "completion_tokens": completion_tokens
    }


# Streamlit App
st.title("AI Chatbot Assistant")

# Persona Selector
persona_options = ["Helpful Assistant", "Data Analyst", "Business Consultant"]
selected_persona = st.selectbox("Select Chatbot Persona:", options=persona_options)

# File Uploader
uploaded_file = st.file_uploader("Upload a dataset (CSV, XLS, or XLSX):", type=["csv", "xls", "xlsx"])

if uploaded_file:
    try:
        # File loading
        if uploaded_file.name.endswith('.csv'):
            df = pd.read_csv(uploaded_file)
        elif uploaded_file.name.endswith(('.xls', '.xlsx')):
            df = pd.read_excel(uploaded_file)
        else:
            st.error("Unsupported file format!")
            df = None

        # Data Insights
        if df is not None:
            df = df.drop_duplicates()
            contexts = df.head(5).to_string()  # Only summarize first 5 rows for context
            st.success(f"Loaded `{uploaded_file.name}` successfully!")
            
            with st.expander("📊 Data Insights"):
                st.write(f"**Shape**: {df.shape}")
                st.write(f"**Columns**: {list(df.columns)}")
                st.write(f"**Missing Values**:\n{df.isnull().sum()}")
                st.write("**Quick Summary**:")
                st.dataframe(df.describe(include='all'))
                
    except Exception as e:
        st.error(f"Error while loading the file: {e}")
        df = None
        contexts = ''
else:
    st.info("Upload a dataset to enable data-driven responses.")
    contexts = ''

# Initialize session state for chat history and token tracking
if "messages" not in st.session_state:
    st.session_state["messages"] = []
if "total_tokens" not in st.session_state:
    st.session_state["total_tokens"] = {"input": 0, "completion": 0}

# Display previous messages
for message in st.session_state["messages"]:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User Input Section
if prompt := st.chat_input("Ask me anything!"):
    # Limit chat history to the last 10 messages for model input
    messages_history = st.session_state.get("messages", [])[-10:]
    history = "\n".join([f'{msg["role"]}: {msg["content"]}' for msg in messages_history]) or " "

    # Display user message
    st.chat_message("user").markdown(prompt)
    st.session_state["messages"].append({"role": "user", "content": prompt})

    # Generate chatbot response
    response = chat(contexts, history, prompt, selected_persona)
    answer = response["answer"]
    input_tokens = response["input_tokens"]
    completion_tokens = response["completion_tokens"]

    # Update token usage
    st.session_state["total_tokens"]["input"] += input_tokens
    st.session_state["total_tokens"]["completion"] += completion_tokens

    # Display response
    with st.chat_message("assistant"):
        st.markdown(answer)
        with st.container():
            st.write(f"**Input Tokens:** {input_tokens}")
            st.write(f"**Completion Tokens:** {completion_tokens}")
    
    # Add assistant response to chat history
    st.session_state["messages"].append({"role": "assistant", "content": answer})

    # Display full chat history (expandable)
    with st.expander("💬 Chat History"):
        for msg in st.session_state["messages"]:
            role = "User" if msg["role"] == "user" else "Assistant"
            st.markdown(f"**{role}:** {msg['content']}")

# Display cumulative token usage
st.sidebar.title("Session Summary")
st.sidebar.write(f"**Total Input Tokens:** {st.session_state['total_tokens']['input']}")
st.sidebar.write(f"**Total Completion Tokens:** {st.session_state['total_tokens']['completion']}")
st.sidebar.write(f"**Total Tokens:** {sum(st.session_state['total_tokens'].values())}")
