import pyttsx3
import speech_recognition as sr
import pywhatkit
import yfinance as yf
import pyjokes
from statsbombpy import sb
import webbrowser
import datetime
import wikipedia


# escuchar nuestro microfono y devolver el audio como texto
def transformar_audio_en_texto():
    # almacenar recognizer en variable
    r = sr.Recognizer()

    # configurar el microfono
    with sr.Microphone() as origen:

        # tiempo de espera (mejorar calidad)
        r.pause_threshold = 0.8

        # informar que comonezo la grabacion
        print("ya puedes hablar")

        # guardar lo que escuche como audio
        audio = r.listen(origen, phrase_time_limit=5)

        try:
            # buscar en google lo que haya escuchado
            pedido = r.recognize_google(audio, language="es-ve")

            # prueba de que pudo ingresar y transformar nuestra voz en texto
            print(f"dijiste: {pedido}")

            # devolver a pedido
            return pedido

        # en caso de que no comprenda el audio
        except sr.UnknownValueError:

            # prueba de que no comprendio el audio
            print("ups no entendi")

            # devolver error
            return "sigo esperando"

        # en caso de que resolver el pedido
        except sr.RequestError:

            # prueba de que no comprendio el audio
            print("ups hay servicio")

            # devolver error
            return "sigo esperando"

        # errores inesperados
        except:

            # prueba de que no comprendio el audio
            print("ups algo ha salido mal")

            # devolver error
            return "sigo esperando"


# funcion para que el asistente pueda ser escuchado
def hablar(mensaje):
    # encender el motor de pyttsx3
    engine = pyttsx3.init()
    engine.setProperty("voice", id1)

    # pronunciar mensaje
    engine.say(mensaje)
    engine.runAndWait()


"""engine = pyttsx3.init()
for voz in engine.getProperty("voices"):
    print(voz)"""

# opciones de voz
id1 = "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_ES-ES_HELENA_11.0"
id2 = "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_EN-US_ZIRA_11.0"


# informar el dia de la semana
def pedir_dia():
    # crear variable con datos de hoy
    dia = datetime.datetime.today()

    # crea una variable para el dia de la semana
    dia_semana = dia.weekday()
    print(dia_semana)

    # diccionario de dias
    calendario = {
        0: "Lunes",
        1: "Martes",
        2: "Miércoles",
        3: "Jueves",
        4: "Viernes",
        5: "Sábado",
        6: "Domingo"
    }

    # decir el dia de la semana
    hablar(f"hoy es {calendario[dia_semana]}")


# informar que hora es
def pedir_hora():

    # crear una variable con los datos de la hora
    hora = datetime.datetime.now()
    hora = f"Mira tito! En este momento, son las {hora.hour} horas con {hora.minute} minutos y {hora.second} segundos"
    # decir la hora
    hablar(hora)


# saludo inicial
def saludo_inicial():

    # crear variable con datos de hora
    hora = datetime.datetime.now()
    if hora.hour < 6 or hora.hour > 20:
        momento = "Buenas Noches"
    elif 6 <= hora.hour < 13:
        momento = "Buen día"
    else:
        momento = "Buenas Tardes"

    hablar(f"{momento} soy Tito de Triana, tu esclavo personal, por favor dime en que te puedo ayudar")


# funcion central del asistente
def pedir_cosas():

    # activar el saludo inicial
    saludo_inicial()

    # variable de corte (true o false)
    comenzar = True
    while comenzar:

        # activar el micro y guardar el pedido en un string
        pedido = transformar_audio_en_texto().lower()

        if "abrir youtube" in pedido:
            hablar("con gusto, estoy abriendo youtube")
            webbrowser.open("https://www.youtube.com/")
            continue
        elif "abrir navegador" in pedido:
            hablar("claro, estoy en eso")
            webbrowser.open("https://www.google.com/")
            continue
        elif "qué día es hoy" in pedido:
            pedir_dia()
            continue
        elif "qué hora es" in pedido:
            pedir_hora()
            continue
        elif "busca en wikipedia" in pedido:
            hablar("Buscando esa vaina en wikipedia, esperá")
            pedido = pedido.replace("busca en wikipedia", "")
            wikipedia.set_lang("es")
            resultado = wikipedia.summary(pedido, sentences=1)
            hablar("Wikipedia dice lo siguente:")
            hablar(resultado)
            continue
        elif "busca en internet" in pedido:
            hablar("ya estoy en eso, tito")
            pedido = pedido.split("internet")[-1].strip()
            pywhatkit.search(pedido)
            hablar("esto es lo que he encontrado")
            continue
        elif "reproducir" in pedido:
            hablar("buena idea, ya empiezo a reproducirlo")
            accion = pedido.split("reproducir")[-1].strip()
            pywhatkit.playonyt(accion)
            continue
        elif "broma" in pedido:
            hablar(pyjokes.get_joke("es"))
            continue
        elif "precio de las acciones" in pedido:
            accion = pedido.split("de")[-1].strip()
            cartera = {
                "apple": "AAPL",
                "amazon": "AMZN",
                "google": "GOOGL"
            }
            try:
                accion_buscada = cartera[accion]
                accion_buscada = yf.Ticker(accion_buscada)
                precio_actual = accion_buscada.info["regularMarketPrice"]
                hablar(f"la encontré, el precio de {accion} es {precio_actual} dolares")
                continue
            except:
                hablar("perdón pero no la he encontrado")
                continue
        elif "adiós" in pedido:
            hablar("me voy a descansar, cualquier cosa me avisas")
            break


pedir_cosas()


