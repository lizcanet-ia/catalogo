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

# Estilos CSS profesionales inspirados en e-commerce de alta gama
st.markdown("""
    <style>
    .main {
        background-color: #f4f5f7;
    }
    .product-card {
        background-color: white;
        border: 1px solid #e5e7eb;
        border-radius: 12px;
        padding: 14px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.02);
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        height: 100%;
        margin-bottom: 16px;
        transition: box-shadow 0.2s ease;
    }
    .product-card:hover {
        box-shadow: 0 4px 12px rgba(0,0,0,0.08);
    }
    .badge-last {
        background-color: #fee2e2;
        color: #b91c1c;
        font-weight: 700;
        font-size: 10px;
        padding: 3px 8px;
        border-radius: 6px;
        display: inline-block;
        margin-bottom: 6px;
    }
    .badge-few {
        background-color: #fef3c7;
        color: #92400e;
        font-weight: 700;
        font-size: 10px;
        padding: 3px 8px;
        border-radius: 6px;
        display: inline-block;
        margin-bottom: 6px;
    }
    .badge-ok {
        background-color: #d1fae5;
        color: #065f46;
        font-weight: 600;
        font-size: 10px;
        padding: 3px 8px;
        border-radius: 6px;
        display: inline-block;
        margin-bottom: 6px;
    }
    .badge-out {
        background-color: #f3f4f6;
        color: #4b5563;
        font-weight: 600;
        font-size: 10px;
        padding: 3px 8px;
        border-radius: 6px;
        display: inline-block;
        margin-bottom: 6px;
    }
    .product-title {
        font-size: 13px;
        font-weight: 500;
        color: #1f2937;
        margin-bottom: 8px;
        line-height: 1.3;
        display: -webkit-box;
        -webkit-line-clamp: 2;
        -webkit-box-orient: vertical;
        overflow: hidden;
        height: 34px;
    }
    .product-brand {
        font-size: 10px;
        font-weight: 700;
        color: #7c3aed;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        margin-bottom: 2px;
    }
    .product-price {
        font-size: 18px;
        font-weight: 800;
        color: #111827;
        margin: 4px 0;
    }
    .shipping-tag {
        color: #059669;
        font-size: 11px;
        font-weight: 600;
        background-color: #ecfdf5;
        padding: 3px 6px;
        border-radius: 4px;
        display: inline-block;
        margin-top: 6px;
        margin-bottom: 10px;
    }
    </style>
""", unsafe_allow_html=True)

# URL de tu Apps Script API JSON
API_URL = "https://script.google.com/macros/s/AKfycbyIQqZPk3e_U17GjuO2LI99KS_wBWV0-91D_beFxaWOb0fWxLmS2gQEpBRwJaE5Y3E9aA/exec"

@st.cache_data(ttl=10)
def cargar_datos():
    try:
        response = requests.get(API_URL)
        result = response.json()
        if result.get("status") == "success":
            return result.get("data", [])
        return []
    except Exception as e:
        return []

# Encabezado principal
st.title("🛍️ Nuestros productos")
st.markdown("Explorá nuestro catálogo y comprá al instante por WhatsApp.")

productos = cargar_datos()

if not productos:
    st.warning("Cargando productos o sin conexión con Google Sheets...")
else:
    # Buscador y Filtros ordenados
    col_busq, col_marca = st.columns([2, 1])
    with col_busq:
        busqueda = st.text_input("🔍 Buscar...", placeholder="Producto, marca o código")
    with col_marca:
        marcas = ["TODAS"] + sorted(list(set(p.get("marca", "").strip() for p in productos if p.get("marca"))))
        marca_seleccionada = st.selectbox("Marca", marcas)

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
        st.write(f"Mostrando {len(productos_filtrados)} artículos")
        
        # Grid de 2 columnas con tarjetas estilo E-commerce moderno
        cols = st.columns(2)
        for idx, prod in enumerate(productos_filtrados):
            col = cols[idx % 2]
            with col:
                stock = prod.get("stock", 0)
                
                # Insignias de Stock estilizadas
                if stock <= 0:
                    badge_html = '<span class="badge-out">Sin stock</span>'
                elif stock == 1:
                    badge_html = '<span class="badge-last">¡ÚLTIMA UNIDAD! 🔥</span>'
                elif stock < 3:
                    badge_html = '<span class="badge-few">¡ÚLTIMAS UNIDADES! 🔥</span>'
                else:
                    badge_html = '<span class="badge-ok">Disponible ✓</span>'

                precio_str = f"$ {prod.get('precioVenta', 0):,.0f}".replace(",", ".")
                
                # Renderizado dentro de contenedor tipo tarjeta
                with st.container():
                    st.markdown('<div class="product-card">', unsafe_allow_html=True)
                    
                    # Imagen del producto
                    img_url = prod.get("imagenUrl", "")
                    if img_url:
                        st.image(img_url, use_column_width=True)
                    else:
                        st.markdown('<div style="height:140px; background:#f9fafb; display:flex; align-items:center; justify-content:center; color:#9ca3af; font-size:11px; border-radius:6px; margin-bottom:8px;">Sin imagen</div>', unsafe_allow_html=True)

                    # Textos y detalles
                    st.markdown(f'<div class="product-brand">{prod.get("marca", "")}</div>', unsafe_allow_html=True)
                    st.markdown(f'<div class="product-title">{prod.get("producto", "")}</div>', unsafe_allow_html=True)
                    st.markdown(f'<div class="product-price">{precio_str}</div>', unsafe_allow_html=True)
                    st.markdown(f'<div>{badge_html}</div>', unsafe_allow_html=True)
                    st.markdown('<div class="shipping-tag">⚡ Envío rápido y seguro</div>', unsafe_allow_html=True)

                    # Botón de WhatsApp con diseño e-commerce
                    wa_msg = f"Hola, me interesa un producto del catalogo, quiero información sobre {prod.get('producto', '')}, {prod.get('marca', '')} y {precio_str}."
                    wa_url = f"https://wa.me/5491165295937?text={urllib.parse.quote(wa_msg)}"
                    
                    st.markdown(f'<a href="{wa_url}" target="_blank" style="display:block; text-align:center; background-color:#059669; color:white; padding:8px 10px; border-radius:8px; text-decoration:none; font-size:12px; font-weight:600; box-shadow: 0 1px 2px rgba(0,0,0,0.05);">💬 Consultar por WhatsApp</a>', unsafe_allow_html=True)
                    
                    st.markdown('</div>', unsafe_allow_html=True)
