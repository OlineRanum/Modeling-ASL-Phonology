import os
import requests
from bs4 import BeautifulSoup
import pandas as pd
import urllib.request

##################################################
# Scripts for scraping SignBank data
# Requiers premission from the SignBank team
##################################################

# Set path to CSV file with URLs
# These paths must be updated
file_path = 'data_url.csv'

def read_csv(file_path):
    """
    Read a CSV file and return a new DataFrame with selected columns.

    Args:
        file_path (str): The path to the CSV file.

    Returns:
        pandas.DataFrame: A new DataFrame with columns 'URL' and 'Signbank ID'.
    """
    df = pd.read_csv(file_path)
    new_df = df[['URL', 'Signbank ID']].copy()
    return new_df

def download_video(video_url, destination_path):
    """
    Downloads a video from the given URL and saves it to the specified destination path.

    Args:
        video_url (str): The URL of the video to download.
        destination_path (str): The path where the downloaded video will be saved.

    Raises:
        Exception: If there is an error while downloading the video.

    Returns:
        None
    """
    try:
        urllib.request.urlretrieve(video_url, destination_path)
        print(f"Downloaded video to {destination_path}")
    except Exception as e:
        print(f"Error downloading video: {e}")

def scrape_and_download_videos(df, folder_name='ngt_data'):
    """
    Scrapes and downloads videos from a given DataFrame.

    Args:
        df (pandas.DataFrame): The DataFrame containing the URLs and Signbank IDs of the videos.
        folder_name (str, optional): The name of the folder where the videos will be saved. Defaults to 'ngt_data'.
    """
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)

    base_url = 'https://signbank.cls.ru.nl'

    # per row in the DataFrame, get URL and Signbank ID
    # download video
    for _, row in df.iterrows():
        web_url = row['URL']
        signbank_id = row['Signbank ID']

        try:
            r = requests.get(web_url)
            soup = BeautifulSoup(r.content, 'html.parser')
            video_tag = soup.find('video', {'id': 'videoplayer'})

            if video_tag and 'src' in video_tag.attrs:
                video_url = base_url + video_tag['src']
                video_path = os.path.join(folder_name, f'video_{signbank_id}.mp4')
                download_video(video_url, video_path)
            else:
                print(f"Video tag not found for URL: {web_url}")

        except Exception as e:
            print(f"Error processing URL {web_url}: {e}")

# Replace 'your_file.csv' with the path to your CSV file
df = read_csv(file_path)
scrape_and_download_videos(df)

