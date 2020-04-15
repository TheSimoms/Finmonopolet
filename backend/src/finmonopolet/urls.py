from django.urls import include, path

from products.urls import product_router


urlpatterns = [
    path('api/', include([
        path('', include(product_router.urls)),
    ])),
]
