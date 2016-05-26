from rest_framework.routers import SimpleRouter, DefaultRouter


class SharedAPIRootRouter(SimpleRouter):
    shared_router = DefaultRouter(trailing_slash=False)

    def register(self, *args, **kwargs):
        self.shared_router.register(*args, **kwargs)

        super().register(*args, **kwargs)
