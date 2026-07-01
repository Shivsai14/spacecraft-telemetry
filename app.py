"""
app.py
Streamlit operator dashboard for spacecraft telemetry health assessment.
Run with: streamlit run app.py
Requires env var ANTHROPIC_API_KEY to be set for live LLM fusion
(falls back gracefully to a numeric-only verdict if unavailable).
"""

import streamlit as st
import pandas as pd
from telemetry_data import PASSES, HARD_LIMITS
from analyzer import analyze_pass as evaluate_pass

st.set_page_config(page_title="Spacecraft Health Console", layout="wide")

SEVERITY_COLORS = {
    "NOMINAL": "#1f9d55",
    "WATCH": "#d4a017",
    "WARNING": "#e8590c",
    "CRITICAL": "#c1121f",
}

if "decision_log" not in st.session_state:
    st.session_state.decision_log = {}

if "eval_cache" not in st.session_state:
    st.session_state.eval_cache = {}


def get_evaluation(pass_record):
    pid = pass_record["pass_id"]
    if pid not in st.session_state.eval_cache:
        st.session_state.eval_cache[pid] = evaluate_pass(pass_record)
    return st.session_state.eval_cache[pid]


# ----------------------------------------------------------------------
# SIDEBAR — MISSION CONTROL CENTER
# ----------------------------------------------------------------------
with st.sidebar:
    st.markdown("### Mission Control Center (MCC)")
    st.markdown(
        """
        **Satellite:** NEXUS-1  
        **Ground Station:** GS-Goonhilly  
        **Operator:** Shiv Sai
        """
    )
    st.divider()
    pass_lookup = {p["pass_id"]: p for p in PASSES}
    selected_id = st.selectbox(
        "Select pass",
        options=list(pass_lookup.keys()),
        format_func=lambda pid: f"{pid} — {pass_lookup[pid]['timestamp']}",
    )
selected_pass = pass_lookup[selected_id]

with st.spinner("Running hard-limit checks, numeric scoring, and AI fusion..."):
    result = get_evaluation(selected_pass)

# ----------------------------------------------------------------------
# HEADER
# ----------------------------------------------------------------------
with st.container():
    st.title("🛰️ Spacecraft Telemetry Health Console")
    st.markdown(
        "Real-time pass health assessment · hard-limit enforcement · AI-assisted fusion"
    )
    st.divider()

# ----------------------------------------------------------------------
# GIANT SEVERITY BADGE
# ----------------------------------------------------------------------
severity = result["final_severity"]
confidence = result["final_confidence"]
color = SEVERITY_COLORS.get(severity, "#888888")

# Convert confidence to display string safely whether it's a float or a string
conf_display = f"{confidence:.0%}" if isinstance(confidence, (int, float)) else str(confidence)
override_text = " · ⚠️ HARD LIMIT OVERRIDE APPLIED" if result["override_applied"] else ""

with st.container():
    st.markdown(
        f"""
        <div style="background-color:{color}; padding:24px; border-radius:10px;
                    text-align:center; margin-bottom:20px; color:white;">
            <h1 style="margin:0; font-size:42px; font-weight:800; letter-spacing:2px; color:white;">
                {severity}
            </h1>
            <p style="margin:5px 0 0 0; font-size:16px; color:white;">
                Confidence: {conf_display}{override_text}
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

# ----------------------------------------------------------------------
# HARD LIMIT STATUS PANEL
# ----------------------------------------------------------------------
with st.container():
    st.subheader("🔒 Hard Limit Status")
    breaches = result["hard_limit_breaches"]
    if not breaches:
        st.success("All parameters within hard operational limits.")
    else:
        for b in breaches:
            st.error(
                f"**{b['parameter']}** = {b['value']} {b['unit']}  "
                f"(allowed range: {b['min']}–{b['max']} {b['unit']}) — LIMIT BREACHED"
            )

    st.divider()

# ----------------------------------------------------------------------
# TWO-COLUMN LAYOUT: TELEMETRY DATA  |  NOTE + AI REASONING
# ----------------------------------------------------------------------
col1, col2 = st.columns(2)

with col1:
    with st.container():
        st.subheader("📊 Telemetry Data")
        rows = []
        for param, value in result["telemetry"].items():
            limits = HARD_LIMITS.get(param, {})
            z = result["anomaly_summary"]["zscores"].get(param, 0.0)
            rows.append(
                {
                    "Parameter": param,
                    "Value": value,
                    "Unit": limits.get("unit", ""),
                    "Hard Limit": f"{limits.get('min', '-')} to {limits.get('max', '-')}",
                    "Z-score": z,
                }
            )
        df = pd.DataFrame(rows)
        breach_params = {b["parameter"] for b in breaches}
        abnormal_bg = "background-color: rgba(255, 99, 99, 0.25)"

        def _row_flagged(row):
            z = row["Z-score"]
            param = row["Parameter"]
            return param in breach_params or z > 2 or z < -2

        row_flags = df.apply(_row_flagged, axis=1)
        styled_df = df.style
        for idx in df.index[row_flags]:
            styled_df = styled_df.map(
                lambda _val: abnormal_bg,
                subset=pd.IndexSlice[idx, :],
            )
        st.dataframe(styled_df, hide_index=True, use_container_width=True)

        trend = result["anomaly_summary"]["battery_trend"]
        metric_col1, metric_col2 = st.columns(2)
        with metric_col1:
            st.metric(
                label="Battery Voltage Trend",
                value=trend["direction"],
                delta=f"Δ {trend['delta']} V · slope {trend['slope']}",
            )
        with metric_col2:
            st.metric(
                label="Eclipse During Pass",
                value="Yes" if result["eclipse"] else "No",
            )

with col2:
    with st.container():
        st.subheader("📝 Operator Note")
        st.info(result["operator_note"])

        st.subheader("🤖 AI Reasoning")
        verdict = result["llm_verdict"]
        st.write(verdict.get("reasoning", "No reasoning returned."))

        if verdict.get("note_contradicts_numbers"):
            st.warning(
                f"⚠️ Note may contradict the numeric data: "
                f"{verdict.get('contradiction_explanation', '')}"
            )
        else:
            st.caption("Note appears consistent with numeric telemetry.")

        if result["override_applied"]:
            st.caption(
                "Note: severity above was forced to CRITICAL by the hard-limit "
                "safety override — this takes priority over the AI's own verdict."
            )

st.divider()

# ----------------------------------------------------------------------
# OPERATOR DECISION OVERRIDE
# ----------------------------------------------------------------------
with st.container():
    st.subheader("🧑‍🚀 Operator Decision")

    with st.form(key=f"decision_form_{selected_id}"):
        decision = st.radio(
            "Operator action",
            options=["Acknowledge", "Escalate", "Override Severity"],
            horizontal=True,
        )

        override_severity = None
        if decision == "Override Severity":
            override_severity = st.selectbox(
                "New severity", options=["NOMINAL", "WATCH", "WARNING", "CRITICAL"]
            )

        rationale = st.text_area("Operator rationale / log entry", height=90)
        submitted = st.form_submit_button("Submit Decision")

        if submitted:
            st.session_state.decision_log[selected_id] = {
                "decision": decision,
                "override_severity": override_severity,
                "rationale": rationale,
                "system_severity": severity,
            }
            st.success(f"Decision logged for {selected_id}.")

    if selected_id in st.session_state.decision_log:
        log = st.session_state.decision_log[selected_id]
        st.markdown("**Logged decision for this pass:**")
        st.json(log)

    st.divider()

# ----------------------------------------------------------------------
# FULL MISSION LOG (all passes, all logged decisions)
# ----------------------------------------------------------------------
with st.container():
    with st.expander("📋 View full decision log (all passes)"):
        if st.session_state.decision_log:
            st.dataframe(
                pd.DataFrame.from_dict(st.session_state.decision_log, orient="index"),
                use_container_width=True,
            )
        else:
            st.caption("No operator decisions logged yet.")
