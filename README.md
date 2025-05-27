# MemeMeow 社区资源包组

## 这个仓库是做什么的？

- 用于在MemeMeow中，导入社区资源包组链接（https://github.com/MemeMeow-Studio/Memes-Community/raw/main/community_manifest.json）。
- 生成用于图库的图片（gallery_generator.py）


## 社区资源包组仓库结构
- 资源包Git仓库：可以存放多个表情包库
- 表情包库：表情包的打包单元，每个表情包库相互独立，有唯一uuid，可以在MMIME中独立选择，或在MemeMeow-python中独立选择。
<!-- - 表情包组（WIP）：包含多个表情包uuid的表情包组，由各个终端应用负责实现。 -->

相关项目链接：

MemeMeow：https://github.com/MemeMeow-Studio/MemeMeow

社区表情包库仓库：https://github.com/MemeMeow-Studio/MemesLib-Community

Meme输入法：https://github.com/MemeMeow-Studio/MemeMeowIME

社区表情包组仓库：https://github.com/MemeMeow-Studio/Memes-Community

### community_manifest.json 文件结构

- 表情包库的uuid
  - 表情包库名称
  - 表情包库描述
  - 表情包库链接(可为list)
  - 表情包库修改时间(timestamp, utc+8)
  
### 社区表情包库文件结构

可以在https://github.com/MemeMeow-Studio/MemesLib-Community 的README.md找到。


<!-- ### 表情包组文件结构(WIP)
```yaml
name: xxx
timestamp: xxx
update_url: xxx(指向该文件本身)
memes_uuid: [xxx, xxx, ...]
```

计划在MemeMeow第三代版本实现。 -->
