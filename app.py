from flask import Flask, render_template, request
from models.keymapping import search_doctors
from flask_cors import CORS

app = Flask(__name__)
CORS(app) 


@app.route('/')
def home():
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search():
    user_input = request.form['symptoms']
    
    # Get doctors
    doctors_df = search_doctors(user_input, top_k=5)

    # ✅ Convert DataFrame to list of dictionaries including overview
    doctors = doctors_df.to_dict(orient="records") if not doctors_df.empty else []

    print("🔍 Final Doctors Data Sent to UI:", doctors)  # Debugging

    return render_template('results.html', doctors=doctors)
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
