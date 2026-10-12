import streamlit as st
import requests
import urllib.parse

# Configuración de la página optimizada para móviles
st.set_page_config(
    page_title="Catálogo de Productos",
    page_icon="🛍️",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Estilos CSS personalizados para una estética profesional y limpia
st.markdown("""
    <style>
    .main {
        background-color: #f9fafb;
    }
    .badge-last {
        background-color: #fee2e2;
        color: #b91c1c;
        font-weight: bold;
        font-size: 11px;
        padding: 2px 8px;
        border-radius: 9999px;
    }
    .badge-few {
        background-color: #fef3c7;
        color: #92400e;
        font-weight: bold;
        font-size: 11px;
        padding: 2px 8px;
        border-radius: 9999px;
    }
    .badge-ok {
        background-color: #d1fae5;
        color: #065f46;
        font-size: 11px;
        padding: 2px 8px;
        border-radius: 9999px;
    }
    .badge-out {
        background-color: #f3f4f6;
        color: #4b5563;
        font-size: 11px;
        padding: 2px 8px;
        border-radius: 9999px;
    }
    </style>
""", unsafe_allow_html=True)

# URL de tu Apps Script API JSON (la misma que ya venías usando)
API_URL = "https://script.google.com/macros/s/AKfycbyIQqZPk3e_U17GjuO2LI99KS_wBWV0-91D_beFxaWOb0fWxLmS2gQEpBRwJaE5Y3E9aA/exec"

@st.cache_data(ttl=15)
def cargar_datos():
    try:
        response = requests.get(API_URL)
        result = response.json()
        if result.get("status") == "success":
            return result.get("data", [])
        return []
    except Exception as e:
        st.error(f"Error al conectar con la planilla: {e}")
        return []

# Encabezado principal
st.title("🛍️ Nuestros productos elegidos para vos")
st.markdown("Explorá nuestro catálogo y consultá al instante por WhatsApp.")

productos = cargar_datos()

if not productos:
    st.warning("No hay productos cargados o no se pudo establecer conexión con Google Sheets.")
else:
    # Buscador en tiempo real
    busqueda = st.text_input("🔍 Buscar por producto, marca o código...", "")

    # Filtro de marcas horizontal / desplegable
    marcas = ["TODAS"] + sorted(list(set(p.get("marca", "").strip() for p in productos if p.get("marca"))))
    marca_seleccionada = st.selectbox("Filtrar por marca:", marcas)

    # Filtrado lógico
    productos_filtrados = []
    for p in productos:
        match_marca = (marca_seleccionada == "TODAS" or p.get("marca", "").strip().lower() == marca_seleccionada.lower())
        query = busqueda.lower().strip()
        match_query = (
            not query or
            query in p.get("producto", "").lower() or
            query in p.get("marca", "").lower() or
            query in str(p.get("cod", "")).lower()
        )
        if match_marca and match_query:
            productos_filtrados.append(p)

    if not productos_filtrados:
        st.info("No se encontraron productos que coincidan con tu búsqueda.")
    else:
        st.write(f"Mostrando {len(productos_filtrados)} productos")
        
        # Grid de 2 columnas ideal para celulares Android
        cols = st.columns(2)
        for idx, prod in enumerate(productos_filtrados):
            col = cols[idx % 2]
            with col:
                stock = prod.get("stock", 0)
                
                # Insignias de Stock
                if stock <= 0:
                    badge_html = '<span class="badge-out">Sin stock</span>'
                elif stock == 1:
                    badge_html = '<span class="badge-last">ÚLTIMA! 🔥</span>'
                elif stock < 3:
                    badge_html = '<span class="badge-few">ÚLTIMAS 3 🔥</span>'
                else:
                    badge_html = '<span class="badge-ok">Disponible</span>'

                precio_str = f"$ {prod.get('precioVenta', 0):,.0f}".replace(",", ".")
                
                # Renderizado de imagen (usando la miniatura de Drive optimizada)
                img_url = prod.get("imagenUrl", "")
                if img_url:
                    st.image(img_url, use_column_width=True)
                else:
                    st.markdown('<div style="height:150px; background:#f3f4f6; display:flex; align-items:center; justify-content:center; color:#9ca3af; font-size:12px; border-radius:8px;">Sin imagen</div>', unsafe_allow_html=True)

                st.markdown(f"**{prod.get('producto', '')}**", unsafe_allow_html=True)
                st.markdown(f"<span style='color:#7c3aed; font-size:12px; font-weight:600; text-transform:uppercase;'>{prod.get('marca', '')}</span>", unsafe_allow_html=True)
                st.markdown(f"<div style='font-size:16px; font-weight:bold; margin-top:2px;'>{precio_str}</div>", unsafe_allow_html=True)
                st.markdown(f"<div style='font-size:12px; color:#4b5563; margin-bottom:8px;'>Stock: {stock} &nbsp; {badge_html}</div>", unsafe_allow_html=True)

                # Botón de WhatsApp con mensaje prearmado
                wa_msg = f"Hola, me interesa un producto del catalogo, quiero información sobre {prod.get('producto', '')}, {prod.get('marca', '')} y {precio_str}."
                wa_url = f"https://wa.me/5491165295937?text={urllib.parse.quote(wa_msg)}"
                
                st.markdown(f'<a href="{wa_url}" target="_blank" style="display:block; text-align:center; background-color:#059669; color:white; padding:8px 12px; border-radius:8px; text-decoration:none; font-size:12px; font-weight:600;">💬 Consultar por WhatsApp</a>', unsafe_allow_html=True)
                st.markdown("---")