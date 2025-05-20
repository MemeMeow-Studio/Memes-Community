import datetime
import yaml
import json
import requests
import logging
import time
from pathlib import Path

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def load_yaml_file(file_path):
    """加载YAML文件并返回其内容"""
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return yaml.safe_load(file)
    except Exception as e:
        logging.error(f"读取YAML文件失败: {e}")
        return None

def download_json(url):
    """从URL下载JSON内容"""
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        logging.error(f"下载JSON文件失败: {e}")
        return None
    except json.JSONDecodeError as e:
        logging.error(f"解析JSON内容失败: {e}")
        return None

def generate_community_manifest():
    """生成community_manifest.json文件"""
    # 文件路径
    current_dir = Path(__file__).parent
    yaml_path = current_dir / "meme_repo.yaml"
    info_yaml_path = current_dir / "community_info.yaml"
    output_path = current_dir / "community_manifest.json"
    
    # 加载YAML文件
    repo_data = load_yaml_file(yaml_path)
    if not repo_data:
        return False
    
    # 加载community_info.yaml文件
    community_info = load_yaml_file(info_yaml_path)
    if not community_info:
        logging.warning("无法读取community_info.yaml，将继续但不包含社区信息")
        community_info = {}
    
    # 添加时间戳（UTC+8）到community_info
    community_info['timestamp'] = int(datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=8))).timestamp())
    
    # 创建输出JSON对象，包含community_info信息
    community_manifest = {
        "community_info": community_info,
        "meme_libs": {}
    }
    
    # 处理每个条目
    for uuid, info in repo_data.items():
        logging.info(f"处理 {info['name']} (UUID: {uuid})")
        
        # 下载JSON
        json_url = info.get('urls')
        if not json_url:
            logging.warning(f"UUID {uuid} 没有提供URL")
            continue
            
        remote_json = download_json(json_url)
        if not remote_json:
            continue
        
        # 提取需要的字段
        required_fields = [
            "name", "version", "author", "description", "created_at", 
            "timestamp", "tags", "url", "update_url", "uuid"
        ]
        
        extracted_data = {field: remote_json.get(field) for field in required_fields if field in remote_json}
        
        # 使用下载的JSON的UUID作为键
        if "uuid" in extracted_data:
            remote_uuid = extracted_data["uuid"]
            community_manifest["meme_libs"][remote_uuid] = extracted_data
            logging.info(f"添加了 {extracted_data.get('name')} (UUID: {remote_uuid})")
        else:
            community_manifest["meme_libs"][uuid] = extracted_data
            logging.warning(f"远程JSON没有UUID，使用本地UUID: {uuid}")
    
    # 保存结果到JSON文件
    try:
        with open(output_path, 'w', encoding='utf-8') as file:
            json.dump(community_manifest, file, ensure_ascii=False, indent=2)
        logging.info(f"成功生成 community_manifest.json，包含 {len(community_manifest['meme_libs'])} 个仓库条目和社区信息")
        return True
    except Exception as e:
        logging.error(f"保存JSON文件失败: {e}")
        return False

if __name__ == "__main__":
    generate_community_manifest()
