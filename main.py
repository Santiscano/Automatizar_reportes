import pandas as pd
import sys
import shutil
import os
from docxtpl import DocxTemplate
import copy


#Corresponde a nuestro excel de alumnos
NOTAS_ALUMNOS_PATH = r'inputs/Notas_Alumnos.xlsx'


#Corresponde a nuestro word de cursos
PLANTILLA_CURSOS_PATH = r'inputs/Plantilla_Notas.docx'


PATH_OUTPUT = r'.\outputs'

CURSO = '2021/2022'

# Colores
SUSPENSO_COLOR = 'ec7c7b'
APROBADO_COLOR = 'fbe083'
NOTABLE_COLOR = '4db4d7'
SOBRESALIENTE_COLOR = '48bf91'


dict_asig = {
        'LENGUA CASTELLANA Y LITERATURA': 'Lengua Castellana y Literatura',
        'BIOLOGIA': 'Biología',
        'GEOGRAFIA E HISTORIA': 'Geografía e Historia',
        'MATEMATICAS': 'Matemáticas',
        'INGLES': 'Inglés',
        'EDUCACION FISICA': 'Educación Física',
        'ETICA': 'Ética',
        'CULTURA CLASICA': 'Cultura clásica',
        'MUSICA': 'Música',
        'TECNOLOGIA': 'Tecnología',
        'EDUCACION PLASTICA': 'Educación Plástica',
        'FRANCES': 'Francés',
    }


def deteccionErrores(df):
    err1, err2, err3 = False, False, False

    alumnos_list = sorted(list(df['NOMBRE'].drop_duplicates()))

    asignatura_list = sorted(list(df['ASIGNATURA'].drop_duplicates()))

    for al in alumnos_list:
        for asig in asignatura_list:
            filt_al_as_df = df[(df['NOMBRE'] == al) & (df['ASIGNATURA'] == asig)]
            print('')

            if(len(filt_al_as_df) == 0):
                print(f'Error: El alumno {al} no tiene la asignatura {asig} asignada')
                err1 = True

            elif(len(filt_al_as_df) > 1):
                print(f'Error: El alumno {al} tiene la asignatura {asig} repetida {len(filt_al_as_df)} veces')
                err2 = True

        for index, row in df.iterrows():
            trimestre_list = ['NOTA T1', 'NOTA T2', 'NOTA T3']
            for trim in trimestre_list:
                if not((row[trim] >= 0.0) and (row[trim] <=10.0)):
                    print(f'Error: El alumno {al} tiene el campo {trim} de la asginatura {asig}  fuera de rango {str(row[trim])}')
                    err3 = True

        if (err1 == True ) or (err2 == True) or (err3 == True):
            print('')
            print('Debes corregir los errores para continuar con la ejecucion del programa')
            sys.exit(1)
        else:
            print('Ningun error detectado ')




def eliminarTildes(texto):

    tildes_dict = {
        'Á': 'A',
        'É': 'E',
        'Í': 'I',
        'Ó': 'O',
        'Ú': 'U',
    }

    textoSinTilde = texto

    for key in tildes_dict:
        textoSinTilde = textoSinTilde.replace(key, tildes_dict[key])

    return textoSinTilde



def eliminarCrearCarpetas(path):
    if os.path.exists(path):
        shutil.rmtree(path)

    os.mkdir(path)

def ObtenerNotaFinal(dict_asignatura):
    newAsignaturaDic = copy.deepcopy(dict_asignatura)
    TRIMESTRE_LIST = ['t1', 't2', 't3']


    #Obtener la nota final
    nota_media = 0
    for trim in TRIMESTRE_LIST:
        nota_media += newAsignaturaDic[trim]
    nota_media /= 3
    newAsignaturaDic['nota_final'] = round(nota_media, 1)

    #Obtenemos la calificacion

    if(nota_media < 5.0):
        calif = 'SUSPENSO'
        color_calif = SUSPENSO_COLOR
    elif (nota_media < 7.0):
        calif = 'APROBADO'
        color_calif = APROBADO_COLOR
    elif (nota_media < 9.0):
        calif = 'NOTABLE'
        color_calif = NOTABLE_COLOR
    else:
        calif = 'SOBRESALIENTE'
        color_calif = SOBRESALIENTE_COLOR
    newAsignaturaDic['calificacion'] = calif
    newAsignaturaDic['color'] = color_calif

    return newAsignaturaDic



def crearWordAsignarTag(datos_alumnos, excel_df):
    asig_list = sorted(list(excel_df['ASIGNATURA'].drop_duplicates()))

    filter_td_asig = []
    for item in asig_list:
        valorTd = dict_asig[item]
        filter_td_asig.append(valorTd.upper())
    print('')

    nombre_Alumno_list = sorted(list(datos_alumnos['NOMBRE']))
    for nombre_alumno in nombre_Alumno_list:
        # Cargar documento
        docs_tpl = DocxTemplate(PLANTILLA_CURSOS_PATH)

        filt_datos_alumnos_df = datos_alumnos[(datos_alumnos['NOMBRE'] == nombre_alumno)]

        clase = filt_datos_alumnos_df.iloc[0]['CLASE']

        #Crear tabla de notas
        asignatura_list = []
        #Iterar sobre los indices de asignaturas
        for asig_idx in range(len(asig_list)):
            asign = asig_list[asig_idx]
            filt_al_as_excel_df = excel_df[(excel_df['NOMBRE'] == nombre_alumno) & (excel_df['ASIGNATURA'] == asign)]
            print('')

            asignatura_dict = {
                'nombre_asignatura': filter_td_asig[asig_idx],
                't1': round(filt_al_as_excel_df.iloc[0]['NOTA T1'],1),
                't2': round( filt_al_as_excel_df.iloc[0]['NOTA T2'],1),
                't3': round(filt_al_as_excel_df.iloc[0]['NOTA T3'],1),
            }
            asignatura_dict = ObtenerNotaFinal(asignatura_dict)

            asignatura_list.append(asignatura_dict)



        #Context
        context = {
            'curso': CURSO,
            'nombre_alumno': nombre_alumno,
            'clase': clase,
            'asignatura_list': asignatura_list,
        }

        #Renderizamos el documento
        docs_tpl.render(context)
        titulo = 'NOTAS_' + nombre_alumno
        titulo = titulo.upper()
        titulo = eliminarTildes(titulo)
        titulo = titulo.replace(" ", "_")
        titulo += '.docx'

        docs_tpl.save(PATH_OUTPUT + '\\' + titulo)





def main():
    eliminarCrearCarpetas(PATH_OUTPUT)

    #Leemos notas y datos alumnos
    excel_df = pd.read_excel(NOTAS_ALUMNOS_PATH, sheet_name='Notas')
    datos_alumnos = pd.read_excel(NOTAS_ALUMNOS_PATH, sheet_name='Datos_Alumnos')

    #Detectamos errores
    deteccionErrores(excel_df)

    #Creamos y asignamos tags en el word
    crearWordAsignarTag(datos_alumnos, excel_df)




if __name__ == '__main__':
    main()