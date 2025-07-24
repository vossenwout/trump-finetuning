### Run GGUF on Ollama

1. Download model from huggingface
   https://huggingface.co/pookie3000/Meta-Llama-3.1-8B-trump-Q4_K_M-GGUF

!!! LFS is required to download the model.

```
git clone https://huggingface.co/pookie3000/Meta-Llama-3.1-8B-trump-Q4_K_M-GGUF
```

2. Rename GGUF to llama-31-trump.gguf and move the gguf file to the llama-3.1 root folder.

3. Create model (run this from the llama-3.1 root folder)

```
ollama create llama-31-trump -f Modelfile
```

4. Run model

```
ollama run llama-31-trump
```
