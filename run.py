import os
import sys

from app import app, db


def create_super_admin():
    """创建超级管理员账户"""
    from models import User
    from werkzeug.security import generate_password_hash

    # 检查是否已存在超级管理员
    super_admin = User.query.filter_by(role="super_admin").first()
    if not super_admin:
        # 创建超级管理员
        admin = User(
            username="admin",
            email="admin@novel.com",
            password_hash=generate_password_hash("admin123"),
            role="super_admin",
        )
        db.session.add(admin)
        db.session.commit()
        print("超级管理员账户已创建:")
        print("用户名: admin")
        print("密码: admin123")
        print("邮箱: admin@novel.com")
    else:
        print("超级管理员账户已存在")


if __name__ == "__main__":
    with app.app_context():
        # 创建数据库表
        db.create_all()

        # 创建超级管理员
        create_super_admin()

        print("=" * 50)
        print("优雅小说网站启动成功！")
        print("访问地址: http://127.0.0.1:5000")
        print("超级管理员账户: admin / admin123")
        print("=" * 50)

    # 启动应用
    app.run(debug=True, host="0.0.0.0", port=5000)
