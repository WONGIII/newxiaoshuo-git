import json
import os
from datetime import datetime
from functools import wraps

from flask import (
    Flask,
    flash,
    jsonify,
    redirect,
    render_template,
    request,
    session,
    url_for,
)
from werkzeug.security import check_password_hash, generate_password_hash

from models import Chapter, Comment, Draft, Message, Novel, User, UserSettings, db

app = Flask(__name__)
app.config["SECRET_KEY"] = "your-secret-key-here"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///novel.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)


# 装饰器
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "user_id" not in session:
            flash("请先登录", "warning")
            return redirect(url_for("login"))
        return f(*args, **kwargs)

    return decorated_function


def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "user_id" not in session:
            flash("请先登录", "warning")
            return redirect(url_for("login"))
        user = User.query.get(session["user_id"])
        if user.role not in ["admin", "super_admin"]:
            flash("权限不足", "danger")
            return redirect(url_for("index"))
        return f(*args, **kwargs)

    return decorated_function


# 路由
@app.route("/")
def index():
    novels = Novel.query.order_by(Novel.updated_at.desc()).limit(12).all()
    return render_template("index.html", novels=novels)


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        email = request.form["email"]
        password = request.form["password"]

        if User.query.filter_by(username=username).first():
            flash("用户名已存在", "danger")
            return render_template("register.html")

        if User.query.filter_by(email=email).first():
            flash("邮箱已被注册", "danger")
            return render_template("register.html")

        user = User(username=username, email=email)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()

        flash("注册成功，请登录", "success")
        return redirect(url_for("login"))

    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        user = User.query.filter_by(username=username).first()

        if user and user.check_password(password):
            session["user_id"] = user.id
            session["username"] = user.username
            session["role"] = user.role
            flash("登录成功", "success")
            return redirect(url_for("index"))
        else:
            flash("用户名或密码错误", "danger")

    return render_template("login.html")


@app.route("/logout")
def logout():
    session.clear()
    flash("已退出登录", "info")
    return redirect(url_for("index"))


@app.route("/novel/<int:novel_id>")
def novel_detail(novel_id):
    novel = Novel.query.get_or_404(novel_id)
    chapters = (
        Chapter.query.filter_by(novel_id=novel_id)
        .order_by(Chapter.chapter_number)
        .all()
    )
    comments = (
        Comment.query.filter_by(novel_id=novel_id)
        .order_by(Comment.created_at.desc())
        .limit(10)
        .all()
    )
    return render_template(
        "novel_detail.html", novel=novel, chapters=chapters, comments=comments
    )


@app.route("/read/<int:novel_id>/<int:chapter_number>")
def read_chapter(novel_id, chapter_number):
    novel = Novel.query.get_or_404(novel_id)
    chapter = Chapter.query.filter_by(
        novel_id=novel_id, chapter_number=chapter_number
    ).first_or_404()
    chapters = (
        Chapter.query.filter_by(novel_id=novel_id)
        .order_by(Chapter.chapter_number)
        .all()
    )

    prev_chapter = Chapter.query.filter_by(
        novel_id=novel_id, chapter_number=chapter_number - 1
    ).first()
    next_chapter = Chapter.query.filter_by(
        novel_id=novel_id, chapter_number=chapter_number + 1
    ).first()

    return render_template(
        "read.html",
        novel=novel,
        chapter=chapter,
        chapters=chapters,
        prev_chapter=prev_chapter,
        next_chapter=next_chapter,
    )


@app.route("/author/dashboard")
@login_required
def author_dashboard():
    user_id = session["user_id"]
    novels = (
        Novel.query.filter_by(author_id=user_id).order_by(Novel.updated_at.desc()).all()
    )

    # 计算统计信息
    total_chapters = sum(len(novel.chapters) for novel in novels)
    total_comments = sum(len(novel.comments) for novel in novels)
    ongoing_novels = sum(1 for novel in novels if novel.status == "ongoing")

    return render_template(
        "author_dashboard.html",
        novels=novels,
        total_chapters=total_chapters,
        total_comments=total_comments,
        ongoing_novels=ongoing_novels,
    )


@app.route("/author/novel/new", methods=["GET", "POST"])
@login_required
def create_novel():
    if request.method == "POST":
        title = request.form["title"]
        description = request.form["description"]
        cover_image = request.form.get("cover_image", "")

        novel = Novel(
            title=title,
            description=description,
            cover_image=cover_image,
            author_id=session["user_id"],
        )
        db.session.add(novel)
        db.session.commit()

        flash("小说创建成功", "success")
        return redirect(url_for("author_dashboard"))

    return render_template("create_novel.html")


@app.route("/author/novel/<int:novel_id>/edit", methods=["GET", "POST"])
@login_required
def edit_novel(novel_id):
    novel = Novel.query.get_or_404(novel_id)
    if novel.author_id != session["user_id"] and session.get("role") not in [
        "admin",
        "super_admin",
    ]:
        flash("权限不足", "danger")
        return redirect(url_for("author_dashboard"))

    if request.method == "POST":
        novel.title = request.form["title"]
        novel.description = request.form["description"]
        novel.status = request.form["status"]
        novel.cover_image = request.form.get("cover_image", "")
        db.session.commit()
        flash("小说信息已更新", "success")
        return redirect(url_for("author_dashboard"))

    return render_template("edit_novel.html", novel=novel)


@app.route("/author/novel/<int:novel_id>/chapter/new", methods=["GET", "POST"])
@login_required
def create_chapter(novel_id):
    novel = Novel.query.get_or_404(novel_id)
    if novel.author_id != session["user_id"]:
        flash("权限不足", "danger")
        return redirect(url_for("author_dashboard"))

    if request.method == "POST":
        title = request.form["title"]
        content = request.form["content"]
        author_note = request.form.get("author_note", "")

        # 获取当前最大章节号
        last_chapter = (
            Chapter.query.filter_by(novel_id=novel_id)
            .order_by(Chapter.chapter_number.desc())
            .first()
        )
        chapter_number = last_chapter.chapter_number + 1 if last_chapter else 1

        chapter = Chapter(
            title=title,
            content=content,
            author_note=author_note,
            chapter_number=chapter_number,
            novel_id=novel_id,
        )
        db.session.add(chapter)

        # 更新小说的更新时间
        novel.updated_at = datetime.utcnow()
        db.session.commit()

        flash("章节发布成功", "success")
        return redirect(url_for("novel_detail", novel_id=novel_id))

    return render_template("create_chapter.html", novel=novel)


@app.route("/author/chapter/<int:chapter_id>/edit", methods=["GET", "POST"])
@login_required
def edit_chapter(chapter_id):
    chapter = Chapter.query.get_or_404(chapter_id)
    novel = Novel.query.get(chapter.novel_id)

    if novel.author_id != session["user_id"] and session.get("role") not in [
        "admin",
        "super_admin",
    ]:
        flash("权限不足", "danger")
        return redirect(url_for("author_dashboard"))

    if request.method == "POST":
        chapter.title = request.form["title"]
        chapter.content = request.form["content"]
        chapter.author_note = request.form.get("author_note", "")
        db.session.commit()

        # 更新小说的更新时间
        novel.updated_at = datetime.utcnow()
        db.session.commit()

        flash("章节已更新", "success")
        return redirect(url_for("novel_detail", novel_id=novel.id))

    return render_template("edit_chapter.html", chapter=chapter, novel=novel)


@app.route("/author/chapter/<int:chapter_id>/delete", methods=["POST"])
@login_required
def delete_chapter(chapter_id):
    chapter = Chapter.query.get_or_404(chapter_id)
    novel = Novel.query.get(chapter.novel_id)

    # 检查权限
    if novel.author_id != session["user_id"] and session.get("role") not in [
        "admin",
        "super_admin",
    ]:
        flash("权限不足", "danger")
        return redirect(url_for("author_dashboard"))

    # 删除章节
    db.session.delete(chapter)
    db.session.commit()

    # 更新小说的更新时间
    novel.updated_at = datetime.utcnow()
    db.session.commit()

    flash("章节删除成功", "success")
    return redirect(url_for("novel_detail", novel_id=novel.id))


@app.route("/comment/<int:novel_id>", methods=["POST"])
@login_required
def add_comment(novel_id):
    content = request.form["content"]
    chapter_id = request.form.get("chapter_id")

    comment = Comment(
        content=content,
        user_id=session["user_id"],
        novel_id=novel_id,
        chapter_id=chapter_id,
    )
    db.session.add(comment)
    db.session.commit()

    flash("评论发布成功", "success")
    return redirect(url_for("novel_detail", novel_id=novel_id))


@app.route("/author/novel/<int:novel_id>/delete", methods=["POST"])
@login_required
def delete_novel(novel_id):
    novel = Novel.query.get_or_404(novel_id)

    # 检查权限
    if novel.author_id != session["user_id"] and session.get("role") not in [
        "admin",
        "super_admin",
    ]:
        flash("权限不足", "danger")
        return redirect(url_for("author_dashboard"))

    # 删除相关章节和评论
    Chapter.query.filter_by(novel_id=novel_id).delete()
    Comment.query.filter_by(novel_id=novel_id).delete()

    # 删除小说
    db.session.delete(novel)
    db.session.commit()

    flash("小说删除成功", "success")
    return redirect(url_for("author_dashboard"))


@app.route("/admin")
@admin_required
def admin_dashboard():
    users = User.query.all()
    novels = Novel.query.all()

    # 计算统计信息
    total_chapters = sum(len(novel.chapters) for novel in novels)
    total_comments = sum(len(novel.comments) for novel in novels)

    # 用户角色统计
    reader_count = sum(1 for user in users if user.role == "reader")
    admin_count = sum(1 for user in users if user.role == "admin")
    super_admin_count = sum(1 for user in users if user.role == "super_admin")

    # 作品状态统计
    ongoing_novels = sum(1 for novel in novels if novel.status == "ongoing")
    completed_novels = sum(1 for novel in novels if novel.status == "completed")

    return render_template(
        "admin_dashboard.html",
        users=users,
        novels=novels,
        total_chapters=total_chapters,
        total_comments=total_comments,
        reader_count=reader_count,
        admin_count=admin_count,
        super_admin_count=super_admin_count,
        ongoing_novels=ongoing_novels,
        completed_novels=completed_novels,
    )


@app.route("/admin/user/<int:user_id>/role", methods=["POST"])
@admin_required
def change_user_role(user_id):
    if session.get("role") != "super_admin":
        flash("权限不足", "danger")
        return redirect(url_for("admin_dashboard"))

    user = User.query.get_or_404(user_id)
    new_role = request.form["role"]
    user.role = new_role
    db.session.commit()

    flash(f"用户 {user.username} 的角色已更新为 {new_role}", "success")
    return redirect(url_for("admin_dashboard"))


# 笔记功能路由
@app.route("/author/novel/<int:novel_id>/drafts")
@login_required
def novel_drafts(novel_id):
    novel = Novel.query.get_or_404(novel_id)
    if novel.author_id != session["user_id"]:
        flash("权限不足", "danger")
        return redirect(url_for("author_dashboard"))

    drafts = (
        Draft.query.filter_by(novel_id=novel_id, user_id=session["user_id"])
        .order_by(Draft.updated_at.desc())
        .all()
    )
    return render_template("drafts_list.html", novel=novel, drafts=drafts)


@app.route("/author/novel/<int:novel_id>/draft/new")
@login_required
def create_draft(novel_id):
    novel = Novel.query.get_or_404(novel_id)
    if novel.author_id != session["user_id"]:
        flash("权限不足", "danger")
        return redirect(url_for("author_dashboard"))

    draft = Draft(
        title="无标题草稿", content="", novel_id=novel_id, user_id=session["user_id"]
    )
    db.session.add(draft)
    db.session.commit()

    return redirect(url_for("edit_draft", draft_id=draft.id))


@app.route("/author/draft/<int:draft_id>")
@login_required
def edit_draft(draft_id):
    draft = Draft.query.get_or_404(draft_id)
    if draft.user_id != session["user_id"]:
        flash("权限不足", "danger")
        return redirect(url_for("author_dashboard"))

    novel = Novel.query.get(draft.novel_id)
    user_settings = UserSettings.query.filter_by(user_id=session["user_id"]).first()

    return render_template(
        "draft_editor.html", draft=draft, novel=novel, user_settings=user_settings
    )


@app.route("/author/draft/<int:draft_id>/save", methods=["POST"])
@login_required
def save_draft(draft_id):
    draft = Draft.query.get_or_404(draft_id)
    if draft.user_id != session["user_id"]:
        return jsonify({"success": False, "error": "权限不足"})

    data = request.get_json()
    draft.title = data.get("title", draft.title)
    draft.content = data.get("content", draft.content)
    db.session.commit()

    return jsonify({"success": True, "updated_at": draft.updated_at.isoformat()})


@app.route("/author/draft/<int:draft_id>/publish", methods=["POST"])
@login_required
def publish_draft(draft_id):
    draft = Draft.query.get_or_404(draft_id)
    if draft.user_id != session["user_id"]:
        flash("权限不足", "danger")
        return redirect(url_for("author_dashboard"))

    novel = Novel.query.get(draft.novel_id)

    # 获取当前最大章节号
    last_chapter = (
        Chapter.query.filter_by(novel_id=novel.id)
        .order_by(Chapter.chapter_number.desc())
        .first()
    )
    chapter_number = last_chapter.chapter_number + 1 if last_chapter else 1

    chapter = Chapter(
        title=draft.title,
        content=draft.content,
        chapter_number=chapter_number,
        novel_id=novel.id,
    )
    db.session.add(chapter)

    # 标记草稿为已发布
    draft.is_published = True
    draft.chapter_number = chapter_number

    # 更新小说的更新时间
    novel.updated_at = datetime.utcnow()
    db.session.commit()

    flash("章节发布成功", "success")
    return redirect(url_for("novel_detail", novel_id=novel.id))


@app.route("/author/draft/<int:draft_id>/delete", methods=["POST"])
@login_required
def delete_draft(draft_id):
    draft = Draft.query.get_or_404(draft_id)
    if draft.user_id != session["user_id"]:
        flash("权限不足", "danger")
        return redirect(url_for("author_dashboard"))

    novel_id = draft.novel_id
    db.session.delete(draft)
    db.session.commit()

    flash("草稿删除成功", "success")
    return redirect(url_for("novel_drafts", novel_id=novel_id))


@app.route("/author/settings", methods=["GET", "POST"])
@login_required
def user_settings():
    user_settings = UserSettings.query.filter_by(user_id=session["user_id"]).first()
    user = User.query.get(session["user_id"])

    if not user_settings:
        user_settings = UserSettings(user_id=session["user_id"])
        db.session.add(user_settings)
        db.session.commit()

    if request.method == "POST":
        # 处理昵称更新
        nickname = request.form.get("nickname", "").strip()
        if nickname:
            user_settings.nickname = nickname

        # 处理密码更新
        current_password = request.form.get("current_password", "")
        new_password = request.form.get("new_password", "")
        confirm_password = request.form.get("confirm_password", "")

        if current_password and new_password and confirm_password:
            if user.check_password(current_password):
                if new_password == confirm_password:
                    user.set_password(new_password)
                    flash("密码更新成功", "success")
                else:
                    flash("新密码和确认密码不匹配", "danger")
            else:
                flash("当前密码错误", "danger")

        # 处理AI设置
        user_settings.openai_api_key = request.form.get("openai_api_key", "")
        user_settings.openai_base_url = request.form.get("openai_base_url", "")
        user_settings.openai_model = request.form.get("openai_model", "")

        db.session.commit()
        flash("设置已保存", "success")
        return redirect(url_for("user_settings"))

    return render_template("user_settings.html", user_settings=user_settings, user=user)


@app.route("/author/ai/assist", methods=["POST"])
@login_required
def ai_assist():
    user_settings = UserSettings.query.filter_by(user_id=session["user_id"]).first()

    if not user_settings or not user_settings.openai_api_key:
        return jsonify({"success": False, "error": "请先配置AI设置"})

    try:
        import openai

        # 配置 OpenAI 设置（兼容 0.28.1 版本）
        openai.api_key = user_settings.openai_api_key
        openai.api_base = user_settings.openai_base_url or "https://api.deepseek.com"

        data = request.get_json()
        prompt = data.get("prompt", "")
        context = data.get("context", "")

        messages = [
            {
                "role": "system",
                "content": "你是一个专业的小说写作助手，帮助作家创作和润色小说内容。",
            },
            {"role": "user", "content": f"上下文：{context}\n\n请求：{prompt}"},
        ]

        response = openai.ChatCompletion.create(
            model=user_settings.openai_model or "gpt-3.5-turbo",
            messages=messages,
            stream=False,
        )

        result = response.choices[0].message.content
        return jsonify({"success": True, "result": result})

    except Exception as e:
        return jsonify({"success": False, "error": str(e)})


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
