# Agent-of-justice
This is a MAS(Multi Agent System) based Court room simulation which fetches court case or court case_id from the dataset as input and tries to depict real time court trial simulation followed with real life instances occuring inside the court. 

## Architecture 
The court room simulation is done by 4 Agents i.e. Judge, Plaintiff, Defense Lawyer, Prosecution Lawyer. The Defendant and Witnesses have very small yet necessary parts and thus they are dynamically called as the court trial proceeds but they are only instantiated at a particular time of simulation so no Agents were created for that case. I have also added one more Agent named as Summarizer who will ensure the token limit (TPM) is not exceeding by summarizing the contextualized text.       
The architecture uses these 5 core agents, each playing a courtroom role (except the Summarizer) which is the boundary condition for the Agent's behaviour, powered by Groq-hosted LLaMA 3 models:

| Role| Description |
|----------|----------|
| Judge | Ensures fair trial, rules objections, delivers verdict |
| Plaintiff	 | Presents the civil claim and legal damages| 
|  Prosecution	 | Argues the case on behalf of the state| 
| Defense	 | Defends the accused and rebuts prosecution | 
| Summarizer | Condenses lengthy case texts to prevent token overflow| 

I have used LLaMA 3b-8192 model as my LLM which gave sufficiently good outputs!
## Execution Flow


Passes the summary to simulate()
### `main()` Function:
- Prompts the user for a case ID or custom case description
- Loads the corresponding case text from data.csv or user input
- Uses the Summarizer Agent to reduce the text to a token-safe summary
- Passes the summary to `simulate()`

### `simulate()` Function:
Runs a structured courtroom sequence:
1. **Opening Statements**
   - Prosecution presents theory
   - Defense counters arguments
2. **Witness Interrogation & Argumentation**
   - Direct examination (by calling attorney)
   - Cross-examination (opposing attorney)
   - Rebuttals
3. **Closing Statements**
   - Final persuasive arguments
4. **Judge’s Verdict**
   - Decision based on arguments
   - Sentencing (if applicable)

> **Note:** Each phase involves interactive back-and-forth between agents. 

## Setup Instructions
1. Clone this repository
```bash
git clone https://github.com/CoderSATTY/Agent-of-justice.git
```
### Requirements

Python 3.8+ is required.\
2. Install dependencies from the requirements.txt file
```bash
pip install -r requirements.txt
```
3. Create a .env file in the root directory with your Groq API key:

```env
GROQ_API_KEY=your_api_key_here
```
4. Place your input data path in the code before running the scripts

5. Run the scripts (see below)
```bash
python scripts/all_courtcases_simulation.py
```
```bash
python scripts/hardcoded_courtroom_simulation.py
```

