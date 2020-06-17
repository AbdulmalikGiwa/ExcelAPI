from Google import Create_Service
import pythoncom
import win32com.client as win32
from flask import render_template, flash, request, redirect, jsonify, make_response, Flask
from werkzeug.utils import secure_filename
import psutil
import os



app  = Flask(__name__, template_folder='public')

app.config["FILE_UPLOAD"] = os.getcwd()+'/files'
app.config["FILE_EXT"] = ["XLS", "XLSX"]

def checkFile(filename):
    if not '.' in filename:
        return False
    ext = filename.rsplit(".", 1)[1]
    if ext.upper() in app.config["FILE_EXT"]:
        return True
    else:
        return False

@app.route("/export", methods=["GET", "POST"])
def upload():
    pythoncom.CoInitialize()
    if request.method == "POST":
        xlApp = win32.Dispatch('Excel.Application')
        if request.files:
            file = request.files["excel"]
            sheetid = request.form['sheetid']
            sname = request.form['sheetname']
            estart = request.form['estart']
            gstart = request.form['gstart']
            print(sheetid)
            if file.filename == "":
                flash('File must have a filename')
                return redirect(request.url)
            if sheetid == "" or sname == "" or estart == "" or gstart == "":
                flash('All Fields must be Filled')
                return redirect(request.url)
            if not checkFile(file.filename):
                flash("File Extension not Supported")
                return redirect(request.url)
            else:
                filename = secure_filename(file.filename)
                print(filename)
                file.save(os.path.join(os.getcwd()+'/files', filename))
                xlApp = win32.Dispatch('Excel.Application')
                wb = xlApp.Workbooks.Open(r""+app.config["FILE_UPLOAD"]+"/"+filename)
                print(wb)
                try:
                    ws = wb.Worksheets(sname)
                except Exception as e:
                    flash("Error opening worksheet")
                    return redirect(request.url)
                rngData = ws.Range(estart).CurrentRegion()

                #191h4mt1-iSzIdeRdbszAcWaV_m7_gbierp_bLImnWnI
                gsheet_id = sheetid
                CLIENT_SECRET_FILE = 'client_token.json'
                API_SERVICE_NAME = 'sheets'
                API_VERSION = 'v4'
                SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
                service = Create_Service(CLIENT_SECRET_FILE, API_SERVICE_NAME, API_VERSION, SCOPES)

                try:
                    response = service.spreadsheets().values().append(
                        spreadsheetId=gsheet_id,
                        valueInputOption='RAW',
                        range='data!'+gstart,
                        body=dict(
                            majorDimension='ROWS',
                            values=rngData
                        )
                    ).execute()                    
                except Exception as e:
                    print('Error Uploading to google sheets: '+ str(e))
                    return redirect(request.url)

                for proc in psutil.process_iter():
                    if proc.name() == 'EXCEL.EXE':
                        proc.kill()
                flash("Uploaded")
                return redirect(request.url)

               
    return render_template("index.htm")

    # sheetid = input("please enter your google sheet id: ")
    # startri = input("please enter your start region on your excel sheet: ")
    # startro = input("please enter your start region for your google sheet: ")
    # wsheet = input("please enter your Worksheet name: ")
    # if startri == '' or startro == '':
    #     print('Enter all Start Regions')
    # else:

    # for proc in psutil.process_iter():
    #     if proc.name() == 'EXCEL.EXE':
    #         print('HHHH')
    #         proc.kill()
    #         os.unlink(app.config["FILE_UPLOAD"])
        

if __name__ == '__main__':
    app.secret_key = 'super secret key'
    app.run(debug=True)