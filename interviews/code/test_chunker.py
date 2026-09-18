import pytest
from chunker import split_text_into_chunks, estimate_token_count


def test_chunker_empty_input():
    chunks = split_text_into_chunks("")
    assert chunks == []


def test_chunker_small_text_single_chunk():
    text = "The enterprise SLA mandates a 15-minute response time for critical incidents."
    chunks = split_text_into_chunks(text, max_tokens=50, doc_id="DOC-001")
    assert len(chunks) == 1
    assert chunks[0].chunk_id == "DOC-001_chunk_000"
    assert chunks[0].chunk_index == 0
    assert chunks[0].total_chunks == 1
    assert chunks[0].metadata["doc_id"] == "DOC-001"
    assert "critical incidents" in chunks[0].content


def test_chunker_splits_and_overlaps():
    text = (
        "Sentence one introduces the compliance policy. "
        "Sentence two details data residency requirements in the EU region. "
        "Sentence three specifies encryption at rest using AES-256 keys. "
        "Sentence four outlines audit log retention for seven calendar years. "
        "Sentence five concludes the governance review."
    )

    chunks = split_text_into_chunks(
        text,
        max_tokens=25,
        overlap_tokens=12,
        doc_id="POLICY-EU",
        base_metadata={"author": "Security Team", "classification": "restricted"},
    )

    assert len(chunks) > 1
    for chunk in chunks:
        assert chunk.token_count <= 40  # Bound by sentence granularity
        assert chunk.metadata["classification"] == "restricted"
        assert chunk.metadata["author"] == "Security Team"

    # Verify sliding overlap: end of first chunk content should overlap start of second chunk
    first_chunk_end = chunks[0].content.split(".")[-2].strip()
    assert first_chunk_end in chunks[1].content
