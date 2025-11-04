# produccion/utils.py
from .models import Cliente

EMPRESA_ACTUAL = 10  # ⚡ si en algún momento cambia, lo modificas aquí solamente

def get_cliente_rq(codigo):
    """
    Devuelve el cliente de la base 'rq' filtrando por empresa actual.
    Evita romper si hay duplicados en otras empresas.
    """
    if not codigo:
        return None

    return (
        Cliente.objects.using('rq')
        .filter(empresa=EMPRESA_ACTUAL, codigo=codigo)
        .first()
    )
