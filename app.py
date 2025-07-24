import sys
import os
import re
import threading
import webbrowser
from flask import Flask, request, jsonify, render_template, Response

from L5XOpt_UDT import extract_udt_definition, optimize_and_regenerate_udt

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        base_path = sys._MEIPASS  # PyInstaller temp folder
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

app = Flask(__name__, template_folder=resource_path("templates"))

def sanitize_filename(name):
    """Remove unsafe characters from filename."""
    return re.sub(r'[^a-zA-Z0-9_]', '_', name.strip())

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_l5x():
    if 'file' not in request.files:
        return jsonify({"success": False, "error": "No file part in request."}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"success": False, "error": "No selected file."}), 400

    if not file.filename.lower().endswith('.l5x'):
        return jsonify({"success": False, "error": "File must be a .l5x file."}), 400

    try:
        l5x_content = file.read().decode('utf-8')
        udt_data = extract_udt_definition(l5x_content)

        if "error" in udt_data:
            return jsonify({"success": False, "error": udt_data["error"]}), 400

        optimized = optimize_and_regenerate_udt(udt_data)

        if not optimized.get("success"):
            return jsonify({"success": False, "error": optimized.get("error", "Optimization failed.")}), 400

        udt_text = optimized["udt_text"]
        raw_name = udt_data.get("name", "UDT")
        clean_name = sanitize_filename(raw_name)
        download_name = f"Optimized_{clean_name}.l5x"

        response = Response(udt_text, mimetype='application/octet-stream')
        response.headers.set('Content-Disposition', f'attachment; filename="{download_name}"')
        return response

    except Exception as e:
        return jsonify({"success": False, "error": f"Internal server error: {str(e)}"}), 500

if __name__ == '__main__':
    def open_browser():
        webbrowser.open_new("http://127.0.0.1:5001")

    threading.Timer(1, open_browser).start()
    app.run(debug=False, port=5001)
