import sys
from bs4 import BeautifulSoup

# Configuración centralizada para los selectores y atributos
CONFIG = {
    "temario": {
        "contenedor": {"tag": "div", "id": "s-div3"},  # Selección por id
        "encabezado": {"tag": "h2", "texto": "Temario"},  # Busca el encabezado "Temario"
        "modulos": {"tag": ["p", "h5"], "strong": True}  # Busca módulos en <p><strong> o <h5>
    }
}

def buscar_temario(soup):
    """
    Busca la sección de Temario en el HTML.
    Si no se encuentra, devuelve XXX.
    """
    try:
        # Busca el contenedor de la sección de Temario por su id
        contenedor_temario = soup.find(**CONFIG["temario"]["contenedor"])
        if not contenedor_temario:
            print("No se encontró el contenedor de la sección 'Temario'.")
            return "XXX"
        
        # Busca el encabezado "Temario" dentro del contenedor
        encabezado_temario = contenedor_temario.find(
            lambda tag: tag.name == CONFIG["temario"]["encabezado"]["tag"] and
                        CONFIG["temario"]["encabezado"]["texto"] in tag.get_text()
        )
        if not encabezado_temario:
            print("No se encontró el encabezado de la sección 'Temario'.")
            return "XXX"
        
        # Extrae los módulos del temario
        modulos = extraer_modulos(contenedor_temario)
        return modulos
    
    except Exception as e:
        print(f"Error al buscar la sección 'Temario': {e}")
        return "XXX"

def extraer_modulos(contenedor):
    """
    Extrae los módulos del temario y los devuelve en una lista de diccionarios.
    Cada módulo tiene un título y una lista de elementos.
    """
    modulos = []
    elementos = contenedor.find_all(CONFIG["temario"]["modulos"]["tag"], recursive=False)
    
    for elemento in elementos:
        if elemento.find("strong"):  # Solo procesa elementos con <strong> (títulos de módulos)
            titulo = elemento.get_text(strip=True)
            items = []
            siguiente = elemento.find_next_sibling()
            
            # Recoge los elementos de la lista (<ul>) que sigue al título del módulo
            while siguiente and siguiente.name not in ["p", "h5"]:
                if siguiente.name == "ul":
                    items = [li.get_text(strip=True) for li in siguiente.find_all("li")]
                    break
                siguiente = siguiente.find_next_sibling()
            
            modulos.append({"titulo": titulo, "items": items})
    
    return modulos if modulos else "XXX"

def construir_html_temario(modulos):
    """
    Construye el HTML de la sección "Temario" a partir de la lista de módulos.
    """
    if modulos == "XXX":
        return "XXX"
    
    html_modulos = []
    for i, modulo in enumerate(modulos, start=1):
        html_items = "".join(f"<li>{item}</li>" for item in modulo["items"])
        html_modulos.append(f'''
            <li class="course__module">
                <h3 class="course__module-title"><span class="course__module-tag">{i}</span>{modulo["titulo"]}</h3>
                <ul class="course__module-description">
                    {html_items}
                </ul>
            </li>
        ''')
    
    return f'''
    <section class="course__content" id="s-div1">
        <h2 class="title__section">
            <span><!-- svg --></span>
            Contenido del curso
        </h2>
        <ul class="course__module-list">
            {"".join(html_modulos)}
        </ul>
    </section>
    '''

def main():
    if len(sys.argv) < 2:
        print("Uso: python convertir_temario.py <archivo.html>")
        return
    
    archivo_html = sys.argv[1]
    
    try:
        with open(archivo_html, "r", encoding="utf-8") as file:
            html_viejo = file.read()
    except FileNotFoundError:
        print(f"Error: No se encontró el archivo {archivo_html}")
        return
    
    # Convertir el HTML viejo a la nueva estructura
    soup = BeautifulSoup(html_viejo, "html.parser")
    modulos = buscar_temario(soup)
    temario_html = construir_html_temario(modulos)
    
    if temario_html:
        with open("temario_convertido.html", "w", encoding="utf-8") as file:
            file.write(temario_html)
        print("Archivo 'temario_convertido.html' creado con éxito.")

if __name__ == "__main__":
    main()