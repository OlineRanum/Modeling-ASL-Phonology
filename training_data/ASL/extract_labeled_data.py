import json
import os

parent_folder = os.path.dirname(os.path.abspath(__file__))
json_file_path = os.path.join(parent_folder, '..', 'wlasl_labeled.json')

def read_json(path):
    with open(path, 'r') as file:
        data = json.load(file)
    
    return data

data = read_json(json_file_path)


import pandas as pd

def process_sign_language_data(data):
    """
    Processes sign language data which is in a nested dictionary format.

    Args:
    data (list): A list of dictionaries containing sign language data.

    Returns:
    pd.DataFrame: A DataFrame with the processed data.
    """

    # Flatten the nested structure and create a DataFrame
    flat_data = []
    for item in data:
        gloss = item['gloss']
        for instance in item['instances']:
            instance_data = instance.copy()
            instance_data['gloss'] = gloss
            flat_data.append(instance_data)
    
    return pd.DataFrame(flat_data)

# Example usage of the function would involve calling it with the data as its argument.

data = process_sign_language_data(data)
print(data)



def count_gloss_classes(df):
    """
    Counts the number of unique gloss classes in the sign language dataset.

    Args:
    df (pd.DataFrame): A DataFrame containing sign language data.

    Returns:
    int: The number of unique gloss classes.
    """
    
    # Assuming 'gloss' is the column name holding gloss classes
    unique_glosses = df['gloss'].unique()
    return len(unique_glosses)

# Example usage
num_gloss_classes = count_gloss_classes(data)
print("Number of unique gloss classes:", num_gloss_classes)


def check_no_negative_ones(df):
    """
    Checks if the specified parameters in any row of the DataFrame take the value of -1.

    Args:
    df (pd.DataFrame): The DataFrame containing the sign language data.

    Returns:
    bool: True if none of the parameters are -1, False otherwise.
    """
    
    # List of columns to check
    columns_to_check = [
        "Minor Location", "Handshape", "Flexion", "Spread", "Sign Type",
        "Second Minor Location", "Nondominant Handshape", "Sign Offset",
        "Handshape Morpheme 2", "Thumb Position", "Major Location",
        "Path Movement", "Repeated Movement", "Spread Change",
        "Wrist Twist", "Thumb Contact", "Sign Onset", "Contact",
        "Selected Fingers"
    ]

    # Check if any of the specified columns have -1 as a value
    for column in columns_to_check:
        if column in df.columns and (df[column] == -1).any():
            return False

    return True

# Example usage
# Assuming df is your DataFrame
#result = check_no_negative_ones(data)
#print("No -1 values in specified parameters:", result)


def preprocess_dataframe(df):
    """
    Preprocesses the DataFrame by removing rows where specified keys have a value of -1.

    Args:
    df (pd.DataFrame): The DataFrame containing the sign language data.

    Returns:
    pd.DataFrame: The preprocessed DataFrame.
    """
    
    # List of columns to check
    columns_to_check = [
        "Minor Location", "Handshape", "Flexion", "Spread", "Sign Type",
        "Second Minor Location", "Nondominant Handshape", "Sign Offset",
        "Handshape Morpheme 2", "Thumb Position", "Major Location",
        "Path Movement", "Repeated Movement", "Spread Change",
        "Wrist Twist", "Thumb Contact", "Sign Onset", "Contact",
        "Selected Fingers"
    ]

    # Boolean mask to select rows where none of the specified columns have -1
    mask = df[columns_to_check].eq(-1).any(axis=1)
    
    # Filter out rows where any column has -1
    preprocessed_df = df[~mask]

    return preprocessed_df

# Example usage
# Assuming df is your original DataFrame
#preprocessed_df = preprocess_dataframe(data)

#num_gloss_classes_preprocessed_df = count_gloss_classes(preprocessed_df)
#print("Number of gloss classes with phonological annotations:", num_gloss_classes_preprocessed_df)

#print(preprocessed_df)


def print_source_counts(df):
    """
    Prints all unique sources in the DataFrame and the count of data entries from each source.

    Args:
    df (pd.DataFrame): The DataFrame containing the sign language data.
    """
    
    # Assuming 'source' is the column name holding the source information
    source_counts = df['source'].value_counts()
    
    for source, count in source_counts.items():
        print(f"Source: {source}, Count: {count}")

# Example usage
# Assuming df is your DataFrame
print_source_counts(data)


def count_unique_glosses_asllex(df):
    """
    Counts the number of unique glosses from the source 'asllex'.

    Args:
    df (pd.DataFrame): The DataFrame containing the sign language data.

    Returns:
    int: The number of unique glosses from 'asllex'.
    """
    
    # Filter the DataFrame for entries from 'asllex'
    asllex_df = df[df['source'] == 'signingsavvy']
    
    # Count unique glosses
    unique_gloss_count = asllex_df['gloss'].nunique()

    return unique_gloss_count

# Example usage
# Assuming df is your DataFrame
unique_glosses_asllex = count_unique_glosses_asllex(data)
print("Number of unique glosses from signingsavvy:", unique_glosses_asllex)


import pandas as pd

class SignDataExtractor:
    def __init__(self, df=None):
        self.df = df[df['source'] == 'aslpro']

    def set_dataframe(self, df):
        """Sets the DataFrame for the extractor."""
        self.df = df[df['source'] == 'aslpro']

    def extract_data(self):
        """Extracts URL and gloss data from the DataFrame."""
        if self.df is None:
            raise ValueError("DataFrame not set. Please set the DataFrame using set_dataframe method.")
        
        return self.df[['gloss', 'url']]

    def write_to_csv(self, file_path):
        """Writes the extracted data to a CSV file."""
        if self.df is None:
            raise ValueError("DataFrame not set. Please set the DataFrame using set_dataframe method.")

        data_to_write = self.extract_data()
        data_to_write.to_csv(file_path, index=False)
        print(f"Data written to {file_path}")

# Example usage:
# Assuming df is your DataFrame and you want to write to 'sign_data.csv'
extractor = SignDataExtractor(data)
extractor.write_to_csv('sign_data.csv')

def print_source_counts_and_unique_glosses(df):
    """
    Prints all unique sources in the DataFrame, the count of data entries from each source,
    and the number of unique gloss values for each source.

    Args:
    df (pd.DataFrame): The DataFrame containing the sign language data.
    """

    # Assuming 'source' is the column name holding the source information
    source_counts = df['source'].value_counts()
    
    for source, count in source_counts.items():
        # Filter DataFrame for the current source and count unique glosses
        unique_glosses_count = df[df['source'] == source]['gloss'].nunique()
        print(f"Source: {source}, Count: {count}, Unique Glosses: {unique_glosses_count}")

# Example usage
# Assuming df is your DataFrame
print('-------------------------------------')
print_source_counts_and_unique_glosses(data)
