from admin import views

urlpatterns = [
    (r"/admin/?", views.AdminHandler),
    (r"/admin/login/?", views.LoginHandler),
    (r"/admin/logout/?", views.LogoutHandler),
    (r"/admin/user_list/?", views.AdminUserListHandler),
    (r"/admin/add_user/?", views.AddUserHandler),
    (r"/admin/check_user/?", views.CheckUserHandler),
    (r"/admin/change_user_info/([a-zA-Z0-9]+)/?", views.ChangeUserInfoHandler),
]
