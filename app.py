import os
import flask
from flask import Flask
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # ✅ Now it works


# Limit memory usage (Optional for ML models)
os.environ["TF_FORCE_GPU_ALLOW_GROWTH"] = "true"

@app.route('/')
def home():
    return flask.render_template('index.html')

@app.route('/search', methods=['POST'])
def search():
    user_input = flask.request.form['symptoms']

    # Avoid crashing if `search_doctors` fails
    try:
        from models.keymapping import search_doctors  # Import inside function to reduce memory at startup
        doctors_df = search_doctors(user_input, top_k=5)
        doctors = doctors_df.to_dict(orient="records") if not doctors_df.empty else []
    except Exception as e:
        print("Error:", e)
        doctors = []

    return flask.render_template('results.html', doctors=doctors)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # Use dynamic port
    app.run(host="0.0.0.0", port=port)
