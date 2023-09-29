from pathlib import Path
import calendar
import zipfile

# --------------------Crear,editar,eliminar carpetas----------------#
# # creamos una carpeta
# # exist_ok=True para que no genere error
# Path("unica").mkdir(exist_ok=True)


# # crear multiples carpetas
# # parents=True cualquier carpeta padre se creara si no existe
# Path('carpeta1/carpeta2/carpeta3').mkdir(parents=True, exist_ok=True)


# # convertimos en lista los meses que entregue desde la posicion 1
# meses_ano = list(calendar.month_name[1:])
# dias_semana = ['dia_1', 'dia_10', 'dia_20', 'dia_30']

# for i, mes in enumerate(meses_ano):
#     for dia in dias_semana:
#         Path(f"2022/{i+1}.{mes}/{dia}").mkdir(parents=True, exist_ok=True)



# # Cambiar nombre de carpetas
# path = Path('unica') # definimos el path
# path.rename('editado_nombre')


# # Renombrar archivo dentro de una carpeta
# path2 = Path('test/gastos.txt')
# nuevoNombrePath = path2.with_name('gastos-diciembre.txt')
# path2.rename(nuevoNombrePath)
# print(nuevoNombrePath)


# # Obtener path de subdirectorios inmediatos
# carpeta = Path('2023')
# for path3 in list(carpeta.iterdir()):
#     print(path3)



# Obtener path de subdirectorios
# paths = carpeta.glob('**/*')
# for pth5 in paths:
#     print(pth5)



# obtener directorio en especifico
# carpeta2 = Path('test')
# for pth6 in carpeta2.glob('**/*.txt'):
#     print (pth6)

# subdirectorio por archivo
# for pth7 in carpeta2.glob('**/*'):
#     if pth7.is_file():
#         print(pth7)
#     else:
#         print('no hay archivo')



#--------------Cambiar extension de archivos--ejemplo de txt a csv--------#

# folder = Path('extensiones')
# for pth8 in list(folder.iterdir()): # casterar lista del folder
#     print('pth8',pth8)
#     if pth8.suffix == '.txt': # comparamos el sufijo es decir la extension
#         nuevoNombreExtension = pth8.with_suffix('.csv') # en variable asignamos la nueva extension
#         pth8.rename(nuevoNombreExtension)


# # pasar de csv a txt
# for pth9 in folder.glob('**/*.csv'):
#     print ('pth9',pth9 )
#     nuevaExtension = pth9.with_suffix('.txt')
#     pth9.rename(nuevaExtension)





# ----------------------crear archivos-------------------#
# crear archivos mediante ficheros
# for i in range(9):
#     with open(f"crear_eliminar_archivos_con_data/test{i + 1}.txt", "w") as file:
#         file.write(f'hola mundo {i+1}')

# eliminar todos los archivos txt
# for pth10 in Path('crear_eliminar_archivos_con_data').glob('*.txt'):
#     pth10.unlink()

# eliminar todos los archivos .txt menos el 9
# for pth10 in Path('crear_eliminar_archivos_con_data').glob('test[1-8].txt'):
#     pth10.unlink()




# --------------------extraer zip -----------------#
# directorio_actual = Path('.')
# directorio_objetivo = Path('temp')

# for pth11 in directorio_actual.glob('*.zip'):
#     print(pth11)
#     with zipfile.ZipFile(pth11, 'r') as zipObj:
#         zipObj.extractall(path=directorio_objetivo) # metodo para extraer



# ---------------extraer informacion de html ------------#
import pandas as pd

simp = pd.read_html('https://es.wikipedia.org/wiki/Anexo:Episodios_de_Los_Simpson')
print (simp)