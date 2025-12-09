"""
Ứng dụng Web Demo - Hệ Cơ Sở Tri Thức Tra Cứu Luật Giao Thông
Sử dụng Forward Chaining với Structured Look-up 3 cấp độ
"""

from flask import Flask, render_template, request, jsonify
import json

app = Flask(__name__)

# Tải dữ liệu từ file rule.json vào bộ nhớ
def load_rules():
    """Tải toàn bộ dữ liệu từ file rule.json"""
    try:
        with open('rule.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
            return data.get('trafficViolations', [])
    except FileNotFoundError:
        print("Lỗi: Không tìm thấy file rule.json")
        return []
    except json.JSONDecodeError:
        print("Lỗi: File rule.json không đúng định dạng JSON")
        return []

# Biến toàn cục lưu trữ dữ liệu
rules_data = load_rules()

@app.route('/')
def index():
    """
    Router chính - Trả về trang index.html
    Lấy danh sách các loiViPham duy nhất cho dropdown đầu tiên
    """
    # Lấy danh sách lỗi vi phạm duy nhất (Cấp 1)
    loi_vi_pham_list = sorted(list(set(rule['loiViPham'] for rule in rules_data)))
    
    return render_template('index.html', loi_vi_pham_list=loi_vi_pham_list)

@app.route('/filter_data', methods=['POST'])
def filter_data():
    """
    Endpoint AJAX - Xử lý lọc dữ liệu theo 3 cấp độ (Forward Chaining)
    
    Trường hợp 1 (Cấp 1): Chỉ nhận loiViPham → Trả về danh sách phuongTien
    Trường hợp 2 (Cấp 2): Nhận loiViPham + phuongTien → Trả về danh sách chiTietLoi
    Trường hợp 3 (Cấp 3): Nhận đủ 3 tham số → Trả về thông tin xử phạt chi tiết
    """
    try:
        # Lấy tham số từ request
        loi_vi_pham = request.json.get('loiViPham', None)
        phuong_tien = request.json.get('phuongTien', None)
        chi_tiet_loi = request.json.get('chiTietLoi', None)
        
        # --- TRƯỜNG HỢP 1: Chỉ có loiViPham (Cấp 1) ---
        if loi_vi_pham and not phuong_tien and not chi_tiet_loi:
            # Lọc các rule khớp với loiViPham
            filtered_rules = [rule for rule in rules_data if rule['loiViPham'] == loi_vi_pham]
            
            # Lấy danh sách phuongTien duy nhất
            phuong_tien_list = sorted(list(set(rule['phuongTien'] for rule in filtered_rules)))
            
            return jsonify({
                'success': True,
                'level': 1,
                'data': phuong_tien_list
            })
        
        # --- TRƯỜNG HỢP 2: Có loiViPham + phuongTien (Cấp 2) ---
        elif loi_vi_pham and phuong_tien and not chi_tiet_loi:
            # Lọc các rule khớp với cả loiViPham và phuongTien
            filtered_rules = [
                rule for rule in rules_data 
                if rule['loiViPham'] == loi_vi_pham and rule['phuongTien'] == phuong_tien
            ]
            
            # Lấy danh sách chiTietLoi duy nhất
            chi_tiet_loi_list = sorted(list(set(rule['chiTietLoi'] for rule in filtered_rules)))
            
            return jsonify({
                'success': True,
                'level': 2,
                'data': chi_tiet_loi_list
            })
        
        # --- TRƯỜNG HỢP 3: Có đủ 3 tham số (Cấp 3 - Truy vấn cuối) ---
        elif loi_vi_pham and phuong_tien and chi_tiet_loi:
            # Tìm rule khớp chính xác với cả 3 điều kiện
            matched_rule = None
            for rule in rules_data:
                if (rule['loiViPham'] == loi_vi_pham and 
                    rule['phuongTien'] == phuong_tien and 
                    rule['chiTietLoi'] == chi_tiet_loi):
                    matched_rule = rule
                    break
            
            if matched_rule:
                # Trả về toàn bộ thông tin xử phạt
                return jsonify({
                    'success': True,
                    'level': 3,
                    'data': {
                        'id': matched_rule.get('id', 'N/A'),
                        'loiViPham': matched_rule['loiViPham'],
                        'phuongTien': matched_rule['phuongTien'],
                        'chiTietLoi': matched_rule['chiTietLoi'],
                        'mucPhat': matched_rule.get('mucPhat', 'Không có thông tin'),
                        'phatBoSung': matched_rule.get('phatBoSung', 'Không có'),
                        'canCuPhapLy': matched_rule.get('canCuPhapLy', 'Không có')
                    }
                })
            else:
                return jsonify({
                    'success': False,
                    'message': 'Không tìm thấy luật phù hợp'
                })
        
        # Trường hợp không hợp lệ
        else:
            return jsonify({
                'success': False,
                'message': 'Tham số không hợp lệ'
            })
            
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Lỗi xử lý: {str(e)}'
        })

if __name__ == '__main__':
    print(f"Đã tải {len(rules_data)} luật từ file rule.json")
    print("Khởi động server Flask tại http://127.0.0.1:5000")
    app.run(debug=True, host='127.0.0.1', port=5000)
