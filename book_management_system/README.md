# Django图书管理系统

基于Django 4.x开发的在线图书管理系统，实现了完整的图书管理、借阅管理、用户管理和统计分析功能。

## 系统功能

### 用户管理
- 用户注册、登录、登出
- 个人资料管理
- 用户权限控制（普通用户/管理员）

### 图书管理
- 图书信息的增删改查
- 图书分类管理
- 作者管理
- 图书搜索（支持关键词、分类、作者筛选）
- 图书封面图片上传

### 借阅管理
- 图书借阅
- 图书归还
- 续借功能（最多续借2次，每次30天）
- 预约功能
- 逾期提醒

### 统计分析
- 图书统计
- 借阅统计
- 热门图书排行
- 逾期管理

## 技术栈

- **后端**: Django 4.2+
- **前端**: HTML5 + CSS3 + JavaScript + Bootstrap 5
- **数据库**: SQLite（开发环境）/ PostgreSQL（生产环境）
- **其他**: Pillow（图像处理）、django-bootstrap5

## 项目结构

```
book_management_system/
├── book_management_system/    # 项目配置
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
├── books/                     # 图书管理应用
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   ├── forms.py
│   ├── admin.py
│   └── templates/books/
├── users/                     # 用户管理应用
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   ├── forms.py
│   ├── admin.py
│   └── templates/users/
├── borrow/                    # 借阅管理应用
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   ├── forms.py
│   ├── admin.py
│   └── templates/borrow/
├── templates/                 # 全局模板
│   └── base.html
├── static/                    # 静态文件
├── media/                     # 上传文件
├── manage.py
└── requirements.txt
```

## 安装部署

### 1. 克隆项目
```bash
cd book_management_system
```

### 2. 创建虚拟环境
```bash
python -m venv venv
venv\Scripts\activate  # Windows
# 或
source venv/bin/activate  # Linux/Mac
```

### 3. 安装依赖
```bash
pip install -r requirements.txt
```

### 4. 数据库迁移
```bash
python manage.py makemigrations
python manage.py migrate
```

### 5. 创建超级用户
```bash
python manage.py createsuperuser
```

### 6. 启动开发服务器
```bash
python manage.py runserver
```

访问 http://127.0.0.1:8000/ 即可使用系统

## 默认管理员账号

- 用户名: admin
- 密码: admin123

## 使用说明

### 普通用户
1. 注册账号并登录
2. 浏览图书列表，搜索感兴趣的图书
3. 点击图书详情页的"借阅图书"按钮借阅
4. 在"借阅历史"页面查看借阅记录和归还图书
5. 可以续借未到期的图书（最多2次）
6. 预约已借出的图书

### 管理员
1. 使用管理员账号登录
2. 可以添加、编辑、删除图书
3. 可以管理图书分类和作者
4. 在"统计分析"页面查看系统统计数据
5. 在"借阅记录"和"逾期管理"页面管理借阅

## 注意事项

- 借阅期限为30天
- 每本图书最多可续借2次
- 逾期图书无法续借
- 生产环境请修改 `SECRET_KEY` 并关闭 `DEBUG` 模式
