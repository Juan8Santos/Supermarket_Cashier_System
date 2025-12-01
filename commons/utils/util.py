def entrar_int_personalizado(msg_personalizado, num_min, num_max):
  while (True):
    try:
        entrada = int(input(msg_personalizado))
        if (entrada < num_min or entrada > num_max):
            raise ValueError
        break
    except ValueError:
      print("Erro! valor inválido.")
  return entrada

def entrar_int(msg_personalizado):
  while (True):
    try:
        entrada = int(input(msg_personalizado))
        break
    except ValueError:
      print("Erro! valor inválido.")
  return entrada

def entrar_float(msg_personalizado):
  while (True):
    try:
        entrada = float(input(msg_personalizado))
        break
    except ValueError:
      print("Erro! valor inválido.")
  return entrada