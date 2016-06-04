from finmonopolet.api import SharedAPIRootRouter, ForeignKeyViewSet


SharedAPIRootRouter().register(r'categories', ForeignKeyViewSet, base_name='categories')
