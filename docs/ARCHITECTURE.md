# System Architecture - Complete Overview

## Workflow Diagram

```
┌─────────────────────────────────────────────────────────────────────┐
│                    CRISIS-AI EVALUATION SYSTEM                       │
└─────────────────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────────────────┐
│  PHASE 1: MODEL TESTING                                              │
├──────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  ┌─────────────────────┐                                            │
│  │ LM Studio (Server)  │                                            │
│  │  • Load model       │                                            │
│  │  • Start API        │                                            │
│  └──────────┬──────────┘                                            │
│             │ HTTP API (localhost:1234)                             │
│             ▼                                                        │
│  ┌─────────────────────────────────┐                                │
│  │  batch_test_models.py           │  ◄─── User selects models     │
│  │  • Lists models via CLI         │                                │
│  │  • Interactive checkbox UI      │                                │
│  │  • Auto load/unload models      │                                │
│  │  • Creates batch folder         │                                │
│  │    (YYYY-MM-DD_N)               │                                │
│  └──────────┬──────────────────────┘                                │
│             │ Calls for each model                                  │
│             ▼                                                        │
│  ┌─────────────────────────────────┐                                │
│  │ llm-crisis-questions-test.py    │                                │
│  │  • Sends questions to model     │                                │
│  │  • Records answers + timing     │                                │
│  │  • Saves to batch folder        │                                │
│  └──────────┬──────────────────────┘                                │
│             │                                                        │
│             ▼                                                        │
│  ┌─────────────────────────────────────────────┐                    │
│  │  test_results/YYYY-MM-DD_N/                 │                    │
│  │  ├── model1_timestamp.json                  │                    │
│  │  ├── model1_timestamp_runinfo.json          │                    │
│  │  ├── model2_timestamp.json                  │                    │
│  │  └── model2_timestamp_runinfo.json          │                    │
│  └─────────────────────────────────────────────┘                    │
│                                                                      │
└──────────────────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────────────────┐
│  PHASE 2: EVALUATION                                                 │
├──────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  ┌─────────────────────────────┐                                    │
│  │  eval_batch.py              │  ◄─── User runs evaluation        │
│  │  • Lists available batches  │                                    │
│  │  • Auto-detect latest       │                                    │
│  │  • Sets BATCH_FOLDER env    │                                    │
│  └──────────┬──────────────────┘                                    │
│             │ Calls with env var                                    │
│             ▼                                                        │
│  ┌─────────────────────────────────┐                                │
│  │  test-evaluation.py             │                                │
│  │  • Reads batch folder           │                                │
│  │  • Filters _runinfo.json files  │                                │
│  │  • Sends to Gemini API          │                                │
│  │  • Gets scores + justifications │                                │
│  └──────────┬──────────────────────┘                                │
│             │ GEMINI_API_KEY                                        │
│             ▼                                                        │
│  ┌────────────────────────────────────────────┐                     │
│  │  Google Gemini API (Cloud)                 │                     │
│  │  • Evaluates each answer                   │                     │
│  │  • Provides ideal answer                   │                     │
│  │  • Scores 0-10 with justification          │                     │
│  └──────────┬─────────────────────────────────┘                     │
│             │                                                        │
│             ▼                                                        │
│  ┌─────────────────────────────────────────────┐                    │
│  │  gemini_evaluation_report_YYYY-MM-DD.json   │                    │
│  │  {                                          │                    │
│  │    "Category": {                            │                    │
│  │      "Subcategory": [                       │                    │
│  │        {                                    │                    │
│  │          "question": "...",                 │                    │
│  │          "gemini_evaluation": {             │                    │
│  │            "gemini_ideal_answer": "...",    │                    │
│  │            "evaluations": [                 │                    │
│  │              {                              │                    │
│  │                "model_name": "...",         │                    │
│  │                "llm_answer": "...",         │                    │
│  │                "score": 8,                  │                    │
│  │                "justification": "..."       │                    │
│  │              }                              │                    │
│  │            ]                                │                    │
│  │          }                                  │                    │
│  │        }                                    │                    │
│  │      ]                                      │                    │
│  │    }                                        │                    │
│  │  }                                          │                    │
│  └─────────────────────────────────────────────┘                    │
│                                                                      │
└──────────────────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────────────────┐
│  PHASE 3: VISUALIZATION                                              │
├──────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  ┌─────────────────────────────────────────────────┐                │
│  │  OPTION A: Interactive Viewer (NEW! ⭐)         │                │
│  │                                                 │                │
│  │  ┌─────────────────────────────┐                │                │
│  │  │  evaluation-viewer.html     │ ◄─ Just open! │                │
│  │  │  • Pure HTML/CSS/JS         │                │                │
│  │  │  • Drag & drop JSON         │                │                │
│  │  │  • No dependencies          │                │                │
│  │  │  • Works offline            │                │                │
│  │  └──────────┬──────────────────┘                │                │
│  │             │                                    │                │
│  │             │ User drags JSON file               │                │
│  │             ▼                                    │                │
│  │  ┌─────────────────────────────────────┐        │                │
│  │  │  Browser (Local Processing)         │        │                │
│  │  │  • Parse JSON                       │        │                │
│  │  │  • Calculate rankings               │        │                │
│  │  │  • Generate UI dynamically          │        │                │
│  │  │  • Interactive score details        │        │                │
│  │  └──────────┬──────────────────────────┘        │                │
│  │             │                                    │                │
│  │             ▼                                    │                │
│  │  ┌─────────────────────────────────────┐        │                │
│  │  │  Beautiful Interactive Report       │        │                │
│  │  │  📊 Performance Summary Cards       │        │                │
│  │  │  📋 Detailed Q&A Tables             │        │                │
│  │  │  🔍 Click scores for details        │        │                │
│  │  │  ✨ Responsive & Mobile-Friendly    │        │                │
│  │  └─────────────────────────────────────┘        │                │
│  └─────────────────────────────────────────────────┘                │
│                                                                      │
│  ┌─────────────────────────────────────────────────┐                │
│  │  OPTION B: Static Generator (Legacy)            │                │
│  │                                                 │                │
│  │  ┌─────────────────────────────┐                │                │
│  │  │  html-report-generator.py   │                │                │
│  │  │  • Reads latest JSON        │                │                │
│  │  │  • Embeds data in HTML      │                │                │
│  │  │  • Creates static file      │                │                │
│  │  └──────────┬──────────────────┘                │                │
│  │             │                                    │                │
│  │             ▼                                    │                │
│  │  ┌─────────────────────────────┐                │                │
│  │  │  evaluation_report.html     │                │                │
│  │  │  • Self-contained           │                │                │
│  │  │  • Fixed data               │                │                │
│  │  │  • Good for archiving       │                │                │
│  │  └─────────────────────────────┘                │                │
│  └─────────────────────────────────────────────────┘                │
│                                                                      │
└──────────────────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────────────────┐
│  KEY FEATURES                                                        │
├──────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  🤖 Automated Model Testing                                         │
│     • CLI-based model switching (lms load/unload)                   │
│     • Interactive checkbox selection                                │
│     • Automatic batch folder creation                               │
│     • Accurate timing (excludes I/O overhead)                       │
│                                                                      │
│  📁 Batch Organization                                              │
│     • Timestamped folders (YYYY-MM-DD_N)                            │
│     • Auto-increment same-day runs                                  │
│     • Clean separation of results                                   │
│     • Metadata tracking (_runinfo.json)                             │
│                                                                      │
│  📊 Smart Evaluation                                                │
│     • Batch-aware evaluation                                        │
│     • Environment variable control                                  │
│     • Automatic file filtering                                      │
│     • Latest-batch detection                                        │
│                                                                      │
│  ✨ Interactive Viewer (NEW!)                                       │
│     • Zero dependencies                                             │
│     • Drag & drop interface                                         │
│     • Instant processing                                            │
│     • Complete privacy (local only)                                 │
│     • Beautiful responsive UI                                       │
│                                                                      │
│  🔧 Developer Friendly                                              │
│     • Comprehensive documentation                                   │
│     • Error handling & Unicode support                              │
│     • Type hints & code quality                                     │
│     • Extensible architecture                                       │
│                                                                      │
└──────────────────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────────────────┐
│  COMPLETE WORKFLOW EXAMPLE                                           │
├──────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  Day 1 - Morning Batch:                                             │
│  $ python batch_test_models.py                                      │
│    → Select: smollm2-360m, gemma-2-2b                               │
│    → Creates: test_results/2025-10-09_1/                            │
│                                                                      │
│  $ python eval_batch.py                                             │
│    → Evaluates: 2025-10-09_1                                        │
│    → Creates: gemini_evaluation_report_2025-10-09_10-30-00.json    │
│                                                                      │
│  $ start evaluation-viewer.html                                     │
│    → Drag: gemini_evaluation_report_2025-10-09_10-30-00.json       │
│    → View results instantly!                                        │
│                                                                      │
│  Day 1 - Afternoon Batch:                                           │
│  $ python batch_test_models.py                                      │
│    → Select: phi-3.5-mini, qwen3-4b                                 │
│    → Creates: test_results/2025-10-09_2/                            │
│                                                                      │
│  $ python eval_batch.py                                             │
│    → Auto-detects latest: 2025-10-09_2                             │
│    → Creates: gemini_evaluation_report_2025-10-09_15-30-00.json    │
│                                                                      │
│  $ start evaluation-viewer.html                                     │
│    → Tab 1: Drag morning results                                    │
│    → Tab 2: Drag afternoon results                                  │
│    → Compare side-by-side!                                          │
│                                                                      │
│  Day 2 - Archive:                                                   │
│  $ python html-report-generator.py                                  │
│    → Creates: evaluation_report.html (static, for archiving)        │
│                                                                      │
└──────────────────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────────────────┐
│  FILE STRUCTURE                                                      │
├──────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  Crisis-AI-evaluation/                                              │
│  ├── 🚀 MAIN SCRIPTS                                                │
│  │   ├── batch_test_models.py          (Automated testing)          │
│  │   ├── llm-crisis-questions-test.py  (Core Q&A)                   │
│  │   ├── test-evaluation.py            (Gemini evaluation)          │
│  │   └── eval_batch.py                 (Batch helper)               │
│  │                                                                   │
│  ├── 🎨 VISUALIZATION                                               │
│  │   ├── evaluation-viewer.html        (Interactive viewer ⭐)      │
│  │   └── html-report-generator.py      (Static generator)           │
│  │                                                                   │
│  ├── 📚 DOCUMENTATION                                               │
│  │   ├── README.md                     (Project overview)           │
│  │   ├── QUICK_START.md                (5-min guide)                │
│  │   ├── EVALUATION_VIEWER_GUIDE.md    (Viewer docs)                │
│  │   ├── BATCH_ORGANIZATION.md         (Batch system)               │
│  │   ├── AUTOMATED_BATCH_TESTING.md    (Automation)                 │
│  │   └── SYSTEM_READY.md               (Feature summary)            │
│  │                                                                   │
│  ├── 📊 DATA                                                        │
│  │   ├── Crisis-Questions.json                                      │
│  │   ├── gemini_evaluation_report_*.json                            │
│  │   └── test_results/                                              │
│  │       ├── 2025-10-09_1/                                          │
│  │       │   ├── model1_*.json                                      │
│  │       │   └── model1_*_runinfo.json                              │
│  │       └── 2025-10-09_2/                                          │
│  │           └── ...                                                │
│  │                                                                   │
│  └── 🔧 UTILITIES                                                   │
│      ├── check_test_status.py                                       │
│      ├── list_gemini_models.py                                      │
│      └── requirements.txt                                           │
│                                                                      │
└──────────────────────────────────────────────────────────────────────┘
```

## Technology Stack

### Backend (Python)
- **Subprocess** - LM Studio CLI control
- **Requests** - HTTP API communication
- **Questionary** - Interactive UI
- **Google Gemini API** - Evaluation

### Frontend (HTML Viewer)
- **HTML5** - Structure
- **Tailwind CSS** - Styling (CDN)
- **JavaScript ES6+** - Logic
- **FileReader API** - Local file access

### Infrastructure
- **LM Studio** - Model serving
- **Batch folders** - Result organization
- **Environment variables** - Configuration

## Data Flow

```
Questions (JSON)
    ↓
LLM Models (via LM Studio API)
    ↓
Answers + Timing (JSON files in batch folders)
    ↓
Gemini Evaluation (via Google API)
    ↓
Scores + Justifications (Evaluation JSON)
    ↓
Interactive Viewer (HTML drag & drop)
    ↓
Visual Analysis (Browser)
```

## Key Innovations

1. **CLI Automation** - Discovered `lms` commands for model control
2. **Batch Folders** - Organized timestamped result storage
3. **Timing Accuracy** - Excludes file I/O from measurements
4. **Unicode Handling** - Windows-compatible subprocess calls
5. **Interactive Viewer** - Zero-dependency browser-based UI

## Status: PRODUCTION READY ✅

All components tested and documented. Ready for immediate use!
