# csrf-demo

## 项目配置

### 安装必要的依赖

可参照群里PPT安装django和mysql

### 安装步骤

1. **克隆项目代码**：
   ```bash
   git clone https://github.com/SylviaHuang0701/csrf-demo.git
   cd csrf-demo
   ```
2. **数据库迁移**：
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

5. **创建超级用户**（用于登录）：
   ```bash
   python manage.py createsuperuser
   ```

### 项目配置

1. **禁用 CSRF 中间件**（仅用于攻击演示，生产环境务必启用）：
   - 打开 `settings.py`，找到 `MIDDLEWARE` 配置，将 `django.middleware.csrf.CsrfViewMiddleware` 注释掉或删除。
   
   ```python
   MIDDLEWARE = [
       'django.middleware.security.SecurityMiddleware',
       # 'django.middleware.csrf.CsrfViewMiddleware',  # 注释掉此行
       ...
   ]
   ```

## 启动项目

1. **运行开发服务器**：
   ```bash
   python manage.py runserver
   ```

2. **访问应用**：
   - 打开浏览器，访问 `http://127.0.0.1:8000`。
   - 使用刚才创建的超级用户账户进行登录。

## 演示 CSRF 攻击


### 1. 在本地托管恶意网页

打开一个终端，导航到包含 `malicious_site.html` 的目录，然后使用 Python 内置的 HTTP 服务器来托管该文件：

```bash
python3 -m http.server 8080
```

### 2. 执行攻击

1. **在浏览器中登录 Django 应用**：
   - 在浏览器中访问 `http://127.0.0.1:8000/login/`，并使用登录。

2. **在同一浏览器会话中打开恶意网页**：
   - 在新的标签页中访问 `http://127.0.0.1:8080/malicious_site.html`。
   - 页面会自动发送一个请求，将登录用户的电子邮件更改为 `attacker@example.com`。

3. **检查攻击效果**：
   - 返回 Django 应用并查看用户个人资料页面，确认电子邮件已被更改为 `attacker@example.com`。

## 参考

- [Django 官方文档 - 跨站请求伪造保护](https://docs.djangoproject.com/en/stable/ref/csrf/)
