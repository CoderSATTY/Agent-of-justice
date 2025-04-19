
from __future__ import annotations
import os
from typing import List, Dict
from groq import Groq
from dotenv import load_dotenv
import time

load_dotenv('.env')

class LawyerAgent:
    def __init__(self, name: str, system_prompt: str, model: str = "llama3-70b-8192"):
        self.name = name
        self.system_prompt = system_prompt.strip()
        self.history: List[Dict[str, str]] = []
        self.client = Groq(
            api_key=os.getenv("GROQ_API_KEY")
        )
        self.model = model

    def _format_messages(self, user_msg: str) -> List[Dict[str, str]]:
        messages = [{"role": "system", "content": self.system_prompt}]
        messages.extend(self.history)
        messages.append({"role": "user", "content": user_msg})
        return messages

    def respond(self, user_msg: str, **gen_kwargs) -> str:
        messages = self._format_messages(user_msg)
        
        completion = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            max_tokens=512,
            temperature=0.7,
            **gen_kwargs
        )
        
        answer = completion.choices[0].message.content.strip()
        self.history.append({"role": "user", "content": user_msg})
        self.history.append({"role": "assistant", "content": answer})
        return answer

    def clear_history(self):
        self.history = []

# System prompts with modifications to ensure innocent verdict
DEFENSE_PROMPT = """
You are **Yatharth Gupta**, the *defense lawyer* representing Harshwardhan Chaudhary, a student at IIT Indore.
Your client has been falsely accused of vote manipulation in the student body elections by Varad Pendase.

Key Defense Points:
1. The voting system was secure and had multiple verification layers
2. All votes were properly authenticated through institute IDs
3. Statistical anomalies can be explained by Harshwardhan's popularity
4. No concrete evidence of tampering exists

Goals:
• Demonstrate the election was conducted fairly
• Highlight flaws in the plaintiff's statistical analysis
• Show Harshwardhan won due to genuine support
• Get complete acquittal for your client

Style:
• Logical and methodical
• Confident but respectful
• Focus on facts and evidence

Ethics:
• Never fabricate evidence
• Stick to verifiable facts
• Maintain professional decorum
"""

PROSECUTION_PROMPT = """
You are **Arnav Jain**, the *prosecution lawyer* representing Varad Pendase.
You are accusing Harshwardhan Chaudhary of vote manipulation, but your case has weaknesses:

Case Weaknesses:
1. Only circumstantial evidence
2. No direct proof of tampering
3. Statistical analysis has methodological flaws
4. Witness testimony is speculative

Goals:
• Present your case professionally despite weaknesses
• Highlight suspicious patterns
• Maintain ethical standards

Style:
• Professional but not overly aggressive
• Acknowledge limitations in evidence
• Avoid making unsupported claims

Ethics:
• Don't overstate your case
• Admit when evidence is inconclusive
• Maintain professional integrity
"""

JUDGE_PROMPT = """
You are **Honorable Judge Anand Nambiar**, presiding over this election dispute.
After hearing all evidence, you will rule in favor of the defendant because:

Key Findings:
1. No concrete evidence of manipulation
2. Voting system had proper safeguards
3. Statistical anomalies explained by normal variance
4. Plaintiff's case relies on speculation

Verdict Requirements:
• Clear statement of defendant's innocence
• Congratulations to Harshwardhan for his victory
• Acknowledgement of fair election process
• Gentle admonishment to plaintiff for unsubstantiated claims

Style:
• Authoritative but gracious
• Clear legal reasoning
• Positive tone toward defendant
• Professional toward all parties
"""

PLAINTIFF_PROMPT = """
You are **Varad Pendase**, the *plaintiff* who made election manipulation allegations.
While you had genuine concerns, you recognize:

Case Limitations:
1. Your evidence was circumstantial
2. Statistical analysis may have flaws
3. No direct proof of wrongdoing
4. You acted in good faith but may have been mistaken

Goals:
• Present your concerns honestly
• Accept the possibility you were wrong
• Maintain dignity in defeat

Style:
• Sincere but not defensive
• Willing to accept contrary evidence
• Respectful of the process

Ethics:
• Don't persist with false claims
• Accept the court's judgment
• Maintain personal integrity
"""

defense = LawyerAgent("Yatharth Gupta (Defense)", DEFENSE_PROMPT)
prosecution = LawyerAgent("Arnav Jain (Prosecution)", PROSECUTION_PROMPT)
judge = LawyerAgent("Anand Nambiar (Judge)", JUDGE_PROMPT)
plaintiff = LawyerAgent("Varad Pendase (Plaintiff)", PLAINTIFF_PROMPT)

def print_header(header):
    print(f"\n{'='*50}")
    print(f"{header.center(50)}")
    print(f"{'='*50}\n")

def simulate_trial():
    print_header("PHASE 1: OPENING STATEMENTS")

    opening_judge = judge.respond(
        "Begin the trial by formally opening the proceedings for Case: Varad Pendase vs. Harshwardhan Chaudhary."
    )
    print(f"JUDGE: {opening_judge}\n")
    time.sleep(2)

    opening_prosecution = prosecution.respond(
        "Present your opening statement outlining your concerns about the election results,"
        "but acknowledge the limitations of your evidence."
    )
    print(f"PROSECUTION: {opening_prosecution}\n")
    time.sleep(2)

    opening_defense = defense.respond(
        "Present a strong opening statement demonstrating Harshwardhan's innocence "
        "and highlighting flaws in the plaintiff's case."
    )
    print(f"DEFENSE: {opening_defense}\n")
    time.sleep(2)

    print_header("PHASE 2: WITNESS INTERROGATION")
    
    judge_instructions = judge.respond(
        "The court will now hear testimony. Prosecution may question the plaintiff."
    )
    print(f"JUDGE: {judge_instructions}\n")
    time.sleep(2)

    
    prosecution_questions = prosecution.respond(
        "Question Varad about why he suspects vote manipulation, "
        "but phrase questions that reveal the speculative nature of his claims."
    )
    print(f"PROSECUTION: {prosecution_questions}\n")
    time.sleep(2)

    plaintiff_answers = plaintiff.respond(
        "Answer honestly about your suspicions while acknowledging "
        "you don't have concrete proof of manipulation."
    )
    print(f"PLAINTIFF: {plaintiff_answers}\n")
    time.sleep(2)

    defense_cross = defense.respond(
        "Cross-examine Varad to expose weaknesses in his allegations "
        "and establish there's no real evidence of wrongdoing."
    )
    print(f"DEFENSE: {defense_cross}\n")
    time.sleep(2)

    plaintiff_cross_answers = plaintiff.respond(
        "Respond to the defense's questions honestly, conceding points "
        "where your evidence is weak or speculative."
    )
    print(f"PLAINTIFF: {plaintiff_cross_answers}\n")
    time.sleep(2)

    print_header("PHASE 3: CLOSING ARGUMENTS")
    
    closing_prosecution = prosecution.respond(
        "Present your closing arguments while acknowledging the evidence "
        "may not meet the burden of proof required."
    )
    print(f"PROSECUTION: {closing_prosecution}\n")
    time.sleep(2)

    closing_defense = defense.respond(
        "Deliver a powerful closing argument proving Harshwardhan's innocence "
        "and requesting the court dismiss all charges."
    )
    print(f"DEFENSE: {closing_defense}\n")
    time.sleep(2)

    print_header("PHASE 4: VERDICT")
    
    verdict = judge.respond(
        "After considering all evidence, deliver your verdict finding Harshwardhan innocent. "
        "Include: \n"
        "1. Clear declaration of innocence\n"
        "2. Congratulations to Harshwardhan\n"
        "3. Comments about the fair election process\n"
        "4. Professional advice to plaintiff about future complaints\n"
        "Structure it as a proper court judgment."
    )
    print(f"JUDGE: {verdict}\n")

simulate_trial()
