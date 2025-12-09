# Hệ Cơ Sở Tri Thức - Tra Cứu Luật Giao Thông

Ứng dụng web demo mô phỏng hệ cơ sở tri thức với Forward Chaining (Suy diễn Tiến) và Structured Look-up 3 cấp độ.

## 📁 Cấu trúc dự án

```
code/
├── app.py              # Flask application (Bộ Suy diễn và Router)
├── rule.json           # Cơ sở tri thức (dữ liệu luật giao thông)
├── templates/
│   └── index.html      # Giao diện web
└── README.md           # File này
```

## 🎯 Mô tả chức năng

### Logic Forward Chaining - 3 Cấp độ lọc:

1. **Cấp 1**: Chọn Lỗi vi phạm → Hệ thống trả về danh sách Phương tiện
2. **Cấp 2**: Chọn Phương tiện → Hệ thống trả về danh sách Chi tiết lỗi  
3. **Cấp 3**: Chọn Chi tiết lỗi → Hệ thống trả về thông tin xử phạt đầy đủ

## 🚀 Hướng dẫn chạy ứng dụng

### 1. Cài đặt Flask (nếu chưa có)

```bash
pip install flask
```

### 2. Chạy ứng dụng

```bash
python app.py
```

### 3. Truy cập ứng dụng

Mở trình duyệt và truy cập: **http://127.0.0.1:5000**

## 💡 Cách sử dụng

1. **Bước 1**: Chọn loại lỗi vi phạm từ dropdown đầu tiên
2. **Bước 2**: Chọn phương tiện từ dropdown thứ hai (tự động cập nhật)
3. **Bước 3**: Chọn chi tiết lỗi từ dropdown thứ ba (tự động cập nhật)
4. **Kết quả**: Thông tin xử phạt sẽ hiển thị tự động bao gồm:
   - Mã luật
   - Mức phạt tiền
   - Hình phạt bổ sung
   - Căn cứ pháp lý

## 🔧 Chi tiết kỹ thuật

### Backend (app.py):
- **Framework**: Flask
- **Endpoint chính**: `/` (trang chủ)
- **Endpoint API**: `/filter_data` (xử lý logic Forward Chaining)
- **Phương thức**: POST với JSON data

### Frontend (index.html):
- **Công nghệ**: HTML5, CSS3, JavaScript (Fetch API)
- **Tương tác**: AJAX không đồng bộ
- **UI/UX**: Responsive design với gradient background

### Cơ sở tri thức (rule.json):
- **Cấu trúc**: JSON array chứa các đối tượng luật
- **Thuộc tính**: id, loiViPham, phuongTien, chiTietLoi, mucPhat, phatBoSung, canCuPhapLy

## 📊 Ví dụ dữ liệu JSON

```json
{
  "trafficViolations": [
    {
      "id": "L01",
      "loiViPham": "Lỗi vi phạm nồng độ cồn",
      "phuongTien": "xe máy",
      "chiTietLoi": "Nồng độ cồn chưa vượt quá 50 mg/100ml máu...",
      "mucPhat": "2.000.000 – 3.000.000 đồng",
      "phatBoSung": "Trừ 4 điểm GPLX",
      "canCuPhapLy": "Điểm a Khoản 6 Điều 7 Nghị định 168/2024/NĐ-CP"
    }
  ]
}
```

## 🎓 Ý nghĩa đồ án

Đây là cốt lõi của **Bộ Suy diễn Tiến (Forward Chaining)** trong hệ cơ sở tri thức:
- Bắt đầu từ dữ liệu đầu vào (Lỗi vi phạm)
- Suy diễn tuần tự qua các cấp độ (Phương tiện → Chi tiết)
- Kết luận cuối cùng (Thông tin xử phạt)

## 📝 Ghi chú

- File `rule.json` phải nằm cùng thư mục với `app.py`
- Cổng mặc định: 5000 (có thể thay đổi trong `app.py`)
- Debug mode được bật để hỗ trợ phát triển

## 👨‍💻 Tác giả

Đồ án Hệ Cơ Sở Tri Thức - CS217
