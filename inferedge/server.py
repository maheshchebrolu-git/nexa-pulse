from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import StreamingResponse
from mlx_lm import load, stream_generate
from mlx_lm.sample_utils import make_sampler
from pydantic import BaseModel
from contextlib import asynccontextmanager
import asyncio
import uvicorn
import json

class ChatRequest(BaseModel):
    messages: list[dict[str, str]]
    max_tokens: int = 1000
    temperature: float = 0.7
    top_p: float = 0.9

class HealthResponse(BaseModel):
    status: str = "loading"
    is_model_loaded: bool = False
    model_name: str = "mlx-community/Meta-Llama-3.1-8B-Instruct-4bit"

MODEL_PATH = "mlx-community/Meta-Llama-3.1-8B-Instruct-4bit"

@asynccontextmanager
async def lifespan(app):
    print("Loading model...")
    model, tokenizer = load(MODEL_PATH)
    app.state.model = model
    app.state.tokenizer = tokenizer
    print("Stream bound to worker thread")
    yield
    print("Shutting down model...")
    app.state.model = None
    app.state.tokenizer = None

app = FastAPI(lifespan=lifespan)

async def generate_token_stream(model, tokenizer, formatted_prompt, max_tokens, temperature, top_p):
    sampler = make_sampler(temperature, top_p)
    try:
        for response in stream_generate(model, tokenizer, formatted_prompt, max_tokens, sampler=sampler):
            chunk = {"choices": [{"delta": {"content": response.text}}]}
            yield f"data: {json.dumps(chunk)}\n\n"
            await asyncio.sleep(0)
    except Exception as e:
        print(f"Generation error: {e!r}")
        yield f"data: {json.dumps({'error': str(e)})}\n\n"
    yield "data: [DONE]\n\n"

@app.post("/v1/chat/completions")
async def chat(request: ChatRequest, req: Request):
    model = req.app.state.model
    tokenizer = req.app.state.tokenizer
    formatted_prompt = tokenizer.apply_chat_template(
        request.messages, 
        tokenize=False,
        add_generation_prompt=True
        )
    curTokens = tokenizer.encode(formatted_prompt)
    contextLimit = 131072
    remainingContext = contextLimit - (len(curTokens) + 100)
    print(f"Current tokens length: {len(curTokens)}")
    print(f"Remaining context: {remainingContext}")
    if remainingContext <= 0:
        raise HTTPException(status_code=413, detail="Context limit exceeded")
    safeMaxTokens = min(request.max_tokens, remainingContext)
    return StreamingResponse(
        generate_token_stream(model, tokenizer, formatted_prompt, safeMaxTokens, request.temperature, request.top_p),
        media_type="text/event-stream"
    )
    
@app.get("/health")
async def health() -> HealthResponse:
    status = "healthy" if app.state.model is not None else "loading"
    is_model_loaded = app.state.model is not None
    return HealthResponse(status=status, is_model_loaded=is_model_loaded)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)











