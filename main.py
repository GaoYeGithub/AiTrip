from flask import Flask, render_template, request, redirect, url_for
import os
from groq import Groq

app = Flask(__name__)

client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

@app.route('/')
def index():
    message = request.args.get('message', '')
    with open("templates/index.html", "r") as f:
        page = f.read()
    page = page.replace("{message}", message)
    return page



@app.route('/add', methods=["POST", "GET"])
def add():
    location = request.form['location']
    start_date = request.form['startdate']
    end_date = request.form['enddate']
    prompt = f"Plan a trip to {location} from {start_date} to {end_date}. Include a daily itinerary with activities."
    response = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
        model="llama3-8b-8192",
    )

    message = response.choices[0].message.content if response else "No idea generated."
    return redirect(url_for('index', message=message))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
