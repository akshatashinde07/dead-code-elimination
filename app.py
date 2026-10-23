
import streamlit as st
from dce_optimizer import eliminate_dead_code

st.set_page_config(
    page_title="Dead Code Elimination Simulator",
    page_icon="⚙️",
    layout="wide"
)

st.title("Dead Code Elimination Simulator")
st.write(
    "A Python-based demonstration of compiler optimization "
    "using backward liveness analysis."
)

example_code = """t1 = 10
t2 = 20
t3 = t1 + t2
t4 = 100
t5 = 200
print(t3)"""

if "source_code" not in st.session_state:
    st.session_state.source_code = example_code

st.subheader("Enter Intermediate Code")

source_code = st.text_area(
    "Source code",
    key="source_code",
    height=220,
    help="Enter simplified assignments and print statements."
)

if st.button("Optimize Code", type="primary"):
    if not source_code.strip():
        st.warning("Please enter some code before optimizing.")
    else:
        result = eliminate_dead_code(source_code)

        st.session_state["dce_result"] = result

if "dce_result" in st.session_state:
    result = st.session_state["dce_result"]

    st.subheader("Optimization Results")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("**Original Code**")
        st.code("\n".join(result["original_code"]), language="python")

    with col2:
        st.markdown("**Optimized Code**")
        st.code("\n".join(result["optimized_code"]), language="python")

    st.subheader("Removed Instructions")

    if result["removed_instructions"]:
        for instruction in result["removed_instructions"]:
            st.write(f"- `{instruction}`")
    else:
        st.info("No dead assignments were found.")

    st.subheader("Optimization Statistics")

    col1, col2, col3 = st.columns(3)
    col1.metric("Original Instructions", result["original_count"])
    col2.metric("Optimized Instructions", result["optimized_count"])
    col3.metric("Removed Instructions", result["removed_count"])

    if result["original_count"] > 0:
        reduction = (
            result["removed_count"] / result["original_count"]
        ) * 100

        st.write(f"Instruction count reduction: **{reduction:.2f}%**")

    st.caption(
        "Educational prototype: supports simplified straight-line code. "
        "It is not a complete production compiler."
    )
