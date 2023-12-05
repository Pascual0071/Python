import datetime
import re
import smtplib
import ssl
import json
from email.message import EmailMessage

# Función para cargar empleados desde un archivo JSON
def cargar_empleados():
    try:
        with open('empleados.json', 'r') as file:
            empleados_lista = json.load(file)
        print('Empleados cargados exitosamente.')
    except FileNotFoundError:
        empleados_lista = []
        print('No se encontró el archivo de empleados. Se creará uno nuevo.')

    cantidad = int(input('Ingrese la cantidad de empleados que desea registrar: '))

    for i in range(cantidad):
        legajo = int(input('''Ingrese número de legajo del trabajador: '''))
        nombre = input('Introduzca el nombre del trabajador: ')
        apellido = input('Introduzca el apellido del trabajador: ')
        edad = int(input('Introduzca la edad del trabajador: '))
        fecha_de_ingreso = input("Introduzca la fecha de ingreso del empleado (DD-MM-YYYY): ") 
        if len(fecha_de_ingreso) <10:
            Fecha_de_ingreso = fecha_de_ingreso.zfill(2)
        puesto = input('Introduzca el puesto que ocupa el trabajador: ')
        mail = input('Ingrese el correo electrónico del trabajador: ')

        empleado = {
            'legajo': legajo,
            'nombre': nombre,
            'apellido': apellido,
            'edad': edad,
            'fecha_de_ingreso': fecha_de_ingreso,
            'puesto': puesto,
            'mail': mail
        }
        empleados_lista.append(empleado)

    with open('empleados.json', 'w') as file:
        json.dump(empleados_lista, file, indent=4)

    return empleados_lista  # Devuelve la lista actualizada

# Función para cargar empleados desde el archivo JSON
def cargar_empleados_desde_archivo():
    try:
        with open('empleados.json', 'r') as file:
            empleados_lista = json.load(file)
        print('Empleados cargados exitosamente.')
    except FileNotFoundError:
        empleados_lista = []
        print('No se encontró el archivo de empleados. No hay empleados cargados.')

    return empleados_lista

# Función para calcular la antigüedad de un empleado
def calcular_antiguedad(empleados_lista):
    nombre = input('Ingrese el nombre de la persona a consultar: ')
    apellido = input('Ingrese el apellido de la persona a consultar: ')

    encontrado = False

    for empleado in empleados_lista:
        if empleado['nombre'] == nombre and empleado['apellido'] == apellido:
            fecha_de_ingreso = datetime.datetime.strptime(empleado['fecha_de_ingreso'], '%d-%m-%Y')
            anios = datetime.datetime.now().year - fecha_de_ingreso.year
            print('La antigüedad de', apellido, nombre, 'es:', anios, 'años.')
            encontrado = True

    if not encontrado:
        print('No se encontró ningún empleado con ese nombre y apellido.')

# Función para determinar la recategorización de un empleado
def determinar_recategorizacion(empleados_lista):
    nombre = input('Ingrese el nombre del empleado a recategorizar o del que desea conocer su categoría: ')
    apellido = input('Ingrese el apellido del empleado a recategorizar o del que desea conocer su categoría: ')

    encontrado = False

    for empleado in empleados_lista:
        if empleado['nombre'] == nombre and empleado['apellido'] == apellido:
            fecha_de_ingreso = datetime.datetime.strptime(empleado['fecha_de_ingreso'], '%d-%m-%Y')
            anios = datetime.datetime.now().year - fecha_de_ingreso.year
            anios_previos = int(input('Ingrese los años que tiene en el puesto antes de entrar a la empresa: '))
            antiguedad_total = anios + anios_previos

            if 0 <= antiguedad_total <= 1:
                print('Este empleado estaría en la categoría Trainee.')
            elif 1 < antiguedad_total <= 3:
                print('Este empleado estaría en la categoría Junior.')
            elif 3 < antiguedad_total <= 6:
                print('Este empleado estaría en la categoría Semi Senior.')
            elif 6 < antiguedad_total:
                print('Este empleado estaría en la categoría Senior.')
            else:
                print('Opción incorrecta.')

            encontrado = True

    if not encontrado:
        print('No se encontró ningún empleado con ese nombre y apellido.')

# Función para enviar un correo electrónico al empleado
def enviar_correo_empleado(empleados_lista):
    nombre = input('Ingrese el nombre del empleado al que desea enviar el correo: ')
    apellido = input('Ingrese el apellido del empleado al que desea enviar el correo: ')
    mensaje = input('Ingrese el mensaje del correo: ')

    encontrado = False

    for empleado in empleados_lista:
        if empleado['nombre'] == nombre and empleado['apellido'] == apellido:
            destinatario = empleado['mail']

            # Configuración del correo electrónico
            email_subject = 'Correo de Recursos Humanos'
            sender_email_address = 'pascual0071@gmai.com'  # Reemplaza con tu dirección de correo
            receiver_email_address = destinatario
            email_smtp = 'smtp.gmail.com'
            email_password = 'kiulrpgazjhmbhew'  # Reemplaza con tu contraseña

            # Crear el objeto de mensaje de correo
            message = EmailMessage()

            # Configurar los encabezados del correo
            message['Subject'] = email_subject
            message['From'] = sender_email_address
            message['To'] = receiver_email_address

            # Establecer el cuerpo del correo
            message.set_content(mensaje)

            # Configurar el servidor SMTP y el puerto
            context = ssl.create_default_context()
            server = smtplib.SMTP(email_smtp, 587)

            try:
                # Establecer una conexión segura SMTP
                server.starttls(context=context)

                # Identificar este cliente ante el servidor SMTP
                server.ehlo()

                # Iniciar sesión en la cuenta de correo
                server.login(sender_email_address, email_password)

                # Enviar el correo
                server.send_message(message)
                print('Correo electrónico enviado exitosamente.')

            except smtplib.SMTPException as e:
                print('Error al enviar el correo electrónico:', str(e))

            finally:
                # Cerrar la conexión con el servidor
                server.quit()

            encontrado = True
            break

    if not encontrado:
        print('No se encontró ningún empleado con ese nombre y apellido.')

# Menú principal
def menu():
    empleados_lista = []  # Agregar esta línea antes del bucle while

    while True:
        print('Menú de opciones de consulta para Recursos Humanos')
        print('a) Cargar lista de empleados')
        print('b) Imprimir lista de empleados de la organización')
        print('c) Calcular antigüedad de un trabajador')
        print('d) Determinar recategorización de un trabajador')
        print('e) Enviar correo electrónico al empleado')
        print('f) Salir del programa')

        opcion = input('Ingrese una opción: ')

        if opcion == 'a':
            empleados_lista = cargar_empleados()  # Obtener la lista actualizada
        elif opcion == 'b':
            empleados_lista = cargar_empleados_desde_archivo()
            print('\nLista de empleados:')
            for empleado in empleados_lista:
                print(empleado)
        elif opcion == 'c':
            calcular_antiguedad(empleados_lista)
        elif opcion == 'd':
            determinar_recategorizacion(empleados_lista)
        elif opcion == 'e':
            enviar_correo_empleado(empleados_lista)
        elif opcion == 'f':
            print('Gracias por utilizar nuestros servicios. ¡Que tenga un buen día!')
            break
        else:
            print('La opción seleccionada es incorrecta.')

# Ejecutar el menú principal
menu()
