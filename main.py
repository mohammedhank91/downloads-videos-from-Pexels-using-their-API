from flask import Flask, render_template, request, session, jsonify 
import pexelsPy, requests, os
from tqdm import tqdm
from dotenv import load_dotenv
load_dotenv()

api_key = os.environ.get('API_KEY')
api = pexelsPy.API(api_key)

app = Flask(__name__, template_folder='template')
app.secret_key = 'your_secret_key'

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/download', methods=['POST'])
def download():
    search_term = request.form['search_term']
    num_videos = int(request.form['num_videos'])

    # Search for videos on Pexels
    api.search_videos(search_term, page=1, results_per_page=num_videos)
    videos = api.get_videos()

    # Create the folder for downloaded videos if it doesn't exist
    folder_name = 'pexels_video'
    if not os.path.exists(folder_name):
        os.mkdir(folder_name)

    # Download each video
    for i, video in enumerate(videos):
        video_url = video._Video__video['video_files'][0]['link']  # Access the video file URL

        # Extract video name or title, sanitize it to remove invalid characters
        video_name = video._Video__video['title'] if 'title' in video._Video__video else f'video-{i + 1}'
        safe_video_name = "".join(c for c in video_name if c.isalnum() or c in (' ', '_', '-')).rstrip()

        # Stream the video and save it locally
        r = requests.get(video_url, stream=True)
        with open(os.path.join(folder_name, f'{safe_video_name}.mp4'), 'wb') as f:
            total_size_in_bytes = int(r.headers.get('content-length', 0))
            block_size = 1024
            progress_bar = tqdm(total=total_size_in_bytes, unit='iB', unit_scale=True, leave=False, position=0, ncols=100)

            if total_size_in_bytes == 0:
                for data in r.iter_content(block_size):
                    f.write(data)
            else:
                for data in r.iter_content(block_size):
                    progress_bar.update(len(data))
                    f.write(data)

                    # Update the progress in the session
                    session['progress'] = int(progress_bar.n / total_size_in_bytes * 100)
                    session.modified = True
            progress_bar.close()

    # Mark download as complete
    session['progress'] = 100
    session.modified = True

    # Return the download complete page
    return render_template('download.html')


            


@app.route('/progress')
def progress():
    return jsonify({'progress': session.get('progress', 0)})

@app.route('/download_complete')
def download_complete():
    return render_template('download.html')

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0')
