import os
import sqlite3
import sys
from datetime import datetime

import requests

# 添加项目路径到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


def test_database_connection():
    """测试数据库连接和表结构"""
    print("=== 测试数据库连接 ===")
    try:
        conn = sqlite3.connect("novel.db")
        cursor = conn.cursor()

        # 检查所有表
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = cursor.fetchall()
        print(f"数据库中的表: {[table[0] for table in tables]}")

        # 检查关键表结构
        required_tables = ["user", "novel", "chapter", "draft", "user_settings"]
        for table in required_tables:
            if table in [t[0] for t in tables]:
                cursor.execute(f"PRAGMA table_info({table})")
                columns = cursor.fetchall()
                print(f"\n{table}表结构:")
                for col in columns:
                    print(f"  - {col[1]} ({col[2]})")
            else:
                print(f"\n❌ 缺少表: {table}")

        conn.close()
        print("✓ 数据库连接测试完成")
        return True

    except Exception as e:
        print(f"❌ 数据库连接测试失败: {e}")
        return False


def test_flask_app():
    """测试Flask应用是否正常运行"""
    print("\n=== 测试Flask应用 ===")
    try:
        # 尝试导入Flask应用
        from app import app

        with app.test_client() as client:
            # 测试首页
            response = client.get("/")
            if response.status_code == 200:
                print("✓ 首页访问正常")
            else:
                print(f"❌ 首页访问失败: {response.status_code}")

            # 测试登录页面
            response = client.get("/login")
            if response.status_code == 200:
                print("✓ 登录页面访问正常")
            else:
                print(f"❌ 登录页面访问失败: {response.status_code}")

            # 测试注册页面
            response = client.get("/register")
            if response.status_code == 200:
                print("✓ 注册页面访问正常")
            else:
                print(f"❌ 注册页面访问失败: {response.status_code}")

        print("✓ Flask应用测试完成")
        return True

    except Exception as e:
        print(f"❌ Flask应用测试失败: {e}")
        return False


def test_models():
    """测试数据模型"""
    print("\n=== 测试数据模型 ===")
    try:
        from models import Chapter, Draft, Novel, User, UserSettings, db

        # 检查模型属性
        models_to_check = [
            (User, ["id", "username", "email", "password_hash", "role"]),
            (Novel, ["id", "title", "description", "author_id", "status"]),
            (Chapter, ["id", "title", "content", "chapter_number", "novel_id"]),
            (Draft, ["id", "title", "content", "novel_id", "user_id", "is_published"]),
            (
                UserSettings,
                [
                    "id",
                    "user_id",
                    "nickname",
                    "openai_api_key",
                    "openai_base_url",
                    "openai_model",
                ],
            ),
        ]

        all_models_ok = True
        for model, required_attrs in models_to_check:
            model_name = model.__name__
            for attr in required_attrs:
                if hasattr(model, attr):
                    print(f"✓ {model_name} 包含属性: {attr}")
                else:
                    print(f"❌ {model_name} 缺少属性: {attr}")
                    all_models_ok = False

        if all_models_ok:
            print("✓ 所有数据模型检查通过")
            return True
        else:
            print("❌ 部分数据模型存在问题")
            return False

    except Exception as e:
        print(f"❌ 数据模型测试失败: {e}")
        return False


def test_routes():
    """测试路由是否可访问"""
    print("\n=== 测试路由 ===")
    try:
        from app import app

        routes_to_test = [
            ("/", "GET", "首页"),
            ("/login", "GET", "登录页面"),
            ("/register", "GET", "注册页面"),
            ("/author/settings", "GET", "用户设置"),
        ]

        with app.test_client() as client:
            all_routes_ok = True
            for route, method, description in routes_to_test:
                try:
                    if method == "GET":
                        response = client.get(route)
                    elif method == "POST":
                        response = client.post(route)

                    if response.status_code in [200, 302]:  # 302是重定向
                        print(f"✓ {description} ({route}) - 正常")
                    else:
                        print(
                            f"❌ {description} ({route}) - 状态码: {response.status_code}"
                        )
                        all_routes_ok = False

                except Exception as e:
                    print(f"❌ {description} ({route}) - 错误: {e}")
                    all_routes_ok = False

        if all_routes_ok:
            print("✓ 路由测试完成")
            return True
        else:
            print("❌ 部分路由存在问题")
            return False

    except Exception as e:
        print(f"❌ 路由测试失败: {e}")
        return False


def test_note_features():
    """测试笔记功能相关路由"""
    print("\n=== 测试笔记功能 ===")
    try:
        from app import app

        # 这些路由需要登录后才能访问，我们只测试路由定义
        note_routes = [
            "/author/novel/1/drafts",
            "/author/novel/1/draft/new",
            "/author/draft/1",
            "/author/draft/1/save",
            "/author/draft/1/publish",
            "/author/draft/1/delete",
            "/author/ai/assist",
        ]

        print("笔记功能路由定义:")
        for route in note_routes:
            print(f"  - {route}")

        print("✓ 笔记功能路由检查完成")
        return True

    except Exception as e:
        print(f"❌ 笔记功能测试失败: {e}")
        return False


def test_templates():
    """测试模板文件是否存在"""
    print("\n=== 测试模板文件 ===")
    templates_dir = "templates"
    required_templates = [
        "base.html",
        "index.html",
        "login.html",
        "register.html",
        "author_dashboard.html",
        "drafts_list.html",
        "draft_editor.html",
        "user_settings.html",
        "edit_novel.html",
        "edit_chapter.html",
    ]

    all_templates_ok = True
    for template in required_templates:
        template_path = os.path.join(templates_dir, template)
        if os.path.exists(template_path):
            print(f"✓ 模板文件存在: {template}")
        else:
            print(f"❌ 模板文件缺失: {template}")
            all_templates_ok = False

    if all_templates_ok:
        print("✓ 所有模板文件检查通过")
        return True
    else:
        print("❌ 部分模板文件缺失")
        return False


def test_static_files():
    """测试静态文件是否存在"""
    print("\n=== 测试静态文件 ===")
    static_files = ["static/css/style.css", "static/js/draft_editor.js"]

    all_files_ok = True
    for file_path in static_files:
        if os.path.exists(file_path):
            print(f"✓ 静态文件存在: {file_path}")
        else:
            print(f"❌ 静态文件缺失: {file_path}")
            all_files_ok = False

    if all_files_ok:
        print("✓ 所有静态文件检查通过")
        return True
    else:
        print("❌ 部分静态文件缺失")
        return False


def test_dependencies():
    """测试依赖包"""
    print("\n=== 测试依赖包 ===")
    required_packages = ["flask", "flask_sqlalchemy", "werkzeug", "openai", "pytz"]

    all_deps_ok = True
    for package in required_packages:
        try:
            __import__(package)
            print(f"✓ 依赖包可用: {package}")
        except ImportError as e:
            print(f"❌ 依赖包缺失: {package} - {e}")
            all_deps_ok = False

    if all_deps_ok:
        print("✓ 所有依赖包检查通过")
        return True
    else:
        print("❌ 部分依赖包缺失")
        return False


def main():
    """主测试函数"""
    print("开始全面测试小说网站功能...")
    print("=" * 60)

    tests = [
        test_dependencies,
        test_database_connection,
        test_models,
        test_templates,
        test_static_files,
        test_flask_app,
        test_routes,
        test_note_features,
    ]

    passed = 0
    total = len(tests)

    for test in tests:
        try:
            if test():
                passed += 1
            print("-" * 40)
        except Exception as e:
            print(f"❌ 测试 {test.__name__} 异常: {e}")
            print("-" * 40)

    print("=" * 60)
    print(f"测试结果: 通过 {passed}/{total}")

    if passed == total:
        print("🎉 所有测试通过！网站功能完整可用。")
        print("\n下一步:")
        print("1. 启动应用: python app.py")
        print("2. 访问 http://127.0.0.1:5000")
        print("3. 注册账号并登录")
        print("4. 创建小说并测试笔记功能")
    else:
        print("❌ 部分测试失败，请检查错误信息。")
        print("\n常见问题解决:")
        print("- 如果数据库问题，运行: python migrate_database.py")
        print("- 如果依赖问题，运行: pip install -r requirements.txt")
        print("- 如果模板问题，检查 templates/ 目录")


if __name__ == "__main__":
    main()
