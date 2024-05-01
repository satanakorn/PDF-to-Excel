from flask import Flask, render_template, request
import pdfplumber
import pandas as pd

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        if file:
            pdf = pdfplumber.open(file)
            pages = pdf.pages
            data = []
            for page in pages:
                data.append(page.extract_text())
            pdf.close()

            df = pd.DataFrame(data)
            df.to_excel("output.xlsx", index=False)

            return render_template('index.html', alert_message="Conversion successful!")

    return render_template('index.html', alert_message="No file selected!")

if __name__ == '__main__':
    app.run(debug=True)
