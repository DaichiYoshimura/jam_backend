from rest_framework.routers import Route, DynamicRoute, DefaultRouter
from rest_framework_nested import routers as NestedRouters


class CustomRouter(DefaultRouter):
    routes = [
        # List route.
        Route(
            url=r'^{prefix}{trailing_slash}$',
            mapping={
                'get': 'list',
                'post': 'create',
                'put': 'update',
                'delete': 'destroy'
            },
            name='{basename}-list',
            detail=False,
            initkwargs={'suffix': 'List'}
        ),
        # Dynamically generated list routes. Generated using
        # @action(detail=False) decorator on methods of the viewset.
        DynamicRoute(
            url=r'^{prefix}/{url_path}{trailing_slash}$',
            name='{basename}-{url_name}',
            detail=False,
            initkwargs={}
        ),
        # Detail route.
        Route(
            url=r'^{prefix}/{lookup}{trailing_slash}$',
            mapping={
                'get': 'retrieve',
                'post': 'create',
                'put': 'update',
                'patch': 'partial_update',
                'delete': 'destroy'
            },
            name='{basename}-detail',
            detail=True,
            initkwargs={'suffix': 'Instance'}
        ),
        # Dynamically generated detail routes. Generated using
        # @action(detail=True) decorator on methods of the viewset.
        DynamicRoute(
            url=r'^{prefix}/{lookup}/{url_path}{trailing_slash}$',
            name='{basename}-{url_name}',
            detail=True,
            initkwargs={}
        ),
    ]

    def extend(self, router):
        self.registry.extend(router.registry)


class DefaultRouter(NestedRouters.DefaultRouter):

    def extend(self, router):
        self.registry.extend(router.registry)


class NestedDefaultRouter(NestedRouters.NestedDefaultRouter):

    def extend(self, router):
        self.registry.extend(router.registry)


class SimpleRouter(NestedRouters.SimpleRouter):

    def extend(self, router):
        self.registry.extend(router.registry)


class NestedSimpleRouter(NestedRouters.NestedSimpleRouter):

    def extend(self, router):
        self.registry.extend(router.registry)
