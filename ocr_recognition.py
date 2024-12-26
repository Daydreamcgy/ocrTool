import os
import requests
import base64

API_KEY = "iwmgR5NI8z2p4VavYiVbqHrf"
SECRET_KEY = "QCT3c6Hkq7AP3FuOEGtN5og3p6RONfCa"

def get_access_token():
    url = "https://aip.baidubce.com/oauth/2.0/token"
    params = {"grant_type": "client_credentials", "client_id": API_KEY, "client_secret": SECRET_KEY}
    response = requests.post(url, params=params)
    if response.status_code == 200:
        return response.json().get("access_token")
    else:
        print(f"获取 access_token 失败，状态码：{response.status_code}")
        return None

def ocr_recognition(image_path):
    access_token = get_access_token()
    if not access_token:
        print("无法获取 access_token")
        return None

    url = "https://aip.baidubce.com/rest/2.0/ocr/v1/accurate?access_token=" + access_token
    
    with open(image_path, 'rb') as f:
        img = base64.b64encode(f.read())
    
    payload = {
        'image': img,
        'language_type': 'JAP',  # 添加语言类型参数，支持日语
        'detect_direction': 'false',
        'vertexes_location': 'false',
        'paragraph': 'false',
        'probability': 'false',
        'char_probability': 'false',
        'multidirectional_recognize': 'false'
    }
    
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Accept': 'application/json'
    }
    
    response = requests.post(url, headers=headers, data=payload)
    
    if response.status_code == 200:
        result = response.json()
        if 'words_result' in result:
            text = "\n".join([item['words'] for item in result['words_result']])
            return text
        else:
            print("OCR识别失败，返回结果中没有 'words_result'")
            print(result)
            return None
    else:
        print(f"请求失败，状态码：{response.status_code}")
        print(response.text)
        return None

def main():
    latest_image = get_latest_image('pix')
    if latest_image:
        print(f"识别文件: {latest_image}")
        ocr_result = ocr_recognition(latest_image)
        if ocr_result:
            print(ocr_result)
    else:
        print("没有找到图片文件")

def get_latest_image(directory):
    files = [os.path.join(directory, f) for f in os.listdir(directory) if f.endswith('.png')]
    if not files:
        return None
    latest_file = max(files, key=os.path.getctime)
    return latest_file

if __name__ == "__main__":
    main()