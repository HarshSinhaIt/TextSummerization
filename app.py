from flask import Flask, render_template, request
from text_summary import summarizer

app= Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analyze', methods=['GET', 'POST'])
def analyze():
    if request.method == 'POST':
        original_text = request.form['original_text']
        summary, doc, original_len, summary_len = summarizer(original_text)
        return render_template('summary.html', original_text=original_text, summary=summary, original_len=original_len, summary_len=summary_len)
    return render_template('summary.html')


if __name__ == "__main__":
    app.run(debug=True)


