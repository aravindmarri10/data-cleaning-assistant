import streamlit as st
# ====== Undo Change ======
def undo_change(df):
    st.subheader("🔁 Undo Change")
    st.warning("⚠️ This will revert the last change. This action cannot be undone.")
    if st.button("↩️ Confirm Undo"):
        if st.session_state.snapshots:
            st.session_state.df = st.session_state.snapshots.pop()
            st.success("✅ Reverted to last saved state.")
        else:
            st.warning("⚠️ No previous state to undo.")

# ====== saved df before distructive change========
def save_snapshot(df):
    """Save a copy of the current DataFrame for undo functionality."""
    st.session_state.snapshots.append(df.copy())


# ====== Reset to Original ======
def reset_data(original):
    st.subheader("🔁 Reset to Original")
    st.warning("⚠️ This will reset to raw data Frame. This action cannot be undone.")
    if st.button("Reset"):
        save_snapshot(st.session_state.df)
        st.session_state.df = original.copy()
        st.success("✅ Data reset to original uploaded file.")
