import streamlit as st

st.set_page_config(page_title="Simulador de Bonos CHUBB 2025", layout="centered")

# Títulos centrados
st.markdown("<h1 style='text-align: center;'>Simulador de Bonos</h1>", unsafe_allow_html=True)
st.markdown("<h2 style='text-align: center;'>CHUBB 2025</h2>", unsafe_allow_html=True)

nombre = st.text_input("Nombre del Agente")
tipo_bono = st.selectbox("Tipo de Bono", ["Autos", "Daños"])

if tipo_bono == "Autos":
    prod_2024 = st.text_input("Producción 2024 ($)", placeholder="Ej. $1,000,000.00")
    prod_2025 = st.text_input("Producción 2025 ($)", placeholder="Ej. $2,000,000.00")
    siniestralidad = st.text_input("Siniestralidad (%)", placeholder="Ej. 40")
    unidades = st.text_input("Número de Unidades Emitidas", placeholder="Ej. 151")
elif tipo_bono == "Daños":
    prod_2025_danios = st.text_input("Producción 2025 Daños ($)", placeholder="Ej. $1,000,000.00")
    siniestralidad_danios = st.text_input("Siniestralidad Daños (%)", placeholder="Ej. 40")

resultado = ""
if st.button("Calcular Bonos"):
    try:
        if tipo_bono == "Autos":
            p2024 = int(prod_2024.replace("$", "").replace(",", "")) if prod_2024 else 0
            p2025 = int(prod_2025.replace("$", "").replace(",", "")) if prod_2025 else 0
            sin = float(siniestralidad)
            unidades_emitidas = int(unidades)

            resultado += f"<h3>📋 Resultado para {nombre.upper()}</h3>"
            resultado += "<h4>📊 Datos Ingresados:</h4><ul>"
            resultado += f"<li>Producción 2024: <strong>${p2024:,.2f}</strong></li>"
            resultado += f"<li>Producción 2025: <strong>${p2025:,.2f}</strong></li>"
            resultado += f"<li>Siniestralidad: <strong>{sin:.2f}%</strong></li>"
            resultado += f"<li>Unidades Emitidas: <strong>{unidades_emitidas}</strong></li></ul>"

            resultado += "<h4>💵 Resultados de Bono:</h4><ul>"
            # Bono Producción
            if sin < 60:
                if p2025 <= 350000:
                    pct_prod = 0.01
                    desc_prod = "En el rango de 250,000 a 350,000 aplica bono del 1%."
                elif p2025 <= 500000:
                    pct_prod = 0.02
                    desc_prod = "En el rango de 350,001 a 500,000 aplica bono del 2%."
                elif p2025 <= 1000000:
                    pct_prod = 0.03
                    desc_prod = "En el rango de 500,001 a 1,000,000 aplica bono del 3%."
                elif p2025 <= 2000000:
                    pct_prod = 0.04
                    desc_prod = "En el rango de 1,000,001 a 2,000,000 aplica bono del 4%."
                else:
                    pct_prod = 0.05
                    desc_prod = "Más de 2,000,000 aplica bono del 5%."
            else:
                if p2025 <= 500000:
                    pct_prod = 0.01
                    desc_prod = "Producción baja y siniestralidad alta, aplica bono del 1%."
                elif p2025 <= 1000000:
                    pct_prod = 0.01
                    desc_prod = "Producción intermedia con siniestralidad alta, aplica bono del 1%."
                elif p2025 <= 2000000:
                    pct_prod = 0.02
                    desc_prod = "Producción mayor con siniestralidad alta, aplica bono del 2%."
                else:
                    pct_prod = 0.03
                    desc_prod = "Producción alta y siniestralidad alta, aplica bono del 3%."
            bono_prod = p2025 * pct_prod
            resultado += f"<li>Bono de Producción: <strong>{pct_prod*100:.2f}%</strong> ➜ <strong>${bono_prod:,.2f}</strong> ➜ {'✅ Aplica' if bono_prod > 0 else '❌ No aplica'}. {desc_prod}</li>"

            # Bono Siniestralidad
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
            resultado += f"<li>Bono de Siniestralidad: <strong>{pct_sini*100:.2f}%</strong> ➜ <strong>${bono_sini:,.2f}</strong> ➜ {'✅ Aplica' if pct_sini > 0 else '❌ No aplica'}. Siniestralidad del {sin:.2f}%.</li>"

            # Bono Crecimiento
            if p2024 == 0:
                bono_crec = p2025 * 0.04
                resultado += f"<li>Bono de Crecimiento (Agente nuevo): <strong>4.00%</strong> ➜ <strong>${bono_crec:,.2f}</strong> ➜ ✅ Aplica bono por producción nueva.</li>"
            else:
                crec = p2025 - p2024
                pct_crec = (crec / p2024) * 100
                def calcular_bono_crecimiento(pct_crec, unidades):
                    if pct_crec < 10:
                        return 0
                    elif pct_crec <= 20:
                        return 0.04 if unidades > 150 else 0.035 if unidades > 50 else 0.025
                    elif pct_crec <= 30:
                        return 0.07 if unidades > 150 else 0.055 if unidades > 50 else 0.04
                    elif pct_crec <= 40:
                        return 0.09 if unidades > 150 else 0.07 if unidades > 50 else 0.06
                    elif pct_crec <= 50:
                        return 0.15 if unidades > 150 else 0.12 if unidades > 50 else 0.09
                    else:
                        return 0.17 if unidades > 150 else 0.15 if unidades > 50 else 0.12
                pct_crec_aplica = calcular_bono_crecimiento(pct_crec, unidades_emitidas)
                bono_crec = crec * pct_crec_aplica
                resultado += f"<li>Bono de Crecimiento: <strong>{pct_crec_aplica*100:.2f}%</strong> ➜ <strong>${bono_crec:,.2f}</strong> ➜ {'✅ Aplica' if bono_crec > 0 else '❌ No aplica'}. Crecimiento real del {pct_crec:.2f}%, {unidades_emitidas} unidades.</li>"

            total = bono_prod + bono_sini + bono_crec
            resultado += f"</ul><h4>🧾 Total del Bono:</h4><p><strong>${total:,.2f}</strong></p>"

        elif tipo_bono == "Daños":
            p2025 = int(prod_2025_danios.replace("$", "").replace(",", ""))
            sin_d = float(siniestralidad_danios)

            resultado += f"<h3>📋 Resultado para {nombre.upper()}</h3>"
            resultado += "<h4>📊 Datos Ingresados:</h4><ul>"
            resultado += f"<li>Producción Daños: <strong>${p2025:,.2f}</strong></li>"
            resultado += f"<li>Siniestralidad: <strong>{sin_d:.2f}%</strong></li></ul>"

            resultado += "<h4>💵 Resultados de Bono:</h4><ul>"
            # Bono Producción Daños
            if sin_d < 60:
                if p2025 <= 350000:
                    pct_prod = 0.01
                elif p2025 <= 500000:
                    pct_prod = 0.02
                else:
                    pct_prod = 0.03
            else:
                pct_prod = 0.01
            bono_prod = p2025 * pct_prod
            resultado += f"<li>Bono Producción Daños: <strong>{pct_prod*100:.2f}%</strong> ➜ <strong>${bono_prod:,.2f}</strong></li>"

            # Bono Siniestralidad Daños
            if sin_d <= 30:
                pct_sini = 0.03
            elif sin_d <= 45:
                pct_sini = 0.02
            elif sin_d <= 55:
                pct_sini = 0.01
            else:
                pct_sini = 0
            bono_sini = p2025 * pct_sini
            resultado += f"<li>Bono Siniestralidad Daños: <strong>{pct_sini*100:.2f}%</strong> ➜ <strong>${bono_sini:,.2f}</strong></li>"

            total = bono_prod + bono_sini
            resultado += f"</ul><h4>🧾 Total del Bono:</h4><p><strong>${total:,.2f}</strong></p>"

        st.markdown("<hr>", unsafe_allow_html=True)
        st.markdown(resultado, unsafe_allow_html=True)
        st.markdown("<p style='text-align: center; font-size:14px;'>Aplican restricciones y condiciones conforme al cuaderno oficial de CHUBB Seguros 2025.</p>", unsafe_allow_html=True)
    except Exception as e:
        st.error(f"❌ Error en los datos ingresados: {e}")
else:
    st.markdown("<p style='text-align: center; font-size:14px;'>Aplican restricciones y condiciones conforme al cuaderno oficial de CHUBB Seguros 2025.</p>", unsafe_allow_html=True)
