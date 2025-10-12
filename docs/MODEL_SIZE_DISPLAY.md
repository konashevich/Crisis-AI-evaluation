# Evaluation Viewer - Model Size Display

## Summary Card Improvements

Updated the evaluation viewer to display model sizes more prominently in the summary cards.

### Display Format

Each model card now shows:

```
┌─────────────────────────────────┐
│ Model Name               #Rank  │
│                                 │
│        8.5                      │
│    Average Score                │
│    32 questions                 │
│                                 │
│  4.47 GB          Q4_K_S        │
│  ⏱️ 19:07                        │
└─────────────────────────────────┘
```

### Features

✅ **Model Size** - Displayed in blue, bold, prominent
✅ **Quantization** - Shown next to size (e.g., Q4_K_M, Q6_K, Q8_0)
✅ **Runtime** - Test duration in MM:SS format with clock emoji
✅ **Ranking** - Position badge in top-right corner
✅ **Score Color** - Green (≥8), Yellow (5-7), Red (<5)

### Example Display

Based on your data:

| Model | Score | Size | Quant | Runtime |
|-------|-------|------|-------|---------|
| smollm2-360m-instruct | 8.5 | **0.36 GB** | Q8_0 | ⏱️ 01:45 |
| phi-4-reasoning-plus | 9.2 | **7.8 GB** | Q6_K | ⏱️ 179:53 |
| deepseek-r1-0528-qwen3-8b | 8.7 | **4.47 GB** | Q4_K_S | ⏱️ 19:07 |

### Size Formatting

- **0-1 GB**: Shows 2 decimals (e.g., 0.36 GB)
- **1-10 GB**: Shows 2 decimals (e.g., 4.47 GB)
- **10+ GB**: Shows 2 decimals (e.g., 12.35 GB)

### Data Source

Model metadata is automatically collected from the `_runinfo.json` files:

```json
{
  "model_size_gb": 0.3598676919937134,
  "model_size_bytes": 386404992,
  "model_quantization": "Q8_0",
  "duration_seconds": 105
}
```

The evaluation script (`test-evaluation.py`) includes this metadata when generating reports.

### Browser View

To see the updated display:

```powershell
python serve_viewer.py
```

Then navigate to `http://localhost:8000/evaluation-viewer.html`

The model size will now be displayed prominently in blue below the score, making it easy to compare model sizes at a glance.
