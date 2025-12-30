# Hệ Cơ Sở Tri Thức - Tra Cứu Luật Giao Thông

Ứng dụng web demo mô phỏng hệ cơ sở tri thức với Forward Chaining (Suy diễn Tiến) và Structured Look-up 3 cấp độ, tích hợp tra cứu khái niệm giao thông và quản lý danh sách vi phạm.

## 📋 Mục lục

- [Giới thiệu](#-giới-thiệu)
- [Tính năng](#-tính-năng)
- [Cấu trúc dự án](#-cấu-trúc-dự-án)
- [Cài đặt và chạy ứng dụng](#-cài-đặt-và-chạy-ứng-dụng)
- [Hướng dẫn sử dụng](#-hướng-dẫn-sử-dụng)
- [Chi tiết kỹ thuật](#-chi-tiết-kỹ-thuật)
- [Cơ sở tri thức](#-cơ-sở-tri-thức)
- [API Endpoints](#-api-endpoints)
- [Ví dụ sử dụng](#-ví-dụ-sử-dụng)
- [Ý nghĩa đồ án](#-ý-nghĩa-đồ-án)

## 🎯 Giới thiệu

Đây là một ứng dụng web demo mô phỏng **Hệ Cơ Sở Tri Thức (Knowledge-Based System)** áp dụng trong lĩnh vực luật giao thông Việt Nam. Ứng dụng sử dụng phương pháp **Forward Chaining (Suy diễn Tiến)** để tra cứu thông tin xử phạt vi phạm giao thông theo 3 cấp độ lọc tuần tự.

### Điểm nổi bật:

✅ **Hệ thống 3 tab chuyên biệt** - Giao diện rõ ràng, dễ sử dụng  
✅ **Forward Chaining 3 cấp độ** - Suy diễn logic thông minh  
✅ **Tra cứu khái niệm giao thông** - Tìm kiếm định nghĩa thuật ngữ với autocomplete  
✅ **Quản lý danh sách vi phạm** - Thêm, xóa và tính tổng mức phạt tự động  
✅ **Xác định phạt bổ sung cao nhất** - Thông minh phân tích mức phạt nghiêm trọng nhất  
✅ **Session-based storage** - Lưu trữ dữ liệu trong phiên làm việc  
✅ **Responsive design** - Giao diện đẹp mắt, hoạt động mượt mà  

## 🎨 Tính năng

### 1. Tab "Tra Cứu Vi Phạm" 🔍

**Forward Chaining 3 cấp độ:**
- **Cấp 1**: Chọn Lỗi vi phạm → Hệ thống lọc và trả về danh sách Phương tiện
- **Cấp 2**: Chọn Phương tiện → Hệ thống lọc và trả về danh sách Chi tiết lỗi
- **Cấp 3**: Chọn Chi tiết lỗi → Hệ thống trả về thông tin xử phạt đầy đủ

**Kết quả hiển thị:**
- Mã luật (ID)
- Mức phạt tiền (khoảng từ - đến)
- Hình phạt bổ sung (trừ điểm GPLX, tước quyền)
- Căn cứ pháp lý đầy đủ

**Thêm vào danh sách:**
- Nút "➕ Thêm vào Danh Sách" sau khi tra cứu
- Tự động chuyển sang Tab "Danh Sách Vi Phạm" sau khi thêm

### 2. Tab "Tra Cứu Khái Niệm" 📖

**Tìm kiếm thông minh:**
- Nhập từ khóa tự do để tìm thuật ngữ giao thông
- Autocomplete gợi ý các thuật ngữ có sẵn
- Tìm kiếm theo: thuật ngữ chính, định nghĩa, từ khóa liên quan

**Kết quả hiển thị:**
- Thuật ngữ chính thức với mã định danh
- Định nghĩa chi tiết, đầy đủ
- Căn cứ pháp lý (QCVN, Nghị định...)
- Từ khóa liên quan giúp tìm kiếm mở rộng

**Hỗ trợ 20+ khái niệm:**
- Xe cơ giới, xe mô tô, xe máy điện
- Đường bộ, làn đường, phần đường xe chạy
- Đèn giao thông, vạch kẻ đường
- Giấy phép lái xe, biển báo...

### 3. Tab "Danh Sách Vi Phạm" 📋

**Quản lý danh sách:**
- Hiển thị tất cả vi phạm đã thêm với số thứ tự
- Badge đỏ thông báo số lượng vi phạm
- Mỗi vi phạm hiển thị đầy đủ thông tin

**Tính năng:**
- Xóa từng vi phạm bằng nút ✕
- Xóa toàn bộ danh sách bằng nút "🗑️ Xóa Toàn Bộ Danh Sách"
- Quay lại tra cứu bằng nút "🔍 Quay Lại Tra Cứu"

**Tổng hợp thông minh:**
- **Tự động tính tổng số vi phạm**
- **Tự động tính tổng mức phạt** (lấy trung bình các khoảng)
- **Xác định hình phạt bổ sung cao nhất** (ưu tiên tước quyền > trừ điểm)
- Hiển thị định dạng VND chuẩn
- Ghi chú về mức phạt ước tính

## 📁 Cấu trúc dự án

```
code/
├── app.py                    # Flask application (Bộ Suy diễn và Router)
├── rule.json                 # Cơ sở tri thức (dữ liệu luật giao thông)
├── khainiem.json             # Từ điển khái niệm giao thông
├── templates/
│   └── index.html            # Giao diện web (3 tabs)
└── README.md                 # File này
```

### Mô tả các file:

- **app.py**: Backend Flask với các API endpoints và logic Forward Chaining
- **rule.json**: Cơ sở tri thức chứa ~100+ luật vi phạm giao thông
- **khainiem.json**: Từ điển chứa 20+ khái niệm giao thông với định nghĩa
- **index.html**: Frontend với giao diện 3 tabs, AJAX, và animation

## 🚀 Cài đặt và chạy ứng dụng

### 1. Yêu cầu hệ thống

- Python 3.7 trở lên
- Trình duyệt web hiện đại (Chrome, Firefox, Edge...)

### 2. Cài đặt Flask

```bash
pip install flask
```

### 3. Chạy ứng dụng

```bash
python app.py
```

### 4. Truy cập ứng dụng

Mở trình duyệt và truy cập: **http://127.0.0.1:5000**

Server sẽ khởi động với thông báo:
```
Đã tải [số lượng] luật từ file rule.json
Đã tải [số lượng] khái niệm từ file khainiem.json
Khởi động server Flask tại http://127.0.0.1:5000
```

## 💡 Hướng dẫn sử dụng

### A. Tra cứu vi phạm (Tab 1)

**Bước 1**: Mở tab **"🔍 Tra Cứu Vi Phạm"** (mặc định)

**Bước 2**: Chọn **Lỗi Vi Phạm** từ dropdown đầu tiên
- Ví dụ: "Lỗi vi phạm nồng độ cồn", "Lỗi không đội mũ bảo hiểm"...

**Bước 3**: Chọn **Phương Tiện** từ dropdown thứ hai (tự động cập nhật)
- Ví dụ: "xe máy", "ô tô", "xe đạp điện"...

**Bước 4**: Chọn **Chi Tiết Lỗi** từ dropdown thứ ba (tự động cập nhật)
- Ví dụ: "Nồng độ cồn từ 50-80 mg/100ml máu"

**Bước 5**: Xem kết quả tra cứu
- Mã luật, Mức phạt, Phạt bổ sung, Căn cứ pháp lý

**Bước 6**: Nhấn **"➕ Thêm vào Danh Sách"** (tùy chọn)
- Hệ thống tự động chuyển sang Tab "Danh Sách Vi Phạm"

### B. Tra cứu khái niệm (Tab 2)

**Bước 1**: Click tab **"📖 Tra Cứu Khái Niệm"**

**Bước 2**: Nhập từ khóa vào ô tìm kiếm
- Ví dụ: "xe máy", "đường bộ", "đèn đỏ", "làn đường"...

**Bước 3**: Chọn từ gợi ý autocomplete (tùy chọn)
- Hệ thống hiển thị danh sách gợi ý khi gõ

**Bước 4**: Nhấn **Enter** hoặc nút **"🔍 Tìm Kiếm"**

**Bước 5**: Xem kết quả
- Thuật ngữ chính thức với mã
- Định nghĩa chi tiết
- Căn cứ pháp lý
- Từ khóa liên quan

### C. Quản lý danh sách vi phạm (Tab 3)

**Bước 1**: Click tab **"📋 Danh Sách Vi Phạm"**
- Badge đỏ hiển thị số lượng vi phạm hiện có

**Bước 2**: Xem danh sách vi phạm
- Mỗi vi phạm có số thứ tự và đầy đủ thông tin

**Bước 3**: Xem tổng hợp
- Tổng số vi phạm
- Tổng mức phạt tiền (tự động tính)
- Hình phạt bổ sung cao nhất

**Bước 4**: Quản lý
- Xóa từng vi phạm: nút **✕** ở góc phải mỗi item
- Xóa tất cả: nút **"🗑️ Xóa Toàn Bộ Danh Sách"**
- Quay lại tra cứu: nút **"🔍 Quay Lại Tra Cứu"**

## 🔧 Chi tiết kỹ thuật

### Backend (app.py)

**Framework**: Flask 2.x

**Các route chính**:

| Route | Method | Mô tả |
|-------|--------|-------|
| `/` | GET | Trang chủ, render giao diện |
| `/filter_data` | POST | Xử lý logic Forward Chaining 3 cấp |
| `/search_concept` | POST | Tìm kiếm khái niệm theo từ khóa |
| `/get_all_concepts` | GET | Lấy danh sách thuật ngữ (autocomplete) |
| `/add_to_list` | POST | Thêm vi phạm vào session |
| `/get_violation_list` | GET | Lấy danh sách vi phạm và tính tổng |
| `/remove_from_list` | POST | Xóa vi phạm theo index |
| `/clear_list` | POST | Xóa toàn bộ danh sách |

**Session Management**:
- Sử dụng Flask session để lưu danh sách vi phạm
- Secret key ngẫu nhiên mỗi lần khởi động
- Dữ liệu tồn tại trong suốt phiên làm việc

**Thuật toán tính toán**:
- `determine_highest_penalty()`: Xác định hình phạt bổ sung cao nhất bằng regex
- Tính tổng mức phạt: Parse chuỗi tiền tệ, lấy trung bình khoảng

### Frontend (index.html)

**Công nghệ**:
- HTML5 semantic markup
- CSS3 với Flexbox/Grid
- Vanilla JavaScript (ES6+)
- Fetch API cho AJAX requests

**Giao diện**:
- Tab-based navigation (3 tabs)
- Badge notifications
- Responsive design
- Gradient backgrounds
- Smooth animations

**JavaScript features**:
- Dynamic form updates
- Autocomplete search
- Real-time calculation
- Session management
- Event delegation

## 📚 Cơ sở tri thức

### rule.json

**Cấu trúc dữ liệu**:
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

**Thuộc tính**:
- `id`: Mã định danh luật
- `loiViPham`: Loại lỗi vi phạm (Cấp 1)
- `phuongTien`: Loại phương tiện (Cấp 2)
- `chiTietLoi`: Chi tiết cụ thể (Cấp 3)
- `mucPhat`: Mức phạt tiền (chuỗi với khoảng)
- `phatBoSung`: Hình phạt bổ sung
- `canCuPhapLy`: Căn cứ pháp lý

### khainiem.json

**Cấu trúc dữ liệu**:
```json
{
  "tuDienKhaiNiem": [
    {
      "id": "C01",
      "thuatNgu": "Xe cơ giới",
      "dinhNghia": "Phương tiện giao thông đường bộ...",
      "canCuPhapLy": "Mục 3.13 QCVN 41:2024/BGTVT",
      "tuKhoa": ["xe cơ giới", "xe máy", "ô tô"]
    }
  ]
}
```

**Thuộc tính**:
- `id`: Mã định danh khái niệm
- `thuatNgu`: Thuật ngữ chính thức
- `dinhNghia`: Định nghĩa đầy đủ
- `canCuPhapLy`: Trích dẫn nguồn
- `tuKhoa`: Các từ khóa tìm kiếm

## 📡 API Endpoints

### POST /filter_data

**Mô tả**: Xử lý Forward Chaining 3 cấp độ

**Request Body**:
```json
{
  "loiViPham": "Lỗi vi phạm nồng độ cồn",
  "phuongTien": "xe máy",
  "chiTietLoi": "Nồng độ cồn từ 50-80 mg/100ml máu"
}
```

**Response (Cấp 1)**:
```json
{
  "success": true,
  "level": 1,
  "data": ["xe máy", "ô tô", "xe đạp điện"]
}
```

**Response (Cấp 3)**:
```json
{
  "success": true,
  "level": 3,
  "data": {
    "id": "L01",
    "loiViPham": "Lỗi vi phạm nồng độ cồn",
    "phuongTien": "xe máy",
    "chiTietLoi": "...",
    "mucPhat": "6.000.000 - 8.000.000 đồng",
    "phatBoSung": "Trừ 6 điểm GPLX",
    "canCuPhapLy": "..."
  }
}
```

### POST /search_concept

**Mô tả**: Tìm kiếm khái niệm theo từ khóa

**Request Body**:
```json
{
  "keyword": "xe máy"
}
```

**Response**:
```json
{
  "success": true,
  "results": [
    {
      "id": "C11",
      "thuatNgu": "Xe mô tô (xe máy)",
      "dinhNghia": "Xe cơ giới hai hoặc ba bánh...",
      "canCuPhapLy": "Mục 3.20 QCVN 41:2024/BGTVT",
      "tuKhoa": ["xe mô tô", "xe máy", "trên 50cm3"]
    }
  ],
  "count": 1
}
```

### GET /get_violation_list

**Mô tả**: Lấy danh sách vi phạm và tính tổng

**Response**:
```json
{
  "success": true,
  "violations": [...],
  "total_count": 3,
  "total_fine_min": 8100000,
  "total_fine_max": 10200000,
  "highest_supplementary_penalty": "Tước quyền sử dụng GPLX 10-12 tháng"
}
```

## 📊 Ví dụ sử dụng

### Tình huống 1: Tra cứu khái niệm "xe máy"

1. Click tab **"📖 Tra Cứu Khái Niệm"**
2. Nhập "xe máy"
3. Chọn từ gợi ý hoặc Enter
4. **Kết quả**:
   ```
   📚 Xe mô tô (xe máy) [C11]
   
   Định nghĩa: Xe cơ giới hai hoặc ba bánh và các loại xe tương tự, 
   có dung tích xi lanh từ 50 cm3 trở lên hoặc động cơ điện có công suất trên 4 kW.
   
   📖 Căn cứ pháp lý: Mục 3.20 QCVN 41:2024/BGTVT
   
   🏷️ Từ khóa: xe mô tô, xe máy, trên 50cm3
   ```

### Tình huống 2: Một người vi phạm nhiều lỗi

**Vi phạm thứ 1 - Nồng độ cồn**:
1. Tab "Tra Cứu Vi Phạm"
2. Chọn: "Lỗi vi phạm nồng độ cồn" > "xe máy" > "Mức 2 (50-80 mg)"
3. Kết quả: Phạt 6.000.000 - 8.000.000 đồng, Trừ 6 điểm GPLX
4. Nhấn "Thêm vào Danh Sách" → Tự động chuyển sang Tab 3

**Vi phạm thứ 2 - Không đội mũ**:
1. Quay lại Tab 1
2. Chọn: "Lỗi không đội mũ bảo hiểm" > "xe máy" > "Không đội mũ"
3. Kết quả: Phạt 100.000 - 200.000 đồng
4. Nhấn "Thêm vào Danh Sách"

**Vi phạm thứ 3 - Vượt tốc độ**:
1. Quay lại Tab 1
2. Chọn: "Lỗi về tốc độ" > "xe máy" > "Vượt 05-10 km/h"
3. Kết quả: Phạt 2.000.000 - 3.000.000 đồng
4. Nhấn "Thêm vào Danh Sách"

**Kết quả tổng hợp (Tab 3)**:
```
📋 Danh Sách Vi Phạm [Badge: 3]

1. Lỗi vi phạm nồng độ cồn (xe máy)
   Phạt: 6.000.000 - 8.000.000 đồng
   Phạt bổ sung: Trừ 6 điểm GPLX

2. Lỗi không đội mũ bảo hiểm (xe máy)
   Phạt: 100.000 - 200.000 đồng

3. Lỗi về tốc độ (xe máy)
   Phạt: 2.000.000 - 3.000.000 đồng

━━━━━━━━━━━━━━━━━━━━━━
📊 TỔNG HỢP:
- Tổng số vi phạm: 3
- Tổng mức phạt: 8.100.000 - 11.200.000 đồng
  (Ước tính: ~9.650.000 đồng)
- Phạt bổ sung cao nhất: Trừ 6 điểm GPLX
```

## 🎓 Ý nghĩa đồ án

### 1. Mô phỏng Hệ Cơ Sở Tri Thức (KBS)

Đây là một **Knowledge-Based System** hoàn chỉnh với các thành phần:
- **Knowledge Base**: rule.json, khainiem.json (Cơ sở tri thức)
- **Inference Engine**: Bộ suy diễn Forward Chaining trong app.py
- **User Interface**: Giao diện web tương tác 3 tabs
- **Working Memory**: Flask session lưu trữ trạng thái

### 2. Forward Chaining (Suy diễn Tiến)

**Cấp 1** (Lỗi vi phạm → Phương tiện):
```
IF user chọn loiViPham
THEN hệ thống lọc và trả về danh sách phuongTien
```

**Cấp 2** (Phương tiện → Chi tiết lỗi):
```
IF user đã chọn loiViPham AND phuongTien
THEN hệ thống lọc và trả về danh sách chiTietLoi
```

**Cấp 3** (Chi tiết lỗi → Kết luận):
```
IF user đã chọn loiViPham AND phuongTien AND chiTietLoi
THEN hệ thống trả về thông tin xử phạt (mucPhat, phatBoSung, canCuPhapLy)
```

### 3. Ứng dụng thực tế

- **Lĩnh vực**: Luật giao thông Việt Nam
- **Nguồn**: Nghị định 168/2024/NĐ-CP, QCVN 41:2024/BGTVT
- **Mục đích**: Hỗ trợ tra cứu nhanh mức phạt vi phạm giao thông
- **Người dùng**: Người dân, CSGT, luật sư, học sinh/sinh viên

### 4. Kỹ thuật nổi bật

✅ **Forward Chaining 3 cấp** - Suy diễn logic từ dữ liệu đến kết luận  
✅ **Structured Look-up** - Tìm kiếm có cấu trúc, không brute-force  
✅ **Full-text Search** - Tìm kiếm linh hoạt trong định nghĩa khái niệm  
✅ **Pattern Matching** - Regex để parse và phân tích dữ liệu  
✅ **Session Management** - Quản lý trạng thái người dùng  
✅ **RESTful API** - Thiết kế endpoint chuẩn REST  
✅ **Responsive UI** - Giao diện thân thiện, hoạt động mượt  

## 📝 Lưu ý và hạn chế

### Lưu ý:

- Dữ liệu được lưu trong **Flask session**, không lưu vào database
- Khi đóng trình duyệt hoặc xóa cookie, danh sách vi phạm sẽ mất
- Secret key được tạo ngẫu nhiên mỗi lần khởi động server
- Debug mode được bật - không dùng cho production

### Hạn chế:

- Dữ liệu trong `rule.json` là demo, không đầy đủ tất cả luật
- Không có xác thực người dùng (authentication)
- Không có phân quyền (authorization)
- Không lưu trữ lâu dài (persistent storage)
- Không có tính năng xuất báo cáo (PDF, Excel)

### Mở rộng trong tương lai:

- Tích hợp database (SQLite, PostgreSQL)
- Thêm tính năng đăng nhập/đăng ký
- Xuất báo cáo PDF/Excel
- Thêm biểu đồ thống kê
- API cho mobile app
- Tích hợp thanh toán phạt online
- Thêm nhiều luật hơn từ nguồn chính thức

## 🛠️ Yêu cầu phát triển

```bash
# Cài đặt môi trường ảo (khuyến nghị)
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# Cài đặt dependencies
pip install flask

# Chạy với hot-reload
python app.py

# Truy cập
http://127.0.0.1:5000
```

## 👨‍💻 Tác giả

**Đồ án môn học**: Hệ Cơ Sở Tri Thức (CS217)  
**Năm học**: 2024-2025  
**Mô hình**: Forward Chaining + Knowledge Base System  

---

**© 2025 - Hệ Tra Cứu Luật Giao Thông Việt Nam**
