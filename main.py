from flask import Flask, render_template, request , session
import pexelsPy , jsonify , requests , os 
from tqdm import tqdm
from dotenv import load_dotenv
load_dotenv()


api_key = os.environ.get('API_KEY')
api = pexelsPy.API(api_key)

app = Flask(__name__ , template_folder='template')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/download', methods=['POST'])
def download():
    search_term = request.form['search_term']
    num_videos = int(request.form['num_videos'])

    api.search_videos(search_term, page=1, results_per_page=num_videos)
    videos = api.get_videos()

    folder_name = 'pexels_video'
    if not os.path.exists(folder_name):
        os.mkdir(folder_name)

    for i, video in enumerate(videos):
        url_video = 'https://www.pexels.com/video/' + str(video.id) + '/download'
        r = requests.get(url_video, stream=True)
        for data in r.iter_content(block_size):
            progress_bar.update(len(data))
            f.write(data)
            session['progress'] = int(progress_bar.n / total_size_in_bytes * 100)
            session.modified = True
        progress_bar.close()
        with open(os.path.join(folder_name, 'video-' + str(i+1) + '.mp4'), 'wb') as f:
            total_size_in_bytes = int(r.headers.get('content-length', 0))
            block_size = 1024
            progress_bar = tqdm(total=total_size_in_bytes, unit='iB', unit_scale=True)
            for data in r.iter_content(block_size):
                progress_bar.update(len(data))
                f.write(data)
            progress_bar.close()

    return render_template('download_complete.html')

@app.route('/progress')
def progress():
    return jsonify({'progress': session.get('progress', 0)})

@app.route('/download_complete')
def download_complete():
    return render_template('download_complete.html')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')