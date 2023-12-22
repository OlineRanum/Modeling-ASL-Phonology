import xml.etree.ElementTree as ET
import pandas as pd
# This code was generated using chat gpt
# TODO: Split the description 


def read_file_to_list(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        words_list = [line.strip() for line in file]
    return words_list

def read_csv(file_path):
    # Create a DataFrame from the merged data
    df = pd.read_csv(file_path)
    
    return df

def filter_data(df):
    """
    If a cell is blank, its loaded as a NaN
    """
    # Filtering out rows where 'Handedness', 'Strong Hand', 'Weak Hand', 'Handshape Change' are all hyphens
    """
    filtered_df = df[~((df['Handedness'] == '-') & \
                       (df['Strong Hand'] == '-') & \
                        (df['Weak Hand'] == '-') & \
                        (df['Handshape Change'] == '-'))]
    """
    # Apply the function to each entry in the column and create two new columns
    df['Word'], df['Version'] = zip(*df['Annotation ID Gloss (Dutch)'].apply(split_word_version))
    # Lowercase every entry in the 'Word' column
    df['Word'] = df['Word'].str.lower()

    
    filtered_df = df[~((df['Strong Hand'] == '-') & \
                        (df['Weak Hand'] == '-') )]
    
    output_file_path = 'processed_common_words.txt'  # Replace with your output file path
    words_list = read_file_to_list(output_file_path)
    # Assuming words_list is your list of words
    words_list = [word.lower() for word in words_list]
    filtered_df = df[df['Word'].isin(words_list)]
    
    # Now df has two new columns: 'Word' and 'Version'
    return filtered_df

# Function to split the entry into word and version
def split_word_version(entry):
    parts = entry.split('-')
    if len(parts) == 1:
        return parts[0], 'A'  # Assign 'A' if there is no version
    else:
        return '-'.join(parts[:-1]), parts[-1]  # Split into word and version



# Call the function with your file path
df = read_csv('output.csv')
df = filter_data(df)


def create_url(row):
    # Construct the URL using the prefix, Text_nld, and CVE_ID
    url = f"https://signbank.cls.ru.nl/dictionary/gloss/{row['Signbank ID']}.html"
    return url

# Assuming df is your existing DataFrame
# Apply the function to each row to create a new column
df['URL'] = df.apply(create_url, axis=1)
# Display the updated DataFrame
print(df[['Signbank ID', 'Word', 'URL']])

# Display the DataFrame
#print(df[0:10])

def write_to_csv(df, filename):
    # Select only the Text_nld and URL columns and write to CSV
    #df[['Text_nld', 'CVE_ID']].to_csv(filename, index=False)
    df.to_csv(filename, index=False)


# Assuming df is your DataFrame with the necessary columns
write_to_csv(df, 'data_url.csv')

#print("Data has been written to output.csv")


######################################## Filter Common words
import re

def extract_words(file_path):
    # Read the file
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    # Extract words
    words = []
    for line in lines:
        # Use regular expression to find words outside parentheses
        match = re.match(r"([^\(]+)", line)
        if match:
            word = match.group(1).strip()  # Remove leading/trailing whitespace
            words.append(word)

    return sorted(set(words))

def write_words_to_file(words, output_file_path):
    # Write words to a new file
    with open(output_file_path, 'w', encoding='utf-8') as file:
        for word in words:
            file.write(word + '\n')

# Replace 'input_file.txt' with the path to your input file
#input_file_path = 'common_words.txt'

# Replace 'output_file.txt' with the path for your output file
#output_file_path = 'processed_common_words.txt'

# Extract words and write them to a new file
#words = extract_words(input_file_path)
#write_words_to_file(words, output_file_path)
