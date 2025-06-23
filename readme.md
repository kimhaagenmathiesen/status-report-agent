# LlamaIndex Agent Workflow Demo

This project demonstrates an agent-based AI workflow using **LlamaIndex** and **Ollama**. The agent retrieves and filters structured data (e.g., measurements and comments) from a CSV file (`input.csv`) based on a specified date range. This forms the foundation for data-driven question answering and reporting.

---

## ✨ Features

- Uses `AgentWorkflow` + `ReActAgent` (LlamaIndex)
- Custom tools:
  - `get_data`: filters data by date
  - `get_comments`: extracts comments from filtered data
- Async implementation
- Context state tracking (e.g., number of tool calls)
- Language-agnostic: demo uses Danish, but supports any language

---

## 📂 Example `input.csv`

Dato,Måling,Kommentar
01-01-2025,2,"Alt OK"
15-01-2025,3,"Mindre fejl observeret"
25-01-2025,4,"Alt OK"
05-02-2025,0,"Større problem fundet"
15-02-2025,3,"Alt OK" 

---

## 💬 Example Query

**Prompt:**  
Hent kommentarer fra perioden 01-01-2025 til 31-01-2025 i input.csv og print data, måling og kommentar.

**Expected filtered data:**  
01-01-2025,10,"Alt OK"  
15-01-2025,12,"Mindre fejl observeret"  
25-01-2025,11,"Alt OK"  

**Expected comments:**  
"Alt OK", "Mindre fejl observeret", "Alt OK"  

---

## ⚙️ Setup

Create and activate a virtual environment:
```
python3 -m venv venv
source venv/bin/activate   
```
Install dependencies:
```
pip3 install -r requirements.txt
```

---

## 📦 `requirements.txt`

llama-index-core  
llama-index-llms-ollama  
pandas  

---

## 🚀 Run

```
python agent_workflow.py
```

---

## 📌 Notes

- The agent demonstrates local language prompt handling (Danish), but works with any language.
- Can be extended for reporting, statistical summaries, or advanced queries.

---

## 📝 License

MIT License.
