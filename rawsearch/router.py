class AuthRouter:
    """
    Router for Auth Group databases It's not the most efficient way to do that, but it's working.
    """
    route_app_labels = {'auth', 'contenttypes', 'sessions', 'admin', 'admin_honeypot'}

    def db_for_read(self, model, **hints):
        if model._meta.app_label in self.route_app_labels:
            return 'users_db'
        return None

    def db_for_write(self, model, **hints):
        if model._meta.app_label in self.route_app_labels:
            return 'users_db'
        return None

    def allow_relation(self, obj1, obj2, **hints):
        if (
            obj1._meta.app_label in self.route_app_labels or
            obj2._meta.app_label in self.route_app_labels
        ):
           return True
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        if app_label in self.route_app_labels:
            return db == 'users_db'
        return None


class CheckerRouter:
    """
    Router for others DB.
    """
    route_app_labels = {'users', 'feedback', 'analytics', 'core', 'crawler'}

    def db_for_read(self, model, **hints):
        if model._meta.app_label == 'users':
            return 'users_db'
        elif model._meta.app_label == 'feedback':
            return 'feedback_db'
        elif model._meta.app_label == 'analytics':
            return 'analytics_db'
        elif model._meta.app_label == 'core':
            return 'search_db'
        elif model._meta.app_label == 'crawler':
            return 'crawler_db'
        return 'default'

    def db_for_write(self, model, **hints):
        if model._meta.app_label == 'users':
            return 'users_db'
        elif model._meta.app_label == 'feedback':
            return 'feedback_db'
        elif model._meta.app_label == 'analytics':
            return 'analytics_db'
        elif model._meta.app_label == 'core':
            return 'search_db'
        elif model._meta.app_label == 'crawler':
            return 'crawler_db'
        return 'default'

    def allow_relation(self, obj1, obj2, **hints):
        if obj1._meta.app_label == 'users' or obj2._meta.app_label == 'users':
            return True
        elif 'users' not in [obj1._meta.app_label, obj2._meta.app_label]:
            return True

        elif obj1._meta.app_label == 'feedback' or obj2._meta.app_label == 'feedback':
            return True
        elif 'feedback' not in [obj1._meta.app_label, obj2._meta.app_label]:
            return True

        elif obj1._meta.app_label == 'analytics' or obj2._meta.app_label == 'analytics':
            return True
        elif 'analytics' not in [obj1._meta.app_label, obj2._meta.app_label]:
            return True

        elif obj1._meta.app_label == 'core' or obj2._meta.app_label == 'core':
            return True
        elif 'core' not in [obj1._meta.app_label, obj2._meta.app_label]:
            return True

        elif obj1._meta.app_label == 'crawler' or obj2._meta.app_label == 'crawler':
            return True
        elif 'crawler' not in [obj1._meta.app_label, obj2._meta.app_label]:
            return True

        return False

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        if app_label == 'users':
            return db == 'users_db'

        elif app_label == 'feedback':
            return db == 'feedback_db'

        elif app_label == 'analytics':
            return db == 'analytics_db'

        elif app_label == 'core':
            return db == 'search_db'

        elif app_label == 'crawler':
            return 'crawler_db'
        return None

