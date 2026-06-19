# TPI-Organizacion-Empresarial-TUP

# Gestión de Vacaciones - Bot de Telegram
Bot automatizado para la gestión de vacaciones de empleados desarrollado en Python con la API de Telegram.
Este bot permite a los empleados solicitar vacaciones de forma automatizada a través de Telegram. El sistema valida fechas, verifica disponibilidad de días, actualiza una base de datos (CSV) y guía al usuario paso a paso mediante una máquina de estados de manera automatizada.



## Tecnologías utilizadas

| Tecnología | Uso |
|------------|-----|
| **Python 3** | Lenguaje de programación principal |
| **pyTelegramBotAPI** | Conexión con la API de Telegram |
| **CSV** | Base de datos para almacenar empleados |


## Instalación y Ejecución

### Clonar repositorioo 
```bash
git clone https://github.com/tu-usuario/gestor_vacaciones_bot.git
cd gestor_vacaciones_bot
```

### Instalar dependencias
En la consola ejecutar
#El comando "pip install pyTelegramBotAPI" instala una librería de Python que permite crear, administrar y programar bots para Telegram. Proporciona una interfaz sencilla para interactuar con la API oficial de Telegram.
Comando:
pip install pyTelegramBotAPI

#El comando "pip install python-dotenv" instala una librería que permite cargar variables de entorno desde un archivo de texto (.env) al entorno de ejecución de tu proyecto en Python.
Comando:
pip install python-dotenv

### Importante
#Para el correcto flujo del programa, sólo se debe mantener una terminal abierta y en caso de querer correr el código nuevamente, todas las terminales que hayan sido iniciadas o estén abiertas deben cerrarse correctamente.

### Ejecución del bot
_Correr código en Python, no cerrar VSCode. 
_Abrir Telegram en tu teléfono o computadora.
_Buscar el bot por su nombre: @gestor_vacaciones_bot
_Escribir /start para iniciar.
_Seguir las instrucciones del bot.

## Comandos Disponibles
| Comando | Función |
|------------|-----|
| /start | Iniciar el bot y ver la lista de empleados |
| /help | Mostrar ayuda |
| solicitar | Iniciar solicitud de vacaciones |
| YYYY-MM-DD YYYY-MM-DD | Ingresar fechas |
| 1, 2, 3 | Elegir alternativa |

## Flujo del Bot
1.El usuario escribe /start
2.El bot muestra la lista de empleados registrados
3.El usuario escribe su nombre completo
4.El bot confirma identidad y muestra días disponibles
5.El usuario escribe solicitar
6.El bot pide las fechas (YYYY-MM-DD YYYY-MM-DD)
7.El bot valida:
  °Formato de fecha correcto
  °Fecha no anterior a hoy
  °Fecha fin mayor a fecha inicio
  °Máximo 20 días de vacaciones
  °Días disponibles suficientes
8.Si todo está bien → Vacaciones aprobadas (se descuentan días y se actualiza el CSV)
9.Si no hay días suficientes → El bot ofrece 3 alternativas:
  1: Pedir menos días
  2: Esperar a tener más días
  3: Contactar a RRH


