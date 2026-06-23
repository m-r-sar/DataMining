import streamlit as st
import pandas as pd
import joblib


@st.cache_resource
def load_assets():
    model = joblib.load(r'csgo_gb_model.pkl')
    scaler = joblib.load(r'csgo_scaler.pkl')
    return model, scaler


model, scaler = load_assets()


MAP_STATS = {
    "de_mirage": {"CT": 0.502206, "T": 0.497794},
    "de_inferno": {"CT": 0.462848, "T": 0.537152},
    "de_dust2": {"CT": 0.457532, "T": 0.542468},
    "de_nuke": {"CT": 0.552989, "T": 0.447011},
    "de_overpass": {"CT": 0.503745, "T": 0.496255},
    "de_vertigo": {"CT": 0.473243, "T": 0.526757},
    "de_train": {"CT": 0.550769, "T": 0.449231}
}

st.title("🔫 CS:GO Round Predictor")
st.markdown("Round winner prediction on the ML basis.")

st.header("🗺️ Current-Situation")
col_map, col_time, col_bomb = st.columns(3)

with col_map:
    selected_map = st.selectbox("Map", list(MAP_STATS.keys()))

with col_time:
    time_left = st.slider("Round time left (s)", min_value=0.0, max_value=115.0, value=90.0)

with col_bomb:
    bomb_planted = st.radio("Bomb planted?", (0.0, 1.0), horizontal=True)

st.divider()

col1, col2 = st.columns(2)

with col1:
    st.header("🔵 CT")
    ct_players_alive = st.number_input("Players alive CT", min_value=0.0, max_value=5.0, value=5.0, step=1.0)
    ct_health = st.number_input("HP CT (sum)", min_value=0.0, max_value=500.0, value=500.0, step=50.0)
    ct_armor = st.number_input("Armor CT (sum)", min_value=0.0, max_value=500.0, value=500.0, step=50.0)
    ct_helmets = st.number_input("Helmets CT", min_value=0.0, max_value=5.0, value=5.0, step=1.0)
    ct_rifles = st.number_input("Rifles CT (M4/AUG/Famas)", min_value=0.0, max_value=5.0, value=5.0, step=1.0)
    ct_snipers = st.number_input("Snipers CT (AWP/Scout)", min_value=0.0, max_value=5.0, value=0.0, step=1.0)
    ct_defuse_kits = st.number_input("Defuse kits", min_value=0.0, max_value=5.0, value=0.0, step=1.0)

with col2:
    st.header("🟠 T")
    t_players_alive = st.number_input("Players alive T", min_value=0.0, max_value=5.0, value=5.0, step=1.0)
    t_health = st.number_input("HP T (sum)", min_value=0.0, max_value=500.0, value=500.0, step=50.0)
    t_armor = st.number_input("Armor T (sum)", min_value=0.0, max_value=500.0, value=500.0, step=50.0)
    t_helmets = st.number_input("Helmets T", min_value=0.0, max_value=5.0, value=5.0, step=1.0)
    t_rifles = st.number_input("Rifles T (AK/Galil/SG)", min_value=0.0, max_value=5.0, value=5.0, step=1.0)

if st.button("Count probability", use_container_width=True):

    ct_ratio = MAP_STATS[selected_map]["CT"]
    t_ratio = MAP_STATS[selected_map]["T"]

    input_data = {
        'ct_rifles': [ct_rifles],
        'ct_snipers': [ct_snipers],
        't_rifles': [t_rifles],
        'time_left': [time_left],
        'bomb_planted': [bomb_planted],
        'ct_health': [ct_health],
        't_health': [t_health],
        'ct_armor': [ct_armor],
        't_armor': [t_armor],
        'ct_helmets': [ct_helmets],
        't_helmets': [t_helmets],
        'ct_defuse_kits': [ct_defuse_kits],
        'ct_players_alive': [ct_players_alive],
        't_players_alive': [t_players_alive],
        'CT': [ct_ratio],
        'T': [t_ratio]
    }

    input_df = pd.DataFrame(input_data)

    input_scaled_array = scaler.transform(input_df)

    input_scaled_df = pd.DataFrame(input_scaled_array, columns=input_df.columns)

    probabilities = model.predict_proba(input_scaled_df)[0]
    t_prob = probabilities[0] * 100
    ct_prob = probabilities[1] * 100

    st.subheader("Round winner:")

    if ct_prob > t_prob:
        st.success(f"🔵 CT takes the round (Prob: {ct_prob:.1f}%)")
        st.progress(int(ct_prob))
    else:
        st.error(f"🟠 T takes the round (Prob: {t_prob:.1f}%)")
        st.progress(int(t_prob))