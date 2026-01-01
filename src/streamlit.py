import pandas as pd
from matplotlib import pyplot as plt
import streamlit as st

from clean_data import clean_data

st.set_page_config(page_title="PyGains 💪", layout="wide")

@st.cache_data
def load_data():
    df = clean_data(
        file_path = '../data/ameer_data_raw.csv',
        multiply_dict = {'Bench press (flat plate-loaded)': 2},
    )
    return df

def run_dashboard() -> None:
    st.title("Gym Progress 💪")

    cleaned_df = load_data()

    exercise_choice = st.selectbox(
        "Choose which exercise to plot",
        cleaned_df['Exercise Name'].unique()
    )

    exercise_set_type = st.radio(
        "Select which set type(s) to plot",
        options=['Warmup set', 'Working set 1', 'Working set 2', 'Working set 3', 'Drop set', 'Set to failure'],
        index=1
    )

    exercise_set_dict = {
        'Warmup set': 'W',
        'Working set 1': '1',
        'Working set 2': '2',
        'Working set 3': '3',
        'Drop set': 'D',
        'Set to failure': 'F',
    }

    cleaned_df = cleaned_df[cleaned_df['Exercise Name'] == exercise_choice]

    mask = cleaned_df['Set Order'] == exercise_set_dict[exercise_set_type]

    st.subheader(f"{exercise_set_type} for {exercise_choice}")
    st.line_chart(cleaned_df[mask], x='Date', y='Weight (kg)', x_label='Date', y_label='Weight (kg)', width='stretch')

    st.bar_chart(cleaned_df[mask], x='Date', y='Reps', x_label='Date', y_label='Reps', width='stretch')

def main():
    run_dashboard()

if __name__ == '__main__':
    main()