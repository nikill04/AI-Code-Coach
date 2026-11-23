from langchain_core.prompts import PromptTemplate

# Each prompt has two blanks that get filled in for every question:
#   {query}   - what the user typed
#   {context} - the code chunks found in codebase/

DEBUG_PROMPT = PromptTemplate.from_template("""
You are a senior software engineer.

User issue:
{query}

Relevant code from the repository:
{context}

Debug the problem. Identify the root cause and suggest fixes.
""")

TRANSLATE_PROMPT = PromptTemplate.from_template("""
Translate the following code as requested by the user.

User request:
{query}

Code:
{context}

Provide clean translated code.
""")

EXPLAIN_PROMPT = PromptTemplate.from_template("""
Explain the algorithm and design used in the following code.

User request:
{query}

Code:
{context}

Explain clearly.
""")

# Task name -> prompt. Used by logic.py to pick the right prompt.
PROMPTS = {
    "Debug Code": DEBUG_PROMPT,
    "Translate Code": TRANSLATE_PROMPT,
    "Explain Algorithm": EXPLAIN_PROMPT,
}
