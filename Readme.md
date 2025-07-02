# API Genius — Agentic AI for REST API Generation from Functional Specs

## 🚀 Overview

**API Genius** is a modular, multi-agent AI application that automatically generates **REST APIs** from **functional specification documents (FSDs)**.

Built for developers who want to convert business requirements into production-ready backend code, API Genius uses **local LLMs**, **document indexing**, and **agentic workflows** to orchestrate the full process — **securely and offline**.

### 🎯 Key Highlights

- Local-first, GPU-accelerated, and fully private (no cloud APIs)
- Step-by-step multi-agent orchestration using [LlamaIndex FunctionAgent + AgentWorkflow](https://docs.llamaindex.ai/en/stable/examples/agents/function_agents/)
- Designed for future extensibility: schema generation, OpenAPI docs, test case creation, and more

---

## 🧠 Agent Architecture

| Agent Name                | Purpose                                                                 |
|---------------------------|-------------------------------------------------------------------------|
| `RequirementsParserAgent` | Parses FSDs and extracts requirements via RAG and tool calling only     |
| `SchemaGeneratorAgent`    | Creates database or Pydantic models from parsed requirements *(planned)*|
| `CodeGeneratorAgent`      | Generates FastAPI-compatible route logic *(planned)*                   |
| `OpenAPIGeneratorAgent`   | Creates OpenAPI v3 specifications *(planned)*                           |
| `TestCaseGeneratorAgent`  | Builds test cases based on validations & constraints *(planned)*        |

Each agent is built using **FunctionAgent** with dedicated tools, context memory, and clear reasoning prompts.

---

## 🧱 Tech Stack

| Tool / Library         | Role                                                        |
|------------------------|-------------------------------------------------------------|
| **LlamaIndex**         | Indexing, RAG, memory, FunctionAgent orchestration          |
| **Mistral (via Ollama)** | Local LLM for tool-using agents                             |
| **FastAPI**            | Framework to serve generated backend (target output)        |
| **Python**             | Core language for orchestration                             |

---

## 🖥️ System Requirements

- ✅ **Fully local setup** — no internet or OpenAI keys required
- ⚙️ Python 3.10+
- 🧠 GPU with **8GB VRAM or higher** recommended (e.g., RTX 4060/5060)
- 🐌 CPU-only fallback possible but slower
- 📦 Ensure latest NVIDIA drivers + CUDA installed (if using GPU)

---

## 🛠️ Installation

### 1. Clone the repository

```bash
git clone https://github.com/yourusername/apigenius.git
cd apigenius

### 2. Set up Python environment

    python -m venv venv
    source venv/bin/activate  # Linux/macOS
    venv\Scripts\activate     # Windows

    pip install --upgrade pip
    pip install -r requirements.txt

### 3. Install Ollama and MistralAI model

Ollama is the local LLM manager and runtime for MistralAI:

#### Install Ollama

- **macOS / Linux**

    curl -fsSL https://ollama.com/install.sh | sh

- **Windows**

Download installer from https://ollama.com/download

#### Pull Mistral Model

    ollama pull mistral

Verify it runs:

    ollama run mistral

---

## Usage

1. Prepare your functional requirement document (`.md` file) in `data/sample_requirements/`.

2. Run the main script to parse requirements and extract API endpoints plus business logic:

    python main.py

3. The output will be a JSON structure listing endpoints with detailed business logic extracted from your FSD.

---

## Project Structure

    apigenius/
    ├── agents/               # Agent classes (BaseAgent, RequirementsParserAgent, etc.)
    ├── config/               # Configuration files
    ├── data/                 # Sample requirements and generated outputs
    ├── prompts/              # Prompt templates for agents
    ├── main.py               # Entry point to run agents
    ├── requirements.txt      # Python dependencies
    └── README.md             # This file

---

## Notes

- This project is **GPU-accelerated**. Running Ollama and Mistral on CPU only is possible but will be significantly slower.
- Ensure your GPU drivers and CUDA toolkit/OpenCL are properly installed and compatible with your setup.
- For best performance, have a GPU with **at least 8GB VRAM**.

---

## Future Enhancements

- Extend the multi-agent pipeline to generate full FastAPI route implementations from extracted business logic.
- Add automated testing generation based on parsed business rules.
- Implement a web interface for uploading FSDs and managing generated APIs.

---

## References & Resources

- [LlamaIndex Documentation](https://gpt-index.readthedocs.io/)
- [Ollama](https://ollama.com/)
- [MistralAI](https://www.mistral.ai/)
- [FastAPI](https://fastapi.tiangolo.com/)

---

## License

MIT License © 2025

---

Feel free to open issues or contribute!
