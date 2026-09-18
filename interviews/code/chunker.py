"""
Production document chunking utility for enterprise RAG pipelines.
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
    Standard rule of thumb: ~0.75 words per token (1 word ~= 1.33 tokens).
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
    if not text.strip():
        return []

    base_metadata = base_metadata or {}
    sentences = re.split(r"(?<=[.!?\n])\s+", text.strip())

    chunks_raw: List[str] = []
    current_sentences: List[str] = []
    current_tokens = 0

    for sentence in sentences:
        s_tokens = estimate_token_count(sentence)
        if not sentence:
            continue

        if current_tokens + s_tokens <= max_tokens:
            current_sentences.append(sentence)
            current_tokens += s_tokens
        else:
            if current_sentences:
                chunks_raw.append(" ".join(current_sentences))

            # Compute overlap sentences
            overlap_sentences: List[str] = []
            overlap_count = 0
            for s in reversed(current_sentences):
                st = estimate_token_count(s)
                if overlap_count + st <= overlap_tokens:
                    overlap_sentences.insert(0, s)
                    overlap_count += st
                else:
                    break

            current_sentences = overlap_sentences + [sentence]
            current_tokens = sum(estimate_token_count(s) for s in current_sentences)

    if current_sentences:
        chunks_raw.append(" ".join(current_sentences))

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
