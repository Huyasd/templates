from flask import Flask, render_template, request, send_file
import pdfplumber
import re

app = Flask(__name__)

# Hàm xử lý PDF (lấy từ mã Python của bạn)
def extract_sizes(text, keyword, min_size):
    pattern = fr'{keyword}:\s*(\d+)-(\d+)-(\d+)'
    matches = re.findall(pattern, text)
    all_sizes = []
    filtered_sizes = []
    
    for match in matches:
        feet = int(match[0]) + int(match[1]) / 12 + int(match[2]) / 144
        size_str = f"{match[0]}-{match[1]}-{match[2]}"
        all_sizes.append(size_str)
        
        if feet > min_size:
            filtered_sizes.append(size_str)
    
    return all_sizes, filtered_sizes

# Trang chủ
@app.route('/')
def index():
    return render_template('index.html')

# Route để xử lý file PDF tải lên
@app.route('/upload', methods=['POST'])
def upload():
    keyword = request.form.get('keyword')
    min_size = float(request.form.get('min_size'))
    pdf_file = request.files['file']
    
    with pdfplumber.open(pdf_file) as pdf:
        text = ''
        for page in pdf.pages:
            text += page.extract_text()
    
    all_sizes, filtered_sizes = extract_sizes(text, keyword, min_size)
    
    return render_template('results.html', all_sizes=all_sizes, filtered_sizes=filtered_sizes, keyword=keyword)

if __name__ == '__main__':
    app.run(debug=True)
