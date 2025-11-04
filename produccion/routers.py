class RQRouter:
    """
    Un enrutador para controlar todas las operaciones de base de datos.
    - Dirige los modelos 'producto', 'kardex' y 'cliente' a la base de datos 'rq'.
    - Dirige el resto de los modelos a la base de datos 'default'.
    - Previene las migraciones para los modelos de la base de datos 'rq'.
    """

    # Lista de los modelos que pertenecen a la base de datos 'RQ'
    rq_models = ['producto', 'kardex', 'cliente']

    def db_for_read(self, model, **hints):
        """
        Envía las lecturas de los modelos de 'rq_models' a la base de datos 'rq'.
        """
        if model._meta.model_name in self.rq_models:
            return 'rq'
        return None

    def db_for_write(self, model, **hints):
        """
        Envía las escrituras de los modelos de 'rq_models' a la base de datos 'rq'.
        """
        if model._meta.model_name in self.rq_models:
            return 'rq'
        return None

    def allow_relation(self, obj1, obj2, **hints):
        """
        Permite relaciones:
        1. Entre dos modelos que pertenecen a la base de datos 'rq'.
        2. Entre dos modelos que pertenecen a la base de datos 'default'.
        3. Entre un modelo de 'default' y uno de 'rq' (para las consignaciones).
        """
        # Si ambos modelos son de 'rq', permite la relación.
        if obj1._meta.model_name in self.rq_models and obj2._meta.model_name in self.rq_models:
            return True
        # Si ninguno de los dos es de 'rq', significa que ambos son de 'default'. Permite la relación.
        elif obj1._meta.model_name not in self.rq_models and obj2._meta.model_name not in self.rq_models:
            return True
        # Permite relaciones entre 'default' y 'rq' (necesario para ForeignKey de Consignacion a Cliente)
        # Django no creará la restricción en la BD si usas `db_constraint=False` en el modelo.
        return True

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        """
        Controla si una migración se debe ejecutar en una base de datos específica.
        """
        # Si el modelo está en nuestra lista de 'rq_models', NUNCA ejecutes una migración.
        if model_name in self.rq_models:
            return False
        
        # Para todos los demás modelos de la app 'produccion', solo permite migraciones en la DB 'default'.
        if app_label == 'produccion':
            return db == 'default'
            
        return None

