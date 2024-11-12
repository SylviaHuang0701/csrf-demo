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

## TODO
1. 模拟修改数据库操作
当前的演示只是简单地修改用户的电子邮件地址，但并未直接展示数据库层面的变化。当 CSRF 攻击成功时，可以在数据库中直接查询并展示被篡改的数据。例如，攻击者成功修改用户电子邮件后，可以在 Django 控制台或通过一个视图直接显示数据库中存储的用户信息。

``` python
from django.db import connection

def show_database(request):
    with connection.cursor() as cursor:
        cursor.execute("SELECT username, email FROM auth_user WHERE username = %s", [request.user.username])
        result = cursor.fetchone()
    return HttpResponse(f"当前用户：{result[0]}, 邮箱：{result[1]}")
```

2. 增加恶意请求的数据多样性/触发更复杂的数据库操作
在演示中，您只修改了一个电子邮件字段，可以进一步通过恶意表单模拟更多种类的攻击。例如：

更改用户密码：攻击者可以通过 CSRF 攻击尝试修改用户的密码字段，模拟重置密码的攻击。

改变用户角色或权限：通过修改用户的 is_staff 或 is_superuser 字段，展示攻击者如何提升自己的权限。
删除某个用户的账户

例如，可以修改恶意表单，使其包含更多字段（如 is_staff）：

``` html
<form id="csrf-form" method="post" action="http://127.0.0.1:8000/users/update_profile/">
    <input type="hidden" name="email" value="attacker@example.com">
    <input type="hidden" name="is_staff" value="True"> <!-- 攻击者试图将用户设为管理员 -->
</form>
```
3. 展示 CSRF 防护措施

启用 CSRF 防护：首先，恢复 Django 默认的 CSRF 防护（启用 CsrfViewMiddleware）。然后，展示通过 CSRF token 来防止恶意请求。

修改表单来使用 CSRF Token：

``` html
<form method="post" action="/users/update_profile/">
    {% csrf_token %}
    <input type="email" name="email" value="new_email@example.com">
    <button type="submit">更新</button>
</form>
```
当 CSRF token 被正确使用时，恶意网页的攻击无法成功提交请求，Django 会返回 CSRF 保护错误。

4. 数据库层面的日志记录
可以展示如何在数据库中记录异常或潜在的攻击事件。例如，可以在用户资料更新时，向数据库的日志表插入记录，或者在 update_profile 视图中增加攻击日志功能，记录恶意请求的源 IP 和其他信息。

``` python
from django.utils.timezone import now
from app01.models import AttackLog

def update_profile(request):
    if request.method == 'POST':
        # 攻击者尝试提交的操作
        new_email = request.POST.get('email')
        # 写入攻击日志
        AttackLog.objects.create(user=request.user, action="修改邮箱", ip=request.META.get('REMOTE_ADDR'), timestamp=now())
        request.user.email = new_email
        request.user.save()
        return HttpResponse("Profile updated successfully")
    return render(request, 'update_profile.html')
```
