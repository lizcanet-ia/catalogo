import streamlit as st
import requests
import urllib.parse

# Configuración de la página optimizada para móviles
st.set_page_config(
    page_title="ELECTRO+",
    page_icon="⚡",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Estilos CSS profesionales inspirados en e-commerce de alta gama
st.markdown("""
    <style>
    .main {
        background-color: #f4f5f7;
        padding-bottom: 80px;
    }
    html {
        scroll-behavior: smooth;
    }
    .top-bar {
        background-color: #7c3aed;
        height: 6px;
        width: 100%;
        margin-bottom: 12px;
        border-radius: 3px;
    }
    .brand-logo {
        font-size: 24px;
        font-weight: 900;
        color: #111827;
        letter-spacing: -0.5px;
    }
    .brand-logo span {
        color: #7c3aed;
    }
    .benefits-bar {
        display: flex;
        justify-content: space-around;
        background-color: white;
        border: 1px solid #e5e7eb;
        border-radius: 10px;
        padding: 12px 8px;
        margin-bottom: 20px;
        text-align: center;
    }
    .benefit-item {
        font-size: 10px;
        font-weight: 700;
        color: #374151;
        display: flex;
        flex-direction: column;
        align-items: center;
        gap: 4px;
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
    .added-badge {
        color: #047857;
        background-color: #d1fae5;
        font-size: 11px;
        font-weight: 700;
        padding: 4px 8px;
        border-radius: 6px;
        display: inline-block;
        margin-bottom: 4px;
        text-align: center;
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

if "categoria_activa" not in st.session_state:
    st.session_state.categoria_activa = "Todas"

# Barra superior purpura
st.markdown('<div class="top-bar"></div>', unsafe_allow_html=True)

productos = cargar_datos()

# Encabezado E-commerce (ELECTRO+ y contador de carrito)
total_items = sum(item["cantidad"] for item in st.session_state.carrito.values())
total_general = sum(item["precio"] * item["cantidad"] for item in st.session_state.carrito.values())

col_logo, col_cart = st.columns([3, 1])
with col_logo:
    st.markdown('<div class="brand-logo">ELECTRO<span>+</span></div>', unsafe_allow_html=True)
with col_cart:
    st.markdown(f'<div style="text-align: right; background-color: #f3f4f6; padding: 8px 12px; border-radius: 8px; font-weight: bold; font-size: 13px; color: #374151;">🛒 {total_items} items</div>', unsafe_allow_html=True)

st.markdown("")

# Barra de beneficios institucional
st.markdown("""
    <div class="benefits-bar">
        <div class="benefit-item">
            <span style="font-size: 16px;">🏪</span>
            <span>RETIRÁ GRATIS EN SUCURSAL</span>
        </div>
        <div class="benefit-item">
            <span style="font-size: 16px;">🎧</span>
            <span>VENTA POR WHATSAPP</span>
        </div>
        <div class="benefit-item">
            <span style="font-size: 16px;">📦</span>
            <span>ENVÍOS A TODO EL PAÍS</span>
        </div>
    </div>
""", unsafe_allow_html=True)

if not productos:
    st.warning("Cargando productos o sin conexión con Google Sheets...")
else:
    # -------------------------------------------------------------
    # 1. SECCIÓN DE CATEGORÍAS (Parte Superior)
    # -------------------------------------------------------------
    st.markdown("### 🗂️ Categorías")
    cat_cols_top = st.columns(4)
    with cat_cols_top[0]:
        if st.button("🏠 Todas", key="cat_top_todas", use_container_width=True):
            st.session_state.categoria_activa = "Todas"
            st.markdown('<meta http-equiv="refresh" content="0;url=#catalogo-productos">', unsafe_allow_html=True)
            st.rerun()
    with cat_cols_top[1]:
        if st.button("📺 Hogar", key="cat_top_hogar", use_container_width=True):
            st.session_state.categoria_activa = "Hogar"
            st.markdown('<meta http-equiv="refresh" content="0;url=#catalogo-productos">', unsafe_allow_html=True)
            st.rerun()
    with cat_cols_top[2]:
        if st.button("🌀 Lavado", key="cat_top_lavado", use_container_width=True):
            st.session_state.categoria_activa = "Lavado"
            st.markdown('<meta http-equiv="refresh" content="0;url=#catalogo-productos">', unsafe_allow_html=True)
            st.rerun()
    with cat_cols_top[3]:
        if st.button("🍳 Cocina", key="cat_top_cocina", use_container_width=True):
            st.session_state.categoria_activa = "Cocina"
            st.markdown('<meta http-equiv="refresh" content="0;url=#catalogo-productos">', unsafe_allow_html=True)
            st.rerun()

    st.markdown("---")

    # Ancla invisible para redirección
    st.markdown('<div id="catalogo-productos"></div>', unsafe_allow_html=True)

    # Buscador Global y Filtro de marcas ("Encontrá lo que querés")
    col_busq, col_marca = st.columns([2, 1])
    with col_busq:
        busqueda = st.text_input("🔍 Buscar...", placeholder="Encontrá lo que querés")
    with col_marca:
        marcas = ["TODAS"] + sorted(list(set(p.get("marca", "").strip() for p in productos if p.get("marca"))))
        marca_seleccionada = st.selectbox("Marca", marcas)

    # -------------------------------------------------------------
    # LÓGICA DE FILTRADO GLOBAL E INTELIGENTE
    # -------------------------------------------------------------
    productos_filtrados = []
    keywords_hogar = ["tv", "ventilador", "aire acondicionado"]
    keywords_lavado = ["lavarropas", "aspiradora"]
    keywords_cocina = ["cocina", "pava", "microondas", "heladera"]

    query = busqueda.lower().strip()

    for p in productos:
        nombre_prod = p.get("producto", "").lower()
        
        if query:
            match_categoria = True
        else:
            match_categoria = True
            cat = st.session_state.categoria_activa
            if cat == "Hogar":
                match_categoria = any(kw in nombre_prod for kw in keywords_hogar)
            elif cat == "Lavado":
                match_categoria = any(kw in nombre_prod for kw in keywords_lavado)
            elif cat == "Cocina":
                match_categoria = any(kw in nombre_prod for kw in keywords_cocina)

        match_marca = (marca_seleccionada == "TODAS" or p.get("marca", "").strip().lower() == marca_seleccionada.lower())
        
        match_query = (
            not query or
            query in nombre_prod or
            query in p.get("marca", "").lower() or
            query in str(p.get("cod", "")).lower()
        )

        if match_categoria and match_marca and match_query:
            productos_filtrados.append(p)

    if not productos_filtrados:
        if query:
            st.warning(f"🔍 No encontramos **'{busqueda}'** en nuestro catálogo.")
            wa_msg_ausente = f"Hola, estoy buscando '{busqueda}' y no lo encontré en el catálogo. ¿Me podrán confirmar si lo tienen disponible o se puede conseguir?"
            wa_url_ausente = f"https://wa.me/5491165295937?text={urllib.parse.quote(wa_msg_ausente)}"
            st.markdown(f'<a href="{wa_url_ausente}" target="_blank" style="display:block; text-align:center; background-color:#059669; color:white; padding:12px; border-radius:8px; text-decoration:none; font-size:14px; font-weight:bold; margin-top:10px; margin-bottom:15px; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">💬 Consultar por WhatsApp si está disponible</a>', unsafe_allow_html=True)
        else:
            st.info(f"No se encontraron productos en la categoría '{st.session_state.categoria_activa}'.")
    else:
        info_texto = f"Mostrando {len(productos_filtrados)} artículos" if query else f"Mostrando {len(productos_filtrados)} artículos (Categoría: **{st.session_state.categoria_activa}**)"
        st.write(info_texto)
        
        cols = st.columns(2)
        for idx, prod in enumerate(productos_filtrados):
            col = cols[idx % 2]
            with col:
                stock = prod.get("stock", 0)
                prod_id = str(prod.get("cod", prod.get("producto")))
                
                en_carrito = prod_id in st.session_state.carrito
                qty_en_carrito = st.session_state.carrito[prod_id]["cantidad"] if en_carrito else 0

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
                    
                    if en_carrito:
                        st.markdown(f'<div class="added-badge">✓ Agregado al carrito ({qty_en_carrito})</div>', unsafe_allow_html=True)
                        st.markdown('<a href="#carrito-abajo" style="color: #047857; font-size: 12px; font-weight: 600; text-decoration: underline; display: block; margin-bottom: 8px;">Ver en carrito 🛒</a>', unsafe_allow_html=True)
                    
                    st.markdown('<div class="shipping-tag">⚡ Envío rápido y seguro</div>', unsafe_allow_html=True)

                    if st.button("🛒 Agregar al carrito", key=f"btn_add_{idx}_{prod_id}", use_column_width=True):
                        if prod_id in st.session_state.carrito:
                            st.session_state.carrito[prod_id]["cantidad"] += 1
                        else:
                            st.session_state.carrito[prod_id] = {
                                "producto": prod.get("producto"),
                                "marca": prod.get("marca"),
                                "precio": precio_num,
                                "cantidad": 1
                            }
                        
                        st.toast(f"¡Agregado al carrito: {prod.get('producto')}!", icon="🛒")
                        st.rerun()
                    
                    st.markdown('</div>', unsafe_allow_html=True)

    # -------------------------------------------------------------
    # 2. SECCIÓN DEL CARRITO EN EL PIE DE PÁGINA
    # -------------------------------------------------------------
    st.markdown('<div id="carrito-abajo"></div>', unsafe_allow_html=True)
    st.markdown("---")
    st.markdown("### 🛒 Carrito de Compras y Pedido")

    if total_items == 0:
        st.info("Tu carrito está vacío. ¡Agregá productos desde el catálogo para armar tu pedido!")
    else:
        st.markdown(f"""
            <div style="background-color: #047857; color: white; padding: 12px 16px; border-radius: 10px; display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px; box-shadow: 0 4px 6px rgba(0,0,0,0.1);">
                <span style="font-weight: bold; font-size: 15px;">🛒 Total de Artículos: {total_items}</span>
                <span style="font-weight: bold; font-size: 15px;">Total: $ {total_general:,.0f}</span>
            </div>
        """.replace(",", "."), unsafe_allow_html=True)

        with st.expander("📦 Ver detalle completo del pedido y enviar a WhatsApp", expanded=True):
            mensaje_wa = "Hola, quiero realizar el siguiente pedido desde el catálogo:\n\n"
            
            for prod_id, item in list(st.session_state.carrito.items()):
                subtotal = item["precio"] * item["cantidad"]
                
                col_det1, col_plus, col_qty, col_minus, col_del = st.columns([2.2, 0.9, 0.9, 0.9, 0.9])
                with col_det1:
                    st.write(f"**{item['producto']}**\n`{item['marca']}` • Subtotal: ${subtotal:,.0f}".replace(",", "."))
                with col_plus:
                    if st.button("➕", key=f"foot_plus_{prod_id}"):
                        st.session_state.carrito[prod_id]["cantidad"] += 1
                        st.rerun()
                with col_qty:
                    st.markdown(f"<div style='text-align: center; font-weight: bold; font-size: 16px; padding-top: 8px;'>{item['cantidad']}</div>", unsafe_allow_html=True)
                with col_minus:
                    if st.button("➖", key=f"foot_minus_{prod_id}"):
                        if st.session_state.carrito[prod_id]["cantidad"] > 1:
                            st.session_state.carrito[prod_id]["cantidad"] -= 1
                        else:
                            del st.session_state.carrito[prod_id]
                        st.rerun()
                with col_del:
                    if st.button("🗑️", key=f"foot_del_{prod_id}"):
                        del st.session_state.carrito[prod_id]
                        st.rerun()
                
                mensaje_wa += f"• {item['cantidad']}x {item['producto']} ({item['marca']}) - Subtotal: $ {subtotal:,.0f}\n"
                st.markdown("---")

            st.markdown(f"### Total General: $ {total_general:,.0f}".replace(",", "."))
            mensaje_wa += f"\nTotal estimado del pedido: $ {total_general:,.0f}".replace(",", ".")
            
            wa_url = f"https://wa.me/5491165295937?text={urllib.parse.quote(mensaje_wa)}"
            
            st.markdown(f'<a href="{wa_url}" target="_blank" style="display:block; text-align:center; background-color:#059669; color:white; padding:14px; border-radius:8px; text-decoration:none; font-size:15px; font-weight:bold; box-shadow: 0 4px 6px rgba(0,0,0,0.15); margin-bottom: 10px;">📤 Enviar pedido completo por WhatsApp</a>', unsafe_allow_html=True)
            
            if st.button("🗑️ Vaciar carrito completo", use_container_width=True):
                st.session_state.carrito = {}
                st.rerun()

    # -------------------------------------------------------------
    # 3. SECCIÓN DE CATEGORÍAS (Al final de la página)
    # -------------------------------------------------------------
    st.markdown("---")
    st.markdown("### 🗂️ Categorías (Explorar más)")
    cat_cols_bottom = st.columns(4)
    with cat_cols_bottom[0]:
        if st.button("🏠 Todas", key="cat_bot_todas", use_container_width=True):
            st.session_state.categoria_activa = "Todas"
            st.markdown('<meta http-equiv="refresh" content="0;url=#catalogo-productos">', unsafe_allow_html=True)
            st.rerun()
    with cat_cols_bottom[1]:
        if st.button("📺 Hogar", key="cat_bot_hogar", use_container_width=True):
            st.session_state.categoria_activa = "Hogar"
            st.markdown('<meta http-equiv="refresh" content="0;url=#catalogo-productos">', unsafe_allow_html=True)
            st.rerun()
    with cat_cols_bottom[2]:
        if st.button("🌀 Lavado", key="cat_bot_lavado", use_container_width=True):
            st.session_state.categoria_activa = "Lavado"
            st.markdown('<meta http-equiv="refresh" content="0;url=#catalogo-productos">', unsafe_allow_html=True)
            st.rerun()
    with cat_cols_bottom[3]:
        if st.button("🍳 Cocina", key="cat_bot_cocina", use_container_width=True):
            st.session_state.categoria_activa = "Cocina"
            st.markdown('<meta http-equiv="refresh" content="0;url=#catalogo-productos">', unsafe_allow_html=True)
            st.rerun()
