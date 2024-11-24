from flask import Flask, request, send_file, render_template, redirect, url_for, flash
import requests
from io import BytesIO

app = Flask(__name__)
app.secret_key = '1234567890pdxcv/*-+hgr567687'  # Required for flash messages

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        image_urls = request.form['image_urls'].strip().split('\n')
        results = []

        for idx, img_url in enumerate(image_urls):
            if img_url:  # Ensure the URL is not empty
                try:
                    response = requests.get(img_url.strip())
                    if response.status_code == 200:
                        img_name = f"downloaded_image_{idx + 1}.jpg"
                        return send_file(BytesIO(response.content),
                                         mimetype='image/jpeg',
                                         as_attachment=True,
                                         download_name=img_name)
                    else:
                        flash(f"Failed to download image from {img_url} (Status code: {response.status_code})")
                except Exception as e:
                    flash(f"Error downloading image from {img_url}: {e}")
        return redirect(url_for('index'))

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
