import streamlit as st

st.set_page_config(page_title="Simulador de Bonos CHUBB 2025", layout="centered")

# Logo e imagen
from PIL import Image
logo = Image.open("link logo.jpg")

# Estilo para ajustar altura del logo con el título
st.markdown("""
    <style>
        .titulo-logo {
            display: flex;
            justify-content: space-between;
            align-items: flex-start;
        }
        .titulo-logo h1, .titulo-logo h2 {
            margin: 0;
            padding: 0;
        }
    </style>
""", unsafe_allow_html=True)

# Mostrar encabezado con logo al lado
st.markdown('<div class="titulo-logo">', unsafe_allow_html=True)
col1, col2 = st.columns([5, 1])
with col1:
    st.markdown("## Simulador de Bonos")
    st.markdown("### CHUBB 2025")
with col2:
    st.image(logo, width=100)
st.markdown('</div>', unsafe_allow_html=True)

# Campo para nombre antes del ramo
nombre = st.text_input("Nombre del Agente")
tipo_ramo = st.selectbox("Selecciona el ramo a simular", ["Autos", "Daños PYME", "Vida", "Hogar", "Accidentes y Enfermedades", "Otros Daños"])

resultado = ""

# === BLOQUE DE AUTOS ===

if tipo_ramo == "Autos":
    st.markdown("#### Datos para Autos")
    prod_2024 = st.text_input("Producción 2024 ($)", placeholder="Ej. $1,000,000")
    prod_2025 = st.text_input("Producción 2025 ($)", placeholder="Ej. $2,000,000")
    siniestralidad = st.text_input("Siniestralidad (%)", placeholder="Ej. 45")
    unidades = st.text_input("Número de Unidades Emitidas", placeholder="Ej. 150")

    if st.button("Calcular Bonos Autos"):
        try:
            p2024 = int(prod_2024.replace("$", "").replace(",", ""))
            p2025 = int(prod_2025.replace("$", "").replace(",", ""))
            sin = float(siniestralidad)
            uds = int(unidades)

            resultado = f"<h3>📋 Resultado para {nombre.upper()}</h3>"
            resultado += "<h4>📊 Datos Ingresados:</h4><ul>"
            resultado += f"<li>Producción 2024: <strong>${p2024:,.2f}</strong></li>"
            resultado += f"<li>Producción 2025: <strong>${p2025:,.2f}</strong></li>"
            resultado += f"<li>Siniestralidad: <strong>{sin:.2f}%</strong></li>"
            resultado += f"<li>Unidades Emitidas: <strong>{uds}</strong></li></ul>"
            resultado += "<h4>💵 Resultados de Bono:</h4><ul>"

            # Bono de Producción (requiere mínimo $250,000)
            bono_prod = 0
            if p2025 < 250000:
                resultado += "<li>📈 <strong>Bono de Producción:</strong> $0.00 ❌ No aplica por no alcanzar los $250,000 requeridos.</li>"
            else:
                if sin < 60:
                    if p2025 <= 350000:
                        pct_prod = 0.01
                    elif p2025 <= 500000:
                        pct_prod = 0.02
                    elif p2025 <= 1000000:
                        pct_prod = 0.03
                    elif p2025 <= 2000000:
                        pct_prod = 0.04
                    else:
                        pct_prod = 0.05
                else:
                    if p2025 <= 500000:
                        pct_prod = 0.01
                    elif p2025 <= 1000000:
                        pct_prod = 0.01
                    elif p2025 <= 2000000:
                        pct_prod = 0.02
                    else:
                        pct_prod = 0.03
                bono_prod = p2025 * pct_prod
                resultado += f"<li>📈 <strong>Bono de Producción:</strong> {pct_prod*100:.2f}% ➜ <strong>${bono_prod:,.2f}</strong><br>✅ Aplica según tabla con siniestralidad del {sin:.2f}%.</li>"

            # Bono de Siniestralidad
            if sin <= 30:
                pct_sini = 0.04
            elif sin <= 45:
                pct_sini = 0.03
            elif sin <= 50:
                pct_sini = 0.02
            elif sin <= 55:
                pct_sini = 0.01
            else:
                pct_sini = 0
            bono_sini = p2025 * pct_sini
            if pct_sini > 0:
                resultado += f"<li>🛡️ <strong>Bono de Siniestralidad:</strong> {pct_sini*100:.2f}% ➜ <strong>${bono_sini:,.2f}</strong><br>✅ Aplica por siniestralidad del {sin:.2f}%.</li>"
            else:
                resultado += f"<li>🛡️ <strong>Bono de Siniestralidad:</strong> $0.00 ❌ No aplica. Siniestralidad de {sin:.2f}% supera el límite.</li>"

            # Bono de Crecimiento
            if p2024 == 0:
                bono_crec = p2025 * 0.04
                resultado += f"<li>🚀 <strong>Bono de Crecimiento:</strong> 4.00% ➜ <strong>${bono_crec:,.2f}</strong><br>✅ Aplica por agente nuevo (sin producción en 2024).</li>"
            else:
                crecimiento = p2025 - p2024
                pct_crec = (crecimiento / p2024) * 100

                def calcular_bono_crecimiento(pct_crec, unidades):
                    if pct_crec < 10:
                        return 0
                    elif pct_crec <= 20:
                        return 0.025 if unidades <= 50 else 0.035 if unidades <= 150 else 0.04
                    elif pct_crec <= 30:
                        return 0.04 if unidades <= 50 else 0.055 if unidades <= 150 else 0.07
                    elif pct_crec <= 40:
                        return 0.06 if unidades <= 50 else 0.07 if unidades <= 150 else 0.09
                    elif pct_crec <= 50:
                        return 0.09 if unidades <= 50 else 0.12 if unidades <= 150 else 0.15
                    else:
                        return 0.12 if unidades <= 50 else 0.15 if unidades <= 150 else 0.17

                pct_crec_aplica = calcular_bono_crecimiento(pct_crec, uds)
                bono_crec = crecimiento * pct_crec_aplica
                if pct_crec_aplica > 0:
                    resultado += f"<li>🚀 <strong>Bono de Crecimiento:</strong> {pct_crec_aplica*100:.2f}% ➜ <strong>${bono_crec:,.2f}</strong><br>✅ Crecimiento del {pct_crec:.2f}% con {uds} unidades emitidas.</li>"
                else:
                    resultado += f"<li>🚀 <strong>Bono de Crecimiento:</strong> $0.00 ❌ No aplica por crecimiento insuficiente ({pct_crec:.2f}%).</li>"

            # Total
            total = bono_prod + bono_sini + bono_crec
            resultado += f"</ul><h4>🧾 <strong>Total del Bono Autos:</strong> ${total:,.2f}</h4>"

        except Exception as e:
            resultado = f"<p style='color:red;'>❌ Error: {e}</p>"

        # Mostrar resultados
        st.markdown("---")
        st.markdown(resultado, unsafe_allow_html=True)
        st.markdown("<p style='text-align: center; font-size:14px;'>Aplican restricciones y condiciones conforme al cuaderno oficial de CHUBB Seguros 2025.</p>", unsafe_allow_html=True)

# === BLOQUE DE DAÑOS PYME ===

elif tipo_ramo == "Daños PYME":
    st.markdown("#### Datos para Daños PYME")
    prod_danios = st.text_input("Producción 2025 Daños ($)", placeholder="Ej. $500,000")
    siniestralidad_d = st.text_input("Siniestralidad (%)", placeholder="Ej. 35")

    if st.button("Calcular Bonos Daños"):
        try:
            p = int(prod_danios.replace("$", "").replace(",", ""))
            sin_d = float(siniestralidad_d)

            resultado = f"<h3>📋 Resultado para {nombre.upper()}</h3>"
            resultado += "<h4>📊 Datos Ingresados:</h4><ul>"
            resultado += f"<li>Producción Daños: <strong>${p:,.2f}</strong></li>"
            resultado += f"<li>Siniestralidad: <strong>{sin_d:.2f}%</strong></li></ul>"
            resultado += "<h4>💵 Resultados de Bono:</h4><ul>"

            # Bono de Producción Daños PYME
            bono_prod = 0
            if p < 350000:
                resultado += "<li>🏢 <strong>Bono de Producción Daños:</strong> $0.00 ❌ No aplica por no alcanzar los $350,000 requeridos.</li>"
            else:
                if sin_d < 60:
                    if p <= 500000:
                        pct_prod = 0.02
                    else:
                        pct_prod = 0.03
                else:
                    pct_prod = 0.01  # Penalización por siniestralidad alta
                bono_prod = p * pct_prod
                resultado += f"<li>🏢 <strong>Bono de Producción Daños:</strong> {pct_prod*100:.2f}% ➜ <strong>${bono_prod:,.2f}</strong><br>✅ Aplica según tabla.</li>"

            # Bono de Siniestralidad Daños PYME
            if sin_d <= 30:
                pct_sini = 0.03
            elif sin_d <= 45:
                pct_sini = 0.02
            elif sin_d <= 55:
                pct_sini = 0.01
            else:
                pct_sini = 0
            bono_sini = p * pct_sini
            if pct_sini > 0:
                resultado += f"<li>🛡️ <strong>Bono de Siniestralidad Daños:</strong> {pct_sini*100:.2f}% ➜ <strong>${bono_sini:,.2f}</strong><br>✅ Aplica por siniestralidad del {sin_d:.2f}%.</li>"
            else:
                resultado += f"<li>🛡️ <strong>Bono de Siniestralidad Daños:</strong> $0.00 ❌ No aplica por siniestralidad superior al 55%.</li>"

            # Total
            total = bono_prod + bono_sini
            resultado += f"</ul><h4>🧾 <strong>Total del Bono Daños PYME:</strong> ${total:,.2f}</h4>"

        except Exception as e:
            resultado = f"<p style='color:red;'>❌ Error: {e}</p>"

        # Mostrar resultados
        st.markdown("---")
        st.markdown(resultado, unsafe_allow_html=True)
        st.markdown("<p style='text-align: center; font-size:14px;'>Aplican restricciones y condiciones conforme al cuaderno oficial de CHUBB Seguros 2025.</p>", unsafe_allow_html=True)

# === BLOQUE DE VIDA ===

elif tipo_ramo == "Vida":
    st.markdown("#### Datos para Vida")
    prod_2024 = st.text_input("Producción 2024 Vida ($)", placeholder="Ej. $500,000")
    prod_2025 = st.text_input("Producción 2025 Vida ($)", placeholder="Ej. $1,200,000")
    siniestralidad = st.text_input("Siniestralidad (%)", placeholder="Ej. 28")

    if st.button("Calcular Bonos Vida"):
        try:
            p2024 = int(prod_2024.replace("$", "").replace(",", "")) if prod_2024 else 0
            p2025 = int(prod_2025.replace("$", "").replace(",", "")) if prod_2025 else 0
            sin = float(siniestralidad)

            resultado = f"<h3>📋 Resultado para {nombre.upper()}</h3>"
            resultado += "<h4>📊 Datos Ingresados:</h4><ul>"
            resultado += f"<li>Producción 2024: <strong>${p2024:,.2f}</strong></li>"
            resultado += f"<li>Producción 2025: <strong>${p2025:,.2f}</strong></li>"
            resultado += f"<li>Siniestralidad: <strong>{sin:.2f}%</strong></li></ul>"
            resultado += "<h4>💵 Resultados de Bono:</h4><ul>"

            # === BONO DE PRODUCCIÓN VIDA ===
            bono_prod = 0
            if sin <= 60:
                if p2025 < 200000:
                    resultado += "<li>🧬 <strong>Bono de Producción Vida:</strong> ❌ No aplica por no alcanzar $200,000.</li>"
                elif p2025 <= 299999:
                    pct_prod = 0.01
                elif p2025 <= 649999:
                    pct_prod = 0.02
                elif p2025 <= 899999:
                    pct_prod = 0.04
                elif p2025 <= 1499999:
                    pct_prod = 0.06
                else:
                    pct_prod = 0.08

                if p2025 >= 200000:
                    bono_prod = p2025 * pct_prod
                    resultado += f"<li>🧬 <strong>Bono de Producción Vida:</strong> {pct_prod*100:.2f}% ➜ <strong>${bono_prod:,.2f}</strong></li>"
            else:
                resultado += "<li>🧬 <strong>Bono de Producción Vida:</strong> ❌ No aplica por siniestralidad mayor a 60%.</li>"

            # === BONO DE CRECIMIENTO VIDA ===
            bono_crec = 0
            if p2024 > 0:
                crecimiento = p2025 - p2024
                pct_crec = (crecimiento / p2024) * 100
                if pct_crec < 5:
                    pct_crec_aplica = 0
                elif pct_crec <= 14.99:
                    pct_crec_aplica = 0.04
                elif pct_crec <= 29.99:
                    pct_crec_aplica = 0.05
                elif pct_crec <= 49.99:
                    pct_crec_aplica = 0.06
                else:
                    pct_crec_aplica = 0.08

                bono_crec = crecimiento * pct_crec_aplica if pct_crec_aplica > 0 else 0
                if pct_crec_aplica > 0:
                    resultado += f"<li>📈 <strong>Bono de Crecimiento Vida:</strong> {pct_crec_aplica*100:.2f}% ➜ <strong>${bono_crec:,.2f}</strong> (Crecimiento del {pct_crec:.2f}%)</li>"
                else:
                    resultado += f"<li>📈 <strong>Bono de Crecimiento Vida:</strong> ❌ No aplica (Crecimiento del {pct_crec:.2f}%). Mínimo requerido: 5%</li>"
            else:
                resultado += "<li>📈 <strong>Bono de Crecimiento Vida:</strong> ❌ No aplica por no tener producción en 2024.</li>"

            # === BONO DE SINIESTRALIDAD VIDA ===
            if sin <= 22.99:
                pct_sini = 0.04
            elif sin <= 34.99:
                pct_sini = 0.02
            else:
                pct_sini = 0

            bono_sini = p2025 * pct_sini
            if pct_sini > 0:
                resultado += f"<li>🩺 <strong>Bono de Siniestralidad Vida:</strong> {pct_sini*100:.2f}% ➜ <strong>${bono_sini:,.2f}</strong></li>"
            else:
                resultado += "<li>🩺 <strong>Bono de Siniestralidad Vida:</strong> ❌ No aplica por siniestralidad mayor al 34.99%.</li>"

            # === TOTAL
            total = bono_prod + bono_crec + bono_sini
            resultado += f"</ul><h4>🧾 <strong>Total del Bono Vida:</strong> ${total:,.2f}</strong></h4>"

        except Exception as e:
            resultado = f"<p style='color:red;'>❌ Error: {e}</p>"

        # Mostrar resultado
        st.markdown("---")
        st.markdown(resultado, unsafe_allow_html=True)
        st.markdown("<p style='text-align: center; font-size:14px;'>Aplican restricciones y condiciones conforme al cuaderno oficial de CHUBB Seguros 2025.</p>", unsafe_allow_html=True)

# === BLOQUE DE HOGAR ===

elif tipo_ramo == "Hogar":
    st.markdown("### Datos para Hogar")
    prod_2024 = st.text_input("Producción 2024 Hogar ($)", placeholder="Ej. $100,000")
    prod_2025 = st.text_input("Producción 2025 Hogar ($)", placeholder="Ej. $150,000")
    siniestralidad = st.text_input("Siniestralidad (%)", placeholder="Ej. 25")

    if st.button("Calcular Bonos Hogar"):
        try:
            p2024 = int(prod_2024.replace("$", "").replace(",", "")) if prod_2024 else 0
            p2025 = int(prod_2025.replace("$", "").replace(",", "")) if prod_2025 else 0
            sin = float(siniestralidad)

            resultado = f"<h3>📋 Resultado para {nombre.upper()}</h3>"
            resultado += "<h4>📊 Datos Ingresados:</h4><ul>"
            resultado += f"<li>Producción 2024: <strong>${p2024:,.2f}</strong></li>"
            resultado += f"<li>Producción 2025: <strong>${p2025:,.2f}</strong></li>"
            resultado += f"<li>Siniestralidad: <strong>{sin:.2f}%</strong></li></ul>"
            resultado += "<h4>💵 Resultados de Bono:</h4><ul>"

            # === BONO DE PRODUCCIÓN HOGAR ===
            if p2025 < 25000:
                pct_prod = 0
                resultado += "<li>🏠 <strong>Bono de Producción Hogar:</strong> ❌ No aplica por no alcanzar $25,000.</li>"
            elif p2025 <= 50000:
                pct_prod = 0.02
            elif p2025 <= 150000:
                pct_prod = 0.03
            elif p2025 <= 350000:
                pct_prod = 0.04
            else:
                pct_prod = 0.07

            bono_prod = p2025 * pct_prod
            if pct_prod > 0:
                resultado += f"<li>🏠 <strong>Bono de Producción Hogar:</strong> {pct_prod*100:.2f}% ➜ <strong>${bono_prod:,.2f}</strong></li>"

            # === BONO DE SINIESTRALIDAD HOGAR ===
            if sin <= 15:
                pct_sini = 0.04
            elif sin <= 25:
                pct_sini = 0.03
            elif sin <= 35:
                pct_sini = 0.02
            elif sin <= 40:
                pct_sini = 0.01
            else:
                pct_sini = 0

            bono_sini = p2025 * pct_sini
            if pct_sini > 0:
                resultado += f"<li>🧯 <strong>Bono de Siniestralidad Hogar:</strong> {pct_sini*100:.2f}% ➜ <strong>${bono_sini:,.2f}</strong></li>"
            else:
                resultado += "<li>🧯 <strong>Bono de Siniestralidad Hogar:</strong> ❌ No aplica por superar el 40%.</li>"

            # === BONO DE CRECIMIENTO HOGAR ===
            if p2024 < 50000:
                bono_crec = 0
                resultado += "<li>📈 <strong>Bono de Crecimiento Hogar:</strong> ❌ No aplica por no alcanzar $50,000 en 2024.</li>"
            else:
                crecimiento = p2025 - p2024
                pct_crec = (crecimiento / p2024) * 100

                if pct_crec < 15:
                    pct_crec_v = 0
                    resultado += f"<li>📈 <strong>Bono de Crecimiento Hogar:</strong> ❌ No aplica (Crecimiento de {pct_crec:.2f}%). Mínimo requerido: 15%</li>"
                elif pct_crec <= 20:
                    pct_crec_v = 0.03
                elif pct_crec <= 30:
                    pct_crec_v = 0.05
                else:
                    pct_crec_v = 0.07

                bono_crec = crecimiento * pct_crec_v if pct_crec_v > 0 else 0
                if pct_crec_v > 0:
                    resultado += f"<li>📈 <strong>Bono de Crecimiento Hogar:</strong> {pct_crec_v*100:.2f}% ➜ <strong>${bono_crec:,.2f}</strong> (Crecimiento del {pct_crec:.2f}%)</li>"

            # === TOTAL
            total = bono_prod + bono_sini + bono_crec
            resultado += f"</ul><h4>🧾 <strong>Total del Bono Hogar:</strong> ${total:,.2f}</strong></h4>"

        except Exception as e:
            resultado = f"<p style='color:red;'>❌ Error: {e}</p>"

        # Mostrar resultado
        st.markdown("---")
        st.markdown(resultado, unsafe_allow_html=True)
        st.markdown("<p style='text-align: center; font-size:14px;'>Aplican restricciones y condiciones conforme al cuaderno oficial de CHUBB Seguros 2025.</p>", unsafe_allow_html=True)

# === BLOQUE DE ACCIDENTES Y ENFERMEDADES (A&H) ===

elif tipo_ramo == "Accidentes y Enfermedades":
    st.markdown("### Datos para Accidentes y Enfermedades (A&H)")
    prod_2024 = st.text_input("Producción 2024 A&H ($)", placeholder="Ej. $300,000")
    prod_2025 = st.text_input("Producción 2025 A&H ($)", placeholder="Ej. $500,000")
    siniestralidad = st.text_input("Siniestralidad (%)", placeholder="Ej. 20")

    if st.button("Calcular Bonos A&H"):
        try:
            p2024 = int(prod_2024.replace("$", "").replace(",", "")) if prod_2024 else 0
            p2025 = int(prod_2025.replace("$", "").replace(",", "")) if prod_2025 else 0
            sin = float(siniestralidad)

            resultado = f"<h3>📋 Resultado para {nombre.upper()}</h3>"
            resultado += "<h4>📊 Datos Ingresados:</h4><ul>"
            resultado += f"<li>Producción 2024: <strong>${p2024:,.2f}</strong></li>"
            resultado += f"<li>Producción 2025: <strong>${p2025:,.2f}</strong></li>"
            resultado += f"<li>Siniestralidad: <strong>{sin:.2f}%</strong></li></ul>"
            resultado += "<h4>💵 Resultados de Bono:</h4><ul>"

            # === BONO DE PRODUCCIÓN A&H ===
            if sin > 60:
                pct_prod = 0
                resultado += "<li>🏥 <strong>Bono de Producción A&H:</strong> ❌ No aplica por superar el 60% de siniestralidad.</li>"
            else:
                if p2025 < 300000:
                    pct_prod = 0
                    resultado += "<li>🏥 <strong>Bono de Producción A&H:</strong> ❌ No aplica por no alcanzar los $300,000 requeridos.</li>"
                elif p2025 <= 399999:
                    pct_prod = 0.01
                elif p2025 <= 649999:
                    pct_prod = 0.045
                elif p2025 <= 999999:
                    pct_prod = 0.055
                else:
                    pct_prod = 0.07

            bono_prod = p2025 * pct_prod if pct_prod > 0 else 0
            if pct_prod > 0:
                resultado += f"<li>🏥 <strong>Bono de Producción A&H:</strong> {pct_prod*100:.2f}% ➜ <strong>${bono_prod:,.2f}</strong></li>"

            # === BONO DE SINIESTRALIDAD A&H ===
            if sin <= 24.99:
                pct_sini = 0.045
            elif sin <= 37.99:
                pct_sini = 0.025
            elif sin <= 45.99:
                pct_sini = 0.01
            else:
                pct_sini = 0

            bono_sini = p2025 * pct_sini
            if pct_sini > 0:
                resultado += f"<li>🧯 <strong>Bono de Siniestralidad A&H:</strong> {pct_sini*100:.2f}% ➜ <strong>${bono_sini:,.2f}</strong></li>"
            else:
                resultado += "<li>🧯 <strong>Bono de Siniestralidad A&H:</strong> ❌ No aplica por superar el 46%.</li>"

            # === BONO DE CRECIMIENTO A&H ===
            if p2024 <= 0:
                bono_crec = 0
                resultado += "<li>📈 <strong>Bono de Crecimiento A&H:</strong> ❌ No aplica por no tener producción en 2024.</li>"
            else:
                crecimiento = p2025 - p2024
                pct_crec = (crecimiento / p2024) * 100

                if pct_crec < 5:
                    pct_crec_v = 0
                    resultado += f"<li>📈 <strong>Bono de Crecimiento A&H:</strong> ❌ No aplica (Crecimiento de {pct_crec:.2f}%). Mínimo requerido: 5%</li>"
                elif pct_crec <= 14.99:
                    pct_crec_v = 0.04
                elif pct_crec <= 29.99:
                    pct_crec_v = 0.05
                elif pct_crec <= 49.99:
                    pct_crec_v = 0.06
                else:
                    pct_crec_v = 0.08

                bono_crec = crecimiento * pct_crec_v if pct_crec_v > 0 else 0
                if pct_crec_v > 0:
                    resultado += f"<li>📈 <strong>Bono de Crecimiento A&H:</strong> {pct_crec_v*100:.2f}% ➜ <strong>${bono_crec:,.2f}</strong> (Crecimiento del {pct_crec:.2f}%)</li>"

            # === TOTAL
            total = bono_prod + bono_sini + bono_crec
            resultado += f"</ul><h4>🧾 <strong>Total del Bono A&H:</strong> ${total:,.2f}</h4>"

        except Exception as e:
            resultado = f"<p style='color:red;'>❌ Error: {e}</p>"

        # Mostrar resultado
        st.markdown("---")
        st.markdown(resultado, unsafe_allow_html=True)
        st.markdown("<p style='text-align: center; font-size:14px;'>Aplican restricciones y condiciones conforme al cuaderno oficial de CHUBB Seguros 2025.</p>", unsafe_allow_html=True)

# === BLOQUE DE OTROS DAÑOS (MM & MAD) ===

elif tipo_ramo == "Otros Daños":
    st.markdown("### Datos para Otros Daños (MM & MAD)")
    prod_otros = st.text_input("Producción 2025 Otros Daños ($)", placeholder="Ej. $300,000")

    if st.button("Calcular Bonos Otros Daños"):
        try:
            p = int(prod_otros.replace("$", "").replace(",", ""))

            resultado = f"<h3>📋 Resultado para {nombre.upper()}</h3>"
            resultado += "<h4>📊 Datos Ingresados:</h4><ul>"
            resultado += f"<li>Producción Otros Daños: <strong>${p:,.2f}</strong></li></ul>"
            resultado += "<h4>💵 Resultados de Bono:</h4><ul>"

            # === BONO PRODUCCIÓN OTROS DAÑOS ===
            if p >= 250000:
                pct = 0.015
                bono = p * pct
                resultado += f"<li>🏗️ <strong>Bono de Producción Otros Daños:</strong> {pct*100:.2f}% ➜ <strong>${bono:,.2f}</strong><br>✅ Aplica por superar $250,000.</li>"
            else:
                bono = 0
                resultado += "<li>🏗️ <strong>Bono de Producción Otros Daños:</strong> ❌ No aplica por no alcanzar los $250,000 requeridos.</li>"

            resultado += f"</ul><h4>🧾 <strong>Total del Bono Otros Daños:</strong> ${bono:,.2f}</h4>"

        except Exception as e:
            resultado = f"<p style='color:red;'>❌ Error: {e}</p>"

        # Mostrar resultado
        st.markdown("---")
        st.markdown(resultado, unsafe_allow_html=True)
        st.markdown("<p style='text-align: center; font-size:14px;'>Aplican restricciones y condiciones conforme al cuaderno oficial de CHUBB Seguros 2025.</p>", unsafe_allow_html=True)
