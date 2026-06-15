# ---------------------------------------------------------------------------
# NOTE: This Dockerfile is NOT the active run path for InferEdge.
#
# InferEdge runs NATIVELY on macOS (outside Docker), because it uses Apple's
# MLX framework for inference. MLX requires direct access to the Apple Silicon
# Metal GPU, which cannot be virtualized inside a Linux Docker container — the
# container has no Metal device, so model inference fails with a GPU stream error.
#
# Active run path (native):
#   source venv/bin/activate
#   cd inferedge
#   python -m uvicorn server:app --host 0.0.0.0 --port 8000
#
# This Dockerfile is retained to document the intended production replacement:
# in a cloud deployment, InferEdge would be swapped for a Linux-based inference
# server (e.g. vLLM on a GPU instance, or a managed endpoint). Because InferEdge
# exposes an OpenAI-compatible API, that swap requires changing only the base URL
# in the client config — no agent code changes.
# ---------------------------------------------------------------------------

FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["uvicorn", "server:app", "--host", "0.0.0.0", "--port", "8000"]