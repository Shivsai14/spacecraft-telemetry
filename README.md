# Spacecraft Telemetry Health Console

## Setup
```
pip install -r requirements.txt
export ANTHROPIC_API_KEY=your_key_here
streamlit run app.py
```

If ANTHROPIC_API_KEY is unset or the API call fails, analyzer.py falls back
to a numeric-only WARNING verdict (logged in the reasoning field) so the
app never crashes — this is a deliberate degradation path, not a bug.

## Files
- telemetry_data.py — hard limits, nominal baselines, 15 synthetic passes
- analyzer.py — hard limit check -> z-score/trend scoring -> LLM fusion -> safety override
- app.py — Streamlit operator dashboard
