import streamlit as st

st.set_page_config(page_title="Simulador de Bonos CHUBB 2025", layout="centered")

st.title("Simulador de Bonos")
st.subheader("CHUBB 2025")

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

            resultado += f"**Agente:** {nombre}\n"
            resultado += f"**Tipo:** Autos\n"
            resultado += f"**Producción 2024:** ${p2024:,.2f}\n"
            resultado += f"**Producción 2025:** ${p2025:,.2f}\n"
            resultado += f"**Siniestralidad:** {sin:.1f}%\n"
            resultado += f"**Unidades Emitidas:** {unidades_emitidas}\n\n"

            # Bono Producción
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
            resultado += f"**Bono Producción ({pct_prod*100:.0f}%):** ${bono_prod:,.2f} {'✔' if bono_prod > 0 else '❌'}\n"

            # Bono Siniestralidad
            pct_sini = 0.04 if sin <= 30 else 0.03 if sin <= 45 else 0.02 if sin <= 50 else 0.01 if sin <= 55 else 0
            bono_sini = p2025 * pct_sini
            motivo_sini = "✔ Aplica por siniestralidad aceptable." if pct_sini > 0 else "❌ No aplica por siniestralidad >55%."
            resultado += f"**Bono Siniestralidad ({pct_sini*100:.0f}%):** ${bono_sini:,.2f} {'✔' if bono_sini > 0 else '❌'} - {motivo_sini}\n"

            # Bono Crecimiento
            if p2024 == 0:
                bono_crec = p2025 * 0.04
                resultado += f"✔ Agente nuevo sin producción previa, aplica bono crecimiento 4% sobre producción 2025. Total: ${bono_crec:,.2f}\n"
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
                bono_crec_pct = calcular_bono_crecimiento(pct_crec, unidades_emitidas)
                bono_crec = crec * bono_crec_pct
                resultado += f"**Bono Crecimiento ({bono_crec_pct*100:.0f}%):** ${bono_crec:,.2f} {'✔' if bono_crec > 0 else '❌'}\n"
                resultado += f"✔ Crecimiento real del {pct_crec:.1f}% con {unidades_emitidas} unidades emitidas. Se asigna bono según tabla.\n"

            total = bono_prod + bono_sini + bono_crec
            resultado += f"\n➡ **Total Bono:** ${total:,.2f}\n"

        elif tipo_bono == "Daños":
            p_danios = int(prod_2025_danios.replace("$", "").replace(",", "")) if prod_2025_danios else 0
            sin_danios = float(siniestralidad_danios)

            resultado += f"**Agente:** {nombre}\n"
            resultado += f"**Tipo:** Daños\n"
            resultado += f"**Producción 2025 Daños:** ${p_danios:,.2f}\n"
            resultado += f"**Siniestralidad Daños:** {sin_danios:.1f}%\n\n"

            if p_danios < 250000:
                resultado += "❌ Producción insuficiente para aplicar bonos.\n"
                total = 0
            else:
                pct_danios = 0
                if sin_danios <= 30:
                    pct_danios = 0.03 if p_danios > 500000 else 0.02 if p_danios > 350000 else 0.01
                elif sin_danios <= 45:
                    pct_danios = 0.02 if p_danios > 350000 else 0.01
                elif sin_danios <= 55:
                    pct_danios = 0.01
                bono_danios = p_danios * pct_danios
                resultado += f"**Bono Producción Daños ({pct_danios*100:.0f}%):** ${bono_danios:,.2f} {'✔' if bono_danios > 0 else '❌'}\n"
                total = bono_danios

            resultado += f"\n➡ **Total Bono:** ${total:,.2f}\n"

    except Exception as e:
        resultado = f"❌ Error en los datos ingresados: {e}"

    st.markdown("---")
    st.markdown("### Resultado")
    st.text_area("", resultado, height=300)
    st.markdown("---")
    st.info("Aplican restricciones y condiciones conforme al cuaderno oficial de CHUBB Seguros 2025.")
