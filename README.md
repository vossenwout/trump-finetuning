# Trump Lora Finetuning

![alt text](assets/trump.png)

This repository contains a complete pipeline for fine-tuning Large Language Models (LLMs) to mimic Donald Trump's speaking style. The project includes data collection, synthetic data generation, model training, and model inference code. The training is done using Unsloth.

## Trained models

1. **Llama-3.1:8b Trump Model**: [HuggingFace Link](https://huggingface.co/pookie3000/Meta-Llama-3.1-8B-trump-Q4_K_M-GGUF)
2. **Gemma-3n:e2b Trump Model**: [HuggingFace Link](https://huggingface.co/pookie3000/gemma-3n-E2B-donald-trump-Q8_0-GGUF)

## Dataset

The training dataset which was created using transcripts and synthetic data.

[HuggingFace Link](https://huggingface.co/datasets/pookie3000/donald_trump_interviews)

## 📁 Project Structure

```
trump-finetune/
├── data/
│   ├── transcripts/          # Interview transcripts
│   └── trainset/             # Actual LLM training data
├── scripts/                  # Training Data download and processing
├── training/                 # Unsloth notebooks for model training
│   ├── donald_trump_finetune_llama3_1.ipynb
│   └── donald_trump_finetune_gemma_3n.ipynb
├── models/                  # Modelfiles to load models into Ollama
│   ├── llama-3.1/
│   └── gemma-3n/
└── config/
```

## 🛠️ Setup and Installation

### Prerequisites

- Python 3.10+
- [uv](https://docs.astral.sh/uv/) package manager
- [Ollama](https://ollama.com/) (for running fine-tuned models)
- Git LFS (for downloading pre-trained models)

### Installation

1. **Clone the repository:**

   ```bash
   git clone <repository-url>
   cd trump-finetune
   ```

2. **Install dependencies:**

   ```bash
   uv sync
   ```

3. **Set up environment variables:**

   ```bash
   mkdir config
   touch config/.env
   ```

   Add your API keys to `config/.env`:

   ```env
   ASSEMBLYAI_API_KEY=YOUR_ASSEMBLYAI_API_KEY
   GEMINI_API_KEY=YOUR_GEMINI_API_KEY
   ```

Get assemblyai api key from [here](https://www.assemblyai.com/dashboard/api-keys)

Get gemini api key from [here](https://aistudio.google.com/prompts/new_chat)
