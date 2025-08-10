# Melody Hunter

基于 **Python Django + CSS Selector** 的音乐资源爬取平台。本项目用于配合个人的 **Java Spring Boot + Vue3 音乐平台**，实现网络音乐数据的采集与管理，作为学习与技术实践之用（非商用）。

## 🎵 项目特性

- **多平台支持**: 支持网易云音乐、QQ音乐、酷狗音乐等主流音乐平台
- **智能爬取**: 基于CSS选择器的灵活爬取策略
- **异步处理**: 使用Celery实现异步任务处理
- **RESTful API**: 提供完整的RESTful API接口
- **管理后台**: Django Admin管理界面
- **日志记录**: 详细的爬取日志和错误追踪

## 🛠️ 技术栈

- **后端框架**: Django 4.2
- **异步任务**: Celery + Redis
- **数据库**: MySQL
- **爬虫工具**: Requests + BeautifulSoup + Selenium
- **API框架**: Django REST Framework

## 📦 项目结构

```
melody-hunter/
├── melody_hunter/          # Django项目配置
├── music/                  # 音乐数据管理应用
│   ├── models.py          # 数据模型（歌曲、艺术家、专辑等）
│   ├── serializers.py     # API序列化器
│   ├── views.py           # API视图
│   └── admin.py           # 管理后台配置
├── crawler/                # 爬虫应用
│   ├── models.py          # 爬虫任务模型
│   ├── tasks.py           # Celery异步任务
│   ├── spiders/           # 爬虫实现
│   │   ├── base.py        # 基础爬虫类
│   │   ├── netease.py     # 网易云音乐爬虫
│   │   ├── qq.py          # QQ音乐爬虫
│   │   └── kugou.py       # 酷狗音乐爬虫
│   └── management/        # Django管理命令
├── static/                 # 静态文件
├── media/                  # 媒体文件
├── templates/              # 模板文件
├── logs/                   # 日志文件
├── fixtures/               # 初始数据
├── requirements.txt        # Python依赖
└── start.py               # 项目启动脚本
```

## 🚀 快速开始

### 1. 环境要求

- Python 3.8+
- MySQL 5.7+
- Redis 6.0+

### 2. 安装部署

```bash
# 克隆项目
git clone https://github.com/your-username/melody-hunter.git
cd melody-hunter

# 创建虚拟环境
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 自动安装和初始化
python start.py
```

### 3. 手动配置

如果自动初始化失败，可以手动执行以下步骤：

```bash
# 安装依赖
pip install -r requirements.txt

# 创建 .env 文件
cp .env.example .env
# 编辑 .env 文件，配置数据库和Redis连接

# 数据库迁移
python manage.py makemigrations
python manage.py migrate

# 创建超级用户
python manage.py createsuperuser

# 初始化平台数据
python manage.py init_platforms

# 启动服务
python manage.py runserver
```

### 4. 启动Celery Worker

```bash
# 新开终端窗口
celery -A melody_hunter worker -l info
```

## 📖 使用指南

### API接口

项目提供以下主要API接口：

- **音乐管理**:
  - `GET /api/music/songs/` - 获取歌曲列表
  - `GET /api/music/artists/` - 获取艺术家列表
  - `GET /api/music/albums/` - 获取专辑列表
  - `GET /api/music/platforms/` - 获取平台列表

- **爬虫管理**:
  - `GET /api/crawler/tasks/` - 获取爬虫任务列表
  - `POST /api/crawler/tasks/` - 创建爬虫任务
  - `POST /api/crawler/tasks/{id}/start/` - 启动任务
  - `POST /api/crawler/tasks/{id}/cancel/` - 取消任务

### 管理命令

```bash
# 初始化平台数据
python manage.py init_platforms

# 创建爬虫任务
python manage.py crawl_music --platform "网易云音乐" --type search --keyword "周杰伦" --pages 3

# 爬取艺术家
python manage.py crawl_music --platform "网易云音乐" --type artist --url "https://music.163.com/artist?id=6452"
```

## 🎯 功能说明

### 支持的爬取类型

1. **搜索爬取** (`search`): 根据关键词搜索歌曲
2. **艺术家爬取** (`artist`): 爬取指定艺术家的所有歌曲
3. **专辑爬取** (`album`): 爬取指定专辑的所有歌曲
4. **歌单爬取** (`playlist`): 爬取指定歌单的所有歌曲

### 数据模型

- **Platform**: 音乐平台信息
- **Artist**: 艺术家信息
- **Album**: 专辑信息
- **Song**: 歌曲信息
- **CrawlTask**: 爬虫任务
- **CrawlLog**: 爬虫日志

## ⚠️ 注意事项

1. **仅供学习**: 本项目仅用于技术学习和研究，请勿用于商业用途
2. **遵守协议**: 使用时请遵守各音乐平台的robots.txt和用户协议
3. **合理频率**: 建议设置合理的爬取间隔，避免对目标网站造成压力
4. **版权声明**: 爬取的音乐资源版权归原作者所有

## 🤝 贡献指南

欢迎提交Issue和Pull Request来改进项目！

1. Fork本仓库
2. 创建特性分支
3. 提交更改
4. 推送到分支
5. 创建Pull Request

## 📄 许可证

本项目采用 [MIT License](LICENSE) 许可证。

## 🔗 相关项目

- **前端项目**: [Java Spring Boot + Vue3 音乐平台]() (开发中)

---

**免责声明**: 本项目仅用于学习和技术交流，使用者需遵守相关法律法规和平台协议，作者不承担任何法律责任。