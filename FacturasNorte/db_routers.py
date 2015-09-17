from FacturasNorte.models import ClienteLegado

__author__ = 'Julian'

class FacturasNorteRouter(object):
    """
    A router to control all database operations on models in the application.
    """
    def db_for_read(self, model, **hints):
        if model == ClienteLegado:
            return 'clientes_legados'
        return 'default'

    def db_for_write(self, model, **hints):
        if model == ClienteLegado:
            return 'clientes_legados'
        return 'default'