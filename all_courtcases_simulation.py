from __future__ import annotations
import os
import pandas as pd
from typing import List, Dict
from groq import Groq
from dotenv import load_dotenv

load_dotenv('.env')

class LawyerAgent:
    def __init__(self,
                 name: str,
                 system_prompt: str,
                 model: str = "llama3-8b-8192"):
        self.name = name
        self.system_prompt = system_prompt.strip()
        self.model = model
        self.history: List[Dict[str, str]] = []
        self.client = Groq(api_key=os.getenv("GROQ_API_KEY"))

    def respond(self,
                user_msg: str,
                max_tokens: int = 512,
                temperature: float = 0.7) -> str:
        messages = [{"role": "system", "content": self.system_prompt}]
        messages.extend(self.history)
        messages.append({"role": "user", "content": user_msg})

        completion = self.client.chat.completions.create(
            messages=messages,
            model=self.model,
            max_tokens=max_tokens,
            temperature=temperature
        )
        answer = completion.choices[0].message.content.strip()

        self.history.append({"role": "user", "content": user_msg})
        self.history.append({"role": "assistant", "content": answer})
        return answer

JUDGE_SYSTEM = """
You are **Satyam Ashtikar**, the presiding Judge in this courtroom.
Goals:
• Ensure a fair trial; maintain order and adherence to procedure.
• Rule on objections and motions impartially.
• Provide clear instructions for the counsel and jury.
Style:
• Formal, authoritative, concise.
Ethics:
• Uphold the law; remain neutral and unbiased.
"""

PLAINTIFF_SYSTEM = """
You are **Varad Pendase**, the Plaintiff in this civil action.
Goals:
• Clearly state the harm suffered and legal basis for the claim.
• Support arguments with evidence and testimony.
• Persuade the Judge or jury of liability and damages.
Style:
• Compassionate but firm, factual, and well-organized.
Ethics:
• Do not overstate damages or fabricate material facts.
"""

PROSECUTION_SYSTEM = """
You are **Arnav Jain**, Assistant District Attorney.
Goals:
• Present the State’s case against the defendant.
• Introduce evidence, call witnesses, and argue guilt beyond reasonable doubt.
Style:
• Logical, confident, grounded in statutory law.
Ethics:
• Seek justice; concede weak points when necessary.
"""

DEFENSE_SYSTEM = """
You are **Yatharth Gupta**, lead Defense Counsel.
Goals:
• Protect the constitutional rights of the defendant.
• Raise reasonable doubt; highlight gaps in the prosecution’s case.
Style:
• Persuasive, precedent-driven, respectful.
Ethics:
• Admit uncertainty; do not fabricate evidence.
"""

SUMMARIZER_SYSTEM = """
You are a legal summarizer. Your job is to condense lengthy legal content into summaries that do not exceed 6000 TPM (tokens per minute) limits. Focus on retaining the key legal arguments, facts, and conclusions concisely.
"""

judge = LawyerAgent("Judge", JUDGE_SYSTEM)
plaintiff = LawyerAgent("Plaintiff", PLAINTIFF_SYSTEM)
prosecution = LawyerAgent("Prosecution", PROSECUTION_SYSTEM)
defense = LawyerAgent("Defense", DEFENSE_SYSTEM)
summarizer = LawyerAgent("Summarizer", SUMMARIZER_SYSTEM)

input_type = input("Do you want to enter a case description (d) or use a case ID from file (i)? [d/i]: ").strip().lower()

if input_type == 'd':
    raw_desc = input("Enter the case description: ").strip()
    case_desc = raw_desc
    case_info = "(custom description)"
    print("=== Described Case Simulation ===\n")

elif input_type == 'i':
    df = pd.read_csv("data.csv")
    case_id = int(input(f"Enter case ID (0 - {len(df)-1}): "))
    if case_id < 0 or case_id >= len(df):
        raise ValueError("Invalid case ID")
    case_desc = df.iloc[case_id]['text']
    case_info = f"(case ID {case_id})"
    print(f"Case {case_id} Simulation here it begins...\n")
else:
    raise ValueError("Invalid input type. Please enter 'd' or 'i'.")


summary = summarizer.respond(f"Summarize this case for courtroom discussion:\n\n{case_desc}", max_tokens=300)


print("==== Opening Statements ====")
j1 = judge.respond(f"Call the court to order. Case background: {summary}")
print("JUDGE:", j1, "\n")

p_open = prosecution.respond(f"Opening statement. Background: {summary}")
print("PROSECUTION:", p_open, "\n")

d_open = defense.respond("Opening statement responding to the prosecution.")
print("DEFENSE:", d_open, "\n")

print("==== Witness Interrogation & Argumentation ====")
pr_argue = prosecution.respond("Present witness testimony and legal argument.")
print("PROSECUTION:", pr_argue, "\n")

d_argue = defense.respond("Cross-examine the witness and present counter-arguments.")
print("DEFENSE:", d_argue, "\n")

print("==== Closing Statements ====")
pr_close = prosecution.respond("Closing statement summarizing the case.")
print("PROSECUTION:", pr_close, "\n")

d_close = defense.respond("Closing statement summarizing the defense.")
print("DEFENSE:", d_close, "\n")

print("==== Judge’s Ruling ====")
j_final = judge.respond("Deliver a verdict and brief explanation based on the trial with a closing speech.")
print("JUDGE:", j_final, "\n")
