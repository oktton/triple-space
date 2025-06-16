from urllib.parse import urljoin
import httpx
import logging
from loading import LoadingPopup
import os

log_path = os.path.join(os.path.dirname(__file__), 'agent.log')
logging.basicConfig(
    filename=log_path,
    level=logging.ERROR,
    format='%(asctime)s - %(levelname)s - %(message)s',
)

class TextTransformer:
    def __init__(self, transform_type: str, target_language: str, api_url: str):
        self.api_url = api_url
        self.transform_type = transform_type
        self.target_language = target_language
    
    def transform(self, text) -> str:
        endpoints = {
            "translate": {"path": "/translate", "data": {"text": text, "target_language": self.target_language}},
            "polish": {"path": "/polish", "data": {"text": text}}
        }
        
        if self.transform_type not in endpoints:
            raise ValueError(f"Unsupported transform_type: {self.transform_type}")
        
        url = urljoin(self.api_url, endpoints[self.transform_type]["path"])
        data = endpoints[self.transform_type]["data"]
        popup = LoadingPopup()
        try:
            with httpx.Client() as client:
                popup.update_status("loading")
                response = client.post(url, json=data, timeout=5)  # 设置超时
                if response.status_code == 502:
                    raise Exception("502 Bad Gateway: 服务器错误")
                data = response.json()
                result = data["processed_text"]
                popup.update_status("sucess")
                return result
        except Exception as e:
            popup.update_status("erro")
            logging.error(f"Error in {self.transform_type}: {e}")
            return text + f"({e})"
