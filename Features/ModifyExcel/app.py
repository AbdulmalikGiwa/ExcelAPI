from flask import Flask, request, redirect, json
import os
from openpyxl import load_workbook

app = Flask(__name__)
UPLOAD_FOLDER = 'files'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['ALLOWED_FILE_EXTENSIONS'] = ['XLSX', 'XLS']


@app.route("/upload", methods=['POST', 'GET'])
def modify_file():
    if request.method == 'POST':

        if request.files and request.form:
            file = request.files['file']
            data = json.loads(request.form.get('data'))
            if file.filename == "":
                print("No Filename")
                return redirect(request.url)

            sheet = data['sheet']
            update = data['updated']

            wb = load_workbook(file)
            ws = wb[sheet]
            ws.append(update)
            filename = file.filename
            path = (os.path.join(app.config['UPLOAD_FOLDER'], filename ))
            wb.save(path)

        return redirect(request.url)
    return "success"


if __name__ == '__main__':
    app.run(debug=True)
