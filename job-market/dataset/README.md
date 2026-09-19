# Empirical FDE Job Market Dataset

A double-verified, machine-readable dataset documenting the rise, employer distribution, responsibilities breakdown, and compensation benchmarks for Forward Deployed Engineers (FDEs).

Following the empirical data collection methodology established in [alexeygrigorev/ai-engineering-field-guide](https://github.com/alexeygrigorev/ai-engineering-field-guide), this dataset avoids generic estimates and is compiled strictly from verified real-world job scrapes, corporate career boards, and labor market analytics.

---

## Dataset Provenance & Sources

| Authority | Measurement & Methodology | Primary Citation | Verified Date |
|---|---|---|---|
| **Alexey Grigorev** | 8 monthly scrapes of builtin.com (Feb–Aug 2026); 146 deduplicated FDE roles across 94 companies | [github.com/alexeygrigorev/ai-engineering-field-guide](https://github.com/alexeygrigorev/ai-engineering-field-guide/blob/main/role/06-fde.md) | 2026-09-19 |
| **Fortune / Lightcast** | Macro labor analysis of advertised postings across tech; median base salary comparison | [fortune.com](https://fortune.com/2026/09/03/forward-deployed-engineers-fast-growing-six-figure-silicon-valley-job-integrate-ai-with-customers-tech-careers-palantir) | 2026-09-19 |
| **Business Insider / Indeed** | Indexed monthly job posting growth (April 2025 to April 2026); employer compensation bands | [businessinsider.com](https://www.businessinsider.com/forward-deployed-engineer-jobs-in-demand-2026-5) | 2026-09-19 |
| **Dr. Sundeep Teki** | AI career coaching analysis; "Ambiguity by default" operating model across frontier AI labs | [sundeepteki.org/advice](https://www.sundeepteki.org/advice/the-definitive-guide-to-forward-deployed-engineer-interviews-in-2026) | 2026-09-19 |
| **Plank** | Aggregated live posting index across growth-stage enterprise AI startups | [joinplank.com](https://joinplank.com) | 2026-09-19 |

---

## Key Empirical Findings

### 1. Monthly Scrape Progression (2026)

| Scrape Date | Total AI Listings | Live FDE Listings | FDE Market Share |
|---|---:|---:|---:|
| **2026-02-04** | 1,416 | 28 | 2.0% |
| **2026-02-27** | 2,057 | 41 | 2.0% |
| **2026-03-27** | 2,341 | 58 | 2.5% |
| **2026-04-22** | 2,473 | 65 | 2.6% |
| **2026-05-29** | 2,751 | 80 | 2.9% |
| **2026-06-25** | 3,024 | 108 | 3.6% |
| **2026-07-22** | 3,320 | 118 | 3.6% |

- **Growth Multiple**: FDE listings grew **321%** (4.2x) over the 6-month scrape window, outpacing the wider AI job market (134% / 2.3x) by a factor of 1.8.

### 2. Responsibilities Distribution (146 Postings Analyzed)

- **90.4% (132 postings)**: Building & Deploying Production Systems
- **88.4% (129 postings)**: Direct Customer & Client Collaboration
- **64.4% (94 postings)**: Integrating Systems, APIs & Data
- **52.1% (76 postings)**: Discovery & Requirements Scoping
- **48.6% (71 postings)**: Evaluation, Testing & Monitoring
- **30.8% (45 postings)**: Feeding Field Lessons into Core Product
- **28.8% (42 postings)**: Rapid Prototypes, POCs & Demos
- **8.9% (13 postings)**: Travel & On-Site Co-location

### 3. Seniority Breakdown

- **No Level Marker (Experienced SWE / Consultant)**: 107 postings (73.3%)
- **Senior**: 19 postings (13.0%)
- **Principal**: 8 postings (5.5%)
- **Staff**: 6 postings (4.1%)
- **Lead**: 5 postings (3.4%)
- **Founding**: 1 posting (0.7%)
- **Junior / Entry-Level**: 0 postings (0.0%)

*Conclusion: FDE is empirically a second role, requiring production engineering chops and customer diplomacy acquired in prior positions.*

---

## Dataset Schema

The dataset is located in [fde_market_data.json](fde_market_data.json):

```json
{
  "dataset_metadata": { ... },
  "monthly_scrapes": [
    {
      "scrape_date": "YYYY-MM-DD",
      "total_ai_listings": 0,
      "fde_listings": 0,
      "fde_share_percentage": 0.0
    }
  ],
  "sample_summary": { ... },
  "top_employers": [ ... ],
  "responsibilities_breakdown": [ ... ],
  "seniority_distribution": [ ... ],
  "compensation_benchmarks": { ... },
  "provenance_sources": [ ... ]
}
```

---

## Automated Validation

To run the automated validation test suite:

```bash
python job-market/dataset/validate_market_data.py
```
