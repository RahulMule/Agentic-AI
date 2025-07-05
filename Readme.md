# API Genius — Agentic AI for REST API Generation from Functional Specs

## 🚀 Overview

**API Genius** is a modular, multi-agent AI application that automatically generates **REST APIs** from **functional specification documents (FSDs)**.

Designed for backend developers, API Genius reads your requirements, extracts business logic, generates database schemas, and plans backend APIs — all using intelligent AI agents powered by **LlamaIndex**, **Streamlit**, and **Groq LLMs**.

## 🎯 Key Highlights

* Streamlit-powered **interactive UI** for ease of use
* Uses **Groq-hosted LLaMA 3.1 models** (free with limits) for reliable responses
* Step-by-step **agent-based orchestration** using [LlamaIndex FunctionAgent + AgentWorkflow](https://docs.llamaindex.ai/en/stable/examples/agents/function_agents/)
* Modular and extensible pipeline for parsing specs, generating schema, APIs, OpenAPI docs, tests, and more
* Optional support for **local LLMs via Ollama**

## 🧠 Agent Architecture

| Agent Name                | Purpose                                                             |
| ------------------------- | ------------------------------------------------------------------- |
| `RequirementsParserAgent` | Parses FSDs and extracts requirements via RAG and tool calling only |
| `SchemaGeneratorAgent`    | Creates database schemas or Pydantic models                         |
| `CodeGeneratorAgent`      | *(Planned)* Generate FastAPI route logic                            |
| `OpenAPIGeneratorAgent`   | *(Planned)* Create OpenAPI v3 specs                                 |
| `TestCaseGeneratorAgent`  | *(Planned)* Build test cases based on constraints                   |

All agents are built using **FunctionAgent** and **tool calling**, with memory between stages.

## 📊 Tech Stack

| Tool / Library          | Role                                                              |
| ----------------------- | ----------------------------------------------------------------- |
| **LlamaIndex**          | RAG, FunctionAgent, indexing, context memory                      |
| **Groq LLaMA 3.1 API**  | Fast and accurate hosted LLM (free with usage caps)               |
| **Streamlit**           | Frontend to interactively run and view agent execution            |
| **Python**              | Core language                                                     |
| **Ollama (optional)**   | Local LLM runtime (Mistral or Code LLaMA) — fallback if preferred |
| **FastAPI** *(planned)* | Target backend framework to generate APIs                         |

## 💻 System Requirements

* ✅ Works with **Groq** hosted LLMs — no GPU required
* ⚙️ Python 3.10+
* 💼 Optional: 8GB+ GPU if running Ollama locally
* 📱 Internet access needed for Groq model usage

## 🛠️ Installation

### 1. Clone the repo

```bash
git clone https://github.com/yourusername/apigenius.git
cd apigenius
```

### 2. Set up Python environment

```bash
python -m venv .venv
source .venv/bin/activate        # macOS/Linux
.venv\Scripts\activate           # Windows

pip install --upgrade pip
pip install -r requirements.txt
```

### 3. Configure your secrets

Create a `.env` file in the root:

```env
GROQ_API_KEY=your_groq_api_key_here
```

> You can get your key from [https://console.groq.com](https://console.groq.com)

## ⏺️ Running the App

### ▶️ Option 1: Using Streamlit UI

```bash
streamlit run app.py
```

* Upload or edit your FSD document
* Click "Run Agents"
* View live streaming output from each agent
* Final schema and requirements will be saved in `./data/req.txt`

### ▶️ Option 2: CLI Execution

```bash
python main.py
```

The agents will stream step-by-step reasoning and tool usage to the console. Output is saved in `./data/req.txt`.

## 📁 Project Structure

```
apigenius/
├── agents/                # Agent definitions
├── config/                # Pydantic settings + secrets
├── data/                  # Input/output files
├── prompts/               # Prompt templates for agents
├── app.py                 # Streamlit frontend
├── main.py                # CLI entrypoint
├── requirements.txt       # Python dependencies
└── README.md              # This file
```

## ☁️ Azure Web App Deployment (Optional)

To deploy on Azure:

1. Set up an Azure Web App for Python
2. Add your `GROQ_API_KEY` as an application setting in Azure Portal
3. Set startup command:

```bash
streamlit run app.py --server.port 8000
```

4. Push code via GitHub Actions or VSCode

## 🔐 Environment & Secrets

Manage secrets using **Pydantic Settings** via `.env`:

```python
# config/secrets.py
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    groq_api_key: str

    class Config:
        env_file = ".env"
```

Use in agents:

```python
from config.secrets import Settings
settings = Settings()
```

## ⚡ Notes

* Groq LLaMA 3.1 models are **significantly faster** and more accurate than local Mistral in most cases
* Local models (Ollama) are still supported for offline fallback
* GPU recommended for local models: RTX 4060 or higher

## 🔮 Future Enhancements

* ✅ Streamlit frontend (added)
* 🧠 Code generation agent (planned)
* 📄 OpenAPI doc generation
* 🧪 Automated test case generation
* ☁️ Optional database scaffolding and FastAPI project export

## 📚 References

* [Groq](https://console.groq.com)
* [LlamaIndex](https://docs.llamaindex.ai/)
* [Streamlit](https://streamlit.io/)
* [FastAPI](https://fastapi.tiangolo.com/)
* [Ollama](https://ollama.com/)

## 🗪 License

MIT License © 2025

Feel free to ⭐ the repo and contribute!
