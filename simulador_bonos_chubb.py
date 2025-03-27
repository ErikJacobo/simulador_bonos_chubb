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

            resultado += f"<h3>📋 Resultado para {nombre.upper()}</h3>"
            resultado += "<h4>📊 Datos Ingresados:</h4><ul>"
            resultado += f"<li>Producción 2024: <strong>${p2024:,.2f}</strong></li>"
            resultado += f"<li>Producción 2025: <strong>${p2025:,.2f}</strong></li>"
            resultado += f"<li>Siniestralidad: <strong>{sin:.2f}%</strong></li>"
            resultado += f"<li>Unidades Emitidas: <strong>{uds}</strong></li></ul>"
            resultado += "<h4>💵 Resultados de Bono:</h4><ul>"

            # BONO PRODUCCIÓN
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

            # BONO SINIESTRALIDAD
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

            # BONO CRECIMIENTO
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

            total = bono_prod + bono_sini + bono_crec
            resultado += f"</ul><h4>🧾 <strong>Total del Bono Autos:</strong> ${total:,.2f}</h4>"

        except Exception as e:
            resultado = f"<p style='color:red;'>❌ Error: {e}</p>"

        st.markdown("<p style='text-align: center; font-size:14px;'>Aplican restricciones y condiciones conforme al cuaderno oficial de CHUBB Seguros 2025.</p>", unsafe_allow_html=True)

# Mostrar resultados
if resultado:
    st.markdown("---")
    st.markdown(resultado, unsafe_allow_html=True)


elif tipo_ramo == "Daños PYME":
    st.markdown("#### Datos para Daños PYME")
    prod_danios = st.text_input("Producción 2025 Daños ($)", placeholder="Ej. $500,000")
    siniestralidad_d = st.text_input("Siniestralidad (%)", placeholder="Ej. 35")

    if st.button("Calcular Bonos Daños"):
        try:
            p = int(prod_danios.replace("$", "").replace(",", ""))
            sin_d = float(siniestralidad_d)

            resultado += f"<h3>📋 Resultado para {nombre.upper()}</h3>"
            resultado += "<h4>📊 Datos Ingresados:</h4><ul>"
            resultado += f"<li>Producción Daños: <strong>${p:,.2f}</strong></li>"
            resultado += f"<li>Siniestralidad: <strong>{sin_d:.2f}%</strong></li></ul>"
            resultado += "<h4>💵 Resultados de Bono:</h4><ul>"

            # Bono Producción
            if sin_d < 60:
                if p <= 350000:
                    pct_prod = 0.01
                elif p <= 500000:
                    pct_prod = 0.02
                else:
                    pct_prod = 0.03
                bono_prod = p * pct_prod
                resultado += f"<li>📈 <strong>Bono de Producción:</strong> {pct_prod*100:.2f}% ➜ <strong>${bono_prod:,.2f}</strong><br>✅ Aplica por siniestralidad menor al 60%.</li>"
            else:
                bono_prod = p * 0.01
                resultado += f"<li>📈 <strong>Bono de Producción:</strong> 1.00% ➜ <strong>${bono_prod:,.2f}</strong><br>⚠️ Aplica con porcentaje reducido por siniestralidad mayor al 60%.</li>"

            # Bono Siniestralidad
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
                resultado += f"<li>🛡️ <strong>Bono de Siniestralidad:</strong> {pct_sini*100:.2f}% ➜ <strong>${bono_sini:,.2f}</strong><br>✅ Aplica por siniestralidad del {sin_d:.2f}%.</li>"
            else:
                resultado += f"<li>🛡️ <strong>Bono de Siniestralidad:</strong> $0.00 ❌ No aplica por siniestralidad mayor al 55%.</li>"

            total = bono_prod + bono_sini
            resultado += f"</ul><h4>🧾 <strong>Total del Bono Daños PYME:</strong> ${total:,.2f}</h4>"

        except Exception as e:
            resultado = f"<p style='color:red;'>❌ Error: {e}</p>"

        st.markdown("<p style='text-align: center; font-size:14px;'>Aplican restricciones y condiciones conforme al cuaderno oficial de CHUBB Seguros 2025.</p>", unsafe_allow_html=True)


elif tipo_ramo == "Vida":
    st.markdown("#### Datos para Vida Grupo")
    suma_asegurada = st.text_input("Suma Asegurada 2025 ($)", placeholder="Ej. $1,000,000")

    if st.button("Calcular Bonos Vida"):
        try:
            sa = int(suma_asegurada.replace("$", "").replace(",", ""))
            resultado += f"<h3>📋 Resultado para {nombre.upper()}</h3>"
            resultado += "<h4>📊 Datos Ingresados:</h4><ul>"
            resultado += f"<li>Suma Asegurada 2025: <strong>${sa:,.2f}</strong></li></ul>"
            resultado += "<h4>💵 Resultados de Bono:</h4><ul>"

            if sa < 250000:
                bono_vida = 0
                resultado += "<li>💔 <strong>Bono de Vida:</strong> $0.00 ❌ No aplica. Mínimo requerido: $250,000 de suma asegurada.</li>"
            else:
                if sa <= 500000:
                    pct_vida = 0.01
                elif sa <= 1000000:
                    pct_vida = 0.02
                elif sa <= 2000000:
                    pct_vida = 0.03
                elif sa <= 3000000:
                    pct_vida = 0.04
                elif sa <= 5000000:
                    pct_vida = 0.05
                else:
                    pct_vida = 0.06

                bono_vida = sa * pct_vida
                resultado += f"<li>❤️ <strong>Bono de Vida:</strong> {pct_vida*100:.2f}% ➜ <strong>${bono_vida:,.2f}</strong><br>✅ Aplica por superar mínimo de $250,000.</li>"

            resultado += f"</ul><h4>🧾 <strong>Total del Bono Vida:</strong> ${bono_vida:,.2f}</h4>"

        except Exception as e:
            resultado = f"<p style='color:red;'>❌ Error: {e}</p>"

        st.markdown("<p style='text-align: center; font-size:14px;'>Aplican restricciones y condiciones conforme al cuaderno oficial de CHUBB Seguros 2025.</p>", unsafe_allow_html=True)


elif tipo_ramo == "Hogar":
    st.markdown("#### Datos para Hogar")
    prod_2024 = st.text_input("Producción 2024 Hogar ($)", placeholder="Ej. $100,000")
    prod_2025 = st.text_input("Producción 2025 Hogar ($)", placeholder="Ej. $150,000")
    siniestralidad = st.text_input("Siniestralidad (%)", placeholder="Ej. 25")

    if st.button("Calcular Bonos Hogar"):
        try:
            p2024 = int(prod_2024.replace("$", "").replace(",", "")) if prod_2024 else 0
            p2025 = int(prod_2025.replace("$", "").replace(",", "")) if prod_2025 else 0
            sin = float(siniestralidad)

            resultado += f"<h3>📋 Resultado para {nombre.upper()}</h3>"
            resultado += "<h4>📊 Datos Ingresados:</h4><ul>"
            resultado += f"<li>Producción 2024: <strong>${p2024:,.2f}</strong></li>"
            resultado += f"<li>Producción 2025: <strong>${p2025:,.2f}</strong></li>"
            resultado += f"<li>Siniestralidad: <strong>{sin:.2f}%</strong></li></ul>"
            resultado += "<h4>💵 Resultados de Bono:</h4><ul>"

            # Bono Producción
            if sin > 60:
                pct_prod = 0
                resultado += "<li>💔 <strong>Bono de Producción Hogar:</strong> $0.00 ❌ No aplica por siniestralidad superior al 60%.</li>"
            elif p2025 < 25000:
                pct_prod = 0
                resultado += "<li>💔 <strong>Bono de Producción Hogar:</strong> $0.00 ❌ No aplica por no alcanzar $25,000 de producción.</li>"
            else:
                if p2025 <= 50000:
                    pct_prod = 0.02
                elif p2025 <= 100000:
                    pct_prod = 0.03
                elif p2025 <= 150000:
                    pct_prod = 0.04
                elif p2025 <= 200000:
                    pct_prod = 0.05
                elif p2025 <= 300000:
                    pct_prod = 0.06
                else:
                    pct_prod = 0.07
                bono_prod = p2025 * pct_prod
                resultado += f"<li>🏡 <strong>Bono de Producción Hogar:</strong> {pct_prod*100:.2f}% ➜ <strong>${bono_prod:,.2f}</strong></li>"

            # Bono Siniestralidad
            if sin <= 22.99:
                pct_sini = 0.03
            elif sin <= 34.99:
                pct_sini = 0.02
            elif sin <= 44.99:
                pct_sini = 0.01
            else:
                pct_sini = 0

            bono_sini = p2025 * pct_sini
            if pct_sini > 0:
                resultado += f"<li>🧯 <strong>Bono de Siniestralidad Hogar:</strong> {pct_sini*100:.2f}% ➜ <strong>${bono_sini:,.2f}</strong></li>"
            else:
                resultado += "<li>💔 <strong>Bono de Siniestralidad Hogar:</strong> $0.00 ❌ No aplica por siniestralidad superior al 44.99%.</li>"

            # Bono Crecimiento
            if p2024 == 0:
                bono_crec = 0
                resultado += "<li>💔 <strong>Bono de Crecimiento Hogar:</strong> $0.00 ❌ No aplica por no tener producción en 2024.</li>"
            else:
                crec = p2025 - p2024
                pct_crec = (crec / p2024) * 100
                if pct_crec < 10:
                    pct_crec_v = 0
                elif pct_crec <= 20:
                    pct_crec_v = 0.01
                elif pct_crec <= 30:
                    pct_crec_v = 0.02
                elif pct_crec <= 40:
                    pct_crec_v = 0.03
                elif pct_crec <= 50:
                    pct_crec_v = 0.04
                else:
                    pct_crec_v = 0.05
                bono_crec = crec * pct_crec_v
                if pct_crec_v > 0:
                    resultado += f"<li>📈 <strong>Bono de Crecimiento Hogar:</strong> {pct_crec_v*100:.2f}% ➜ <strong>${bono_crec:,.2f}</strong> (Crecimiento del {pct_crec:.2f}%)</li>"
                else:
                    resultado += f"<li>💔 <strong>Bono de Crecimiento Hogar:</strong> $0.00 ❌ No aplica por crecimiento menor al 10% (tuvo {pct_crec:.2f}%).</li>"

            total = bono_prod + bono_sini + bono_crec
            resultado += f"</ul><h4>🧾 <strong>Total del Bono Hogar:</strong> ${total:,.2f}</h4>"

        except Exception as e:
            resultado = f"<p style='color:red;'>❌ Error: {e}</p>"

        st.markdown("<p style='text-align: center; font-size:14px;'>Aplican restricciones y condiciones conforme al cuaderno oficial de CHUBB Seguros 2025.</p>", unsafe_allow_html=True)


elif tipo_ramo == "Accidentes y Enfermedades":
    st.markdown("#### Datos para Accidentes y Enfermedades (A&H)")
    prod_2024 = st.text_input("Producción 2024 A&H ($)", placeholder="Ej. $300,000")
    prod_2025 = st.text_input("Producción 2025 A&H ($)", placeholder="Ej. $500,000")
    siniestralidad = st.text_input("Siniestralidad (%)", placeholder="Ej. 20")

    if st.button("Calcular Bonos A&H"):
        try:
            p2024 = int(prod_2024.replace("$", "").replace(",", "")) if prod_2024 else 0
            p2025 = int(prod_2025.replace("$", "").replace(",", "")) if prod_2025 else 0
            sin = float(siniestralidad)

            resultado += f"<h3>📋 Resultado para {nombre.upper()}</h3>"
            resultado += "<h4>📊 Datos Ingresados:</h4><ul>"
            resultado += f"<li>Producción 2024: <strong>${p2024:,.2f}</strong></li>"
            resultado += f"<li>Producción 2025: <strong>${p2025:,.2f}</strong></li>"
            resultado += f"<li>Siniestralidad: <strong>{sin:.2f}%</strong></li></ul>"
            resultado += "<h4>💵 Resultados de Bono:</h4><ul>"

            # Bono Producción A&H
            if p2025 < 300000:
                pct_prod = 0
                resultado += "<li>💔 <strong>Bono de Producción A&H:</strong> $0.00 ❌ No aplica por no alcanzar $300,000 de producción.</li>"
            else:
                if p2025 <= 500000:
                    pct_prod = 0.02
                elif p2025 <= 750000:
                    pct_prod = 0.03
                elif p2025 <= 1000000:
                    pct_prod = 0.04
                elif p2025 <= 1250000:
                    pct_prod = 0.05
                elif p2025 <= 1500000:
                    pct_prod = 0.06
                else:
                    pct_prod = 0.07
                bono_prod = p2025 * pct_prod
                resultado += f"<li>🏥 <strong>Bono de Producción A&H:</strong> {pct_prod*100:.2f}% ➜ <strong>${bono_prod:,.2f}</strong></li>"

            # Bono Siniestralidad A&H
            if sin <= 22.99:
                pct_sini = 0.045
            elif sin <= 34.99:
                pct_sini = 0.025
            else:
                pct_sini = 0

            bono_sini = p2025 * pct_sini
            if pct_sini > 0:
                resultado += f"<li>🧯 <strong>Bono de Siniestralidad A&H:</strong> {pct_sini*100:.2f}% ➜ <strong>${bono_sini:,.2f}</strong></li>"
            else:
                resultado += "<li>💔 <strong>Bono de Siniestralidad A&H:</strong> $0.00 ❌ No aplica por siniestralidad superior al 34.99%.</li>"

            # Bono Crecimiento A&H
            if p2024 == 0:
                bono_crec = 0
                resultado += "<li>💔 <strong>Bono de Crecimiento A&H:</strong> $0.00 ❌ No aplica por no tener producción en 2024.</li>"
            else:
                crec = p2025 - p2024
                pct_crec = (crec / p2024) * 100
                if pct_crec < 10:
                    pct_crec_v = 0
                elif pct_crec <= 20:
                    pct_crec_v = 0.02
                elif pct_crec <= 30:
                    pct_crec_v = 0.03
                elif pct_crec <= 40:
                    pct_crec_v = 0.04
                elif pct_crec <= 50:
                    pct_crec_v = 0.06
                else:
                    pct_crec_v = 0.08
                bono_crec = crec * pct_crec_v
                if pct_crec_v > 0:
                    resultado += f"<li>📈 <strong>Bono de Crecimiento A&H:</strong> {pct_crec_v*100:.2f}% ➜ <strong>${bono_crec:,.2f}</strong> (Crecimiento del {pct_crec:.2f}%)</li>"
                else:
                    resultado += f"<li>💔 <strong>Bono de Crecimiento A&H:</strong> $0.00 ❌ No aplica por crecimiento menor al 10% (tuvo {pct_crec:.2f}%).</li>"

            total = bono_prod + bono_sini + bono_crec
            resultado += f"</ul><h4>🧾 <strong>Total del Bono A&H:</strong> ${total:,.2f}</h4>"

        except Exception as e:
            resultado = f"<p style='color:red;'>❌ Error: {e}</p>"

        st.markdown("<p style='text-align: center; font-size:14px;'>Aplican restricciones y condiciones conforme al cuaderno oficial de CHUBB Seguros 2025.</p>", unsafe_allow_html=True)


elif tipo_ramo == "Otros Daños":
    st.markdown("#### Datos para Otros Daños (MM & MAD)")
    prod_otros = st.text_input("Producción 2025 Otros Daños ($)", placeholder="Ej. $300,000")

    if st.button("Calcular Bonos Otros Daños"):
        try:
            p = int(prod_otros.replace("$", "").replace(",", ""))

            resultado += f"<h3>📋 Resultado para {nombre.upper()}</h3>"
            resultado += "<h4>📊 Datos Ingresados:</h4><ul>"
            resultado += f"<li>Producción 2025 Otros Daños: <strong>${p:,.2f}</strong></li></ul>"
            resultado += "<h4>💵 Resultados de Bono:</h4><ul>"

            if p >= 250000:
                pct_prod = 0.015
                bono = p * pct_prod
                resultado += f"<li>🏗️ <strong>Bono de Producción Otros Daños:</strong> {pct_prod*100:.2f}% ➜ <strong>${bono:,.2f}</strong> ✅ Aplica por superar el mínimo de $250,000</li>"
            else:
                bono = 0
                resultado += f"<li>💔 <strong>Bono de Producción Otros Daños:</strong> $0.00 ❌ No aplica. Mínimo requerido: $250,000</li>"

            resultado += f"</ul><h4>🧾 <strong>Total del Bono Otros Daños:</strong> ${bono:,.2f}</h4>"

        except Exception as e:
            resultado = f"<p style='color:red;'>❌ Error: {e}</p>"

        st.markdown("<p style='text-align: center; font-size:14px;'>Aplican restricciones y condiciones conforme al cuaderno oficial de CHUBB Seguros 2025.</p>", unsafe_allow_html=True)

# Mostrar resultados y restricciones
if resultado:
    st.markdown("---")
    st.markdown(resultado, unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; font-size:14px;'>Aplican restricciones y condiciones conforme al cuaderno oficial de CHUBB Seguros 2025.</p>", unsafe_allow_html=True)
