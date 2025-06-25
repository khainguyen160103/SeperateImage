import requests 
import base64 
import os 
import json 
import time
from dotenv import load_dotenv

load_dotenv()

app_key = os.getenv('APP_KEY')
app_id = os.getenv('APP_ID')

def send_pdf_to_mathpix(file_path):
    """Gửi PDF đến Mathpix API để convert"""
    print(f"🚀 Bắt đầu gửi PDF: {os.path.basename(file_path)}")
    
    if not app_key or not app_id:
        print("❌ APP_KEY hoặc APP_ID chưa được thiết lập!")
        return None
       
    with open(file_path , 'rb') as f: 
        try:
            print("📤 Đang gửi request đến Mathpix...")
            response = requests.post("https://api.mathpix.com/v3/pdf", 
                                headers= { 
                                    "app_id" : app_id,
                                    "app_key": app_key
                                },
                                files={'file': f} , 
                                data= {"conversion_formats[docx]" : "true"}
            )
            
            if response.status_code == 200:
                result = response.json()
                print(result)
                print("✅ Gửi thành công!")
                return result
            else:
                print(f"❌ Lỗi API: {response.status_code} - {response.text}")
                return None
        except Exception as e:
            print(f"❌ Lỗi: {e}")
            return None

def check_conversion_status(pdf_id):
    """Kiểm tra trạng thái conversion"""
    headers = {'app_key': app_key, 'app_id': app_id}
    
    try:
        url = f"https://api.mathpix.com/v3/pdf/{pdf_id}"
        response = requests.get(url, headers=headers)
        
        if response.status_code == 200:
            result = response.json()
            return result
        else:
            print(f"❌ Lỗi check status: {response.status_code}")
            return None
    except Exception as e:
        print(f"❌ Lỗi check status: {e}")
        return None

def download_docx(pdf_id, output_path):
    """Download file DOCX đã convert"""
    headers = {'app_key': app_key, 'app_id': app_id}
    
    try:
        url = f"https://api.mathpix.com/v3/pdf/{pdf_id}.docx"
        response = requests.get(url, headers=headers)
        
        if response.status_code == 200:
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            
            with open(output_path, 'wb') as f:
                f.write(response.content)
            
            print(f"✅ Downloaded: {output_path}")
            return output_path
        else:
            print(f"❌ Lỗi download: {response.status_code}")
            return None
    except Exception as e:
        print(f"❌ Lỗi download: {e}")
        return None

def wait_for_conversion(pdf_id, max_wait_time=300):
    """Chờ conversion hoàn thành"""
    print(f"⏳ Chờ conversion hoàn thành...")
    start_time = time.time()
    
    while time.time() - start_time < max_wait_time:
        status_result = check_conversion_status(pdf_id)
        
        if not status_result:
            return False
        
        status = status_result.get('status', 'unknown')
        print(f"📋 Status: {status}")
        
        if status == 'completed':
            print("✅ Conversion hoàn thành!")
            return True
        elif status == 'error':
            print(f"❌ Conversion lỗi: {status_result.get('error', 'Unknown')}")
            return False
        
        time.sleep(10)
    
    print("⏰ Timeout!")
    return False

def convert_pdf_to_docx(pdf_path, output_path=None):
    """Convert PDF to DOCX"""
    print("🎯 Bắt đầu convert PDF to DOCX")
    
    if not os.path.exists(pdf_path):
        print(f"❌ File không tồn tại: {pdf_path}")
        return None
    
    # Gửi PDF
    result = send_pdf_to_mathpix(pdf_path)
    if not result:
        return None
    
    pdf_id = result.get('pdf_id')
    if not pdf_id:
        print("❌ Không nhận được pdf_id")
        return None
    
    print(f"📋 PDF ID: {pdf_id}")
    
    # Chờ conversion
    if not wait_for_conversion(pdf_id):
        return None
    
    # Tạo output path
    if not output_path:
        pdf_name = os.path.splitext(os.path.basename(pdf_path))[0]
        output_path = f"output/{pdf_name}_converted.docx"
    
    # Download
    downloaded_file = download_docx(pdf_id, output_path)
    
    if downloaded_file:
        print(f"🎉 Hoàn thành! File DOCX: {downloaded_file}")
        return downloaded_file
    else:
        return None

# THỰC HIỆN CONVERT NGAY
if __name__ == "__main__": 
    # Đặt đường dẫn PDF của bạn ở đây
    pdf_path = r"E:\Data\Work\SeperateImage\Unlock_SBT\SBT Toan 6 tap 1 ruot(TB2025)_KNTT (14.3.2025) (1).pdf"
    
    print(f"🔑 App ID: {app_id[:10]}..." if app_id else "❌ APP_ID not found")
    print(f"🔑 App Key: {app_key[:10]}..." if app_key else "❌ APP_KEY not found")
    print()
    
    # CONVERT NGAY
    result = convert_pdf_to_docx(pdf_path)
    
    if result:
        print(f"\n✅ SUCCESS! File đã convert: {result}")
    else:
        print(f"\n❌ FAILED! Không thể convert file")