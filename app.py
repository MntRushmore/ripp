from flask import Flask, request, redirect, render_template
from urllib.parse import urlparse
app = Flask(__name__)
url_mapping = {} 
import random
import string

def generate_short_url():
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(6)) 

def is_valid_url(url):
    parsed_url = urlparse(url)
    return bool(parsed_url.netloc)

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        long_url = request.form["long_url"]
        
        if is_valid_url(long_url):
            short_url = generate_short_url()
            url_mapping[short_url] = long_url
            return f"Short URL: <a href='/{short_url}'>http://localhost:4000/{short_url}</a>"
        else:
            return "Invalid URL provided", 400
    return render_template("index.html")

@app.route("/<short_url>")
def redirect_url(short_url):
    long_url = url_mapping.get(short_url)

    if long_url:
        return redirect(long_url)
    else:
        return render_template("error.html", message="URL not found!")

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=4000)