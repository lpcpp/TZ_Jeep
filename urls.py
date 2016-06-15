# -*- coding: utf-8 -*-
import index
import auth.urls

urlpatterns = [
    (r"/?", index.IndexHandler),
]


urlpatterns += auth.urls.urlpatterns
