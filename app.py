from flask import Flask, render_template, request
from main import summarizer

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/summarize', methods=['POST'])
def summarize():
    text = request.form['text']
    summary = summarizer(text)
    return render_template('result.html', original_text=text, summary=summary)

if __name__ == '__main__':
    app.run(debug=True)
