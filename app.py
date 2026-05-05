import streamlit as st
import pandas as pd
import math
import random

st.title("🏭 Smart Warehouse 4.0 - PRO SYSTEM")

# =========================
# 🧠 SESSION STATE (IMPORTANT)
# =========================
if "data" not in st.session_state:
    st.session_state.data = pd.DataFrame({
        "Product": ["A", "B", "C", "D", "E"],
        "X": [1, 5, 2, 8, 6],
        "Y": [1, 2, 6, 3, 7],
        "Stock": [10, 8, 15, 5, 12],
        "Defect_rate": [0.1, 0.05, 0.2, 0.08, 0.12]
    })

if "order_path" not in st.session_state:
    st.session_state.order_path = []

if "alerts" not in st.session_state:
    st.session_state.alerts = []

data = st.session_state.data

# =========================
# 📊 DASHBOARD KPI
# =========================
st.subheader("📊 Dashboard KPI")

col1, col2, col3 = st.columns(3)

col1.metric("Total Stock", int(data["Stock"].sum()))
col2.metric("Nb Produits", len(data))
col3.metric("Taux Défaut Moyen", round(data["Defect_rate"].mean(), 2))

st.dataframe(data)

# =========================
# 🛒 COMMANDES
# =========================
st.subheader("🛒 Nouvelle Commande")

order = st.multiselect(
    "Choisir les produits",
    data["Product"].tolist()
)

# =========================
# 📏 DISTANCE
# =========================
def distance(a, b):
    return math.sqrt((a[0]-b[0])**2 + (a[1]-b[1])**2)

# =========================
# 🚶 OPTIMISATION PICKING
# =========================
def optimize(order_list, df):
    path = []
    current = (0, 0)
    remaining = order_list.copy()

    while remaining:
        nearest = None
        min_d = float("inf")

        for p in remaining:
            row = df[df["Product"] == p].iloc[0]
            pos = (row["X"], row["Y"])
            d = distance(current, pos)

            if d < min_d:
                min_d = d
                nearest = p

        path.append(nearest)
        row = df[df["Product"] == nearest].iloc[0]
        current = (row["X"], row["Y"])
        remaining.remove(nearest)

    return path

# =========================
# 🚀 PROCESS ORDER
# =========================
if st.button("🚀 Générer Picking Optimisé"):

    if not order:
        st.warning("Sélectionne au moins un produit")
    else:
        path = optimize(order, data)
        st.session_state.order_path = path

        st.success("✅ Picking optimisé généré")

        st.write("📍 Chemin opérateur :")
        st.write(" → ".join(path))

# =========================
# 📡 QR SCAN SIMULATION
# =========================
st.subheader("📡 Scan Produit (QR Simulation)")

scan_product = st.selectbox(
    "Scanner un produit",
    data["Product"].tolist()
)

if st.button("📡 Scanner"):

    row = data[data["Product"] == scan_product].iloc[0]

    is_defect = random.random() < row["Defect_rate"]

    if is_defect:
        alert = f"❌ {scan_product} DEFECTUEUX détecté !"
        st.session_state.alerts.append(alert)
        st.error(alert)
    else:
        st.success(f"✅ {scan_product} OK")

        # 🔄 mise à jour stock
        st.session_state.data.loc[
            st.session_state.data["Product"] == scan_product,
            "Stock"
        ] -= 1

# =========================
# 🚨 ALERTES
# =========================
st.subheader("🚨 Alertes Qualité")

if st.session_state.alerts:
    for a in st.session_state.alerts:
        st.warning(a)
else:
    st.info("Aucune alerte")

# =========================
# 📦 TRAJET OPÉRATEUR
# =========================
st.subheader("🚶 Dernier Trajet Opérateur")

if st.session_state.order_path:
    st.write(" → ".join(st.session_state.order_path))
else:
    st.info("Aucune commande traitée")
