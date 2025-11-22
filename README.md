# 优雅小说网站

一个基于Python Flask开发的精美舒适的小说阅读和创作平台，采用优雅的设计风格和毛玻璃模糊效果。

## 项目特色

- 🎨 **优雅设计** - 精心设计的界面，使用毛玻璃模糊效果和柔和渐变
- 📚 **完整功能** - 小说创作、阅读、评论、管理等完整功能
- 👥 **权限系统** - 多级用户权限管理（读者、作家、管理员、超级管理员）
- 📱 **响应式设计** - 完美适配桌面端和移动端
- 💬 **互动社区** - 读者评论、作者留言等互动功能

## 功能特性

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

### 管理员功能
- 用户管理
- 作品管理
- 权限设置
- 系统统计

## 技术栈

- **后端**: Python Flask
- **数据库**: SQLite
- **前端**: HTML5, CSS3, JavaScript
- **样式**: 自定义CSS，毛玻璃模糊效果
- **字体**: Noto Serif SC (思源宋体)

## 安装和运行

### 环境要求
- Python 3.7+
- pip

### 安装步骤

1. 克隆或下载项目文件
2. 安装依赖：
   ```bash
   pip install -r requirements.txt
   ```

3. 运行项目：
   ```bash
   python run.py
   ```

4. 访问网站：
   打开浏览器访问 `http://127.0.0.1:5000`

### 默认管理员账户
- 用户名: `admin`
- 密码: `admin123`
- 邮箱: `admin@novel.com`

## 项目结构

```
xiaoshou/
├── app.py              # Flask主应用
├── models.py           # 数据模型
├── run.py              # 启动脚本
├── requirements.txt    # Python依赖
├── README.md          # 项目说明
├── templates/         # HTML模板
│   ├── base.html
│   ├── index.html
│   ├── login.html
│   ├── register.html
│   ├── novel_detail.html
│   ├── read.html
│   ├── author_dashboard.html
│   ├── create_novel.html
│   ├── create_chapter.html
│   ├── edit_novel.html
│   ├── edit_chapter.html
│   └── admin_dashboard.html
└── static/            # 静态文件
    ├── css/
    │   └── style.css
    └── js/
        └── main.js
```

## 使用指南

### 注册账户
1. 点击首页"注册"按钮
2. 填写用户名、邮箱、密码
3. 注册成功后登录

### 创作小说
1. 登录后进入"作家后台"
2. 点击"创建新小说"
3. 填写小说标题和简介
4. 发布章节内容

### 阅读小说
1. 浏览首页小说列表
2. 点击感兴趣的小说
3. 选择章节开始阅读
4. 可以在章节末尾发表评论

### 管理后台
1. 使用管理员账户登录
2. 点击"管理后台"
3. 管理用户和作品

## 设计理念

- **舒适优雅** - 避免过度设计，采用柔和的色彩和适当的留白
- **毛玻璃效果** - 使用backdrop-filter实现现代化的毛玻璃模糊效果
- **响应式布局** - 适配各种屏幕尺寸
- **无障碍设计** - 良好的对比度和可读性

## 开发说明

### 数据库模型
- User: 用户信息
- Novel: 小说信息
- Chapter: 章节内容
- Comment: 评论信息
- Message: 留言信息

### 权限系统
- `reader`: 普通读者
- `admin`: 管理员
- `super_admin`: 超级管理员

### 自定义样式
项目使用CSS变量系统，便于主题定制：
```css
:root {
    --primary-color: #2c3e50;
    --accent-color: #3498db;
    --shadow-md: 0 4px 16px rgba(0, 0, 0, 0.12);
    /* ... */
}
```

## 许可证

MIT License

## 贡献

欢迎提交Issue和Pull Request来改进这个项目。

## 联系方式

如有问题或建议，请通过项目Issue进行反馈。

---

**让阅读成为一种享受** ✨
