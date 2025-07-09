import streamlit as st
import numpy as np

st.set_page_config(page_title="MoCA-Rechner", layout="centered")
st.title("🧠 MoCA-Prognoserechner")
st.markdown("""
Gib klinische Parameter ein und erhalte eine Wahrscheinlichkeit für kognitive Verbesserung oder Verschlechterung basierend auf SHAP-basierten Schwellenwerten.
""")

# Eingabeparameter
st.header("📥 Eingabe")
updrs = st.number_input("UPDRS (Baseline)", min_value=0.0, max_value=100.0, value=50.0)
moca = st.number_input("MoCA (Baseline)", min_value=0.0, max_value=30.0, value=25.0)
insula_thickness = st.number_input("lh_insula_thickness", min_value=0.0, max_value=5.0, value=2.5)
rostral_acc_thickness = st.number_input("lh_rostralanteriorcingulate_thickness", min_value=0.0, max_value=5.0, value=2.5)

# Gewichte (aus deinem Modell)
insula_weight = 0.7  # Beispielwert
rostral_acc_weight = 0.3  # Beispielwert

# SN_score berechnen
sn_score = insula_thickness * insula_weight + rostral_acc_thickness * rostral_acc_weight

# Thresholds aus vorheriger Analyse
thresholds = {
    "UPDRS": {"low": 44.88, "high": 57.50},
    "MoCA": {"low": 24.13, "high": 27.18},
    "SN_score": {"low": 0.86, "high": 0.95}
}

# Wahrscheinlichkeiten definieren

def interpret_score(value, low, high):
    if value < low:
        return ("🟦 Niedrig (wahrscheinlich kognitive Verbesserung)", 0.95)
    elif value > high:
        return ("🟥 Hoch (wahrscheinlich kognitive Verschlechterung)", 0.95)
    else:
        return ("🟨 Zwischenbereich (unsichere Prognose)", 0.5)

# Ausgabe
st.header("📊 Prognose")

updrs_text, updrs_prob = interpret_score(updrs, **thresholds["UPDRS"])
moca_text, moca_prob = interpret_score(moca, **thresholds["MoCA"])
sn_text, sn_prob = interpret_score(sn_score, **thresholds["SN_score"])

st.markdown(f"**UPDRS:** {updrs_text}  ")
st.markdown(f"**MoCA:** {moca_text}  ")
st.markdown(f"**SN_score:** {sn_text}  ")

# Durchschnittliche Wahrscheinlichkeit
avg_prob = np.mean([updrs_prob, moca_prob, sn_prob])

if avg_prob >= 0.9:
    st.success(f"Gesamteinschätzung: 🧠 Mit hoher Wahrscheinlichkeit kognitive **Verschlechterung** ({avg_prob*100:.1f}%)")
elif avg_prob <= 0.1:
    st.success(f"Gesamteinschätzung: ✅ Mit hoher Wahrscheinlichkeit kognitive **Verbesserung** ({(1-avg_prob)*100:.1f}%)")
else:
    st.warning(f"Gesamteinschätzung: ⚖️ Unsichere Prognose ({avg_prob*100:.1f}% für Verschlechterung)")
