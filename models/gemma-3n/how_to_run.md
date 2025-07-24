### Run GGUF on Ollama

1. Download model from huggingface
   https://huggingface.co/pookie3000/gemma-3n-E2B-donald-trump-Q8_0-GGUF

!!! LFS is required to download the model.

```
git clone https://huggingface.co/pookie3000/gemma-3n-E2B-donald-trump-Q8_0-GGUF
```

2. Rename GGUF to gemma-3n-e2b-donald-trump.gguf and put it in th gemini-3n root folder.

3. Create model

```
ollama create gemma-trump -f Modelfile
```

4. Run model

```
ollama run gemma-trump
```
