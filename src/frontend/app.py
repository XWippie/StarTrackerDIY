from flask import Flask, render_template
import os

app = Flask(__name__, static_url_path="/static")

backend_url = os.environ.get("BACKEND_URL", "http://backend:8000")

@app.route("/")
def index():
    return render_template("main.html")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80)
