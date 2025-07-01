# API Genius — Agentic AI for REST API Generation from Functional Specs

## Overview

**API Genius** is an agentic AI application designed to automatically generate REST APIs from functional requirement documents (FSDs).  
It uses a multi-agent architecture leveraging:

- **LlamaIndex** for local document ingestion, chunking, and vector indexing
- **MistralAI (via Ollama)** as a local large language model (LLM) for natural language understanding and generation
- **FastAPI** for serving the generated API code (future extension)

This project demonstrates how to build fully **local, private, and GPU-accelerated AI workflows** for software automation.

---

## Key Components

| Component          | Purpose                                               |
|--------------------|-------------------------------------------------------|
| `LlamaIndex`       | Document parsing, chunking, local embedding & retrieval |
| `MistralAI` via `Ollama` | Local open-weight LLM for prompt completion and generation |
| `FastAPI`          | Web framework to serve generated APIs (planned)         |
| Multi-agent system | Agents for parsing requirements, designing schemas, generating code |

---

## Hardware & Environment Requirements

- This project runs **fully locally** — no cloud API calls or external services needed after setup.
- You **need a GPU with at least 8GB of VRAM or more** to efficiently run the MistralAI model via Ollama.
- The tested example GPU is an **RTX 5060 with 8GB VRAM**, but any GPU with similar VRAM (from NVIDIA or other vendors) should work.
- Running on CPU only is possible but will be significantly slower.
- Ensure your GPU drivers and CUDA/OpenCL libraries are properly installed for optimal performance.

---

## Installation

### 1. Clone this repository

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

MIT License © 2025 Your Name

---

Feel free to open issues or contribute!
