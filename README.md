# 🤖 Coding Agent MVP1 on Google Colab (free, no API key)

A mini **Claude Code–style coding agent** you can run for free in **Google Colab**. It chats with you, then **creates, reads, edits and lists files**, **runs shell commands** and manages **background jobs** (like a Flask server) inside a workspace folder, asking for your approval before it touches anything.

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/YOUR_USERNAME/YOUR_REPO/blob/main/Colab_Coding_Agent_MVP1.ipynb)

> ✅ **Tested on Colab** with a free **Tesla T4 GPU** and **`qwen2.5:7b`** served by **Ollama**. No paid API, no Hugging Face credits.

Adapted from `5.CodingAgentMVP1` in [singhsanket143/AiEngineeringConcepts](https://github.com/singhsanket143/AiEngineeringConcepts). The original uses the OpenAI API; this version swaps the model layer so it runs on free models.

## Features
- 📝 `write_file`, `edit_file`, `read_file`, `list_files`
- 💻 `run_command`, `list_jobs`, `stop_job` (foreground and background processes)
- 🙋 **Human-in-the-loop**: shows the exact file content or command and waits for `y/N`
- 🛡 **Safety middleware**: blocks dangerous commands (`sudo`, `rm -rf`, `curl | sh`, ...) and keeps an audit log
- 🧠 Conversation memory within a session
- 📄 Editable behavior through Jinja prompts (`prompts/system.jinja`)
- 🔌 Works with any OpenAI-compatible endpoint: **Ollama (default)**, Groq, OpenRouter, Hugging Face router, OpenAI

## Quick start (Colab)
1. Open `Colab_Coding_Agent_MVP1.ipynb` in Google Colab (badge above).
2. **Runtime → Change runtime type → T4 GPU**.
3. Make sure `CodingAgentMVP1_HF/` is in your Google Drive (`MyDrive/CodingAgentMVP1_HF`), or upload the zip when the notebook asks.
4. Run the cells in order. The first run downloads the model (a few minutes).
5. Chat, approve actions with `y`, type `exit` to stop.

Example session (real output from a T4):

```
You: write binary search file .txt
LLM: Sure, I will create a file named binary_search.txt ... Would you like me to proceed?
You: yes
--- human-in-the-loop ---
1. write_file (Write or overwrite a file on disk)
    path: binary_search.txt
    content: def binary_search(arr, target): ...
Allow write_file? (y/N): y
LLM: The file binary_search.txt has been created successfully in the working directory.
```

## Choosing a backend
Set `MODE` in step 2 of the notebook:

| MODE | Cost | Needs | Notes |
|---|---|---|---|
| `ollama` (default) | Free | T4 GPU | Runs `qwen2.5:7b` on Colab. Re-downloaded every session |
| `groq` | Free tier | `GROQ_API_KEY` in Colab Secrets | Larger model, fast |
| `openrouter` | Free models | `OPENROUTER_API_KEY` in Colab Secrets | `...:free` models |
| Hugging Face router | Limited free credits | `HF_TOKEN` | Credits run out quickly (HTTP 402) |

Environment variables used by `src/models.py`: `CUSTOM_BASE_URL`, `CUSTOM_API_KEY`, `CUSTOM_MODEL`, `CUSTOM_NAME` (any OpenAI-compatible endpoint), `HF_TOKEN` / `HF_MODEL`, `OPENAI_API_KEY`. Others: `WORK_DIR`, `HITL_ENABLED`, `MAX_MODEL_CALLS_PER_RUN`.

## Project layout
```
CodingAgentMVP1_HF/
├── Colab_Coding_Agent_MVP1.ipynb   # run this on Colab
├── requirements.txt
├── .env.example
├── prompts/                        # system.jinja, greeting.jinja
├── src/
│   ├── main.py                     # chat loop + approval prompts
│   ├── agent.py                    # LangChain agent + middleware stack
│   ├── models.py                   # provider selection (Ollama/HF/Groq/OpenAI...)
│   ├── tools/                      # write/edit/read/list files, shell, background jobs
│   └── middlewares/                # audit, protection, human-in-the-loop
└── workspace/                      # files the agent creates
```

## Run locally (optional)
```bash
pip install -r requirements.txt
# with Ollama installed:  ollama pull qwen2.5:7b
export CUSTOM_BASE_URL=http://localhost:11434/v1 CUSTOM_API_KEY=ollama CUSTOM_MODEL=qwen2.5:7b
cd src && python main.py
```

## Limitations
- Small open models are weaker than Claude/GPT at tool calling. Keep requests simple and expect to say "yes" when the model asks for confirmation.
- Colab resets the runtime when idle, so Ollama and the model are reinstalled each session. Project files persist on Google Drive.
- Commands run on the Colab VM (not a hardened sandbox). Keep approvals on (`HITL_ENABLED=true`) and read what the agent proposes before pressing `y`.

## Credits
Original project by Sanket Singh ([AiEngineeringConcepts](https://github.com/singhsanket143/AiEngineeringConcepts)). Colab/free-model adaptation: this repo. Check the original repository's license before redistributing.
# colab-claude-code-lite
