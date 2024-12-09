import os
from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
from io import BytesIO
from PIL import Image
import zipfile
import gzip
import nibabel as nib
from gradio_client import Client, handle_file
import tempfile
import shutil
app = Flask(__name__)
CORS(app)
def save_zip_file(zip_ref):
    # Tạo thư mục tạm để giải nén các file
    temp_dir = tempfile.mkdtemp()  # Tạo thư mục tạm
    extracted_folder = os.path.join(temp_dir, "extracted_files")
    os.makedirs(extracted_folder, exist_ok=True)

    # Giải nén các file vào thư mục tạm
    for file_info in zip_ref.infolist():
        with zip_ref.open(file_info) as source_file:
            file_path = os.path.join(extracted_folder, file_info.filename)
            with open(file_path, 'wb') as dest_file:
                dest_file.write(source_file.read())

    # Tạo một file ZIP mới từ thư mục đã giải nén
    zip_file_path = os.path.join(temp_dir, "recompressed_file.zip")
    with zipfile.ZipFile(zip_file_path, 'w', zipfile.ZIP_DEFLATED) as new_zip:
        for root, _, files in os.walk(extracted_folder):
            for file in files:
                new_zip.write(os.path.join(root, file), os.path.relpath(os.path.join(root, file), extracted_folder))

    # Xóa thư mục tạm đã giải nén
    shutil.rmtree(extracted_folder)

    return zip_file_path

@app.route('/predict', methods=['POST'])
def predict():
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400

    file = request.files['file']
    number = request.form.get('number')
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400

    if number == "1":
        try:
            # Đọc file .zip từ bộ nhớ
            zip_data = BytesIO(file.read())
            with zipfile.ZipFile(zip_data, 'r') as zip_ref:
                # Lấy danh sách các file trong file nén
                extracted_files = zip_ref.namelist()
                if not extracted_files:
                    return jsonify({'error': 'No files found in the zip archive'}), 400

                # Lọc các file có đuôi .nii
                nii_files = [f for f in extracted_files if f.lower().endswith('.nii')]
                if not nii_files:
                    return jsonify({'error': 'No .nii files found in the zip archive'}), 400
                zip_file_path = save_zip_file(zip_ref)
                try:
                    client = Client("NhatNam214/Segformer3DBraTS2021")
                    result = client.predict(
                        zip_file=handle_file(zip_file_path), 
                        api_name="/predict" 
                    )
                except Exception as e:
                    print(f"Error during prediction: {e}")
                    result = None  # Gán giá trị None nếu xảy ra lỗi
                if result is None:
                    return jsonify({'error': 'Prediction failed'}), 500
                print(result)
                nii_file_path = result
                nii_image = nib.load(nii_file_path)
                nii_buffer = BytesIO()
                file_map = nib.FileHolder(fileobj=nii_buffer)
                nii_image.to_file_map({'image': file_map})
                nii_buffer.seek(0)

                # Nén file NIfTI thành .gz
                gz_buffer = BytesIO()
                with gzip.GzipFile(fileobj=gz_buffer, mode='wb') as gz_file:
                    gz_file.write(nii_buffer.read())
                gz_buffer.seek(0)

                # Gửi file nén .gz về client
                sanitized_file_name = "overlay_all_slices.nii.gz"
                return send_file(
                    gz_buffer,
                    as_attachment=True,
                    download_name=sanitized_file_name,
                    mimetype='application/gzip'
                )

        except zipfile.BadZipFile:
            return jsonify({'error': 'Invalid zip file'}), 400

    elif number == "2":
        try:
            img = Image.open(file.stream)
            # Lưu ảnh vào file tạm thời
            temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".png")
            img.save(temp_file, format="PNG")
            temp_file.close()

            client = Client("NhatNam214/SegformerISIC2018")
            try:
                result = client.predict(
                    image=handle_file(temp_file.name),
                    api_name="//predict"
                )
            except Exception as e:
                print(e)
            # Chuyển kết quả từ API thành ảnh và lưu lại
            result_path = result
            if not os.path.exists(result_path):
                return jsonify({'error': 'Result file does not exist'}), 500
            with open(result_path, 'rb') as result_file:
                img_io = BytesIO(result_file.read())
            os.remove(result_path)
            img_io.seek(0)
            return send_file(img_io, mimetype='image/png')

        except Exception as e:
            return jsonify({'error': str(e)}), 500

    return jsonify({'error': 'Invalid request'}), 400


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
