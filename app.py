import streamlit as st
from supabase import create_client
import urllib.parse

# Configuración de la página optimizada para móviles y PC
st.set_page_config(
    page_title="ELECTRO+",
    page_icon="🛒",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Estilos CSS avanzados y totalmente responsive para PC y Android
st.markdown("""
    <style>
    /* Tipografía unificada sans-serif moderna */
    html, body, [class*="css"] {
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif !important;
    }
    
    .main {
        background-color: #f4f5f7;
        padding-bottom: 60px;
    }
    
    html {
        scroll-behavior: smooth;
    }
    
    /* Barra superior violeta con mayor separación */
    .top-bar {
        background-color: #7c3aed;
        height: 6px;
        width: 100%;
        margin-top: 6px;
        margin-bottom: 32px;
        border-radius: 3px;
    }
    
    /* Logotipo ELECTRO+ ampliado */
    .brand-logo {
        font-size: 28px;
        font-weight: 900;
        color: #111827;
        letter-spacing: -0.5px;
        line-height: 1.1;
    }
    
    .brand-logo span {
        color: #7c3aed;
    }
    
    /* Enlace cliqueable para el contador de carrito */
    .cart-link-badge {
        display: block;
        text-align: right;
        background-color: #f3f4f6;
        padding: 8px 12px;
        border-radius: 8px;
        font-weight: bold;
        font-size: 16px; 
        color: #374151;
        text-decoration: none;
        transition: background-color 0.2s ease;
    }
    .cart-link-badge:hover {
        background-color: #e5e7eb;
        color: #111827;
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

    /* -------------------------------------------------------------
       CUSTOMIZACIÓN RESALTADA DEL BOTÓN FULLSCREEN DE IMÁGENES
    ------------------------------------------------------------- */
    div[data-testid="stImage"] [data-testid="stElementActionButton"] {
        opacity: 1 !important;
        visibility: visible !important;
    }

    div[data-testid="stImage"] [data-testid="stElementActionButton"] button {
        background-color: #ffffff !important;
        border: 1px solid #7c3aed !important;
        border-radius: 20px !important;
        padding: 6px 14px !important;
        box-shadow: 0 4px 10px rgba(124, 58, 237, 0.25) !important;
        display: flex !important;
        align-items: center !important;
        gap: 6px !important;
        cursor: pointer !important;
        transition: transform 0.2s ease, box-shadow 0.2s ease !important;
    }

    div[data-testid="stImage"] [data-testid="stElementActionButton"] button:hover {
        transform: scale(1.05) !important;
        box-shadow: 0 6px 14px rgba(124, 58, 237, 0.35) !important;
    }

    div[data-testid="stImage"] [data-testid="stElementActionButton"] svg {
        width: 18px !important;
        height: 18px !important;
        color: #7c3aed !important;
    }

    div[data-testid="stImage"] [data-testid="stElementActionButton"] button::after {
        content: "Amplia foto" !important;
        font-size: 12px !important;
        font-weight: 700 !important;
        color: #7c3aed !important;
        white-space: nowrap !important;
    }
    </style>
""", unsafe_allow_html=True)

# CONFIGURACIÓN DE SUPABASE Y CLIENTE
SUPABASE_URL = "https://fyakcgfnhrsiohistsac.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImZ5YWtjZ2ZuaHJzaW9oaXN0c2FjIiwicm9sZSI6ImFub24iLCJpYXQiOjE3OTE4NDU1MzYsImV4cCI6MjEwNzQyMTUzNn0.NSguf7dQUss3LOz_hhpFlEr20YfvjxEbVATg4OX01sM"

CLIENTE_ACTUAL = "electro_plus"
URL_BASE_APP = "https://catalogo-lizia.streamlit.app"

@st.cache_data(ttl=10)
def cargar_datos():
    try:
        supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
        response = (
            supabase.table("productos")
            .select("*")
            .eq("client_id", CLIENTE_ACTUAL)
            .eq("activo", True)
            .execute()
        )
        data = response.data
        if data:
            productos = []
            for p in data:
                productos.append({
                    "cod": p.get("cod"),
                    "producto": p.get("producto"),
                    "marca": p.get("marca"),
                    "precioVenta": float(p.get("precio_venta", 0)),
                    "stock": int(p.get("stock", 0)),
                    "imagenUrl": p.get("imagen_url", "")
                })
            return productos
        return []
    except Exception as e:
        st.error(f"Error al conectar con Supabase: {e}")
        return []

# Inicializar estados
if "carrito" not in st.session_state:
    st.session_state.carrito = {}

if "categoria_activa" not in st.session_state:
    st.session_state.categoria_activa = "Todas"

# Detectar si la URL trae un producto específico (ej: ?prod=AR-ELEC-0001)
query_params = st.query_params
prod_en_url = query_params.get("prod", "")

# Barra superior purpura y Ancla para el inicio
st.markdown('<div class="top-bar"></div>', unsafe_allow_html=True)
st.markdown('<div id="top-inicio"></div>', unsafe_allow_html=True)

productos = cargar_datos()

# Encabezado E-commerce
total_items = sum(item["cantidad"] for item in st.session_state.carrito.values())
total_general = sum(item["precio"] * item["cantidad"] for item in st.session_state.carrito.values())

col_logo, col_cart = st.columns([2.6, 1.4])
with col_logo:
    st.markdown('<div class="brand-logo">ELECTRO<span>+</span></div>', unsafe_allow_html=True)
with col_cart:
    st.markdown(f'<a href="#carrito-abajo" class="cart-link-badge">🛒 {total_items} items</a>', unsafe_allow_html=True)

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
    st.warning("Cargando productos o sin conexión con Supabase...")
else:
    # -------------------------------------------------------------
    # 1. SECCIÓN DE CATEGORÍAS (Parte Superior)
    # -------------------------------------------------------------
    st.markdown("### Categorías")
    cat_cols_top = st.columns(4)
    with cat_cols_top[0]:
        if st.button("Todas", key="cat_top_todas", use_container_width=True):
            st.session_state.categoria_activa = "Todas"
            st.session_state.input_busqueda = ""
            st.query_params.clear()
            st.rerun()
    with cat_cols_top[1]:
        if st.button("Hogar", key="cat_top_hogar", use_container_width=True):
            st.session_state.categoria_activa = "Hogar"
            st.session_state.input_busqueda = ""
            st.query_params.clear()
            st.rerun()
    with cat_cols_top[2]:
        if st.button("Lavado", key="cat_top_lavado", use_container_width=True):
            st.session_state.categoria_activa = "Lavado"
            st.session_state.input_busqueda = ""
            st.query_params.clear()
            st.rerun()
    with cat_cols_top[3]:
        if st.button("Cocina", key="cat_top_cocina", use_container_width=True):
            st.session_state.categoria_activa = "Cocina"
            st.session_state.input_busqueda = ""
            st.query_params.clear()
            st.rerun()

    st.markdown("---")

    st.markdown('<div id="catalogo-productos"></div>', unsafe_allow_html=True)

    # Buscador y Marcas
    col_busq, col_marca = st.columns([2, 1])
    with col_busq:
        busqueda = st.text_input("🔍 Buscar...", placeholder="Encontrá lo que querés", key="input_busqueda")
    with col_marca:
        marcas = ["TODAS"] + sorted(list(set(p.get("marca", "").strip() for p in productos if p.get("marca"))))
        marca_seleccionada = st.selectbox("Marca", marcas)

    # Filtrado
    productos_filtrados = []
    keywords_hogar = ["tv", "ventilador", "aire acondicionado"]
    keywords_lavado = ["lavarropas", "aspiradora"]
    keywords_cocina = ["cocina", "pava", "microondas", "heladera"]

    query = busqueda.lower().strip()

    for p in productos:
        nombre_prod = p.get("producto", "").lower()
        prod_id = str(p.get("cod", ""))
        
        # Si la URL trae un producto específico, filtramos estrictamente por él
        if prod_en_url:
            match = (prod_id.lower() == prod_en_url.lower())
        else:
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
                query in prod_id.lower()
            )
            match = match_categoria and match_marca and match_query

        if match:
            productos_filtrados.append(p)

    if prod_en_url and productos_filtrados:
        st.info(f"✨ Viendo producto compartido. [Ver todo el catálogo]({URL_BASE_APP})")

    if not productos_filtrados:
        if query or prod_en_url:
            st.warning("🔍 No encontramos el producto solicitado.")
            if prod_en_url:
                if st.button("Ver catálogo completo"):
                    st.query_params.clear()
                    st.rerun()
        else:
            st.info(f"No se encontraron productos en la categoría '{st.session_state.categoria_activa}'.")
    else:
        info_texto = f"Mostrando {len(productos_filtrados)} artículos" if query or prod_en_url else f"Mostrando {len(productos_filtrados)} artículos (Categoría: **{st.session_state.categoria_activa}**)"
        st.write(info_texto)
        
        cols = st.columns(2)
        for idx, prod in enumerate(productos_filtrados):
            col = cols[idx % 2]
            with col:
                stock = prod.get("stock", 0)
                prod_id = str(prod.get("cod", prod.get("producto")))
                
                en_carrito = prod_id in st.session_state.carrito
                qty_en_carrito = st.session_state.carrito[prod_id]["cantidad"] if en_carrito else 0

                precio_num = prod.get('precioVenta', 0)
                precio_str = f"$ {precio_num:,.0f}".replace(",", ".")
                
                with st.container():
                    st.markdown('<div class="product-card">', unsafe_allow_html=True)
                    
                    # Imagen
                    img_url = prod.get("imagenUrl", "")
                    if img_url:
                        st.image(img_url, use_column_width=True)
                    else:
                        st.markdown('<div style="height:140px; background:#f9fafb; display:flex; align-items:center; justify-content:center; color:#9ca3af; font-size:11px; border-radius:6px; margin-bottom:8px;">Sin imagen</div>', unsafe_allow_html=True)

                    st.markdown(f'<div class="product-brand">{prod.get("marca", "")}</div>', unsafe_allow_html=True)
                    st.markdown(f'<div class="product-title">{prod.get("producto", "")}</div>', unsafe_allow_html=True)
                    st.markdown(f'<div class="product-price">{precio_str}</div>', unsafe_allow_html=True)

                    # Botón de Compartir por WhatsApp con enlace directo al producto
                    link_directo_producto = f"{URL_BASE_APP}/?prod={prod_id}"
                    wa_share_msg = f"¡Mirá este producto en Electro+: {prod.get('producto')} ({prod.get('marca')}) a solo {precio_str}!\n👉 Ver producto: {link_directo_producto}"
                    wa_share_url = f"https://wa.me/?text={urllib.parse.quote(wa_share_msg)}"
                    st.markdown(f'<a href="{wa_share_url}" target="_blank" style="display:block; text-align:center; background-color:#25d366; color:white; padding:6px; border-radius:6px; text-decoration:none; font-size:11px; font-weight:bold; margin-bottom:8px; box-shadow:0 1px 2px rgba(0,0,0,0.05);">📲 Compartir por WhatsApp</a>', unsafe_allow_html=True)

                    # Gestión de stock y carrito
                    if stock <= 0:
                        badge_html = '<span class="badge-out">Sin stock</span>'
                        st.markdown(f'<div>{badge_html}</div>', unsafe_allow_html=True)
                        st.markdown('<div class="shipping-tag" style="background-color:#fef2f2; color:#b91c1c;">🚫 Producto agotado</div>', unsafe_allow_html=True)
                        
                        with st.expander("🔔 Avísame cuando ingrese"):
                            with st.form(key=f"form_stock_{idx}_{prod_id}"):
                                st.markdown(f"<p style='font-size:11px; color:#4b5563; margin-bottom:4px;'>Dejanos tus datos para avisarte ni bien entre stock de este producto.</p>", unsafe_allow_html=True)
                                nombre_lead = st.text_input("Tu Nombre", key=f"lead_nombre_{idx}_{prod_id}")
                                tel_lead = st.text_input("Tu Teléfono / WhatsApp", key=f"lead_tel_{idx}_{prod_id}")
                                
                                enviar_lead = st.form_submit_button("📤 Registrarme", use_container_width=True)
                                if enviar_lead:
                                    if nombre_lead.strip() and tel_lead.strip():
                                        try:
                                            supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
                                            supabase.table("stock_leads").insert({
                                                "client_id": CLIENTE_ACTUAL,
                                                "cod": prod_id,
                                                "producto": prod.get("producto"),
                                                "nombre": nombre_lead.strip(),
                                                "telefono": tel_lead.strip()
                                            }).execute()
                                            st.success("¡Listo! Te avisaremos cuando ingrese.")
                                        except Exception as e:
                                            st.error("Hubo un error al registrar tus datos.")
                                    else:
                                        st.warning("Por favor completa ambos campos.")
                    else:
                        if stock == 1:
                            badge_html = '<span class="badge-last">¡ÚLTIMA UNIDAD! 🔥</span>'
                        elif stock < 3:
                            badge_html = '<span class="badge-few">¡ÚLTIMAS UNIDADES! 🔥</span>'
                        else:
                            badge_html = '<span class="badge-ok">Disponible ✓</span>'
                        
                        st.markdown(f'<div>{badge_html}</div>', unsafe_allow_html=True)
                        
                        if en_carrito:
                            st.markdown(f'<div class="added-badge">✓ Agregado al carrito ({qty_en_carrito})</div>', unsafe_allow_html=True)
                            st.markdown('<a href="#carrito-abajo" style="color: #047857; font-size: 12px; font-weight: 600; text-decoration: underline; display: block; margin-bottom: 8px;">Ver en carrito 🛒</a>', unsafe_allow_html=True)
                        
                        st.markdown('<div class="shipping-tag">⚡ Envío rápido y seguro</div>', unsafe_allow_html=True)

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
                            
                            st.toast(f"¡Agregado al carrito: {prod.get('producto')}!", icon="🛒")
                            st.rerun()
                    
                    st.markdown('</div>', unsafe_allow_html=True)

    # -------------------------------------------------------------
    # 2. SECCIÓN DEL CARRITO EN EL PIE DE PÁGINA
    # -------------------------------------------------------------
    st.markdown('<div id="carrito-abajo"></div>', unsafe_allow_html=True)
    st.markdown("---")
    st.markdown("### Carrito de Compras y Pedido")

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
                
                c_info, c_qty, c_del = st.columns([2.5, 2, 1])
                with c_info:
                    st.markdown(f"**{item['producto']}**<br><span style='font-size:11px; color:#7c3aed; font-weight:600;'>{item['marca']}</span><br><span style='font-size:12px; font-weight:700;'>Subtotal: ${subtotal:,.0f}</span>".replace(",", "."), unsafe_allow_html=True)
                with c_qty:
                    nueva_cantidad = st.number_input(
                        "Cant",
                        min_value=1,
                        max_value=99,
                        value=item["cantidad"],
                        key=f"qty_input_{prod_id}",
                        label_visibility="collapsed"
                    )
                    if nueva_cantidad != item["cantidad"]:
                        item["cantidad"] = nueva_cantidad
                        st.rerun()
                with c_del:
                    if st.button("🗑️", key=f"foot_del_{prod_id}", use_container_width=True):
                        del st.session_state.carrito[prod_id]
                        st.rerun()
                
                mensaje_wa += f"• {item['cantidad']}x {item['producto']} ({item['marca']}) - Subtotal: $ {subtotal:,.0f}\n"
                st.markdown("<hr style='margin: 8px 0; border-color: #e5e7eb;'>", unsafe_allow_html=True)

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
    st.markdown("### Categorías (Explorar más)")
    cat_cols_bottom = st.columns(4)
    with cat_cols_bottom[0]:
        if st.button("Todas", key="cat_bot_todas", use_container_width=True):
            st.session_state.categoria_activa = "Todas"
            st.session_state.input_busqueda = ""
            st.query_params.clear()
            st.rerun()
    with cat_cols_bottom[1]:
        if st.button("Hogar", key="cat_bot_hogar", use_container_width=True):
            st.session_state.categoria_activa = "Hogar"
            st.session_state.input_busqueda = ""
            st.query_params.clear()
            st.rerun()
    with cat_cols_bottom[2]:
        if st.button("Lavado", key="cat_bot_lavado", use_container_width=True):
            st.session_state.categoria_activa = "Lavado"
            st.session_state.input_busqueda = ""
            st.query_params.clear()
            st.rerun()
    with cat_cols_bottom[3]:
        if st.button("Cocina", key="cat_bot_cocina", use_container_width=True):
            st.session_state.categoria_activa = "Cocina"
            st.session_state.input_busqueda = ""
            st.query_params.clear()
            st.rerun()

    # Botón Volver arriba
    st.markdown(
        """
        <div style="text-align: center; margin-top: 25px; margin-bottom: 20px;">
            <a href="#top-inicio" style="display: inline-block; background-color: #ffffff; color: #374151; padding: 10px 24px; border-radius: 8px; text-decoration: none; font-size: 13px; font-weight: bold; border: 1px solid #d1d5db; box-shadow: 0 2px 4px rgba(0,0,0,0.05);">
                ⬆️ Volver arriba
            </a>
        </div>
        """,
        unsafe_allow_html=True
    )
