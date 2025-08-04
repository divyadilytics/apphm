from flask import Flask, render_template, request, redirect
import openpyxl
import os

app = Flask(__name__)

EXCEL_FILE = 'students.xlsx'

# Create Excel file if not exists
if not os.path.exists(EXCEL_FILE):
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.append(['Student Name', 'PIN Number'])
    wb.save(EXCEL_FILE)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        name = request.form['name']
        pin = request.form['pin']

        wb = openpyxl.load_workbook(EXCEL_FILE)
        ws = wb.active
        ws.append([name, pin])
        wb.save(EXCEL_FILE)

        return redirect('/')

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
