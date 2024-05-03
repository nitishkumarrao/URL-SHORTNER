from flask import Flask, render_template, request, redirect, flash, abort
import hashlib
import validators
import os

app = Flask(__name__)

url_mapping = {}

def generate_short_url(long_url):
    hash_object = hashlib.sha1(long_url.encode())
    hash_hex = hash_object.hexdigest()[:6]
    return hash_hex

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        long_url = request.form['long_url']
        if validators.url(long_url):
            if long_url in url_mapping:
                short_url = url_mapping[long_url]
            else:
                short_url = generate_short_url(long_url)
                url_mapping[long_url] = short_url
            return render_template('index.html', short_url=request.url_root + short_url)
        else:
            flash('Invalid URL. Please enter a valid URL.', 'error')
    return render_template('index.html')

@app.route('/<short_url>')
def redirect_to_long_url(short_url):
    for long_url, mapped_short_url in url_mapping.items():
        if mapped_short_url == short_url:
            return redirect(long_url)
    abort(404)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
