import os
import sqlite3
from datetime import datetime


def migrate_database():
    """迁移数据库，添加新的字段到现有表"""
    db_path = "novel.db"

    if not os.path.exists(db_path):
        print("数据库文件不存在，无需迁移")
        return

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    try:
        # 检查user_settings表是否存在
        cursor.execute(
            "SELECT name FROM sqlite_master WHERE type='table' AND name='user_settings'"
        )
        user_settings_exists = cursor.fetchone()

        if user_settings_exists:
            # 检查是否已经有nickname字段
            cursor.execute("PRAGMA table_info(user_settings)")
            columns = [column[1] for column in cursor.fetchall()]

            if "nickname" not in columns:
                print("正在添加nickname字段到user_settings表...")
                # 创建临时表
                cursor.execute("""
                    CREATE TABLE user_settings_new (
                        id INTEGER PRIMARY KEY,
                        user_id INTEGER NOT NULL UNIQUE,
                        nickname TEXT,
                        openai_api_key TEXT,
                        openai_base_url TEXT,
                        openai_model TEXT,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        FOREIGN KEY (user_id) REFERENCES user (id)
                    )
                """)

                # 复制数据到新表
                cursor.execute("""
                    INSERT INTO user_settings_new
                    (id, user_id, openai_api_key, openai_base_url, openai_model, created_at, updated_at)
                    SELECT id, user_id, openai_api_key, openai_base_url, openai_model, created_at, updated_at
                    FROM user_settings
                """)

                # 删除旧表
                cursor.execute("DROP TABLE user_settings")

                # 重命名新表
                cursor.execute("ALTER TABLE user_settings_new RENAME TO user_settings")

                print("✓ user_settings表迁移完成")
            else:
                print("✓ user_settings表已包含nickname字段")
        else:
            print("user_settings表不存在，无需迁移")

        # 检查draft表是否存在
        cursor.execute(
            "SELECT name FROM sqlite_master WHERE type='table' AND name='draft'"
        )
        draft_exists = cursor.fetchone()

        if not draft_exists:
            print("正在创建draft表...")
            cursor.execute("""
                CREATE TABLE draft (
                    id INTEGER PRIMARY KEY,
                    title VARCHAR(200) NOT NULL DEFAULT '无标题草稿',
                    content TEXT DEFAULT '',
                    novel_id INTEGER NOT NULL,
                    user_id INTEGER NOT NULL,
                    is_published BOOLEAN DEFAULT 0,
                    chapter_number INTEGER,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (novel_id) REFERENCES novel (id),
                    FOREIGN KEY (user_id) REFERENCES user (id)
                )
            """)
            print("✓ draft表创建完成")
        else:
            print("✓ draft表已存在")

        conn.commit()
        print("🎉 数据库迁移完成！")

    except Exception as e:
        conn.rollback()
        print(f"❌ 迁移失败: {e}")
        raise
    finally:
        conn.close()


def backup_database():
    """备份数据库"""
    db_path = "novel.db"
    if os.path.exists(db_path):
        backup_path = f"novel_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.db"
        import shutil

        shutil.copy2(db_path, backup_path)
        print(f"✓ 数据库已备份到: {backup_path}")
        return backup_path
    return None


def main():
    """主函数"""
    print("开始数据库迁移...")
    print("=" * 50)

    # 备份数据库
    backup_file = backup_database()
    if backup_file:
        print(f"备份文件: {backup_file}")

    print("-" * 50)

    try:
        migrate_database()
    except Exception as e:
        print(f"\n❌ 迁移过程中出现错误: {e}")
        if backup_file:
            print(f"您可以从备份文件恢复: {backup_file}")
        exit(1)

    print("=" * 50)
    print("✅ 所有迁移操作已完成！")
    print("\n下一步:")
    print("1. 重新启动应用: python app.py")
    print("2. 访问 http://127.0.0.1:5000")
    print("3. 测试笔记功能是否正常工作")


if __name__ == "__main__":
    main()
