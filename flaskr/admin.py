from flask_admin import Admin, AdminIndexView
from flask_admin.contrib.sqla import ModelView
from flask_login import current_user
from flask import redirect, url_for

from .models import User, Post
from .extensions import db

class AdminMixin:
    def is_accessible(self):
        return current_user.is_authenticated and current_user.is_admin
    
    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('auth.login'))
    
# ===== 自訂首頁 =====
class MyAdminIndexView(AdminMixin, AdminIndexView):
    pass

class UserAdmin(AdminMixin, ModelView):
    page_size = 20

class PostAdmin(AdminMixin, ModelView):
    page_size = 20    

def setup_admin(app):
    admin = Admin(
        app,
        name='網站後台',
        index_view=MyAdminIndexView(),
    )
    admin.add_view(UserAdmin(User, db.session))
    admin.add_view(PostAdmin(Post, db.session))