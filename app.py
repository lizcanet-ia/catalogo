import streamlit as st
from supabase import create_client
import urllib.parse
import textwrap

st.set_page_config(
    page_title="Catálogo Digital",
    page_icon="🛒",
    layout="wide",
    initial_sidebar_state="collapsed"
)

SUPABASE_URL = "https://fyakcgfnhrsiohistsac.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImZ5YWtjZ2ZuaHJzaW9oaXN0c2FjIiwicm9sZSI6ImFub24iLCJpYXQiOjE3OTE4NDU1MzYsImV4cCI6MjEwNzQyMTUzNn0.NSguf7dQUss3LOz_hhpFlEr20YfvjxEbVATg4OX01sM"

URL_BASE_APP = "https://catalogo-lizia.streamlit.app"

# --- DETECCIÓN MULTI-CLIENTE POR URL ---
query_params = st.query_params
CLIENTE_SOLICITADO = query_params.get("cliente", "electro_plus").strip().lower()
prod_en_url = query_params.get("prod", "")

@st.cache_data(ttl=10)
def cargar_config_cliente(slug_cliente):
    try:
        supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
        response = (
            supabase.table("clientes")
            .select("*")
            .eq("client_id", slug_cliente)
            .eq("activo", True)
            .execute()
        )
        if response.data and len(response.data) > 0:
            row = response.data[0]
            return {
                "client_id": row.get("client_id", slug_cliente),
                "nombre_comercio": row.get("nombre_comercio") or "ELECTRO+",
                "whatsapp_numero": row.get("whatsapp_numero") or "5491165295937",
                "color_primario": row.get("color_primario") or "#7c3aed"
            }
        # Fallback de seguridad en caso de no encontrar el cliente en la tabla
        return {
            "client_id": slug_cliente,
            "nombre_comercio": "ELECTRO+",
            "whatsapp_numero": "5491165295937",
            "color_primario": "#7c3aed"
        }
    except Exception:
        return {
            "client_id": slug_cliente,
            "nombre_comercio": "ELECTRO+",
            "whatsapp_numero": "5491165295937",
            "color_primario": "#7c3aed"
        }

@st.cache_data(ttl=10)
def cargar_productos_cliente(slug_cliente):
    try:
        supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
        response = (
            supabase.table("productos")
            .select("*")
            .eq("client_id", slug_cliente)
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
                    "precioAnterior": float(p.get("precio_anterior")) if p.get("precio_anterior") is not None else None,
                    "descTransferenciaPct": float(p.get("descuento_transferencia_pct")) if p.get("descuento_transferencia_pct") is not None else None,
                    "cuotasSinInteres": int(p.get("cuotas_sin_interes")) if p.get("cuotas_sin_interes") is not None else None,
                    "envioTexto": str(p.get("envio_texto") or "").strip(),
                    "retiroTexto": str(p.get("retiro_texto") or "").strip(),
                    "fichaTecnica": str(p.get("ficha_tecnica") or "").strip(),
                    "categoria": str(p.get("categoria") or "General").strip(),
                    "stock": int(p.get("stock", 0)),
                    "imagenUrl": p.get("imagen_url", "")
                })
            return productos
        return []
    except Exception as e:
        st.error(f"Error al conectar con Supabase: {e}")
        return []

config_cliente = cargar_config_cliente(CLIENTE_SOLICITADO)
COLOR_MARCA = config_cliente.get("color_primario", "#7c3aed")
NOMBRE_MARCA = config_cliente.get("nombre_comercio", "ELECTRO+")
WHATSAPP_NUMERO = config_cliente.get("whatsapp_numero", "5491165295937")

# Función para formatear el logo destacando el símbolo o última letra con el color de marca
def formatear_logo_html(nombre):
    if "+" in nombre:
        partes = nombre.rsplit("+", 1)
        return f'{partes[0]}<span>+</span>{partes[1]}'
    elif "&" in nombre:
        partes = nombre.rsplit("&", 1)
        return f'{partes[0]}<span>&</span>{partes[1]}'
    else:
        return nombre

LOGO_HTML = formatear_logo_html(NOMBRE_MARCA)

st.markdown(f"""
    <style>
    .block-container {{
        max-width: 95% !important;
        padding-top: 2rem !important;
        padding-bottom: 3rem !important;
        padding-left: 2rem !important;
        padding-right: 2rem !important;
    }}

    html, body, [class*="css"] {{
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif !important;
    }}
    
    .main {{
        background-color: #f4f5f7;
        padding-bottom: 60px;
    }}
    
    html {{
        scroll-behavior: smooth;
    }}
    
    .top-bar {{
        background-color: {COLOR_MARCA};
        height: 6px;
        width: 100%;
        margin-top: 6px;
        margin-bottom: 32px;
        border-radius: 3px;
    }}
    
    .brand-logo {{
        font-size: 42px;
        font-weight: 900;
        color: #111827;
        letter-spacing: -0.5px;
        line-height: 1.1;
    }}
    
    .brand-logo span {{
        color: {COLOR_MARCA};
    }}
    
    .cart-link-badge {{
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
    }}
    .cart-link-badge:hover {{
        background-color: #e5e7eb;
        color: #111827;
    }}
    
    .benefits-bar {{
        display: flex;
        justify-content: space-around;
        background-color: white;
        border: 1px solid #e5e7eb;
        border-radius: 10px;
        padding: 14px 10px;
        margin-bottom: 20px;
        text-align: center;
    }}
    
    .benefit-item {{
        font-size: 12px;
        font-weight: 700;
        color: #374151;
        display: flex;
        flex-direction: column;
        align-items: center;
        gap: 4px;
    }}
    
    .badge-last {{
        background-color: #fee2e2;
        color: #b91c1c;
        font-weight: 700;
        font-size: 12px;
        padding: 5px 12px;
        border-radius: 6px;
        display: inline-block;
    }}
    
    .badge-few {{
        background-color: #fef3c7;
        color: #92400e;
        font-weight: 700;
        font-size: 12px;
        padding: 5px 12px;
        border-radius: 6px;
        display: inline-block;
    }}
    
    .badge-ok {{
        background-color: #d1fae5;
        color: #065f46;
        font-weight: 700;
        font-size: 12px;
        padding: 5px 12px;
        border-radius: 6px;
        display: inline-block;
    }}
    
    .badge-out {{
        background-color: #f3f4f6;
        color: #4b5563;
        font-weight: 700;
        font-size: 12px;
        padding: 5px 12px;
        border-radius: 6px;
        display: inline-block;
    }}

    .badge-discount {{
        background-color: #ef4444;
        color: #ffffff;
        font-weight: 800;
        font-size: 13px;
        padding: 4px 10px;
        border-radius: 6px;
        display: inline-block;
        margin-left: 8px;
        vertical-align: middle;
    }}

    .old-price {{
        font-size: 18px;
        color: #9ca3af;
        text-decoration: line-through;
        font-weight: 600;
        margin-right: 8px;
    }}
    
    .product-title {{
        font-size: 18px;
        font-weight: 700;
        color: #111827;
        margin-bottom: 10px;
        line-height: 1.4;
        display: -webkit-box;
        -webkit-line-clamp: 2;
        -webkit-box-orient: vertical;
        overflow: hidden;
        min-height: 50px;
    }}
    
    .product-brand {{
        font-size: 13px;
        font-weight: 800;
        color: {COLOR_MARCA};
        text-transform: uppercase;
        letter-spacing: 0.8px;
        margin-bottom: 6px;
    }}
    
    .product-price {{
        font-size: 24px;
        font-weight: 900;
        color: #111827;
        margin: 6px 0 12px 0;
        display: flex;
        align-items: center;
        flex-wrap: wrap;
        gap: 6px;
    }}

    .promo-box {{
        background-color: #f9fafb;
        border: 1px solid #e5e7eb;
        border-radius: 8px;
        padding: 12px;
        margin-top: 10px;
        margin-bottom: 12px;
        display: flex;
        flex-direction: column;
        gap: 10px;
        min-height: 160px;
    }}

    .promo-transfer {{
        background-color: #ecfdf5;
        border: 1px solid #a7f3d0;
        color: #065f46;
        padding: 10px;
        border-radius: 6px;
        font-size: 13px;
        font-weight: 700;
        line-height: 1.4;
    }}

    .promo-item {{
        font-size: 14px;
        color: #374151;
        display: flex;
        align-items: center;
        gap: 8px;
        line-height: 1.4;
    }}

    .cart-status-box {{
        background-color: #f0fdf4;
        border: 1px solid #bbf7d0;
        padding: 8px 12px;
        border-radius: 8px;
        margin-bottom: 10px;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }}

    .added-badge {{
        color: #047857;
        font-size: 13px;
        font-weight: 700;
    }}

    .view-cart-link {{
        color: #047857 !important;
        font-size: 14px !important;
        font-weight: 700 !important;
        text-decoration: underline !important;
    }}

    div[data-testid="stImage"] [data-testid="stElementActionButton"] {{
        opacity: 1 !important;
        visibility: visible !important;
    }}

    div[data-testid="stImage"] [data-testid="stElementActionButton"] button {{
        background-color: #ffffff !important;
        border: 1px solid {COLOR_MARCA} !important;
        border-radius: 20px !important;
        padding: 6px 14px !important;
        box-shadow: 0 4px 10px rgba(124, 58, 237, 0.25) !important;
        display: flex !important;
        align-items: center !important;
        gap: 6px !important;
        cursor: pointer !important;
        transition: transform 0.2s ease, box-shadow 0.2s ease !important;
    }}

    div[data-testid="stImage"] [data-testid="stElementActionButton"] button:hover {{
        transform: scale(1.05) !important;
        box-shadow: 0 6px 14px rgba(124, 58, 237, 0.35) !important;
    }}

    div[data-testid="stImage"] [data-testid="stElementActionButton"] svg {{
        width: 18px !important;
        height: 18px !important;
        color: {COLOR_MARCA} !important;
    }}

    div[data-testid="stImage"] [data-testid="stElementActionButton"] button::after {{
        content: "Ampliar foto" !important;
        font-size: 13px !important;
        font-weight: 700 !important;
        color: {COLOR_MARCA} !important;
        white-space: nowrap !important;
    }}
    </style>
""", unsafe_allow_html=True)

if "carrito" not in st.session_state:
    st.session_state.carrito = {}

if "categoria_activa" not in st.session_state:
    st.session_state.categoria_activa = "Todas"

st.markdown('<div class="top-bar"></div>', unsafe_allow_html=True)
st.markdown('<div id="top-inicio"></div>', unsafe_allow_html=True)

productos = cargar_productos_cliente(CLIENTE_SOLICITADO)

total_items = sum(item["cantidad"] for item in st.session_state.carrito.values())
total_general = sum(item["precio"] * item["cantidad"] for item in st.session_state.carrito.values())

total_ahorro = 0
for item in st.session_state.carrito.values():
    precio_ant = item.get("precioAnterior")
    precio_actual = item.get("precio")
    if precio_ant and precio_ant > precio_actual:
        total_ahorro += (precio_ant - precio_actual) * item["cantidad"]

col_logo, col_cart = st.columns([2.6, 1.4])
with col_logo:
    st.markdown(f'<div class="brand-logo">{LOGO_HTML}</div>', unsafe_allow_html=True)
with col_cart:
    st.markdown(f'<a href="#carrito-abajo" class="cart-link-badge">🛒 {total_items} items</a>', unsafe_allow_html=True)

st.markdown("")

st.markdown("""
<div class="benefits-bar">
    <div class="benefit-item">
        <span style="font-size: 20px;">🏪</span>
        <span>RETIRÁ GRATIS EN SUCURSAL</span>
    </div>
    <div class="benefit-item">
        <span style="font-size: 20px;">🎧</span>
        <span>VENTA POR WHATSAPP</span>
    </div>
    <div class="benefit-item">
        <span style="font-size: 20px;">📦</span>
        <span>ENVÍOS A TODO EL PAÍS</span>
    </div>
</div>
""", unsafe_allow_html=True)

if not productos:
    st.warning(f"No hay productos cargados o activos para el comercio: '{NOMBRE_MARCA}'.")
else:
    st.markdown("### Categorías")
    
    categorias_unicas = ["Todas"] + sorted(list(set(p.get("categoria", "General") for p in productos if p.get("categoria"))))
    
    cat_cols_top = st.columns(min(len(categorias_unicas), 6))
    for idx_cat, cat_nombre in enumerate(categorias_unicas):
        col_target = cat_cols_top[idx_cat % len(cat_cols_top)]
        with col_target:
            es_activa = (st.session_state.categoria_activa == cat_nombre)
            btn_label = f"• {cat_nombre} •" if es_activa else cat_nombre
            
            if st.button(btn_label, key=f"cat_top_{cat_nombre}", use_container_width=True):
                st.session_state.categoria_activa = cat_nombre
                st.session_state.input_busqueda = ""
                st.session_state.select_marca = "TODAS"
                st.rerun()

    st.markdown("---")

    st.markdown('<div id="catalogo-productos"></div>', unsafe_allow_html=True)

    col_busq, col_marca = st.columns([2, 1])
    with col_busq:
        busqueda = st.text_input("🔍 Buscar...", placeholder="Encontrá lo que querés", key="input_busqueda")
    with col_marca:
        marcas = ["TODAS"] + sorted(list(set(p.get("marca", "").strip() for p in productos if p.get("marca"))))
        marca_seleccionada = st.selectbox("Marca", marcas, key="select_marca")

    productos_filtrados = []
    query = busqueda.lower().strip()

    for p in productos:
        nombre_prod = p.get("producto", "").lower()
        prod_id = str(p.get("cod", ""))
        
        if prod_en_url:
            match = (prod_id.lower() == prod_en_url.lower())
        else:
            cat_prod = p.get("categoria", "General")
            cat_activa = st.session_state.categoria_activa
            
            match_categoria = (cat_activa == "Todas" or cat_prod.lower() == cat_activa.lower())
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
        st.info(f"✨ Viendo producto compartido. [Ver todo el catálogo]({URL_BASE_APP}/?cliente={CLIENTE_SOLICITADO})")

    if not productos_filtrados:
        if query or prod_en_url:
            st.warning("🔍 No encontramos el producto solicitado.")
            if prod_en_url:
                if st.button("Ver catálogo completo"):
                    st.query_params.clear()
                    st.query_params["cliente"] = CLIENTE_SOLICITADO
                    st.rerun()
        else:
            st.info(f"No se encontraron productos en la categoría '{st.session_state.categoria_activa}'.")
    else:
        info_texto = f"Mostrando {len(productos_filtrados)} artículos" if query or prod_en_url else f"Mostrando {len(productos_filtrados)} artículos (Categoría: **{st.session_state.categoria_activa}**)"
        st.write(info_texto)
        
        for i in range(0, len(productos_filtrados), 2):
            fila_productos = productos_filtrados[i:i+2]
            cols = st.columns(2)
            
            for idx, prod in enumerate(fila_productos):
                col = cols[idx]
                with col:
                    stock = prod.get("stock", 0)
                    prod_id = str(prod.get("cod", prod.get("producto")))
                    
                    en_carrito = prod_id in st.session_state.carrito
                    qty_en_carrito = st.session_state.carrito[prod_id]["cantidad"] if en_carrito else 0

                    precio_num = prod.get('precioVenta', 0)
                    precio_str = f"$ {precio_num:,.0f}".replace(",", ".")
                    
                    desc_transf_pct = prod.get("descTransferenciaPct")
                    cuotas_num = prod.get("cuotasSinInteres")
                    envio_txt = prod.get("envioTexto")
                    retiro_txt = prod.get("retiroTexto")
                    ficha_txt = prod.get("fichaTecnica")

                    promo_items = []
                    
                    if desc_transf_pct and desc_transf_pct > 0:
                        precio_transf = precio_num * (1 - (desc_transf_pct / 100))
                        precio_transf_str = f"$ {precio_transf:,.0f}".replace(",", ".")
                        promo_items.append(
                            f'<div class="promo-transfer">🏦 <strong>{int(desc_transf_pct)}% OFF</strong> pagando por Transferencia Bancaria<br><span style="font-size:14px;">Total con transferencia: <strong>{precio_transf_str}</strong></span></div>'
                        )
                    
                    if cuotas_num and cuotas_num > 0:
                        monto_cuota = precio_num / cuotas_num
                        monto_cuota_str = f"$ {monto_cuota:,.0f}".replace(",", ".")
                        promo_items.append(
                            f'<div class="promo-item">💳 <strong>{cuotas_num} cuotas sin interés</strong> de <strong>{monto_cuota_str}</strong></div>'
                        )

                    if envio_txt:
                        promo_items.append(f'<div class="promo-item">{envio_txt}</div>')

                    if retiro_txt:
                        promo_items.append(f'<div class="promo-item">{retiro_txt}</div>')

                    promo_box_html = f'<div class="promo-box">{"".join(promo_items)}</div>' if promo_items else ""
                    
                    precio_ant = prod.get("precioAnterior")
                    old_price_html = ""
                    discount_badge_html = ""
                    
                    if precio_ant and precio_ant > precio_num:
                        precio_ant_str = f"$ {precio_ant:,.0f}".replace(",", ".")
                        old_price_html = f'<span class="old-price">{precio_ant_str}</span>'
                        
                        pct_descuento = round(((precio_ant - precio_num) / precio_ant) * 100)
                        discount_badge_html = f'<span class="badge-discount">{pct_descuento}% OFF</span>'
                    
                    with st.container(border=True):
                        img_url = prod.get("imagenUrl", "")
                        if img_url:
                            st.image(img_url, use_column_width=True)
                        else:
                            st.markdown('<div style="height:160px; background:#f9fafb; display:flex; align-items:center; justify-content:center; color:#9ca3af; font-size:13px; border-radius:6px; margin-bottom:8px;">Sin imagen</div>', unsafe_allow_html=True)

                        st.markdown(f'<div class="product-brand">{prod.get("marca", "")}</div>', unsafe_allow_html=True)
                        st.markdown(f'<div class="product-title">{prod.get("producto", "")}</div>', unsafe_allow_html=True)
                        st.markdown(f'<div class="product-price">{old_price_html}<span>{precio_str}</span>{discount_badge_html}</div>', unsafe_allow_html=True)

                        if promo_box_html:
                            st.markdown(textwrap.dedent(promo_box_html).strip(), unsafe_allow_html=True)

                        if ficha_txt:
                            with st.expander("📋 Ver Ficha Técnica / Especificaciones"):
                                st.markdown(f"<div style='font-size:13px; color:#374151; line-height:1.5;'>{ficha_txt}</div>", unsafe_allow_html=True)

                        link_directo_producto = f"{URL_BASE_APP}/?cliente={CLIENTE_SOLICITADO}&prod={prod_id}"
                        wa_share_msg = f"¡Mirá este producto en {NOMBRE_MARCA}: {prod.get('producto')} ({prod.get('marca')}) a solo {precio_str}!\n👉 Ver producto: {link_directo_producto}"
                        wa_share_url = f"https://wa.me/?text={urllib.parse.quote(wa_share_msg)}"
                        st.markdown(f'<a href="{wa_share_url}" target="_blank" style="display:block; text-align:center; background-color:#25d366; color:white; padding:10px; border-radius:8px; text-decoration:none; font-size:13px; font-weight:bold; margin-bottom:10px; margin-top:8px; box-shadow:0 1px 2px rgba(0,0,0,0.05);">📲 Compartir por WhatsApp</a>', unsafe_allow_html=True)

                        if stock <= 0:
                            badge_html = '<span class="badge-out">Sin stock</span>'
                            st.markdown(f'<div style="margin-bottom:10px;">{badge_html}</div>', unsafe_allow_html=True)
                            
                            with st.expander("🔔 Avísame cuando ingrese"):
                                with st.form(key=f"form_stock_{idx}_{prod_id}"):
                                    st.markdown("<p style='font-size:13px; color:#4b5563; margin-bottom:4px;'>Dejanos tus datos para avisarte ni bien entre stock de este producto.</p>", unsafe_allow_html=True)
                                    nombre_lead = st.text_input("Tu Nombre", key=f"lead_nombre_{idx}_{prod_id}")
                                    tel_lead = st.text_input("Tu Teléfono / WhatsApp", key=f"lead_tel_{idx}_{prod_id}")
                                    
                                    enviar_lead = st.form_submit_button("📤 Registrarme", use_container_width=True)
                                    if enviar_lead:
                                        if nombre_lead.strip() and tel_lead.strip():
                                            try:
                                                supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
                                                supabase.table("stock_leads").insert({
                                                    "client_id": CLIENTE_SOLICITADO,
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
                            
                            st.markdown(f'<div style="margin-bottom:10px;">{badge_html}</div>', unsafe_allow_html=True)
                            
                            if st.button("🛒 Agregar al carrito", key=f"btn_add_{idx}_{prod_id}", use_container_width=True):
                                if prod_id in st.session_state.carrito:
                                    st.session_state.carrito[prod_id]["cantidad"] += 1
                                else:
                                    st.session_state.carrito[prod_id] = {
                                        "producto": prod.get("producto"),
                                        "marca": prod.get("marca"),
                                        "precio": precio_num,
                                        "precioAnterior": precio_ant,
                                        "descTransferenciaPct": desc_transf_pct,
                                        "cantidad": 1
                                    }
                                
                                st.toast(f"¡Agregado al carrito: {prod.get('producto')}!", icon="🛒")
                                st.rerun()

                            if en_carrito:
                                st.markdown(
                                    f'<div class="cart-status-box"><span class="added-badge">✓ Agregado ({qty_en_carrito})</span><a href="#carrito-abajo" class="view-cart-link">Ver mi carrito 🛒</a></div>',
                                    unsafe_allow_html=True
                                )

    # -------------------------------------------------------------
    # 2. SECCIÓN DEL CARRITO EN EL PIE DE PÁGINA
    # -------------------------------------------------------------
    st.markdown('<div id="carrito-abajo"></div>', unsafe_allow_html=True)
    st.markdown("---")
    st.markdown("### Mi Carrito")

    if total_items == 0:
        st.info("Tu carrito está vacío. ¡Agregá productos desde el catálogo para armar tu pedido!")
    else:
        total_str = f"$ {total_general:,.0f}".replace(",", ".")
        
        banner_total_html = f'<div style="background-color: #047857; color: white; padding: 12px 16px; border-radius: 10px; display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px; box-shadow: 0 4px 6px rgba(0,0,0,0.1);"><span style="font-weight: bold; font-size: 16px;">🛒 Total de Artículos: {total_items}</span><span style="font-weight: bold; font-size: 16px;">Total: {total_str}</span></div>'
        st.markdown(banner_total_html, unsafe_allow_html=True)

        if total_ahorro > 0:
            ahorro_str = f"$ {total_ahorro:,.0f}".replace(",", ".")
            banner_ahorro_html = f'<div style="background-color: #fef3c7; border: 1px solid #f59e0b; color: #b45309; padding: 10px 14px; border-radius: 8px; font-weight: bold; font-size: 15px; text-align: center; margin-bottom: 12px; box-shadow: 0 2px 4px rgba(0,0,0,0.04);">🔥 ¡Estás ahorrando {ahorro_str} en esta compra por precios en oferta!</div>'
            st.markdown(banner_ahorro_html, unsafe_allow_html=True)

        with st.expander("📦 Ver detalle completo del pedido y enviar a WhatsApp", expanded=True):
            mensaje_wa = f"Hola *{NOMBRE_MARCA}*, quiero realizar el siguiente pedido desde el catálogo:\n\n"
            
            for prod_id, item in list(st.session_state.carrito.items()):
                subtotal = item["precio"] * item["cantidad"]
                subtotal_str = f"$ {subtotal:,.0f}".replace(",", ".")
                
                c_info, c_qty, c_del = st.columns([2.5, 2, 1])
                with c_info:
                    item_html = f"**{item['producto']}**<br><span style='font-size:13px; color:{COLOR_MARCA}; font-weight:600;'>{item['marca']}</span><br><span style='font-size:14px; font-weight:700;'>Subtotal: {subtotal_str}</span>"
                    st.markdown(item_html, unsafe_allow_html=True)
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
                
                mensaje_wa += f"• {item['cantidad']}x {item['producto']} ({item['marca']}) - Subtotal: {subtotal_str}\n"
                st.markdown("<hr style='margin: 8px 0; border-color: #e5e7eb;'>", unsafe_allow_html=True)

            st.markdown(f"### Total de mi pedido: {total_str}")
            
            if total_ahorro > 0:
                ahorro_str = f"$ {total_ahorro:,.0f}".replace(",", ".")
                st.markdown(f"<p style='color:#059669; font-weight:bold; font-size:15px; margin-top:-10px;'>🎉 Ahorro total acumulado en ofertas: {ahorro_str}</p>", unsafe_allow_html=True)
                mensaje_wa += f"\n🎉 ¡Ahorro total en ofertas: {ahorro_str}!"

            mensaje_wa += f"\n\nTotal estimado mi pedido: {total_str}"
            mensaje_wa += f"\n* Pedido sujeto a confirmación de stock por parte del comercio."
            
            wa_url = f"https://wa.me/{WHATSAPP_NUMERO}?text={urllib.parse.quote(mensaje_wa)}"
            
            st.markdown(f'<a href="{wa_url}" target="_blank" style="display:block; text-align:center; background-color:#059669; color:white; padding:14px; border-radius:8px; text-decoration:none; font-size:16px; font-weight:bold; box-shadow: 0 4px 6px rgba(0,0,0,0.15); margin-bottom: 10px;">📤 Pagar mi carrito por WhatsApp</a>', unsafe_allow_html=True)
            
            if st.button("🗑️ Vaciar carrito completo", use_container_width=True):
                st.session_state.carrito = {}
                st.rerun()

    # -------------------------------------------------------------
    # 3. SECCIÓN DE CATEGORÍAS EN PIE DE PÁGINA
    # -------------------------------------------------------------
    st.markdown("---")
    st.markdown("### Categorías (Explorar más)")
    
    cat_cols_bottom = st.columns(min(len(categorias_unicas), 6))
    for idx_cat, cat_nombre in enumerate(categorias_unicas):
        col_target = cat_cols_bottom[idx_cat % len(cat_cols_bottom)]
        with col_target:
            if st.button(cat_nombre, key=f"cat_bot_{cat_nombre}", use_container_width=True):
                st.session_state.categoria_activa = cat_nombre
                st.session_state.input_busqueda = ""
                st.session_state.select_marca = "TODAS"
                st.rerun()

    st.markdown(
        """
        <div style="text-align: center; margin-top: 25px; margin-bottom: 20px;">
            <a href="#top-inicio" style="display: inline-block; background-color: #ffffff; color: #374151; padding: 10px 24px; border-radius: 8px; text-decoration: none; font-size: 14px; font-weight: bold; border: 1px solid #d1d5db; box-shadow: 0 2px 4px rgba(0,0,0,0.05);">
                ⬆️ Volver arriba
            </a>
        </div>
        """,
        unsafe_allow_html=True
    )
