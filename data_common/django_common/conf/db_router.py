from data_common.django_common.conf import settings

DATABASE_MAPPING = settings.DATABASE_APPS_MAPPING


class DatabaseAppsRouter(object):
    """
    数据库自动路由
    使用多数据库最简单的方法是建立一个数据库路由模式。
    默认的路由模式确保对象"粘滞"在它们原始的数据库上（例如，从foo数据库中获取的对象将保存在同一个数据库中）。
    默认的路由模式还确保如果没有指明数据库，所有的查询都回归到default数据库中。
    你不需要做任何事情来激活默认的路由模式
    —— 它在每个Django项目上"直接"提供。然而，如果你想实现更有趣的数据库分配行为，你可以定义并安装你自己的数据库路由。

    数据库路由
    数据库路由是一个类，它提供4个方法：
        db_for_read(model, **hints)
        建议model类型的对象的读操作应该使用的数据库。
        如果一个数据库操作能够提供其它额外的信息可以帮助选择一个数据库，它将在hints字典中提供。合法的hints
        的详细信息在下文给出。如果没有建议，则返回None。

        db_for_write(model, **hints)
        建议Model类型的对象的写操作应该使用的数据库。
        如果一个数据库操作能够提供其它额外的信息可以帮助选择一个数据库，它将在hints字典中提供。 合法的hints
        的详细信息在下文给出。如果没有建议，则返回None。

        allow_relation(obj1, obj2, **hints)
        如果obj1和obj2之间应该允许关联则返回True，如果应该防止关联则返回False，如果路由无法判断则返回None。
        这是纯粹的验证操作，外键和多对多操作使用它来决定两个对象之间是否应该允许一个关联。

        allow_migrate(db, app_label, model_name=None, **hints)
        定义迁移操作是否允许在别名为db的数据库上运行。如果操作应该运行则返回True ，如果不应该运行则返回False，如果路由无法判断则返回None。
        位置参数app_label是正在迁移的应用的标签。
        大部分迁移操作设置model_name的值为正在迁移的模型的model._meta.model_name（模型的__name__的小写）。对于RunPython和RunSQL
        操作它的值为None，除非这两个操作使用hint提供它。

        hints
        用于某些操作来传递额外的信息给路由。当设置了model_name时，hints通常通过键'model'包含该模型的类。
        注意，它可能是一个历史模型，因此不会有自定的属性、方法或管理器。你应该只依赖_meta。这个方法还可以用来决定一个给定数据库上某个模型的可用性。

        数据库路由使用DATABASE_ROUTERS 设置安装。这个设置定义一个类名的列表，其中每个类表示一个路由，它们将被主路由（django.db.router）使用
    A router to control all database operations on models for different
    databases.

    In case an app is not set in settings.DATABASE_APPS_MAPPING, the router
    will fallback to the `default` database.

    Settings example:

    DATABASE_APPS_MAPPING = {'app1': 'db1', 'app2': 'db2'}
    """

    @staticmethod
    def db_for_read(model, **hints):
        """"Point all read operations to the specific database."""
        if model._meta.app_label in DATABASE_MAPPING:
            return DATABASE_MAPPING[model._meta.app_label]
        return None

    @staticmethod
    def db_for_write(model, **hints):
        """Point all write operations to the specific database."""
        if model._meta.app_label in DATABASE_MAPPING:
            return DATABASE_MAPPING[model._meta.app_label]
        return None

    @staticmethod
    def allow_relation(obj1, obj2, **hints):
        """Allow any relation between apps that use the same database."""
        db_obj1 = DATABASE_MAPPING.get(obj1._meta.app_label)
        db_obj2 = DATABASE_MAPPING.get(obj2._meta.app_label)
        if db_obj1 and db_obj2:
            if db_obj1 == db_obj2:
                return True
            else:
                return False
        return None

    @staticmethod
    def allow_syncdb(db, model):
        """Make sure that apps only appear in the related database."""

        if db in DATABASE_MAPPING.values():
            return DATABASE_MAPPING.get(model._meta.app_label) == db
        elif model._meta.app_label in DATABASE_MAPPING:
            return False
        return None

    @staticmethod
    def allow_migrate(db, app_label, model=None, **hints):
        """
        Make sure the auth app only appears in the 'auth_db'
        database.
        """
        if db in DATABASE_MAPPING.values():
            return DATABASE_MAPPING.get(app_label) == db
        elif app_label in DATABASE_MAPPING:
            return False
        return None