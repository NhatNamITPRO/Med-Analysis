
# Hướng Dẫn Thiết Lập Môi Trường

Dự án này yêu cầu sử dụng Python và các gói cần thiết được liệt kê trong tệp `requirements.txt`. Dưới đây là các bước để thiết lập môi trường và cài đặt các gói.

## 1. Kiểm tra phiên bản Python

Đảm bảo rằng bạn đã cài đặt Python 3.10 trở lên trên hệ thống của mình.  
Kiểm tra bằng lệnh:

```bash
python --version
```

Hoặc (trên một số hệ thống):

```bash
python3 --version
```

## 2. Tạo môi trường ảo

### Trên Windows:
```bash
python -m venv venv
```

### Trên Linux/MacOS:
```bash
python3 -m venv venv
```

Lệnh trên sẽ tạo một thư mục `env` chứa môi trường ảo.

## 3. Kích hoạt môi trường ảo

### Trên Windows:
```bash
venv\Scripts\activate
```

### Trên Linux/MacOS:
```bash
source venv/bin/activate
```

Sau khi kích hoạt thành công, bạn sẽ thấy tên môi trường ảo xuất hiện ở đầu dòng lệnh, ví dụ: `(env)`.

## 4. Cài đặt các gói

Đảm bảo rằng tệp `requirements.txt` có trong thư mục làm việc của bạn. Chạy lệnh sau để cài đặt các gói:

```bash
pip install -r requirements.txt
```

## 5. Kiểm tra cài đặt

Đảm bảo rằng tất cả các gói đã được cài đặt bằng cách chạy lệnh sau:

```bash
pip freeze
```

Danh sách các gói đã cài đặt sẽ được hiển thị. Hãy kiểm tra xem tất cả các gói trong `requirements.txt` đã được cài đặt.

## 6. Vô hiệu hóa môi trường ảo (Khi hoàn tất)

Khi không còn sử dụng, bạn có thể thoát khỏi môi trường ảo bằng lệnh:

```bash
deactivate
```

---

### Lưu ý

- Hãy đảm bảo sử dụng đúng phiên bản Python mà dự án yêu cầu.
- Nếu gặp lỗi trong quá trình cài đặt, hãy kiểm tra lại tệp `requirements.txt` hoặc cập nhật `pip` lên phiên bản mới nhất:

```bash
pip install --upgrade pip
```
Danh sách các gói đã cài đặt sẽ được hiển thị. Hãy kiểm tra xem tất cả các gói trong `requirements.txt` đã được cài đặt.

## 7. Khởi chạy server
Chạy câu lệnh bên dưới để start server tại port 5000

```bash
python app.py
```