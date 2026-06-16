import streamlit as st
import asyncio
from agents.graph import app_graph
from init_db import initialize_vector_store
from workers.tasks import MOCK_PROSPECTS, gather_linkedin_signal, gather_intent_signal

st.set_page_config(page_title="Sales AI Agent", layout="wide")

if "db_ready" not in st.session_state:
    with st.spinner("Initializing System..."):
        asyncio.run(initialize_vector_store())
        st.session_state.db_ready = True

st.title("🚀 Sales Prospecting AI")

prospect_ids = list(MOCK_PROSPECTS.keys())

with st.sidebar:
    st.header("Settings")
    mode = st.radio("Execution Mode", ["Run All", "Run Selected"])
    if mode == "Run Selected":
        range_val = st.slider("Select IDs", 1, len(prospect_ids), (1, 3))

if st.button("Execute Research Pipeline", type="primary"):
    active_ids = prospect_ids if mode == "Run All" else [str(i) for i in range(range_val[0], range_val[1] + 1)]

    results = []
    progress_bar = st.progress(0)

    for i, p_id in enumerate(active_ids):
        l_signal = gather_linkedin_signal(p_id)
        i_signal = gather_intent_signal(p_id)

        initial_input = {
            "prospect_id": p_id,
            "event_trigger": "streamlit_manual",
            "gathered_signals": {
                "linkedin": l_signal.get("linkedin"),
                "intent": i_signal.get("intent")
            },
            "retrieved_context": [],
            "score": 0,
            "rationale": "",
            "next_action": "",
            "needs_human_review": False
        }

        final_state = asyncio.run(app_graph.ainvoke(initial_input))
        results.append(final_state)
        progress_bar.progress((i + 1) / len(active_ids))

    st.divider()
    st.subheader("Results Summary")

    summary = []
    for res in results:
        summary.append({
            "ID": res["prospect_id"],
            "Score": res["score"],
            "Recommended Action": res.get("next_action", "Review"),
            "Rationale": res["rationale"]
        })

    st.table(summary)

    with st.expander("View Raw Data"):
        st.json(results)

st.divider()
st.caption("OmniMD Assesement")
