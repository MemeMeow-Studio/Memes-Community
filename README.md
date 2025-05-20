# VVfromVideo

从《这就是中国》中提取的vv表情包。欢迎帮忙去重，纠错和挑选精选图片。推荐在线编辑。精选图片请把图片复制到文件夹后，从原文件夹删除。

# 在VVQuest里导入

vv大全 表情包链接：https://github.com/MemeMeow-Studio/VVfromVideo/raw/main/all_vvs/manifest.json
# 教程：如何创建一个类似的仓库

## 表情包社区仓库结构
- 表情包仓库：可以存放多个表情包库
- 表情包库：表情包的打包单元，每个表情包库相互独立，有唯一uuid，可以在MMIME中独立选择，或在MemeMeow-python中独立选择。
- 表情包组：包含多个表情包uuid的表情包组，由各个终端应用负责实现。



### community_manifest.json 文件结构

- 表情包库的uuid
  - 表情包库名称
  - 表情包库描述
  - 表情包库链接(可为list)
  - 表情包库修改时间(timestamp, utc+8)
  
### 一个表情包仓库的info.yaml结构
```yaml
author: Official
version: 1.0.1
resource_url: "https://raw.githubusercontent.com/MemeMeow-Studio/VVfromVideo/main/"
resources:
  - name: "《这就是中国》大全"
    relative_path: all_vvs
    tags: 
      - vv
      - 张维为
    regex:
      pattern: "^\\d+\\^"
      replacement: ""
  - name: "精选v图"
    relative_path: 精选表情
    tags:
      - vv
      - 张维为
```
### 表情包仓库metadata.json的格式
运行generate_metadata.py，生成的json如下格式：
```json
{
    "author": "Official",
    "version": "1.0.1",
    "resource_url": "https://raw.githubusercontent.com/MemeMeow-Studio/VVfromVideo/main/",
    "resources": [
        {
            "name": "《这就是中国》大全",
            "relative_path": "all_vvs",
            "tags": [
                "vv",
                "张维为"
            ],
            "regex": {
                "pattern": "^\\d+\\^",
                "replacement": ""
            },
            "uuid": "4946f03b-11ae-4b03-81d5-db74dbf3f853"
        },
        {
            "name": "精选v图",
            "relative_path": "精选表情",
            "tags": [
                "vv",
                "张维为"
            ],
            "uuid": "13e30784-6ebf-4c17-9139-aafe95719c61"
        }
    ]
}
```
注意到，json添加了uuid标志。
### 表情包库manifest.json的格式
运行resource_pack.py，生成表情包库的manifest.json:
```json
{
    "name": "精选v图",
    "version": "1.0.1",
    "author": "Official",
    "description": "none",
    "created_at": "2025-05-19",
    "timestamp": 1747667458,
    "tags": [],
    "url": "https://raw.githubusercontent.com/MemeMeow-Studio/VVfromVideo/main/精选表情",
    "update_url": "https://raw.githubusercontent.com/MemeMeow-Studio/VVfromVideo/main/精选表情/manifest.json",
    "uuid": "13e30784-6ebf-4c17-9139-aafe95719c61",
    "contents": {
        "images": {
            "description": "图像资源目录",
            "files": {
                "1740372336^谢谢.jpg": {
                    "hash": "23b81b3db363aabc8bc77750eb182e3ef3103d9133df85d612b7b9d963228f7e",
                    "filepath": "1740372336^谢谢.jpg"
                }
            }
        }
    }
}
```
注意到，添加了timestamp，同时复制了uuid。

以上所有功能将在MemeMeow第二代版本实现。

### 表情包组文件结构(WIP)
```yaml
name: xxx
timestamp: xxx
update_url: xxx(指向该文件本身)
memes_uuid: [xxx, xxx, ...]
```

计划在MemeMeow第三代版本实现。
