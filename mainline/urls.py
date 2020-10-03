from django.contrib import admin
from django.urls import path, include

from kakao_i_hanyang import url as kakao_i_router

urlpatterns = [
    path('admin/', admin.site.urls),
    path('kakao/', include(kakao_i_router)),
    # path('web/', include(web))
]
