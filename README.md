# 优雅小说网站

一个基于Python Flask开发的精美舒适的小说阅读和创作平台，采用优雅的设计风格和毛玻璃模糊效果，集成了实用的笔记功能。

## 🎯 项目特色

- 🎨 **优雅设计** - 精心设计的界面，使用毛玻璃模糊效果和柔和渐变，避免AI感的不协调设计
- 📚 **完整功能** - 小说创作、阅读、评论、管理等完整功能体系
- 👥 **权限系统** - 多级用户权限管理（读者、作家、管理员、超级管理员）
- 📱 **响应式设计** - 完美适配桌面端和移动端
- 💬 **互动社区** - 读者评论、作者留言等互动功能
- ✍️ **笔记功能** - 实用的草稿编辑器，支持实时自动保存和AI写作助手

## ✨ 核心功能特性

### 读者功能
- 浏览小说列表
- 阅读小说章节
- 发表评论
- 用户注册登录

### 作家功能
- 创建和管理小说
- 发布和编辑章节
- 添加作者说
- 作品统计
- **笔记功能** - 草稿编辑器，实时自动保存
- **AI写作助手** - 集成OpenAI兼容API，辅助创作

### 管理员功能
- 用户管理
- 作品管理
- 权限设置
- 系统统计

## 🎨 设计理念

### 视觉风格
- **舒适优雅** - 避免过度设计，采用柔和的色彩和适当的留白
- **毛玻璃效果** - 使用`backdrop-filter`实现现代化的毛玻璃模糊效果
- **响应式布局** - 适配各种屏幕尺寸
- **无障碍设计** - 良好的对比度和可读性

### 色彩系统
```css
:root {
    --primary-color: #2c3e50;    /* 主色调 - 深蓝灰 */
    --accent-color: #3498db;     /* 强调色 - 柔和蓝 */
    --secondary-color: #ecf0f1;  /* 辅助色 - 米白 */
}
```

### 字体选择
- **思源宋体** - 使用Google Fonts的Noto Serif SC字体提升阅读体验

## 🛠 技术栈

- **后端**: Python Flask 2.3.3
- **数据库**: SQLite + SQLAlchemy ORM
- **前端**: HTML5, CSS3, JavaScript
- **样式**: 自定义CSS，毛玻璃模糊效果
- **字体**: Noto Serif SC (思源宋体)
- **AI集成**: OpenAI兼容API支持

## 📁 项目结构

```
newxiaoshuo-git/
├── 核心文件
│   ├── app.py              # Flask主应用（包含笔记功能路由）
│   ├── models.py           # 数据模型定义（包含Draft和UserSettings）
│   ├── run.py              # 启动脚本（含管理员创建）
│   └── requirements.txt    # 依赖包列表
├── 模板文件
│   ├── base.html          # 基础布局
│   ├── index.html         # 首页
│   ├── login.html         # 登录页
│   ├── register.html      # 注册页
│   ├── novel_detail.html  # 小说详情
│   ├── read.html          # 阅读页面
│   ├── author_dashboard.html  # 作家后台
│   ├── create_novel.html  # 创建小说
│   ├── create_chapter.html # 创建章节
│   ├── edit_novel.html    # 编辑小说
│   ├── edit_chapter.html  # 编辑章节
│   ├── admin_dashboard.html # 管理后台
│   ├── drafts_list.html   # 草稿列表页面
│   ├── draft_editor.html  # 草稿编辑器页面
│   └── user_settings.html # 扩展的用户设置页面
├── 静态资源
│   ├── css/style.css      # 主样式文件（包含笔记相关样式）
│   └── js/
│       ├── main.js        # JavaScript功能
│       └── draft_editor.js # 编辑器JavaScript逻辑
└── 文档文件
    └── README.md          # 项目说明（本文件）
```

## 🚀 快速安装指南

### 环境要求
- Windows 10 或更高版本
- Python 3.7 或更高版本
- 网络连接（用于下载依赖包）

### 安装步骤

#### 1. 安装 Python
1. 访问 Python 官网：https://www.python.org/downloads/
2. 下载 Python 3.9 或更高版本的 Windows 安装包
3. 运行安装程序，**务必勾选 "Add Python to PATH"** 选项
4. 选择 "Install Now" 完成安装

#### 2. 验证 Python 安装
打开命令提示符，输入：
```cmd
python --version
```
如果显示 Python 版本号（如 `Python 3.9.0`），说明安装成功。

#### 3. 安装项目依赖
1. 打开命令提示符
2. 切换到项目目录：
```cmd
cd C:\Users\jayde\Documents\zed\newxiaoshuo-git
```
3. 安装依赖包：
```cmd
pip install -r requirements.txt
```

#### 4. 运行网站
在项目目录下执行：
```cmd
python run.py
```

#### 5. 访问网站
打开浏览器，访问：`http://127.0.0.1:5000`

### 默认管理员账户
- **用户名**: `admin`
- **密码**: `admin123`
- **邮箱**: `admin@novel.com`

**重要**：首次登录后请立即修改密码！

## ✍️ 笔记功能使用指南

### 概述
本系统新增了实用的笔记功能，专为小说创作设计。您可以使用Markdown格式创建小说章节草稿，所有内容都会自动保存到SQLite数据库，不会因刷新而丢失。写完后可以直接发布为正式章节。

### 主要特性
- **实时自动保存** - 每输入一个字符都会自动保存，永不丢失
- **Markdown支持** - 支持粗体、斜体、列表等基本格式
- **AI写作助手** - 集成OpenAI兼容API，辅助创作
- **优雅设计** - 舒适的界面设计
- **草稿管理** - 每本小说独立的草稿空间

### 快速开始

#### 1. 配置AI助手
1. 登录后进入**作家后台**
2. 点击右上角 **"AI设置"** 按钮
3. 填写以下信息：
   - **API Key**: 从DeepSeek或其他OpenAI兼容服务获取
   - **Base URL**: 例如 `https://api.deepseek.com`
   - **模型名称**: 例如 `deepseek-chat` 或 `gpt-3.5-turbo`

#### 2. 创建草稿
1. 在作家后台找到您的小说
2. 点击 **"草稿笔记"** 按钮
3. 点击 **"新建草稿"** 开始创作

#### 3. 使用编辑器
- **标题**: 在顶部输入框输入章节标题
- **内容**: 在编辑器中输入章节内容
- **工具栏**: 使用工具栏按钮添加格式
- **自动保存**: 右下角显示保存状态

#### 4. AI助手使用
1. 点击 **"AI助手"** 或 **"AI建议"** 按钮
2. 在弹出的窗口中：
   - 输入您的请求（如：润色这段文字、续写故事等）
   - 可选：提供上下文信息
   - 点击 **"生成"** 获取AI回复
3. 可以选择 **"插入到编辑器"** 或 **"复制"** 结果

#### 5. 发布章节
1. 完成草稿后，点击 **"发布章节"** 按钮
2. 系统会自动分配章节号并发布
3. 发布后草稿会标记为"已发布"

### 支持的API提供商

#### 🚀 推荐配置
**DeepSeek** - 性价比高，中文优化
- Base URL: `https://api.deepseek.com`
- 模型: `deepseek-chat`
- 获取API Key: 访问 DeepSeek 官网

#### 🔧 其他选项
- **OpenAI官方** - 稳定可靠
- **其他兼容OpenAI格式的API** - 如Azure OpenAI等

## 🔧 故障排除

### 常见问题

#### 问题1：Python 未找到
**错误信息**：`'python' 不是内部或外部命令，也不是可运行的程序`

**解决方案**：
1. 重新安装 Python，确保勾选 "Add Python to PATH"
2. 或使用完整路径运行：`C:\Users\您的用户名\AppData\Local\Programs\Python\Python39\python.exe run.py`

#### 问题2：pip 命令不可用
**解决方案**：
```cmd
python -m pip install -r requirements.txt
```

#### 问题3：端口被占用
**错误信息**：`Address already in use`

**解决方案**：
1. 关闭其他占用 5000 端口的程序
2. 或修改端口：编辑 `run.py` 文件，将 `port=5000` 改为其他端口号

#### 问题4：依赖安装失败
**解决方案**：
1. 更新 pip：`python -m pip install --upgrade pip`
2. 尝试使用国内镜像源：
```cmd
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
```

#### 问题5：AI助手无法使用
**解决方案**：
检查AI设置中的API配置是否正确，确保API Key有效且余额充足。

## 📊 数据库模型

### 核心模型
```python
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    role = db.Column(db.String(20), default='reader')

class Novel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'))

class Chapter(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    chapter_number = db.Column(db.Integer, nullable=False)
    novel_id = db.Column(db.Integer, db.ForeignKey('novel.id'))
```

### 笔记功能扩展模型
```python
class Draft(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False, default="无标题草稿")
    content = db.Column(db.Text, default="")
    novel_id = db.Column(db.Integer, db.ForeignKey("novel.id"), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    is_published = db.Column(db.Boolean, default=False)
    chapter_number = db.Column(db.Integer, nullable=True)

class UserSettings(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False, unique=True)
    nickname = db.Column(db.String(100), nullable=True)
    openai_api_key = db.Column(db.String(255), nullable=True)
    openai_base_url = db.Column(db.String(500), nullable=True)
    openai_model = db.Column(db.String(100), nullable=True)
```

## 🎯 API端点

### 核心功能
- `GET /` - 首页
- `GET/POST /login` - 用户登录
- `GET/POST /register` - 用户注册
- `GET /logout` - 用户登出
- `GET /novel/<novel_id>` - 小说详情
- `GET /read/<novel_id>/<chapter_number>` - 阅读章节

### 作家功能
- `GET /author/dashboard` - 作家后台
- `GET/POST /author/create_novel` - 创建小说
- `GET/POST /author/novel/<novel_id>/create_chapter` - 创建章节
- `GET/POST /author/edit_novel/<novel_id>` - 编辑小说
- `GET/POST /author/edit_chapter/<chapter_id>` - 编辑章节

### 笔记功能
- `GET/POST /author/settings` - 用户设置管理
- `GET /author/novel/<novel_id>/drafts` - 草稿列表
- `GET /author/novel/<novel_id>/draft/new` - 创建草稿
- `GET /author/draft/<draft_id>` - 编辑草稿
- `POST /author/draft/<draft_id>/save` - 保存草稿
- `POST /author/draft/<draft_id>/publish` - 发布草稿
- `POST /author/draft/<draft_id>/delete` - 删除草稿
- `POST /author/ai/assist` - AI助手API

### 管理员功能
- `GET /admin/dashboard` - 管理后台
- `GET /admin/users` - 用户管理
- `POST /admin/user/<user_id>/update_role` - 更新用户角色

## 🔒 权限系统

### 角色定义
- `reader`: 普通读者 - 浏览小说、阅读、评论
- `writer`: 作家 - 所有读者功能 + 创作管理
- `admin`: 管理员 - 所有作家功能 + 用户管理
- `super_admin`: 超级管理员 - 所有权限

### 权限控制
- 装饰器验证用户权限
- 后端验证所有操作权限
- 前端根据权限显示不同界面

## 🎉 项目成就

✅ **完整实现**：从数据库到前端的完整Web应用  
✅ **优雅设计**：符合要求的舒适高雅风格  
✅ **功能丰富**：涵盖小说网站所有核心功能  
✅ **笔记集成**：实用的草稿编辑器  
✅ **AI助手**：灵活的AI写作辅助功能  
✅ **代码规范**：清晰的结构和良好的注释  
✅ **用户体验**：流畅的交互和响应式设计  
✅ **文档完善**：详细的安装和使用指南  

## 📈 扩展建议

### 功能扩展
- 小说分类和标签系统
- 收藏和书架功能
- 作者打赏系统
- 高级搜索功能
- 阅读进度同步
- 草稿版本历史
- 协作编辑功能

### 技术优化
- 数据库迁移到PostgreSQL
- 添加Redis缓存
- 实现RESTful API
- 添加单元测试
- 部署到云平台

## 📄 许可证

MIT License

## 🤝 贡献

欢迎提交Issue和Pull Request来改进这个项目。

## 📞 联系方式

如有问题或建议，请通过项目Issue进行反馈。

---

**让阅读和创作成为一种享受** 📚✨
