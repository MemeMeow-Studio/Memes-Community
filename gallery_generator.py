import json
import requests
import os
from typing import Dict, List, Any
from urllib.parse import urljoin
import concurrent.futures
import threading

class GalleryGenerator:
    def __init__(self, manifest_path: str = "community_manifest.json", max_workers: int = 5):
        self.manifest_path = manifest_path
        self.meme_libs_data = {}
        self.gallery_folder = "./gallery"
        self.max_workers = max_workers
        self.download_lock = threading.Lock()
        
        # 创建 gallery 文件夹
        if not os.path.exists(self.gallery_folder):
            os.makedirs(self.gallery_folder)
            print(f"创建文件夹: {self.gallery_folder}")
    
    def load_manifest(self) -> Dict[str, Any]:
        """加载 community_manifest.json 文件"""
        try:
            with open(self.manifest_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"错误：找不到文件 {self.manifest_path}")
            return {}
        except json.JSONDecodeError:
            print(f"错误：无法解析 JSON 文件 {self.manifest_path}")
            return {}
    
    def extract_update_urls(self, manifest_data: Dict[str, Any]) -> List[str]:
        """从 manifest 数据中提取所有 meme_libs 的 update_url"""
        update_urls = []
        meme_libs = manifest_data.get('meme_libs', {})
        
        for lib_id, lib_info in meme_libs.items():
            update_url = lib_info.get('update_url')
            if update_url:
                update_urls.append(update_url)
                print(f"找到 update_url: {update_url}")
        
        return update_urls
    
    def download_url(self, url: str) -> Dict[str, Any]:
        """下载指定 URL 的内容"""
        try:
            print(f"正在下载: {url}")
            response = requests.get(url, timeout=30)
            response.raise_for_status()
            
            # 尝试解析为 JSON
            try:
                return response.json()
            except json.JSONDecodeError:
                print(f"警告：URL {url} 返回的不是有效的 JSON 格式")
                return {"raw_content": response.text}
                
        except requests.exceptions.RequestException as e:
            print(f"下载失败 {url}: {e}")
            return {}
    
    def download_image(self, url: str, hash_name: str) -> bool:
        """下载图像文件并保存为哈希名"""
        try:
            print(f"正在下载图像: {url}")
            response = requests.get(url, timeout=30)
            response.raise_for_status()
            
            # 获取文件扩展名
            original_ext = os.path.splitext(url.split('/')[-1])[1]
            if not original_ext:
                original_ext = '.jpg'  # 默认扩展名
            
            # 保存文件
            filename = f"{hash_name}{original_ext}"
            filepath = os.path.join(self.gallery_folder, filename)
            
            with open(filepath, 'wb') as f:
                f.write(response.content)
            
            print(f"成功保存: {filename}")
            return True
            
        except requests.exceptions.RequestException as e:
            print(f"下载图像失败 {url}: {e}")
            return False
        except Exception as e:
            print(f"保存图像失败 {url}: {e}")
            return False
    
    def download_image_thread_safe(self, args_tuple) -> bool:
        """线程安全的图像下载函数"""
        url, hash_name = args_tuple
        try:
            with self.download_lock:
                print(f"正在下载图像: {url}")
            
            response = requests.get(url, timeout=30)
            response.raise_for_status()
            
            # 获取文件扩展名
            original_ext = os.path.splitext(url.split('/')[-1])[1]
            if not original_ext:
                original_ext = '.jpg'  # 默认扩展名
            
            # 保存文件
            filename = f"{hash_name}{original_ext}"
            filepath = os.path.join(self.gallery_folder, filename)
            
            with open(filepath, 'wb') as f:
                f.write(response.content)
            
            with self.download_lock:
                print(f"成功保存: {filename}")
            return True
            
        except requests.exceptions.RequestException as e:
            with self.download_lock:
                print(f"下载图像失败 {url}: {e}")
            return False
        except Exception as e:
            with self.download_lock:
                print(f"保存图像失败 {url}: {e}")
            return False
    
    def process_manifest_images(self, manifest_data: Dict[str, Any], base_url: str):
        """处理 manifest 中的图像文件"""
        contents = manifest_data.get('contents', {})
        images = contents.get('images', {})
        files = images.get('files', {})
        
        if not files:
            print("未找到图像文件")
            return
        
        print(f"找到 {len(files)} 个图像文件，开始多线程下载...")
        
        # 准备下载任务
        download_tasks = []
        for filename, file_info in files.items():
            filepath = file_info.get('filepath')
            hash_value = file_info.get('hash')
            
            if not filepath or not hash_value:
                print(f"跳过无效文件: {filename}")
                continue
            
            # 拼接完整 URL
            image_url = urljoin(base_url + "/", filepath)
            download_tasks.append((image_url, hash_value))
        
        if not download_tasks:
            print("没有有效的下载任务")
            return
        
        # 多线程下载
        success_count = 0
        with concurrent.futures.ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            future_to_task = {executor.submit(self.download_image_thread_safe, task): task for task in download_tasks}
            
            for future in concurrent.futures.as_completed(future_to_task):
                if future.result():
                    success_count += 1
        
        print(f"图像下载完成: {success_count}/{len(download_tasks)} 成功")
    
    def download_all_update_urls(self):
        """下载所有 meme_libs 的 update_url"""
        manifest_data = self.load_manifest()
        if not manifest_data:
            return
        
        update_urls = self.extract_update_urls(manifest_data)
        if not update_urls:
            print("没有找到任何 update_url")
            return
        
        print(f"共找到 {len(update_urls)} 个 update_url，开始下载...")
        
        # 获取原始库信息用于获取 base url
        meme_libs = manifest_data.get('meme_libs', {})
        
        for url in update_urls:
            data = self.download_url(url)
            if data:
                self.meme_libs_data[url] = data
                print(f"成功下载 manifest: {url}")
                
                # 找到对应的库信息获取 base_url
                base_url = None
                for lib_info in meme_libs.values():
                    if lib_info.get('update_url') == url:
                        base_url = lib_info.get('url')
                        break
                
                if base_url:
                    # 处理图像文件
                    self.process_manifest_images(data, base_url)
                else:
                    print(f"警告：无法找到 {url} 对应的 base_url")
            else:
                print(f"下载失败: {url}")
        
        print(f"所有处理完成，成功获取 {len(self.meme_libs_data)} 个 manifest")
        return self.meme_libs_data

def main():
    generator = GalleryGenerator()
    generator.download_all_update_urls()
    print()

if __name__ == "__main__":
    main()
