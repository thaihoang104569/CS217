"""
Ứng dụng Web Demo - Hệ Cơ Sở Tri Thức Tra Cứu Luật Giao Thông
Sử dụng Forward Chaining với Structured Look-up 3 cấp độ
"""

from flask import Flask, render_template, request, jsonify, session
import json
import secrets

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)

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

def load_concepts():
    """Tải dữ liệu khái niệm từ file khainiem.json"""
    try:
        with open('khainiem.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
            return data.get('tuDienKhaiNiem', [])
    except FileNotFoundError:
        print("Lỗi: Không tìm thấy file khainiem.json")
        return []
    except json.JSONDecodeError:
        print("Lỗi: File khainiem.json không đúng định dạng JSON")
        return []

def determine_highest_penalty(penalties):
    """
    Xác định hình phạt bổ sung cao nhất
    Ước lượng dựa vào số điểm GPLX bị trừ và thời gian tước quyền sử dụng
    """
    if not penalties:
        return 'Không có'
    
    import re
    
    # Thứ tự ưu tiên: Tước quyền > Trừ điểm
    max_revocation_months = 0
    max_deducted_points = 0
    revocation_penalty = None
    points_penalty = None
    
    for penalty in penalties:
        penalty_lower = penalty.lower()
        
        # Kiểm tra tước quyền sử dụng GPLX
        if 'tước quyền' in penalty_lower:
            # Tìm số tháng
            months = re.findall(r'(\d+)\s*[\u2013\-]\s*(\d+)\s*tháng', penalty)
            if months:
                max_months = int(months[0][1])  # Lấy giá trị cao nhất
                if max_months > max_revocation_months:
                    max_revocation_months = max_months
                    revocation_penalty = penalty
        
        # Kiểm tra trừ điểm GPLX
        elif 'trừ' in penalty_lower and 'điểm' in penalty_lower:
            # Tìm số điểm
            points = re.findall(r'trừ\s*(\d+)\s*điểm', penalty_lower)
            if points:
                deducted_points = int(points[0])
                if deducted_points > max_deducted_points:
                    max_deducted_points = deducted_points
                    points_penalty = penalty
    
    # Trả về phạt bổ sung cao nhất
    if revocation_penalty:
        return revocation_penalty
    elif points_penalty:
        return points_penalty
    else:
        # Trả về phạt bổ sung đầu tiên nếu không phân loại được
        return penalties[0]

# Biến toàn cục lưu trữ dữ liệu
rules_data = load_rules()
concepts_data = load_concepts()

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

@app.route('/add_to_list', methods=['POST'])
def add_to_list():
    """Thêm vi phạm vào danh sách"""
    try:
        violation = request.json
        
        # Khởi tạo danh sách nếu chưa có
        if 'violation_list' not in session:
            session['violation_list'] = []
        
        # Thêm vi phạm vào danh sách
        session['violation_list'].append(violation)
        session.modified = True
        
        return jsonify({
            'success': True,
            'message': 'Đã thêm vi phạm vào danh sách',
            'total_count': len(session['violation_list'])
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Lỗi: {str(e)}'
        })

@app.route('/get_violation_list', methods=['GET'])
def get_violation_list():
    """Lấy danh sách vi phạm và tính tổng mức phạt"""
    try:
        violation_list = session.get('violation_list', [])
        
        # Tính tổng mức phạt dạng khoảng
        import re
        total_min = 0
        total_max = 0
        
        # Thu thập phạt bổ sung để tổng hợp
        supplementary_penalties = []

        # Tổng hợp điểm trừ + tước quyền sử dụng GPLX (nếu có)
        total_deducted_points = 0
        highest_revocation_penalty = None
        highest_revocation_months = 0
        
        for violation in violation_list:
            muc_phat = violation.get('mucPhat', '0')
            # Trích xuất số tiền từ chuỗi (ví dụ: "2.000.000 – 3.000.000 đồng")
            numbers = re.findall(r'[\d.]+', muc_phat.replace('.', ''))
            
            if numbers:
                if len(numbers) >= 2:
                    # Có khoảng: lấy min và max
                    total_min += int(numbers[0])
                    total_max += int(numbers[1])
                else:
                    # Chỉ có 1 số: cộng vào cả min và max
                    total_min += int(numbers[0])
                    total_max += int(numbers[0])
            
            # Thu thập phạt bổ sung
            phat_bo_sung = violation.get('phatBoSung', '')
            if phat_bo_sung and phat_bo_sung != 'Không có':
                supplementary_penalties.append(phat_bo_sung)

                phat_bo_sung_lower = phat_bo_sung.lower()

                # Cộng tổng điểm trừ (nếu có)
                deducted_points_matches = re.findall(r'trừ\s*(\d+)\s*điểm', phat_bo_sung_lower)
                if deducted_points_matches:
                    total_deducted_points += sum(int(p) for p in deducted_points_matches)

                # Lấy mức tước quyền sử dụng GPLX cao nhất (nếu có)
                if 'tước' in phat_bo_sung_lower and ('gplx' in phat_bo_sung_lower or 'giấy phép' in phat_bo_sung_lower):
                    # Ưu tiên dạng khoảng "từ A – B tháng"
                    months_range = re.findall(r'(\d+)\s*[\u2013\-]\s*(\d+)\s*tháng', phat_bo_sung)
                    if months_range:
                        max_months = max(int(b) for (_, b) in months_range)
                        if max_months > highest_revocation_months:
                            highest_revocation_months = max_months
                            highest_revocation_penalty = phat_bo_sung
                    else:
                        # Dạng 1 số "X tháng"
                        months_single = re.findall(r'(\d+)\s*tháng', phat_bo_sung)
                        if months_single:
                            max_months = max(int(m) for m in months_single)
                            if max_months > highest_revocation_months:
                                highest_revocation_months = max_months
                                highest_revocation_penalty = phat_bo_sung
        
        # Xác định phạt bổ sung cao nhất
        highest_penalty = determine_highest_penalty(supplementary_penalties)
        
        return jsonify({
            'success': True,
            'violations': violation_list,
            'total_count': len(violation_list),
            'total_fine_min': total_min,
            'total_fine_max': total_max,
            # Backward compatible (đang dùng ở UI cũ)
            'highest_supplementary_penalty': highest_penalty,
            # UI tổng hợp mới
            'total_deducted_points': total_deducted_points,
            'revocation_penalty': highest_revocation_penalty or 'Không có'
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Lỗi: {str(e)}'
        })

@app.route('/remove_from_list', methods=['POST'])
def remove_from_list():
    """Xóa vi phạm khỏi danh sách theo index"""
    try:
        index = request.json.get('index')
        
        if 'violation_list' in session and 0 <= index < len(session['violation_list']):
            removed = session['violation_list'].pop(index)
            session.modified = True
            
            return jsonify({
                'success': True,
                'message': 'Đã xóa vi phạm khỏi danh sách',
                'removed': removed
            })
        else:
            return jsonify({
                'success': False,
                'message': 'Index không hợp lệ'
            })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Lỗi: {str(e)}'
        })

@app.route('/clear_list', methods=['POST'])
def clear_list():
    """Xóa toàn bộ danh sách vi phạm"""
    try:
        session['violation_list'] = []
        session.modified = True
        
        return jsonify({
            'success': True,
            'message': 'Đã xóa toàn bộ danh sách'
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Lỗi: {str(e)}'
        })

@app.route('/search_concept', methods=['POST'])
def search_concept():
    """Tìm kiếm khái niệm theo từ khóa"""
    try:
        keyword = request.json.get('keyword', '').lower().strip()
        
        if not keyword:
            return jsonify({
                'success': False,
                'message': 'Vui lòng nhập từ khóa tìm kiếm'
            })
        
        # Tìm kiếm trong dữ liệu khái niệm
        results = []
        for concept in concepts_data:
            # Tìm trong thuật ngữ
            if keyword in concept['thuatNgu'].lower():
                results.append(concept)
                continue
            
            # Tìm trong định nghĩa
            if keyword in concept['dinhNghia'].lower():
                results.append(concept)
                continue
            
            # Tìm trong từ khóa
            if 'tuKhoa' in concept:
                for tk in concept['tuKhoa']:
                    if keyword in tk.lower():
                        results.append(concept)
                        break
        
        if results:
            return jsonify({
                'success': True,
                'results': results,
                'count': len(results)
            })
        else:
            return jsonify({
                'success': False,
                'message': f'Không tìm thấy khái niệm nào với từ khóa "{keyword}"'
            })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Lỗi: {str(e)}'
        })

@app.route('/get_all_concepts', methods=['GET'])
def get_all_concepts():
    """Lấy danh sách tất cả khái niệm (cho autocomplete)"""
    try:
        # Lấy danh sách thuật ngữ và từ khóa
        terms = []
        for concept in concepts_data:
            terms.append(concept['thuatNgu'])
            if 'tuKhoa' in concept:
                terms.extend(concept['tuKhoa'])
        
        # Loại bỏ trùng lặp và sắp xếp
        unique_terms = sorted(list(set(terms)))
        
        return jsonify({
            'success': True,
            'terms': unique_terms
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Lỗi: {str(e)}'
        })

if __name__ == '__main__':
    print(f"Đã tải {len(rules_data)} luật từ file rule.json")
    print(f"Đã tải {len(concepts_data)} khái niệm từ file khainiem.json")
    print("Khởi động server Flask tại http://127.0.0.1:5000")
    app.run(debug=True, host='127.0.0.1', port=5000)
