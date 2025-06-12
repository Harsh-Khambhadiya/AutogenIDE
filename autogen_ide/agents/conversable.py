from __future__ import annotations

from typing import Optional

from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline


class ConversableAgent:
    """Basic chat agent using a local HuggingFace model."""

    def __init__(self, model_path: str | None = None) -> None:
        self.model_path = model_path or "deepseek/deepseek-r1-0528-qwen3-8b"
        try:
            self.tokenizer = AutoTokenizer.from_pretrained(self.model_path)
            self.model = AutoModelForCausalLM.from_pretrained(self.model_path)
            self.pipe = pipeline(
                "text-generation",
                model=self.model,
                tokenizer=self.tokenizer,
                device=0 if self.model.device.type == "cuda" else -1,
            )
        except Exception:
            # Model not available; fall back to echo behaviour
            self.pipe = None

    def respond(self, prompt: str) -> str:
        if self.pipe:
            out = self.pipe(prompt, max_new_tokens=128)[0]["generated_text"]
            return out[len(prompt) :].strip()
        return f"You said: {prompt}"
