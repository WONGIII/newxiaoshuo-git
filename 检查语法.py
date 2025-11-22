import os
import sys


def check_python_syntax():
    """检查Python文件的语法"""
    print("正在检查Python文件语法...")
    print("=" * 50)

    files_to_check = ["app.py", "models.py", "run.py"]

    all_passed = True

    for filename in files_to_check:
        if not os.path.exists(filename):
            print(f"❌ 文件不存在: {filename}")
            all_passed = False
            continue

        try:
            with open(filename, "r", encoding="utf-8") as f:
                source_code = f.read()

            # 编译检查语法
            compile(source_code, filename, "exec")
            print(f"✅ {filename} - 语法正确")

        except SyntaxError as e:
            print(f"❌ {filename} - 语法错误")
            print(f"   错误位置: 第{e.lineno}行, 第{e.offset}列")
            print(f"   错误信息: {e.msg}")
            all_passed = False
        except Exception as e:
            print(f"❌ {filename} - 检查失败: {e}")
            all_passed = False

    print("=" * 50)
    if all_passed:
        print("🎉 所有文件语法检查通过！")
        return True
    else:
        print("⚠️  发现语法错误，请修复后再运行")
        return False


def check_imports():
    """检查导入是否正常"""
    print("\n正在检查导入...")
    print("=" * 50)

    try:
        from app import app, db

        print("✅ app.py 导入正常")
    except Exception as e:
        print(f"❌ app.py 导入失败: {e}")
        return False

    try:
        from models import Chapter, Comment, Message, Novel, User

        print("✅ models.py 导入正常")
    except Exception as e:
        print(f"❌ models.py 导入失败: {e}")
        return False

    print("=" * 50)
    print("✅ 所有导入检查通过！")
    return True


if __name__ == "__main__":
    print("优雅小说网站 - 语法检查工具")
    print("=" * 50)

    # 检查当前目录
    if not os.path.exists("app.py"):
        print("❌ 请在项目根目录运行此脚本")
        sys.exit(1)

    syntax_ok = check_python_syntax()
    imports_ok = check_imports()

    if syntax_ok and imports_ok:
        print("\n🎉 所有检查通过！可以运行网站了。")
        print("运行命令: python run.py")
    else:
        print("\n❌ 检查未通过，请修复问题后再运行。")
        sys.exit(1)
