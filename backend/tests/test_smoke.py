import pytest


@pytest.mark.skip(reason="Falta configurar base de datos de test y datos iniciales")
def test_login_and_me(client):
  """
  Placeholder: debe probar login con credenciales validas y el endpoint /auth/me
  usando un cliente de tests configurado.
  """
  assert False


@pytest.mark.skip(reason="Falta configurar base de datos de test y datos iniciales")
def test_create_and_list_appointments(client):
  """
  Placeholder: debe crear una cita y luego comprobar que aparece en el listado,
  respetando permisos del rol autenticado.
  """
  assert False


@pytest.mark.skip(reason="Falta configurar base de datos de test y datos iniciales")
def test_permissions_admin_vs_worker_vs_client(client):
  """
  Placeholder: debe verificar que solo los roles permitidos pueden confirmar/cancelar
  o registrar sesiones, segun las reglas del negocio.
  """
  assert False
