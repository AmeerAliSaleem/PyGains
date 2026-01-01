import os
import pandas as pd

def clean_data(file_path: str, multiply_dict = None) -> pd.DataFrame:
    """
    Reads in data from the raw Strong App .csv file and cleans it.

    Parameters
    ----------
    file_path : str
        The path to the raw Strong App data file.
    multiply_dict: dict
        A dictionary that maps column names to multiplicative factors.
        Useful if the weight lifted for an exercise was only recorded for one arm,
        e.g. measuring lat pulldown progression with the single-arm variant.

    Returns
    ----------
    cleaned_df: pd.DataFrame
        The cleaned DataFrame.
    """
    # Read in data
    if multiply_dict is None:
        multiply_dict = {}
    first_col_name = 'Workout #;"Date";"Workout Name";"Duration (sec)";"Exercise Name";"Set Order";"Weight (kg)";"Reps";"RPE";"Distance (meters)";"Seconds";"Notes";"Workout Notes"'

    df = pd.read_csv(
        os.path.join(file_path),
        header=1,
        names=[first_col_name, 'Extra'],
        usecols=[0, 1]
    )

    second_col_name = df.columns[1]
    df[second_col_name] = df[second_col_name].fillna('')

    # Combine all relevant data into the first column
    df[first_col_name] = df[first_col_name] + df[second_col_name]

    new_cols = first_col_name.replace('"', '').split(';')

    # Clean text data
    list_series = df[first_col_name].apply(lambda x: x.replace('"', '').split(';'))
    cleaned_df = list_series.apply(pd.Series)

    # Drop any extra columns
    cleaned_df = cleaned_df.iloc[:, :len(new_cols)]
    cleaned_df.columns = new_cols

    # Convert data types
    cleaned_df['Date'] = pd.to_datetime(cleaned_df['Date'], format='%Y-%m-%d %H:%M:%S')
    num_cols = ['Workout #', 'Duration (sec)', 'Weight (kg)', 'Reps', 'RPE', 'Distance (meters)', 'Seconds']
    cleaned_df[num_cols] = cleaned_df[num_cols].apply(pd.to_numeric, errors='coerce')

    # Apply multiplicative transformations (if any)
    if multiply_dict:
        for key, value in multiply_dict.items():
            print(f"key: {key}, value: {value}")
            mask = cleaned_df['Exercise Name'] == key
            cleaned_df.loc[mask, 'Weight (kg)'] = cleaned_df.loc[mask, 'Weight (kg)'] * value

    # Could potentially drop null values here too

    return cleaned_df

