from flask import Flask, render_template, request, redirect, url_for, send_from_directory,send_file
from lidkaarten import maak_lidkaarten
from waitress import serve
import io
import tempfile
import os
from pathlib import Path

app = Flask(__name__)

UPLOAD_FOLDER = tempfile.mkdtemp()
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

OUTPUT_FOLDER = tempfile.mkdtemp()
app.config['OUTPUT_FOLDER'] = OUTPUT_FOLDER

@app.route('/')
@app.route('/index', methods=['POST'])
def index():
    global leden_path  # Make leden_path and template_path global
    global template_path
    
    if request.method == 'POST':
        leden_file = request.files['leden']
        template_file = request.files['template']
        action = request.form.get('action')
        
        if 'download' in request.form:
            print('button clicked')
            
            leden_path = os.path.join(app.config['UPLOAD_FOLDER'], 'leden.txt')
            leden_file.save(leden_path)
            
            template_path = os.path.join(app.config['UPLOAD_FOLDER'], 'template.png')
            template_file.save(template_path)
        
            print("files uploaded siuhhh")

            print('download button clicked')
            maak_lidkaarten(leden_path,template_path,app.config['OUTPUT_FOLDER'])
        
            print('pdf saved in temp folder siuhhh')
            return send_file(os.path.join(app.config['OUTPUT_FOLDER'], 'lidkaarten.pdf'), as_attachment=True, download_name='lidkaarten.pdf', mimetype='application/pdf')

    return render_template('index.html')

if __name__ == "__main__":
    app.debug = True  # Enable the debug mode
    app.run(host="0.0.0.0", port=8000)
