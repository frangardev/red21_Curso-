import sys
from bs4 import BeautifulSoup

def convertir_objetivos(html_viejo):
    # Parsear el HTML viejo
    soup = BeautifulSoup(html_viejo, "html.parser")
    
    # Buscar el encabezado que contiene "Objetivos"
    encabezado = soup.find(lambda tag: tag.name == "h2" and "Objetivos" in tag.get_text())
    
    if not encabezado:
        print("No se encontró la sección de objetivos.")
        return None
    
    # Encontrar la lista de objetivos
    objetivos_div = encabezado.find_next("div", class_="contenido_tab")
    
    if not objetivos_div:
        print("No se encontró el contenido de los objetivos.")
        return None
    
    lista_items = objetivos_div.find_all("li")
    objetivos_texto = [li.get_text(strip=True) for li in lista_items]
    
    # Construir el nuevo HTML
    nuevo_html = f'''
    <section>
        <h2 class="title__section">
            <span>
                <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512">
                    <path d="M256 512A256 256 0 1 0 256 0a256 256 0 1 0 0 512zm50.7-186.9L162.4 380.6c-19.4 7.5-38.5-11.6-31-31l55.5-144.3c3.3-8.5 9.9-15.1 18.4-18.4l144.3-55.5c19.4-7.5 38.5 11.6 31 31L325.1 306.7c-3.2 8.5-9.9 15.1-18.4 18.4zM288 256a32 32 0 1 0 -64 0 32 32 0 1 0 64 0z"/>
                </svg>
            </span>
            Objetivos                
        </h2>
        <ul class="info__list info__list--bullets">
            {''.join(f'<li class="info-item info-item__small">{objetivo}</li>' for objetivo in objetivos_texto)}
        </ul>
    </section>
    '''
    
    return nuevo_html.strip()

def main():
    if len(sys.argv) < 2:
        print("Uso: python convertir_objetivos.py <archivo.html>")
        return
    
    archivo_html = sys.argv[1]
    
    try:
        with open(archivo_html, "r", encoding="utf-8") as file:
            html_viejo = file.read()
    except FileNotFoundError:
        print(f"Error: No se encontró el archivo {archivo_html}")
        return
    
    html_nuevo = convertir_objetivos(html_viejo)
    if html_nuevo:
        with open("objetivos_convertidos.html", "w", encoding="utf-8") as file:
            file.write(html_nuevo)
        print("Archivo 'objetivos_convertidos.html' creado con éxito.")

if __name__ == "__main__":
    main()