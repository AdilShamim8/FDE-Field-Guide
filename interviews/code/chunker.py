"""
Bounded document chunking exercise for RAG pipelines.
Provides token-aware boundary splitting, sliding overlap, and metadata inheritance.
"""

import re
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class TextChunk:
    chunk_id: str
    content: str
    token_count: int
    chunk_index: int
    total_chunks: int
    metadata: Dict[str, Any] = field(default_factory=dict)


def estimate_token_count(text: str) -> int:
    """
    Estimates token count using a deterministic regex token pattern.
    This is a local regex-token budget, not a model-specific tokenizer.
    """
    tokens = re.findall(r"\b\w+\b|[^\w\s]", text)
    return len(tokens)


def split_text_into_chunks(
    text: str,
    max_tokens: int = 100,
    overlap_tokens: int = 20,
    doc_id: str = "doc_default",
    base_metadata: Optional[Dict[str, Any]] = None,
) -> List[TextChunk]:
    """
    Splits text into chunks respecting sentence and paragraph boundaries where possible.
    Enforces maximum token budget and sliding overlap across chunks.
    Injects document metadata, chunk index, and total chunk count.
    """
    if max_tokens <= 0 or not 0 <= overlap_tokens < max_tokens:
        raise ValueError("Require max_tokens > 0 and 0 <= overlap_tokens < max_tokens")
    if not text.strip():
        return []

    base_metadata = base_metadata or {}
    tokens = list(re.finditer(r"\b\w+\b|[^\w\s]", text))
    chunks_raw: List[str] = []
    start = 0
    while start < len(tokens):
        end = min(start + max_tokens, len(tokens))
        if end < len(tokens):
            # Prefer a sentence end only when the next window still advances.
            boundaries = [i + 1 for i in range(start, end)
                          if tokens[i].group() in {".", "!", "?"}
                          and i + 1 - start > overlap_tokens]
            if boundaries:
                end = boundaries[-1]
        chunks_raw.append(text[tokens[start].start():tokens[end - 1].end()].strip())
        if end == len(tokens):
            break
        start = end - overlap_tokens

    # Construct final chunk objects with metadata
    total_chunks = len(chunks_raw)
    result: List[TextChunk] = []

    for idx, content in enumerate(chunks_raw):
        chunk_meta = dict(base_metadata)
        chunk_meta["doc_id"] = doc_id
        chunk_meta["chunk_index"] = idx

        result.append(
            TextChunk(
                chunk_id=f"{doc_id}_chunk_{idx:03d}",
                content=content,
                token_count=estimate_token_count(content),
                chunk_index=idx,
                total_chunks=total_chunks,
                metadata=chunk_meta,
            )
        )

    return result
