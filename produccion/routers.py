class RQRouter:
    """
    Router para dirigir productos, kardex y clientes a 'rq',
    y todo lo demás (como consignaciones) a 'default' (Personal).
    """
    rq_models = ['producto', 'kardex', 'cliente']

    def db_for_read(self, model, **hints):
        if model._meta.model_name in self.rq_models:
            return 'rq'
        return 'default'   # 👈 si no está en rq_models, va a Personal

    def db_for_write(self, model, **hints):
        if model._meta.model_name in self.rq_models:
            return 'rq'
        return 'default'   # 👈 si no está en rq_models, va a Personal

    def allow_relation(self, obj1, obj2, **hints):
        db_list = ('default', 'rq')
        if obj1._state.db in db_list and obj2._state.db in db_list:
            return True
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        if model_name in self.rq_models:
            return False
        if app_label == 'produccion':
            return db == 'default'
        return None
