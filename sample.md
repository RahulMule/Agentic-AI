apigenius/
├── agents/
│   ├── base_agent.py
│   ├── requirements_parser.py
│   ├── schema_designer.py
│   ├── api_spec_generator.py
│   ├── code_generator.py
│   └── test_generator.py
│
├── core/
│   ├── agent_manager.py        # Orchestrator: routes tasks to agents
│   ├── pipeline.py             # Full pipeline from FRD to code output
│   └── utils.py                # Helpers (e.g., slugify, path resolver)
│
├── prompts/
│   ├── parser_prompt.txt
│   ├── schema_prompt.txt
│   ├── codegen_prompt.txt
│   └── testgen_prompt.txt
│
├── data/
│   ├── sample_requirements/
│   │   └── blog_system.md
│   └── outputs/
│       ├── blog_system/
│       │   ├── api/
│       │   │   ├── main.py
│       │   │   ├── models.py
│       │   │   └── routes/
│       │   │       ├── users.py
│       │   │       └── posts.py
│       │   ├── openapi.yaml
│       │   └── tests/
│       │       └── test_posts.py
│       └── ...
│
├── config/
│   └── settings.py             # LlamaIndex & Ollama settings, model config
│
├── index/
│   ├── frd_index.json          # Persisted LlamaIndex vector store
│   └── loader.py               # Loads and indexes FRD
│
├── main.py                     # CLI entry point
├── app.py                      # Optional: Web UI using FastAPI/Streamlit
├── requirements.txt
├── README.md
└── .env                        # For model paths, keys, etc.
