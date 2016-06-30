from auth import views

urlpatterns = [
    (r"/register/?", views.RegisterHandler),
    (r"/login/?", views.LoginHandler),
    (r"/member/?", views.InfoHandler),
    (r"/auth/transaction/([a-z]*)/?", views.TransactionHandler),
    (r"/auth/review_list/?", views.ReviewHandler),
    (r"/jslogin/?", views.JsLoginHandler),
    (r"/logout/?", views.LogoutHandler),
]
