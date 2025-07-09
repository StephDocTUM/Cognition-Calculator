import streamlit as st
import numpy as np

# Seitenkonfiguration
st.set_page_config(page_title="MoCA-Rechner", layout="centered")
st.title("🧠 MoCA-Prognoserechner nach DBS Operation bei Patienten mit Parkinson Erkrankung")

st.markdown("""
Gib klinische Parameter ein und erhalte eine Wahrscheinlichkeit für kognitive Verbesserung oder Verschlechterung basierend auf SHAP-basierten Schwellenwerten.
""")

# Eingabeparameter
st.header("📥 Eingabe")

updrs = st.number_input("UPDRS (Baseline)", min_value=0.0, max_value=100.0, value=20.0)
moca = st.number_input("MoCA (Baseline)", min_value=0.0, max_value=30.0, value=28.0)
sn_score = st.number_input("SN_score (direkt eingeben)", min_value=0.0, max_value=2.0, value=0.99)

# SHAP-Schwellenwerte
thresholds = {
    "UPDRS": {"low": 44.88288288288288, "high": 57.4954954954955},
    "MoCA": {"low": 24.13113113113113, "high": 27.176176176176178},
    "SN_score": {"low": 0.857152416056056, "high": 0.94969650802802}
}

# Interpretationen pro Wert mit je nach Richtung angepasster Logik
def interpret_updrs(value, low, high):
    if value < low:
        return ("🟦 Niedrig (wahrscheinlich kognitive Verbesserung)", 0.1)
    elif value > high:
        return ("🟥 Hoch (wahrscheinlich kognitive Verschlechterung)", 0.9)
    else:
        return ("🟨 Zwischenbereich (unsichere Prognose)", 0.5)

def interpret_moca(value, low, high):
    if value < low:
        return ("🟥 Niedrig (wahrscheinlich kognitive Verschlechterung)", 0.9)
    elif value > high:
        return ("🟦 Hoch (wahrscheinlich kognitive Verbesserung)", 0.1)
    else:
        return ("🟨 Zwischenbereich (unsichere Prognose)", 0.5)

def interpret_sn(value, low, high):
    if value < low:
        return ("🟥 Niedrig (wahrscheinlich kognitive Verschlechterung)", 0.9)
    elif value > high:
        return ("🟦 Hoch (wahrscheinlich kognitive Verbesserung)", 0.1)
    else:
        return ("🟨 Zwischenbereich (unsichere Prognose)", 0.5)

# Prognoseausgabe
st.header("📊 Prognose")

updrs_text, updrs_prob = interpret_updrs(updrs, **thresholds["UPDRS"])
moca_text, moca_prob = interpret_moca(moca, **thresholds["MoCA"])
sn_text, sn_prob = interpret_sn(sn_score, **thresholds["SN_score"])

st.markdown(f"**UPDRS:** {updrs_text}  ")
st.markdown(f"**MoCA:** {moca_text}  ")
st.markdown(f"**SN_score:** {sn_text}  ")

# 🧠 Gesamteinschätzung basierend auf Einzelbewertungen
probs = [updrs_prob, moca_prob, sn_prob]

if all(p == 0.1 for p in probs):
    st.success("Gesamteinschätzung: ✅ Mit hoher Wahrscheinlichkeit kognitive **Verbesserung** (alle Marker positiv)")
elif all(p == 0.9 for p in probs):
    st.error("Gesamteinschätzung: 🧠 Mit hoher Wahrscheinlichkeit kognitive **Verschlechterung** (alle Marker negativ)")
else:
    avg_prob = np.mean(probs)
    st.warning(f"Gesamteinschätzung: ⚖️ Uneinheitliche Marker – Prognose unsicher ({avg_prob*100:.1f}% für Verschlechterung)")
