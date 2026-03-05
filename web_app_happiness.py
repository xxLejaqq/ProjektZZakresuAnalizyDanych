import streamlit as st
import joblib
import numpy as np
import pandas as pd
from pathlib import Path
from classes_preprocessing import ColumnDropper, ChangeNameCountry, AddRegion, TransPower, TransLog, OneH
# Create region mapping dictionary
region_proxy_map = {
    'Northern Europe': 'Finland',
    'Southern Europe': 'Malta',
    'Western Europe': 'Netherlands',
    'Eastern Europe': 'Czechia',
    'Northern America': 'Canada',
    'Central America': 'Costa Rica',
    'South America': 'Chile',
    'Central Asia': 'Uzbekistan',
    'Southern Asia': 'Pakistan',
    'South-eastern Asia': 'Singapore',
    'Eastern Asia': 'Taiwan',
    'Western Asia': 'Israel',
    'Northern Africa': 'Libya',
    'Middle Africa': 'Cameroon',
    'Southern Africa': 'South Africa',
    'Western Africa': 'Nigeria',
    'Eastern Africa': 'Mauritius',
    'Australia and New Zealand': 'New Zealand',
    'Caribbean': 'Trinidad and Tobago',
}

def main():
    # Setup UI and input widgets to control variable values
    st.title("Happiness Prediction Application")
    st.markdown("Choose the region, level of features and calculate prediction of happiness.")
    selected_region = st.selectbox("Region", list(region_proxy_map.keys()))
    GDP_per_capita = st.slider("GDP per capita", min_value=0.0, max_value=10.0, step=0.01)
    Social_support = st.slider("Social support", min_value=0.0, max_value=1.0, step=0.01)
    Healt_life_expectacy = st.slider("Health life expectancy", min_value=0, max_value=100, step=1)
    Freedom_to_make_life_choices = st.slider("Freedom to make life choices", min_value=0.0, max_value=1.0, step=0.01)
    Generosity = st.slider("Generosity", min_value=0.0, max_value=1.0, step=0.01)
    Perceptions_of_corruption = st.slider("Perceptions of corruption", min_value=0.0, max_value=1.0, step=1.0)

    # Create button to trigger predictions
    if st.button("Calculate Happiness"):
        try:
            # Wyznaczenie folderu z modelem
            BASE_DIR = Path(__file__).resolve().parent
            # Łączenie folderu z nazwą pliku modelu
            model_path = BASE_DIR / 'XGBoost_happiness'
            # Wczytanie modelu
            model = joblib.load(model_path)
            proxy_country = region_proxy_map[selected_region]
            X_new = pd.DataFrame({
                'Country': [proxy_country],
                'GDP per capita': [GDP_per_capita],
                'Social support': [Social_support],
                'Healthy life expectancy': [Healt_life_expectacy],
                'Freedom to make life choices': [Freedom_to_make_life_choices],
                'Generosity': [Generosity],
                'Perceptions of corruption': [Perceptions_of_corruption]
            })
            model_result = model.predict(X_new)
            st.write("Predicted Happiness:", model_result[0])
        except Exception as e:
            st.error(f"Error: {e}")

if __name__ == '__main__':
    main()
