# **MedImEncryption: Cifrado de Imágenes para Aplicaciones Médicas**

Este repositorio contiene un proyecto universitario basado en el estudio del artículo académico:  
**"An efficient and robust image encryption scheme for medical applications"**  
Autores: A. Kanso, M. Ghebleh.

---

## **Descripción del Proyecto**
Este proyecto tiene como objetivo explorar y aplicar un esquema robusto y eficiente de cifrado selectivo y completo de imágenes basado en mapas caóticos tipo "cat". Este enfoque es especialmente adecuado para aplicaciones médicas donde la seguridad de las imágenes es crítica.

El estudio original describe un esquema que emplea:
- **Fases de mezcla y enmascaramiento**: Utiliza mapas caóticos para reorganizar y proteger píxeles en imágenes.
- **Matrices pseudoaleatorias**: Mejora la seguridad y la eficiencia del proceso.

El esquema busca combinar altos niveles de **seguridad** con un rendimiento óptimo, haciendo que sea adecuado para aplicaciones médicas sensibles.

---

## **Inspiración del Proyecto**
Este proyecto universitario toma como referencia el artículo publicado por A. Kanso y M. Ghebleh, disponible en:  
*Department of Mathematics, Kuwait University (2015).*

En el artículo, los autores proponen un enfoque novedoso para el cifrado de imágenes médicas que incluye varias rondas de procesamiento con dos fases principales:
1. **Fase de Mezcla**: Reorganiza los píxeles de la imagen original utilizando mapas caóticos.
2. **Fase de Enmascaramiento**: Aplica operaciones para proteger los valores de los píxeles reorganizados.

---

## **Estructura del Repositorio**
- `src/`: Código fuente del esquema de cifrado basado en mapas caóticos.
- `docs/`: Documentación detallada del proyecto.
- `tests/`: Pruebas unitarias para verificar la implementación.
- `examples/`: Ejemplos de imágenes cifradas y descifradas.

---

## **Requisitos**
Para ejecutar este proyecto, necesitarás:
- Python 3.x
- Librerías: NumPy, Matplotlib, OpenCV

Instalación de dependencias:
```bash
pip install -r requirements.txt
