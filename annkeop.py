import ctypes
import os

# Cargar la DLL
dll_path = os.path.abspath("NetSDK.dll")
netsdk = ctypes.CDLL(dll_path)

# Ejemplo: llamar a una función de inicialización (según la documentación del SDK)
# Por ejemplo, si la función es: BOOL NETSDK_Init()
# Primero, define el tipo de retorno y argumentos:
netsdk.NETSDK_Init.restype = ctypes.c_bool
netsdk.NETSDK_Init.argtypes = []

# Llama a la función
if netsdk.NETSDK_Init():
    print("NetSDK inicializado correctamente")
else:
    print("Error al inicializar NetSDK")

# ...aquí deberías seguir con el resto de funciones del SDK, como login, abrir stream, etc.