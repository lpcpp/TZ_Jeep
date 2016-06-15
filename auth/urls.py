from auth import views

urlpatterns = [
    (r"/register/?", views.RegisterHandler),
    (r"/login/?", views.LoginHandler),
    (r"/jslogin/?", views.JsLoginHandler),
    (r"/logout/?", views.LogoutHandler),
]
