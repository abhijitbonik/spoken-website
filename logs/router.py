from builtins import object


class LogsRouter(object):
    """A router to manage database operations in the logs app.
    """
    def db_for_read(self, model, **hints):
        """Point all read operations on logs app to spoken database.
        """
        if model._meta.app_label == 'logs':
            return 'logs'
        return None

    def db_for_write(self, model, **hints):

        if model._meta.app_label in self.router.app_labels:
            return 'logs'
        return None

    def allow_relation(self, obj1, obj2, **hints):
        return True

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        
        if app_label in self.route_app_labels:
            return db == 'logs'
        return None