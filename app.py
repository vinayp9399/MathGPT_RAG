import streamlit as st
import re
from langchain_groq import ChatGroq
from langchain_community.utilities import WikipediaAPIWrapper
from langchain_core.prompts import PromptTemplate
from langchain_core.tools import Tool
from langchain_community.callbacks.streamlit import StreamlitCallbackHandler

# Keeping classic structures for robust legacy tool interaction
from langchain_classic.agents import AgentExecutor
from langchain_classic.agents.react.agent import create_react_agent
from langchain_classic.chains import LLMChain

## Set up the Streamlit app
st.set_page_config(page_title="Text To Math Problem Solver And Data Search Assistant", page_icon="🧮")
st.title("Text To Math Problem Solver Using Google Gemma 2")

groq_api_key = st.sidebar.text_input(label="Groq API Key", type="password")

if not groq_api_key:
    st.info("Please add your Groq API key to continue")
    st.stop()

llm = ChatGroq(model="llama-3.3-70b-versatile", groq_api_key=groq_api_key)

## Initializing the tools
wikipedia_wrapper = WikipediaAPIWrapper()
wikipedia_tool = Tool(
    name="Wikipedia",
    func=wikipedia_wrapper.run,
    description="A tool for searching the Internet to find various information on the topics mentioned."
)

## Bulletproof Native Calculator Function
def safe_calculator_exec(expression: str) -> str:
    """
    Cleans up conversational noise from Chat LLMs, extracts 
    the raw mathematical expression, and evaluates it safely.
    """
    # Clean out common markdown formatting wrappers if present
    clean_expr = expression.replace("```text", "").replace("```python", "").replace("```", "").strip()
    
    # Isolate characters belonging to standard math equations
    math_match = re.search(r"[\d\s\+\-\*\/\(\)\.]+", clean_expr)
    if math_match:
        target_expression = math_match.group(0).strip()
        try:
            # Evaluate the safe math block preventing arbitrary code injection
            return str(eval(target_expression, {"__builtins__": None}, {}))
        except Exception as e:
            return f"Error evaluating expression: {str(e)}"
            
    return "Could not parse a valid mathematical expression out of the LLM response."

# Replacing legacy LLMMathChain with our resilient custom parsing Tool
calculator = Tool(
    name="Calculator",
    func=safe_calculator_exec,
    description="Useful for when you need to answer mathematical calculations. Input must be a string containing a basic math equation like '5 - 2 + (2 * 25)'."
)

prompt_text = """
You are an agent tasked with solving users' mathematical questions. Logically arrive at the solution and provide a detailed explanation
and display it point wise for the question below.
Question: {question}
Answer:
"""

prompt_template = PromptTemplate(
    input_variables=["question"],
    template=prompt_text
)

## Combine all the tools into chain
chain = LLMChain(llm=llm, prompt=prompt_template)

reasoning_tool = Tool(
    name="Reasoning_tool",
    func=chain.run,
    description="A tool for answering logic-based and reasoning questions."
)

tools = [wikipedia_tool, calculator, reasoning_tool]

## Define the explicit ReAct agent prompt layout
react_prompt = PromptTemplate.from_template(
    "Answer the following questions as best you can. You have access to the following tools:\n\n"
    "{tools}\n\n"
    "Use the following format:\n"
    "Question: the input question you must answer\n"
    "Thought: you should always think about what to do\n"
    "Action: the action to take, should be one of [{tool_names}]\n"
    "Action Input: the input to the action\n"
    "Observation: the result of the action\n"
    "... (this Thought/Action/Action Input/Observation can repeat N times)\n"
    "Thought: I now know the final answer\n"
    "Final Answer: the final answer to the original input question\n\n"
    "Begin!\n\n"
    "Question: {input}\n"
    "Thought: {agent_scratchpad}"
)

## Initialize the agent structure
agent = create_react_agent(llm=llm, tools=tools, prompt=react_prompt)
assistant_agent = AgentExecutor(
    agent=agent, 
    tools=tools, 
    verbose=True, 
    handle_parsing_errors=True
)

if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {"role": "assistant", "content": "Hi, I'm a Math chatbot who can answer all your maths questions!"}
    ]

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg['content'])

## Let's start the interaction
question = st.text_area(
    "Enter your question:",
    "I have 5 bananas and 7 grapes. I eat 2 bananas and give away 3 grapes. Then I buy a dozen apples and 2 packs of blueberries. Each pack of blueberries contains 25 berries. How many total pieces of fruit do I have at the end?"
)

if st.button("find my answer"):
    if question:
        with st.spinner("Generating response..."):
            st.session_state.messages.append({"role": "user", "content": question})
            st.chat_message("user").write(question)

            # Set up Streamlit Callback to show real-time thinking
            st_cb = StreamlitCallbackHandler(st.container(), expand_new_thoughts=False)
            
            # Execute logic using dictionary mapping via .invoke()
            res = assistant_agent.invoke(
                {"input": question}, 
                config={"callbacks": [st_cb]}
            )
            
            response = res["output"]
            
            st.session_state.messages.append({'role': 'assistant', "content": response})
            st.write('### Response:')
            st.success(response)
    else:
        st.warning("Please enter a question")