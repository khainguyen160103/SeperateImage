import os
import json
import re
import shutil

def rename_images_with_json(images_folder, json_file):
    """Đổi tên file ảnh dựa trên dữ liệu JSON"""
    
    # Đọc dữ liệu JSON
    try:
        with open(json_file, 'r', encoding='utf-8') as f:
            json_data = json.load(f)
        print(f"📋 Đã đọc {len(json_data)} entries từ JSON")
    except Exception as e:
        print(f"❌ Lỗi đọc file JSON: {e}")
        return
    
    # Tạo mapping từ JSON
    mapping = {}
    for item in json_data:
        filename = item['filename']
        
        # Extract key từ filename JSON (Bài X.Y, Hình X.Y, etc.)
        bai_match = re.search(r'Bài (\d+\.\d+)', filename)
        hinh_match = re.search(r'Hình (\d+\.\d+)', filename)
        
        if bai_match:
            key = f"Bài {bai_match.group(1)}"
            mapping[key] = filename + ".jpg"  # Thêm extension
        elif hinh_match:
            key = f"Hình {hinh_match.group(1)}"
            mapping[key] = filename + ".jpg"  # Thêm extension
        else:
            # Các trường hợp khác như "KIẾN THỨC CẦN NHỚ", "SƠ ĐỒ TỔNG KẾT"
            special_patterns = [
                r'KIẾN THỨC CẦN NHỚ',
                r'SƠ ĐỒ TỔNG KẾT CHƯƠNG [IVX]+',
                r'Lời giải Bài \d+\.\d+',
                r'Bìa sách'
            ]
            
            for pattern in special_patterns:
                if re.search(pattern, filename):
                    # Lấy phần pattern làm key
                    match = re.search(pattern, filename)
                    if match:
                        key = match.group(0)
                        if key not in mapping:  # Chỉ lấy cái đầu tiên
                            mapping[key] = filename + ".jpg"
                        break
    
    print(f"🗂️  Tạo được {len(mapping)} mapping keys")
    
    # Lấy danh sách file ảnh hiện tại
    image_files = []
    for filename in os.listdir(images_folder):
        if filename.endswith(('.jpg', '.jpeg', '.png')):
            image_files.append(filename)
    
    print(f"📁 Tìm thấy {len(image_files)} file ảnh")
    
    # Đổi tên file
    renamed_count = 0
    not_found_count = 0
    
    for old_filename in image_files:
        old_path = os.path.join(images_folder, old_filename)
        
        # Extract key từ tên file ảnh hiện tại
        found_key = None
        new_filename = None
        
        # Tìm Bài X.Y
        bai_match = re.search(r'Bài (\d+\.\d+)', old_filename)
        if bai_match:
            found_key = f"Bài {bai_match.group(1)}"
        
        # Tìm Hình X.Y
        if not found_key:
            hinh_match = re.search(r'Hình (\d+\.\d+)', old_filename)
            if hinh_match:
                found_key = f"Hình {hinh_match.group(1)}"
        
        # Tìm các pattern đặc biệt
        if not found_key:
            special_patterns = [
                r'KIẾN THỨC CẦN NHỚ',
                r'A\. KIẾN THỨC CẦN NHỚ',  # Thêm pattern này
                r'SƠ ĐỒ TỔNG KẾT CHƯƠNG [IVX]+',
                r'Lời giải Bài \d+\.\d+',
                r'Bìa sách'
            ]
            
            for pattern in special_patterns:
                match = re.search(pattern, old_filename)
                if match:
                    found_key = match.group(0)
                    # Normalize key
                    if found_key == "A. KIẾN THỨC CẦN NHỚ":
                        found_key = "KIẾN THỨC CẦN NHỚ"
                    break
        
        # Tìm mapping
        if found_key and found_key in mapping:
            new_filename = mapping[found_key]
            
            # Đảm bảo extension đúng
            old_ext = os.path.splitext(old_filename)[1]
            new_filename = os.path.splitext(new_filename)[0] + old_ext
            
            new_path = os.path.join(images_folder, new_filename)
            
            # Đổi tên file
            try:
                if old_path != new_path:  # Tránh đổi tên file giống nhau
                    os.rename(old_path, new_path)
                    print(f"✅ {old_filename}")
                    print(f"   → {new_filename}")
                    renamed_count += 1
                else:
                    print(f"⚠️  {old_filename} (đã đúng tên)")
            except Exception as e:
                print(f"❌ Lỗi đổi tên {old_filename}: {e}")
        else:
            print(f"❓ Không tìm thấy mapping cho: {old_filename}")
            if found_key:
                print(f"   Key tìm được: '{found_key}'")
            not_found_count += 1
    
    # Báo cáo kết quả
    print("\n" + "="*60)
    print(f"🎉 KẾT QUẢ:")
    print(f"   ✅ Đã đổi tên: {renamed_count} file")
    print(f"   ❓ Không tìm thấy: {not_found_count} file")
    print(f"   📊 Tổng cộng: {len(image_files)} file")
    print("="*60)

def preview_rename_mapping(images_folder, json_file):
    """Xem trước việc đổi tên mà không thực hiện"""
    
    # Đọc dữ liệu JSON
    try:
        with open(json_file, 'r', encoding='utf-8') as f:
            json_data = json.load(f)
        print(f"📋 Đã đọc {len(json_data)} entries từ JSON")
    except Exception as e:
        print(f"❌ Lỗi đọc file JSON: {e}")
        return
    
    # Tạo mapping từ JSON
    mapping = {}
    for item in json_data:
        filename = item['filename']
        
        # Extract key từ filename JSON
        bai_match = re.search(r'Bài (\d+\.\d+)', filename)
        hinh_match = re.search(r'Hình (\d+\.\d+)', filename)
        
        if bai_match:
            key = f"Bài {bai_match.group(1)}"
            mapping[key] = filename + ".jpg"
        elif hinh_match:
            key = f"Hình {hinh_match.group(1)}"
            mapping[key] = filename + ".jpg"
        else:
            # Các trường hợp khác
            special_patterns = [
                r'KIẾN THỨC CẦN NHỚ',
                r'SƠ ĐỒ TỔNG KẾT CHƯƠNG [IVX]+',
                r'Lời giải Bài \d+\.\d+',
                r'Bìa sách'
            ]
            
            for pattern in special_patterns:
                if re.search(pattern, filename):
                    match = re.search(pattern, filename)
                    if match:
                        key = match.group(0)
                        if key not in mapping:
                            mapping[key] = filename + ".jpg"
                        break
    
    # Lấy danh sách file ảnh hiện tại
    image_files = []
    for filename in os.listdir(images_folder):
        if filename.endswith(('.jpg', '.jpeg', '.png')):
            image_files.append(filename)
    
    print(f"📁 Tìm thấy {len(image_files)} file ảnh")
    print("\n🔍 XEM TRƯỚC VIỆC ĐỔI TÊN:")
    print("="*80)
    
    # Preview đổi tên
    will_rename = 0
    not_found = 0
    
    for old_filename in image_files:
        # Extract key từ tên file ảnh hiện tại
        found_key = None
        
        # Tìm Bài X.Y
        bai_match = re.search(r'Bài (\d+\.\d+)', old_filename)
        if bai_match:
            found_key = f"Bài {bai_match.group(1)}"
        
        # Tìm Hình X.Y
        if not found_key:
            hinh_match = re.search(r'Hình (\d+\.\d+)', old_filename)
            if hinh_match:
                found_key = f"Hình {hinh_match.group(1)}"
        
        # Tìm các pattern đặc biệt
        if not found_key:
            special_patterns = [
                r'KIẾN THỨC CẦN NHỚ',
                r'A\. KIẾN THỨC CẦN NHỚ',
                r'SƠ ĐỒ TỔNG KẾT CHƯƠNG [IVX]+',
                r'Lời giải Bài \d+\.\d+',
                r'Bìa sách'
            ]
            
            for pattern in special_patterns:
                match = re.search(pattern, old_filename)
                if match:
                    found_key = match.group(0)
                    if found_key == "A. KIẾN THỨC CẦN NHỚ":
                        found_key = "KIẾN THỨC CẦN NHỚ"
                    break
        
        # Kiểm tra mapping
        if found_key and found_key in mapping:
            new_filename = mapping[found_key]
            old_ext = os.path.splitext(old_filename)[1]
            new_filename = os.path.splitext(new_filename)[0] + old_ext
            
            print(f"✅ {old_filename}")
            print(f"   → {new_filename}")
            print(f"   🔑 Key: '{found_key}'")
            print()
            will_rename += 1
        else:
            print(f"❓ {old_filename}")
            if found_key:
                print(f"   🔑 Key tìm được: '{found_key}' (không có trong mapping)")
            else:
                print(f"   ❌ Không extract được key")
            print()
            not_found += 1
    
    print("="*80)
    print(f"📊 TỔNG KẾT PREVIEW:")
    print(f"   ✅ Sẽ đổi tên: {will_rename} file")
    print(f"   ❓ Không tìm thấy: {not_found} file")
    print(f"   📁 Tổng cộng: {len(image_files)} file")
    print("="*80)

def main():
    """Hàm main"""
    
    print("🎯 CHƯƠNG TRÌNH ĐỔI TÊN FILE ẢNH THEO JSON")
    print("="*50)
    
    # Đường dẫn mặc định
    images_folder = r"e:\Data\Work\SeperateImage\images"
    json_file = r"e:\Data\Work\SeperateImage\code.json"
    
    # Kiểm tra đường dẫn
    if not os.path.exists(images_folder):
        print(f"❌ Thư mục ảnh không tồn tại: {images_folder}")
        return
    
    if not os.path.exists(json_file):
        print(f"❌ File JSON không tồn tại: {json_file}")
        return
    
    print(f"📁 Thư mục ảnh: {images_folder}")
    print(f"📋 File JSON: {json_file}")
    
    # Menu
    print("\n🎯 CHỌN CHỨC NĂNG:")
    print("1. Xem trước việc đổi tên")
    print("2. Đổi tên ngay")
    print("3. Xem trước rồi quyết định")
    
    choice = input("Chọn (1-3): ").strip()
    
    if choice == "1":
        preview_rename_mapping(images_folder, json_file)
        
    elif choice == "2":
        rename_images_with_json(images_folder, json_file)
        
    elif choice == "3":
        preview_rename_mapping(images_folder, json_file)
        confirm = input("\n❓ Tiếp tục đổi tên? (y/n): ").strip().lower()
        if confirm == 'y':
            rename_images_with_json(images_folder, json_file)
        else:
            print("✋ Hủy đổi tên.")
    else:
        print("❌ Lựa chọn không hợp lệ!")

if __name__ == "__main__":
    main()