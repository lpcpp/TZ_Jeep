from admin import views

urlpatterns = [
    (r"/admin/?", views.AdminHandler),
    (r"/admin/login/?", views.LoginHandler),
    (r"/admin/logout/?", views.LogoutHandler),
    (r"/admin/add_user/?", views.AddUserHandler),
    (r"/admin/check_user/?", views.CheckUserHandler),
]
