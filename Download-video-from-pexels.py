import pexelsPy  # Import the Pexels API client library
import requests  # Import the requests library for making HTTP requests
from tqdm import tqdm  # Import the tqdm library for showing download progress
import os  # Import the os library for working with file paths and directories

# Set up the Pexels API client
PEXELS_API = 'api-key'
api = pexelsPy.API(PEXELS_API)

# Search for videos on Pexels and retrieve the search results
api.search_videos('nature', page=1, results_per_page=100)
videos = api.get_videos()

# Create a folder to store the downloaded videos (if it doesn't exist)
folder_name = 'pexels_video'
if not os.path.exists(folder_name):
    os.mkdir(folder_name)

# Download each video and save it to the folder
for i, video in enumerate(videos):
    url_video = 'https://www.pexels.com/video/' + str(video.id) + '/download'  # Get the download URL for the video
    r = requests.get(url_video, stream=True)  # Make an HTTP request to download the video

    # Save the video to a file in the folder
    with open(os.path.join(folder_name, 'video-' + str(i+1) + '.mp4'), 'wb') as f:
        total_size_in_bytes = int(r.headers.get('content-length', 0))  # Get the total size of the video in bytes
        block_size = 1024  # Define the block size for iterating over the response content
        progress_bar = tqdm(total=total_size_in_bytes, unit='iB', unit_scale=True)  # Create a progress bar to show the download progress
        for data in r.iter_content(block_size):
            progress_bar.update(len(data))  # Update the progress bar with the amount of data downloaded in each iteration
            f.write(data)  # Write the downloaded data to the file
        progress_bar.close()  # Close the progress bar once the download is complete
