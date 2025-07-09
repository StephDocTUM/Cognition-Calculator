import streamlit as st
import numpy as np

# Seitenkonfiguration
st.set_page_config(page_title="MoCA-Rechner", layout="centered")
st.title("🧠 MoCA-Prognoserechner")

st.markdown("""
Gib klinische Parameter ein und erhalte eine Wahrscheinlichkeit für kognitive Verbesserung oder Verschlechterung basierend auf SHAP-basierten Schwellenwerten.
""")

# Eingabeparameter
st.header("📥 Eingabe")

updrs = st.number_input("UPDRS (Baseline)", min_value=0.0, max_value=100.0, value=50.0)
moca = st.number_input("MoCA (Baseline)", min_value=0.0, max_value=30.0, value=25.0)
sn_score = st.number_input("SN_score (direkt eingeben)", min_value=0.0, max_value=2.0, value=0.9)

# SHAP-Schwellenwerte
thresholds = {
    "UPDRS": {"low": 44.88288288288288, "high": 57.4954954954955},
    "MoCA": {"low": 24.13113113113113, "high": 27.176176176176178},
    "SN_score": {"low": 0.857152416056056, "high": 0.94969650802802}
}

# Interpretationsfunktionen
def interpret_score(value, low, high):
    if value < low:
        return ("🟦 Niedrig (wahrscheinlich kognitive Verbesserung)", 0.05)
    elif value > high:
        return ("🟥 Hoch (wahrscheinlich kognitive Verschlechterung)", 0.95)
    else:
        return ("🟨 Zwischenbereich (unsichere Prognose)", 0.5)

def interpret_updrs(value, low, high):
    if value < low:
        return ("🟦 Niedrig (wahrscheinlich kognitive Verbesserung)", 0.05)
    elif value > high:
        return ("🟥 Hoch (wahrscheinlich kognitive Verschlechterung)", 0.95)
    else:
        return ("🟨 Zwischenbereich (unsichere Prognose)", 0.5)

# Prognoseausgabe
st.header("📊 Prognose")

updrs_text, updrs_prob = interpret_updrs(updrs, **thresholds["UPDRS"])
moca_text, moca_prob = interpret_score(moca, **thresholds["MoCA"])
sn_text, sn_prob = interpret_score(sn_score, **thresholds["SN_score"])

st.markdown(f"**UPDRS:** {updrs_text}  ")
st.markdown(f"**MoCA:** {moca_text}  ")
st.markdown(f"**SN_score:** {sn_text}  ")

# Durchschnittliche Wahrscheinlichkeit für Verschlechterung
avg_prob = np.mean([updrs_prob, moca_prob, sn_prob])

if avg_prob >= 0.9:
    st.error(f"Gesamteinschätzung: 🧠 Mit hoher Wahrscheinlichkeit kognitive **Verschlechterung** ({avg_prob*100:.1f}%)")
elif avg_prob <= 0.1:
    st.success(f"Gesamteinschätzung: ✅ Mit hoher Wahrscheinlichkeit kognitive **Verbesserung** ({(1-avg_prob)*100:.1f}%)")
else:
    st.warning(f"Gesamteinschätzung: ⚖️ Unsichere Prognose ({avg_prob*100:.1f}% für Verschlechterung)")
