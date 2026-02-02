from flask import Flask, request, send_file, render_template, after_this_request
from PyPDF2 import PdfReader, PdfWriter
import os
import time
import webbrowser
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024

os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/merge', methods=['POST'])
def merge_pdfs():
    try:
        pdf_files = request.files.getlist('pdf_files')
        if not pdf_files:
            return "错误：未选择任何PDF文件", 400

        writer = PdfWriter()
        temp_files = []  # 用于记录所有临时文件

        # 逐个处理PDF文件
        for pdf_file in pdf_files:
            if not pdf_file.filename.endswith('.pdf'):
                continue

            filename = secure_filename(pdf_file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)

            # 保存临时文件
            pdf_file.save(filepath)
            temp_files.append(filepath)

            # 读取PDF内容
            reader = PdfReader(filepath)
            for page in reader.pages:
                writer.add_page(page)

        # 生成合并后的PDF
        output_filename = f'merged_{int(time.time())}.pdf'
        output_path = os.path.join(app.config['UPLOAD_FOLDER'], output_filename)

        with open(output_path, 'wb') as output_file:
            writer.write(output_file)

        temp_files.append(output_path)  # 将输出文件也加入临时文件列表

        @after_this_request
        def cleanup(response):
            """请求完成后清理临时文件"""
            try:
                for filepath in temp_files:
                    if os.path.exists(filepath):
                        os.remove(filepath)
            except Exception as e:
                print(f"清理临时文件时出错: {e}")
            return response

        return send_file(output_path, as_attachment=True, download_name='merged.pdf')

    except Exception as e:
        return f"错误：{str(e)}", 500


if __name__ == '__main__':
    # 自动打开浏览器（仅首次启动时触发）
    webbrowser.open('http://127.0.0.1:5000', new=1, autoraise=True)
    app.run(debug=True)