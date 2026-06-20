import telebot
import csv
from datetime import datetime, date
import os
# Importamos la librería para leer el archivo .env
from dotenv import load_dotenv

# Cargar las variables de entorno desde el archivo .env
load_dotenv()
# ========================================
# CONFIGURACIÓN
# ========================================

#TOKEN = "8905620962:AAGDBetaY6cc9aARxfQLiHKZ-uB98Zl2pZM"  
#bot = telebot.TeleBot(TOKEN)
#archivo_empleados = "empleados_vacaciones.csv"
# Os.environ busca la variable TELEGRAM_TOKEN que guardaste en el archivo .env
TOKEN = os.environ.get("TELEGRAM_TOKEN")

if not TOKEN:
    raise ValueError("❌ ¡Error! No se encontró el TELEGRAM_TOKEN en las variables de entorno.")

bot = telebot.TeleBot(TOKEN)
archivo_empleados = "empleados_vacaciones.csv"
# ========================================
# FUNCIONES SIMPLES
# ========================================

def leer_empleados():
    """Lee el archivo de empleados"""
    try:
        with open(archivo_empleados, 'r', encoding='utf-8') as archivo:
            return list(csv.DictReader(archivo))
    except:
        return []

def buscar_empleado(nombre):
    """Busca un empleado por nombre"""
    lista_empleados= leer_empleados()
    for emp in lista_empleados:
        if emp['nombre_completo'].lower() == nombre.lower():
            return emp
    return None

def guardar_dias(nombre, nuevos_dias):
    """Actualiza los días disponibles en el CSV"""
    empleados = leer_empleados()

    for emp in empleados:
        if emp['nombre_completo'].lower() == nombre.lower():
            emp['dias_vacaciones'] = str(nuevos_dias)

    with open(archivo_empleados, 'w', newline='', encoding='utf-8') as archivo:
        campos = ['id', 'nombre_completo', 'dias_vacaciones']
        writer = csv.DictWriter(archivo, fieldnames=campos)
        writer.writeheader()
        writer.writerows(empleados)
# ========================================
# COMANDOS DEL BOT
# ========================================

@bot.message_handler(commands=['start'])
def start(message):
    chat_id = message.chat.id
    
    # Mostrar lista de empleados
    empleados = leer_empleados()
    if not empleados:
        bot.send_message(chat_id, "❌ No hay empleados. Creando archivo...")
        # Crear archivo con empleados de ejemplo
        with open(archivo_empleados, 'w', encoding='utf-8') as f:
            f.write("id,nombre_completo,dias_vacaciones\n")
            f.write("1,Ana García,23\n")
            f.write("2,Sofía Pérez,30\n")
            f.write("3,Ana Romero,22\n")
            f.write("4,Andrés Diaz,11\n")
            f.write("5,Juan González,26\n")
            f.write("6,Sofía Álvarez,39\n")
            f.write("7,Juan Romero,26\n")
            f.write("8,Valentina Diaz,27\n")
            f.write("9,Javier Alonso,28\n")
            f.write("10,Juan Martínez,33\n")
            f.write("11,Pedro Gómez,24\n")
            f.write("12,José Jiménez,23\n")
            f.write("13,Carlos Hernández,23\n")
            f.write("14,Lucía Ruiz,39\n")
            f.write("15,Diego Rodríguez,34\n")
            f.write("16,Valentina Fernández,32\n")
            f.write("17,Carlos Romero,19\n")
            f.write("18,Camila Ruiz,28\n")
            f.write("19,José González,11\n")
            f.write("20,Sofía Martin,22\n")
        empleados = leer_empleados()
    
    # Crear lista de nombres
    lista = "\n".join([f"• {emp['nombre_completo']}" for emp in empleados])
    
    bot.send_message(
        chat_id,
        f"🏢 SISTEMA DE VACACIONES\n\n"
        f"📋 Empleados:\n{lista}\n\n"
        f"👤 Escribí tu nombre completo"
    )

@bot.message_handler(commands=['help'])
def help(message):
    bot.send_message(
        message.chat.id,
        "🤖 COMANDOS:\n"
        "/start - Iniciar\n"
        "/help - Ayuda\n\n"
        "📝 Cómo usar:\n"
        "1. Escribí /start\n"
        "2. Poné tu nombre\n"
        "3. Escribí 'solicitar'\n"
        "4. Poné fechas (YYYY-MM-DD YYYY-MM-DD)"
    )

# ========================================
# MANEJAR MENSAJES
# ========================================

# Diccionario para guardar datos de cada usuario
usuarios = {}

@bot.message_handler(func=lambda m: True)
def mensajes(message):
    chat_id = message.chat.id
    texto = message.text
    user_id = str(message.from_user.id)
    
    # Si no está registrado, pedir nombre
    if user_id not in usuarios:
        empleado = buscar_empleado(texto)
        if empleado:
            usuarios[user_id] = {
                'nombre': empleado['nombre_completo'],
                'dias': int(empleado['dias_vacaciones']),
                'estado': 'esperando'
            }
            bot.send_message(
                chat_id,
                f"✅ ¡Hola {empleado['nombre_completo']}!\n"
                f"📊 Días disponibles: {empleado['dias_vacaciones']}\n\n"
                f"📝 Escribí 'solicitar' para pedir vacaciones"
            )
        else:
            bot.send_message(
                chat_id,
                "❌ No te encontré. Escribí tu nombre como aparece en la lista.\n"
                "Usá /start para ver la lista"
            )
        return
    
    # Si ya está registrado
    usuario = usuarios[user_id]
    
    # Comando para solicitar vacaciones
    if texto.lower() == 'solicitar':
        usuario['estado'] = 'esperando_fechas'
        bot.send_message(
            chat_id,
            "📅 Escribí las fechas así:\n"
            "YYYY-MM-DD YYYY-MM-DD\n\n"
            "Ejemplo: 2024-12-20 2024-12-25"
        )
        return
    
    # Si está esperando fechas
    if usuario['estado'] == 'esperando_fechas':
        try:
            # Separar las fechas
            partes = texto.split()
            fecha_inicio = datetime.strptime(partes[0], '%Y-%m-%d').date()
            fecha_fin = datetime.strptime(partes[1], '%Y-%m-%d').date()
            
            # Calcular días
            dias = (fecha_fin - fecha_inicio).days + 1
            
            # Validar
            if fecha_fin < fecha_inicio:
                bot.send_message(chat_id, "❌ La fecha fin no puede ser anterior")
                return
            
            if fecha_inicio < date.today():
                bot.send_message(chat_id, "❌ La fecha inicio no puede ser anterior a hoy")
                return
            
            if dias > 20:
                bot.send_message(chat_id, f"❌ Máximo 20 días. Pediste {dias}")
                return
            
            if dias > usuario['dias']:
                bot.send_message(
                    chat_id,
                    f"❌ No tenés suficientes días.\n"
                    f"Tenés: {usuario['dias']}\n"
                    f"Pedís: {dias}\n\n"
                    f"Alternativas:\n"
                    f"1 - Pedir menos días\n"
                    f"2 - Esperar a tener más días\n"
                    f"3 - Consultar RRHH\n\n"
                    f"Respondé con 1, 2 o 3"
                )
                usuario['estado'] = 'alternativas'
                usuario['dias_pedidos'] = dias
                return
            
            # Si todo está bien, aprobar
            usuario['dias'] -= dias
            # Guardar en el CSV
            guardar_dias(usuario['nombre'], usuario['dias']) 

            bot.send_message(
                chat_id,
                f"✅ ¡VACACIONES APROBADAS!\n\n"
                f"👤 {usuario['nombre']}\n"
                f"📅 {fecha_inicio} al {fecha_fin}\n"
                f"📊 Días: {dias}\n"
                f"📈 Te quedan: {usuario['dias']} días\n\n"
                f"🏖️ ¡Disfrutá!"
            )
            usuario['estado'] = 'esperando'
            
        except:
            bot.send_message(
                chat_id,
                "❌ Formato incorrecto.\n"
                "Usá: YYYY-MM-DD YYYY-MM-DD\n"
                "Ejemplo: 2024-12-20 2024-12-25"
            )
        return
    
    # Manejar alternativas
    if usuario['estado'] == 'alternativas':
        if texto == '1':
            bot.send_message(
                chat_id,
                "✅ Escribí 'solicitar' para pedir menos días"
            )
            usuario['estado'] = 'esperando'
        elif texto == '2':
            bot.send_message(
                chat_id,
                "📌 OK. Volvé cuando tengas más días disponibles."
            )
            usuario['estado'] = 'esperando'
        elif texto == '3':
            bot.send_message(
                chat_id,
                "📞 Contactá a RRHH al 555-1234"
            )
            usuario['estado'] = 'esperando'
        else:
            bot.send_message(
                chat_id,
                "❌ Respondé con 1, 2 o 3"
            )
        return
    
    # Mensaje genérico
    bot.send_message(
        chat_id,
        f"📩 Recibí: {texto}\n\n"
        f"Comandos:\n"
        f"- Escribí 'solicitar' para pedir vacaciones\n"
        f"- Usá /help para ayuda"
    )

# ========================================
# INICIAR EL BOT
# ========================================

if __name__ == "__main__":
    print("🤖 BOT DE VACACIONES (VERSIÓN SIMPLE)")
    print("=" * 40)
    print("🚀 Bot iniciado...")
    print("📱 Buscá tu bot @gestor_vacaciones_bot y usá /start")
    print("⏹️  Presioná Ctrl+C para detener")
    print("=" * 40)
    
    # Crear archivo si no existe
    if not os.path.exists(archivo_empleados):
        with open(archivo_empleados, 'w', encoding='utf-8') as f:
            f.write("id,nombre_completo,dias_vacaciones\n")
            f.write("1,Ana García,23\n")
            f.write("2,Sofía Pérez,30\n")
            f.write("3,Ana Romero,22\n")
            f.write("4,Andrés Diaz,11\n")
            f.write("5,Juan González,26\n")
            f.write("6,Sofía Álvarez,39\n")
            f.write("7,Juan Romero,26\n")
            f.write("8,Valentina Diaz,27\n")
            f.write("9,Javier Alonso,28\n")
            f.write("10,Juan Martínez,33\n")
            f.write("11,Pedro Gómez,24\n")
            f.write("12,José Jiménez,23\n")
            f.write("13,Carlos Hernández,23\n")
            f.write("14,Lucía Ruiz,39\n")
            f.write("15,Diego Rodríguez,34\n")
            f.write("16,Valentina Fernández,32\n")
            f.write("17,Carlos Romero,19\n")
            f.write("18,Camila Ruiz,28\n")
            f.write("19,José González,11\n")
            f.write("20,Sofía Martin,22\n")
        print("✅ Archivo creado con 5 empleados")
    
    try:
        bot.delete_webhook()
        bot.infinity_polling()
    except KeyboardInterrupt:
        print("\n🛑 Bot detenido")
