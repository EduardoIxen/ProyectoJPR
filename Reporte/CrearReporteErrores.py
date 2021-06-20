import webbrowser
import os.path
from tabulate import *
from TS.Excepcion import listaErrores


class CrearReporteErrores:
    def crearReporteErrores(self):
        contador = 0
        listaFormateada = []
        dictTemp = {}
        contenidoTabla = ""
        '''
            Recorrer cada diccionario de la lista para agregarle el elemento No
            y volver a guardar en un diccionario para crear las tablas html con
            la libreria tabulate.
        '''
        for itemError in listaErrores:
            contador = contador + 1
            dictTemp["No"] = contador
            dictTemp["Tipo"] = itemError.get("Tipo")
            dictTemp["Descripcion"] = itemError.get("Descripcion")
            dictTemp["Fila"] = itemError.get("Fila")
            dictTemp["Columna"] = itemError.get("Columna")
            listaFormateada.append(dictTemp)
            dictTemp = {}

        if listaErrores != []:
            content = tabulate(listaFormateada, headers="keys", tablefmt='html')
            contenidoTabla = str(content)
            contenidoTabla = contenidoTabla.replace('<table>',
                                                    '<table class="table table-striped table-bordered" style="margin: 2%  auto; width:80%" >',
                                                    1)
            contenidoTabla = contenidoTabla.replace('<thead>', '<thead class="thead-dark">', 1)
            contenidoTabla = contenidoTabla.replace('right', 'center')
            contenidoTabla = contenidoTabla.replace('<td>', '<td style="text-align: center;">')
            contenidoTabla = contenidoTabla.replace('<th>', '<th style="text-align: center;">')

        # obtiene la ruta absoluta del archivo
        my_path1 = os.path.abspath(os.path.dirname(__file__))
        path1 = os.path.join(my_path1, f"../ReportesDeErrores.html")
        path1 = path1.replace("\\", "/")
        path1 = path1.replace("../", "")

        file = open(path1, "w")

        file.write('<!DOCTYPE html>')
        file.write('<html>')
        file.write('<head>')
        file.write('<title>Reporte</title>')
        file.write('<meta charset="utf-8">')
        file.write('<meta name="viewport" content="width=device-width, initial-scale=1">')
        file.write(
            '<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.4.1/css/bootstrap.min.css">')
        file.write('<script src="https://ajax.googleapis.com/ajax/libs/jquery/3.5.1/jquery.min.js"></script>')
        file.write('<script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.4.1/js/bootstrap.min.js"></script>')
        file.write('<link rel="stylesheet" href="css/estilo.css">')
        file.write(
            "<style>body{background: rgba(242,246,248,1);background: -moz-linear-gradient(45deg, rgba(242,246,248,1) 0%, rgba(216,225,231,1) 28%, rgba(104,149,179,1) 100%);background: -webkit-gradient(left bottom, right top, color-stop(0%, rgba(242,246,248,1)), color-stop(28%, rgba(216,225,231,1)), color-stop(100%, rgba(104,149,179,1)));background: -webkit-linear-gradient(45deg, rgba(242,246,248,1) 0%, rgba(216,225,231,1) 28%, rgba(104,149,179,1) 100%);background: -o-linear-gradient(45deg, rgba(242,246,248,1) 0%, rgba(216,225,231,1) 28%, rgba(104,149,179,1) 100%);background: -ms-linear-gradient(45deg, rgba(242,246,248,1) 0%, rgba(216,225,231,1) 28%, rgba(104,149,179,1) 100%);background: linear-gradient(45deg, rgba(242,246,248,1) 0%, rgba(216,225,231,1) 28%, rgba(104,149,179,1) 100%);filter: progid:DXImageTransform.Microsoft.gradient( startColorstr='#f2f6f8', endColorstr='#6895b3', GradientType=1 );}"
            "table{-webkit-box-shadow: 6px 11px 14px 1px rgba(0,0,0,0.75);-moz-box-shadow: 6px 11px 14px 1px rgba(0,0,0,0.75);box-shadow: 6px 11px 14px 1px rgba(0,0,0,0.75);}</style>")
        file.write('</head>')
        file.write('<body>')
        file.write('<center>')
        file.write(f'<h1>Reportes de errores</h1>')
        file.write(contenidoTabla)
        if listaErrores == []:
            file.write(f'<h1>NO HAY ERRORES!! :D</h1>')
        file.write('</center>')
        file.write('</body>')
        file.write('</html>')
        file.close()

        # obtiene la ruta absoluta del archivo y abre el archivo en el navegador con webbrowser.
        my_path = os.path.abspath(os.path.dirname(__file__))
        path = os.path.join(my_path, f"../ReportesDeErrores.html")
        path = path.replace("\\", "/")
        path = path.replace("../", "")
        webbrowser.open_new_tab(path)
