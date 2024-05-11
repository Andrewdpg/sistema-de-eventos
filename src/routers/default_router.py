class DefaultRouter:
    default_db = ['admin', 'auth', 'contenttypes', 'sessions']

    def db_for_read(self, model, **hints):
        if model._meta.app_label in self.default_db:
            return 'django_db'
        return None
    
    def db_for_write(self, model, **hints):
        if model._meta.app_label in self.default_db:
            return 'django_db'
        return None
    
    def allow_relation(self, obj1, obj2, **hints):
        if obj1._meta.app_label in self.default_db and \
           obj2._meta.app_label in self.default_db:
            return 'django_db'
        return None
    
    def allow_migrate(self, db, app_label, model_name=None, **hints):
        if app_label in self.default_db:
            return db == 'django_db'
        return None