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

# Estilos CSS profesionales con soporte para anclaje suave
st.markdown("""
    <style>
    .main {
        background-color: #f4f5f7;
        padding-bottom: 80px;
    }
    html {
        scroll-behavior: smooth;
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

# Inicializar estados
if "carrito" not in st.session_state:
    st.session_state.carrito = {}

if "ultimo_agregado" not in st.session_state:
    st.session_state.ultimo_agregado = None

# Encabezado principal estilo E-commerce
st.title("🛍️ Catálogo Exclusivo")
st.markdown("Elegí tus productos, armá tu pedido y envianos la lista al instante por WhatsApp.")

# -------------------------------------------------------------
# ALERTA DINÁMICA CON BOTÓN "VER CARRITO"
# -------------------------------------------------------------
if st.session_state.ultimo_agregado:
    st.markdown(f"""
        <div style="background-color: #047857; color: white; padding: 12px 16px; border-radius: 10px; display: flex; justify-content: space-between; align-items: center; margin-bottom: 15px; box-shadow: 0 4px 6px rgba(0,0,0,0.1);">
            <span style="font-weight: 600; font-size: 14px;">✅ ¡Agregado: {st.session_state.ultimo_agregado}!</span>
            <a href="#carrito-seccion" style="background-color: white; color: #047857; padding: 6px 14px; border-radius: 6px; text-decoration: none; font-weight: bold; font-size: 13px; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">Ver Carrito 🛒</a>
        </div>
    """, unsafe_allow_html=True)

productos = cargar_datos()

if not productos:
    st.warning("Cargando productos o sin conexión con Google Sheets...")
else:
    # -------------------------------------------------------------
    # SECCIÓN DE CATEGORÍAS (Tarjetas de navegación rápida)
    # -------------------------------------------------------------
    st.markdown("### 🗂️ Categorías")
    if "categoria_activa" not in st.session_state:
        st.session_state.categoria_activa = "Todas"

    cat_cols = st.columns(4)
    with cat_cols[0]:
        if st.button("🏠 Todas", use_container_width=True):
            st.session_state.categoria_activa = "Todas"
    with cat_cols[1]:
        if st.button("📺 Hogar", use_container_width=True):
            st.session_state.categoria_activa = "Hogar"
    with cat_cols[2]:
        if st.button("🌀 Lavado", use_container_width=True):
            st.session_state.categoria_activa = "Lavado"
    with cat_cols[3]:
        if st.button("🍳 Cocina", use_container_width=True):
            st.session_state.categoria_activa = "Cocina"

    st.markdown("---")

    # Buscador y Filtro de marcas
    col_busq, col_marca = st.columns([2, 1])
    with col_busq:
        busqueda = st.text_input("🔍 Buscar...", placeholder="Producto, marca o código")
    with col_marca:
        marcas = ["TODAS"] + sorted(list(set(p.get("marca", "").strip() for p in productos if p.get("marca"))))
        marca_seleccionada = st.selectbox("Marca", marcas)

    # Lógica de filtrado
    productos_filtrados = []
    keywords_hogar = ["tv", "ventilador", "aire acondicionado"]
    keywords_lavado = ["lavarropas", "aspiradora"]
    keywords_cocina = ["cocina", "pava", "microondas", "heladera"]

    for p in productos:
        nombre_prod = p.get("producto", "").lower()
        match_categoria = True
        cat = st.session_state.categoria_activa
        if cat == "Hogar":
            match_categoria = any(kw in nombre_prod for kw in keywords_hogar)
        elif cat == "Lavado":
            match_categoria = any(kw in nombre_prod for kw in keywords_lavado)
        elif cat == "Cocina":
            match_categoria = any(kw in nombre_prod for kw in keywords_cocina)

        match_marca = (marca_seleccionada == "TODAS" or p.get("marca", "").strip().lower() == marca_seleccionada.lower())
        query = busqueda.lower().strip()
        match_query = (
            not query or
            query in nombre_prod or
            query in p.get("marca", "").lower() or
            query in str(p.get("cod", "")).lower()
        )

        if match_categoria and match_marca and match_query:
            productos_filtrados.append(p)

    if not productos_filtrados:
        st.info(f"No se encontraron productos en la categoría '{st.session_state.categoria_activa}'.")
    else:
        st.write(f"Mostrando {len(productos_filtrados)} artículos (Categoría: **{st.session_state.categoria_activa}**)")
        
        cols = st.columns(2)
        for idx, prod in enumerate(productos_filtrados):
            col = cols[idx % 2]
            with col:
                stock = prod.get("stock", 0)
                
                if stock <= 0:
                    badge_html = '<span class="badge-out">Sin stock</span>'
                elif stock == 1:
                    badge_html = '<span class="badge-last">¡ÚLTIMA UNIDAD! 🔥</span>'
                elif stock < 3:
                    badge_html = '<span class="badge-few">¡ÚLTIMAS UNIDADES! 🔥</span>'
                else:
                    badge_html = '<span class="badge-ok">Disponible ✓</span>'

                precio_num = prod.get('precioVenta', 0)
                precio_str = f"$ {precio_num:,.0f}".replace(",", ".")
                
                with st.container():
                    st.markdown('<div class="product-card">', unsafe_allow_html=True)
                    
                    img_url = prod.get("imagenUrl", "")
                    if img_url:
                        st.image(img_url, use_column_width=True)
                    else:
                        st.markdown('<div style="height:140px; background:#f9fafb; display:flex; align-items:center; justify-content:center; color:#9ca3af; font-size:11px; border-radius:6px; margin-bottom:8px;">Sin imagen</div>', unsafe_allow_html=True)

                    st.markdown(f'<div class="product-brand">{prod.get("marca", "")}</div>', unsafe_allow_html=True)
                    st.markdown(f'<div class="product-title">{prod.get("producto", "")}</div>', unsafe_allow_html=True)
                    st.markdown(f'<div class="product-price">{precio_str}</div>', unsafe_allow_html=True)
                    st.markdown(f'<div>{badge_html}</div>', unsafe_allow_html=True)
                    st.markdown('<div class="shipping-tag">⚡ Envío rápido y seguro</div>', unsafe_allow_html=True)

                    # Botón para agregar al carrito
                    prod_id = str(prod.get("cod", prod.get("producto")))
                    if st.button("🛒 Agregar al carrito", key=f"btn_add_{idx}_{prod_id}", use_container_width=True):
                        if prod_id in st.session_state.carrito:
                            st.session_state.carrito[prod_id]["cantidad"] += 1
                        else:
                            st.session_state.carrito[prod_id] = {
                                "producto": prod.get("producto"),
                                "marca": prod.get("marca"),
                                "precio": precio_num,
                                "cantidad": 1
                            }
                        # Guardamos el nombre del último producto agregado para mostrar el banner
                        st.session_state.ultimo_agregado = prod.get('producto')
                        st.rerun()
                    
                    st.markdown('</div>', unsafe_allow_html=True)

    # -------------------------------------------------------------
    # ANCLAJE Y SECCIÓN DEL CARRITO EN EL PIE DE PÁGINA
    # -------------------------------------------------------------
    # Este div actúa como punto de destino al hacer clic en "Ver Carrito"
    st.markdown('<div id="carrito-seccion"></div>', unsafe_allow_html=True)
    
    total_items = sum(item["cantidad"] for item in st.session_state.carrito.values())
    total_general = sum(item["precio"] * item["cantidad"] for item in st.session_state.carrito.values())

    if total_items > 0:
        st.markdown("---")
        st.markdown("### 🛒 Resumen de tu Carrito y Pedido")
        
        mensaje_wa = "Hola, quiero realizar el siguiente pedido desde el catálogo:\n\n"
        
        for prod_id, item in list(st.session_state.carrito.items()):
            subtotal = item["precio"] * item["cantidad"]
            
            col_det1, col_det2, col_det3, col_det4 = st.columns([3, 1, 1, 1])
            with col_det1:
                st.write(f"**{item['producto']}**\n`{item['marca']}` • ${subtotal:,.0f}".replace(",", "."))
            with col_det2:
                if st.button("➕", key=f"foot_plus_{prod_id}"):
                    st.session_state.carrito[prod_id]["cantidad"] += 1
                    st.rerun()
            with col_det3:
                if st.button("➖", key=f"foot_minus_{prod_id}"):
                    if st.session_state.carrito[prod_id]["cantidad"] > 1:
                        st.session_state.carrito[prod_id]["cantidad"] -= 1
                    else:
                        del st.session_state.carrito[prod_id]
                    st.rerun()
            with col_det4:
                if st.button("🗑️", key=f"foot_del_{prod_id}"):
                    del st.session_state.carrito[prod_id]
                    st.rerun()
            
            mensaje_wa += f"• {item['cantidad']}x {item['producto']} ({item['marca']}) - Subtotal: $ {subtotal:,.0f}\n"
            st.markdown("---")

        st.markdown(f"### Total General: $ {total_general:,.0f}".replace(",", "."))
        mensaje_wa += f"\nTotal estimado del pedido: $ {total_general:,.0f}".replace(",", ".")
        
        wa_url = f"https://wa.me/5491165295937?text={urllib.parse.quote(mensaje_wa)}"
        
        st.markdown(f'<a href="{wa_url}" target="_blank" style="display:block; text-align:center; background-color:#059669; color:white; padding:14px; border-radius:8px; text-decoration:none; font-size:15px; font-weight:bold; box-shadow: 0 4px 6px rgba(0,0,0,0.15); margin-bottom: 20px;">📤 Enviar pedido completo por WhatsApp</a>', unsafe_allow_html=True)
        
        if st.button("🗑️ Vaciar carrito completo", use_container_width=True):
            st.session_state.carrito = {}
            st.session_state.ultimo_agregado = None
            st.rerun()
    else:
        st.info("Tu carrito está vacío. ¡Agregá productos para verlos acá resumidos!")
