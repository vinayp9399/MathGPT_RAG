# Text To Math Problem Solver And Data Search Assistant

An interactive Multi-Tool AI Agent application built with Streamlit. This project leverages **LangChain ReAct Agents** and Groq's high-performance `llama-3.3-70b-versatile` model to combine natural language reasoning, automated internet search via Wikipedia, and a secure, injection-proof mathematical calculator.

**Live Link:** 

---

## 📌 Introduction

Large Language Models (LLMs) are exceptionally talented at generating text and writing creative prose, but they are notoriously unreliable when tasked with complex mathematics or sourcing real-time factual trivia. They tend to hallucinate mathematical totals or lack awareness of niche data.

This application overcomes these computational bottlenecks by wrapping the LLM inside an autonomous **ReAct (Reasoning and Action) Agent Toolkit**. Instead of guessing calculations or web queries, the agent evaluates incoming problems dynamically and shifts responsibilities to specific dedicated toolkits: executing complex string math securely via a sandboxed python parser, scraping internet reference files using Wikipedia API wrappers, or utilizing high-level structured prompt reasoning.

---

## 💼 Practical Use Cases

* **Complex Word-Problem Deciphering:** Input long-form math riddles (e.g., inventory counts, conditional logic statements) and watch the agent break down the word puzzle into separate, logical steps.
* **Homework & Academic Explanations:** Get point-by-point educational breakdowns of math, logic, and physics problems with fully expanded procedural explanations instead of a single flat answer number.
* **Contextual Fact-Checking & Arithmetic:** Ask multi-layer questions requiring external knowledge followed by operational computation (e.g., *"Look up the population of Tokyo, divide it by 100, and multiply the result by 5"*).
* **General Analytical Discovery:** Solve multi-step puzzle problems that require a combination of general knowledge extraction and step-by-step rationalization.

---

## ⚙️ How It Works

The system utilizes an automated choice-loop architecture to break down compound user questions:

1. **The ReAct Agent Controller:** The core `llama-3.3-70b-versatile` engine handles incoming user questions inside a rigid **Thought ➔ Action ➔ Observation** loops protocol.
2. **Wikipedia API Integration:** If the problem references historical entities, geographical milestones, or scientific constants, the model calls the `WikipediaAPIWrapper` to fetch highly accurate internet baseline records.
3. **Bulletproof Safe Calculator:** To handle equations flawlessly without standard LLM arithmetic drift, text inputs are redirected to a customized computation function. This module uses Python regular expressions to extract purely numeric text expressions and processes them safely using a sandbox configuration (`__builtins__: None`) to prevent malicious arbitrary code execution.
4. **Logical Reasoning Engine:** For structural abstract challenges, a dedicated sub-prompt `LLMChain` forces the model to structure final answers in clean, sequential, point-wise layouts.
5. **Live Step-by-Step Visualization:** The execution journey, tool triggers, and internal computational logs are streamed to the interface using the `StreamlitCallbackHandler`.

---

## 🔄 The Process Flow

```text
               [User Submits Text/Math Problem]
                              │
                              ▼
                [LangChain ReAct Agent Engine]
                              │
         ┌────────────────────┼────────────────────┐
         ▼                    ▼                    ▼
 [Wikipedia Tool]      [Safe Calculator]   [Reasoning Tool]
  (Internet Lookup)    (Regex + Eval Sandbox) (Point-wise Chain)
         │                    │                    │
         └────────────────────┼────────────────────┘
                              │
                              ▼
                  [Tool Output Observation]
                              │
             Is Final Answer Achieved?
               ├──► NO  ➔ [Loop back to Agent Thought]
               └──► YES ➔ [Aggregate Final Output]
                              │
                              ▼
                 [Streamlit Callback Window]
                 (Live Trace & Success Display)
```

---

## Interacting with the UI
1. **Authenticate Agent:** Navigate to the application sidebar and input your Groq API key securely into the password input box.

2. **Input Complex Problem:** Type your targeted logic puzzle, history trivia, or compound mathematical word problem into the main text box area.

3. **Trace and Solve:** Click the "find my answer" button. The application will render an expandable trace logging screen displaying exactly which tools (Wikipedia, Calculator, or Reasoning Engine) are selected, followed immediately by a final structured solution report.

---

## 🏁 Conclusion
This application highlights a resilient framework for overcoming the classic native computation limits of generative language models. By managing LangChain ReAct agents over low-latency Groq Cloud Infrastructure, the utility smoothly transitions from creative semantic text parsing into deterministic mathematical calculations, delivering a flexible, audit-friendly agent interface.