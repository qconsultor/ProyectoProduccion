class RQRouter:
    """
    Un enrutador para controlar todas las operaciones de base de datos
    en los modelos relacionados con la base de datos RQ.
    """
    def db_for_read(self, model, **hints):
        if model._meta.app_label == 'produccion' and model._meta.model_name in ['producto', 'kardex']:
            return 'rq'
        return None

    def db_for_write(self, model, **hints):
        if model._meta.app_label == 'produccion' and model._meta.model_name in ['producto', 'kardex']:
            return 'rq'
        return None

    def allow_relation(self, obj1, obj2, **hints):
        # Permite relaciones si ambos objetos están en la base de datos rhqm.
        if obj1._meta.app_label == 'produccion' and obj1._meta.model_name in ['producto', 'kardex'] and \
           obj2._meta.app_label == 'produccion' and obj2._meta.model_name in ['producto', 'kardex']:
           return True
        # Por ahora, no permitimos relaciones entre las dos bases de datos
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        if app_label == 'produccion' and model_name in ['producto', 'kardex']:
            # Evita que se ejecuten migraciones para Producto y Kardex en CUALQUIER base de datos
            return False

        # Para todos los demás modelos de 'produccion', solo permite migraciones en la DB 'default'
        if app_label == 'produccion':
            return db == 'default'

        return None