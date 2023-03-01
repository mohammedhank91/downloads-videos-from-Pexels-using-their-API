# Pexels Video Downloader

This Python script downloads videos from Pexels and shows a progress bar for each video using the tqdm library.

## Prerequisites

- Python 3.x
- `requests` library
- `tqdm` library
- Pexels API key

## Installation

1. Clone this repository to your local machine or download the ZIP file and extract it.
2. Install the required libraries by running `pip install -r requirements.txt`.
3. Replace `PEXELS_API` variable with your own API key from [Pexels](https://www.pexels.com/api/).

## Usage

1. Open a terminal and navigate to the directory where the script is saved.
2. Run the command `python pexels_video_downloader.py`.
3. The script will download the videos and show a progress bar for each video in the terminal.
4. The downloaded videos will be saved in a new folder called `pexels_video`.

## Notes

- The script will download the first 100 videos that match the search query. If you want to download more or less videos, change the `results_per_page` parameter in the `api.search_videos` method.
- The progress bar is shown using the `tqdm` library. If you don't want to see the progress bar, remove the `tqdm` code block in the script.
- This script is provided as-is and is not guaranteed to work in all situations. Use at your own risk.

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details.
