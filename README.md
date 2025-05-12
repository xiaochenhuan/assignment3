# README

## Intro

## Installation
Install the required dependency

```bash
pip install -r requirements.txt
```

Update `requirements.txt` file after new dependency is added

```bash
pip freeze > requirements.txt
```

## Database Operations

**Dependency**

```bash
pip install flask
pip install flask-sqlalchemy
pip install flask-migrate
pip install python-dotenv
```

**Manual Operations**

Run Flask Shell in terminal

```bash
flask shell
```

Insert the first row in user table

```bash
>>> u = User(id='1', employee_id='001', merchant_id='001', user_type='Merchant', username='kai', email='CITS5505@student.uwa', password_hash='asdfghjkl')
>>> db.session.add(u)
>>> db.session.commit()
```

Modify field

```bash
>>> user = User.query.get(user_id)
>>> user.username = 'new_name'
>>> db.session.commit()
```

Query: `SELECT * FROM user;`

```bash
>>> query = sa.select(User)
>>> users = db.session.scalars(query).all()
>>> Users
[<User 1>]
```

```bash
>>> users[0].username
'kai'
```

Delete the user `where id='1'`

```bash
>>> user = User.query.get(1)
>>> db.session.delete(user)
>>> db.session.commit()
```





```python
1.使用 Flask 创建数据库驱动的应用，必须包含 两个及以上关联的数据表。
2.基于公开数据源（open data） 开发，并以合适的方式展示数据。
3.加载 2000 到 7000 条记录的数据 到应用中，合理地加载。
4.使用适当的模板（HTML 页面）。
5.实现适当的错误处理机制（如 404 页面等）。
6.代码结构良好，有条理地使用不同组件（蓝图、模块等）。
7.使用 Git 进行版本控制。
8.为项目编写测试代码（如 pytest 测试模型、视图等）。
9.将项目部署到 Render 平台。
10.提交一个 一页的最终报告（PDF） 和 README 文件，内容包括：
应用设计与开发过程
安装与使用方法
Render 的部署地址
```



```python
# This file was produced by the NASA Exoplanet Archive  http://exoplanetarchive.ipac.caltech.edu
# Thu May  8 13:14:37 2025
#
# User preference: *
#
# COLUMN pl_name:        Planet Name
# COLUMN hostname:       Host Name
# COLUMN sy_pnum:        Number of Planets
# COLUMN discoverymethod: Discovery Method
# COLUMN disc_year:      Discovery Year
# COLUMN disc_facility:  Discovery Facility
# COLUMN sy_dist:        Distance [pc]
# COLUMN sy_disterr1:    Distance [pc] Upper Unc
# COLUMN sy_disterr2:    Distance [pc] Lower Unc
#
```

