import urllib.parse
import requests

route_url = "https://graphhopper.com/api/1/route?"
loc_url = "https://graphhopper.com/api/1/geocode?"

key = "TU_API_KEY_AQUI"


def geocodificar(localizacion, api_key):
    while localizacion == "":
        localizacion = input(
            "Por favor, ingrese una ubicación válida (origen/destino): "
        )

    url = loc_url + urllib.parse.urlencode(
        {"q": localizacion, "limit": "1", "key": api_key}
    )
    respuesta = requests.get(url)
    estado = respuesta.status_code
    datos = respuesta.json()

    if estado == 200 and len(datos.get("hits", [])) > 0:
        hit = datos["hits"][0]
        lat = hit["point"]["lat"]
        lng = hit["point"]["lng"]
        nombre = hit.get("name", "")
        estado_local = hit.get("state", "")
        pais = hit.get("country", "")
        nombre_completo = f"{nombre}, {estado_local}, {pais}".strip(", ")
        return estado, lat, lng, nombre_completo
    else:
        return estado, None, None, localizacion


while True:
    print("\n" + "=" * 60)
    print("      SISTEMA DE GEOLOCALIZACIÓN Y RUTAS (GRAPHHOPPER)")
    print("      (Escriba 's' o 'salir' para finalizar el programa)")
    print("=" * 60)

    origen = input("\nIngrese la ciudad/ubicación de ORIGEN: ").strip()
    if origen.lower() in ["s", "salir"]:
        print(
            "\n¡Gracias por utilizar el software de geolocalización! Hasta"
            " luego."
        )
        break

    destino = input("Ingrese la ciudad/ubicación de DESTINO: ").strip()
    if destino.lower() in ["s", "salir"]:
        print(
            "\n¡Gracias por utilizar el software de geolocalización! Hasta"
            " luego."
        )
        break

    print("\nBuscando coordenadas...")
    estado1, lat1, lng1, nombre_origen = geocodificar(origen, key)
    estado2, lat2, lng2, nombre_destino = geocodificar(destino, key)

    if (
        estado1 == 200
        and estado2 == 200
        and lat1 is not None
        and lat2 is not None
    ):
        print(f"\n[+] Origen confirmado: {nombre_origen}")
        print(f"[+] Destino confirmado: {nombre_destino}")

        parametros = [
            ("point", f"{lat1},{lng1}"),
            ("point", f"{lat2},{lng2}"),
            ("vehicle", "car"),
            ("locale", "es"),
            ("key", key),
        ]

        url_ruta = route_url + urllib.parse.urlencode(parametros)
        resp_ruta = requests.get(url_ruta)
        estado_ruta = resp_ruta.status_code
        datos_ruta = resp_ruta.json()

        if estado_ruta == 200:
            camino = datos_ruta["paths"][0]
            distancia_m = camino["distance"]
            tiempo_ms = camino["time"]

            distancia_km = distancia_m / 1000.0

            segundos_totales = int(tiempo_ms / 1000)
            horas = segundos_totales // 3600
            minutos = (segundos_totales % 3600) // 60
            segundos = segundos_totales % 60

            print("\n" + "-" * 50)
            print("RESUMEN DEL VIAJE:")
            print(f"• Distancia total : {distancia_km:.2f} km")
            print(f"• Tiempo estimado : {horas}h {minutos}m {segundos}s")
            print("-" * 50)

            print("\nNARRATIVA DEL VIAJE PASO A PASO:")
            instrucciones = camino.get("instructions", [])
            for idx, paso in enumerate(instrucciones, 1):
                texto_paso = paso.get("text", "")
                dist_paso_km = paso.get("distance", 0) / 1000.0
                print(f"  {idx}. {texto_paso} ({dist_paso_km:.2f} km)")
        else:
            print("\n[-] Error al calcular la ruta en Graphhopper.")
            print("    Asegúrese de haber ingresado una API Key válida.")
    else:
        print(
            "\n[-] Error: No se pudo localizar alguna de las ciudades"
            " ingresadas."
        )