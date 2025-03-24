import streamlit as st
import re

st.set_page_config(page_title="Simulador de Bonos CHUBB 2025", layout="centered")

st.title("Simulador de Bonos")
st.subheader("CHUBB 2025")

# Entradas generales
agente = st.text_input("Nombre del agente")
tipo = st.selectbox("Tipo de Bono", ["Autos", "Daños"])

# Funciones auxiliares
def format_currency(value):
    try:
        return "$" + f"{int(round(value)):,}"
    except:
        return "$0"

def parse_currency(value):
    try:
        if "." in str(value) and "," not in str(value):
            st.warning("⚠ Usa comas (,) para separar miles. No uses puntos (.) ya que se interpretan como decimales.")
        value = str(value).replace(",", "")
        value = re.sub(r'[^\d.]', '', value)
        if "." in value:
            entero, decimal = value.split(".", 1)
            if decimal and int(decimal[0]) >= 5:
                return int(entero) + 1
            else:
                return int(entero)
        return int(value)
    except:
        return 0

if tipo == "Autos":
    input_prod_2024 = st.text_input("Producción 2024 ($)", value="", placeholder="Ej. $1,000,000")
    prod_2024 = parse_currency(input_prod_2024)

    input_prod_2025 = st.text_input("Producción 2025 ($)", value="", placeholder="Ej. $2,000,000")
    prod_2025 = parse_currency(input_prod_2025)

    siniestralidad = st.number_input("Siniestralidad (%)", min_value=0.0, max_value=100.0, step=0.1)
    unidades = st.number_input("Número de Unidades Emitidas", min_value=0)

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

    if st.button("Calcular Bonos Autos"):
        comentarios = []
        notas = []

        st.markdown("### Datos Ingresados")
        st.markdown(f"- Agente: **{agente.upper()}**")
        st.markdown(f"- Producción 2024: **{format_currency(prod_2024)}**")
        st.markdown(f"- Producción 2025: **{format_currency(prod_2025)}**")
        st.markdown(f"- Siniestralidad: **{siniestralidad:.2f}%**")
        st.markdown(f"- Unidades Emitidas: **{int(unidades)}**")

        if siniestralidad < 60:
            if prod_2025 <= 350000:
                pct_prod = 0.01
            elif prod_2025 <= 500000:
                pct_prod = 0.02
            elif prod_2025 <= 1000000:
                pct_prod = 0.03
            elif prod_2025 <= 2000000:
                pct_prod = 0.04
            else:
                pct_prod = 0.05
        else:
            if prod_2025 <= 500000:
                pct_prod = 0.01
            elif prod_2025 <= 1000000:
                pct_prod = 0.01
            elif prod_2025 <= 2000000:
                pct_prod = 0.02
            else:
                pct_prod = 0.03
            notas.append("⚠ Siniestralidad ≥60%, se aplica tabla de producción ajustada.")

        bono_prod = prod_2025 * pct_prod
        comentarios.append(f"Bono Producción ({pct_prod*100:.0f}%): {format_currency(bono_prod)} {'✔' if bono_prod>0 else '❌'}")

        if siniestralidad <= 30:
            pct_sini = 0.04
        elif siniestralidad <= 45:
            pct_sini = 0.03
        elif siniestralidad <= 50:
            pct_sini = 0.02
        elif siniestralidad <= 55:
            pct_sini = 0.01
        else:
            pct_sini = 0

        bono_sini = prod_2025 * pct_sini
        motivo_sini = "✔ Aplica por siniestralidad aceptable." if pct_sini > 0 else "❌ No aplica por siniestralidad >55%."
        comentarios.append(f"Bono Siniestralidad ({pct_sini*100:.0f}%): {format_currency(bono_sini)} {'✔' if bono_sini>0 else '❌'} - {motivo_sini}")

        if prod_2024 == 0:
            bono_crec = prod_2025 * 0.04
            comentarios.append(f"✔ Agente nuevo sin producción previa, aplica bono crecimiento 4% sobre producción 2025. Total: {format_currency(bono_crec)}")
        else:
            crec = prod_2025 - prod_2024
            pct_crec = (crec / prod_2024) * 100
            bono_crec_pct = calcular_bono_crecimiento(pct_crec, unidades)
            bono_crec = crec * bono_crec_pct
            comentarios.append(f"Bono Crecimiento ({bono_crec_pct*100:.0f}%): {format_currency(bono_crec)} {'✔' if bono_crec>0 else '❌'}")
            notas.append(f"✔ Crecimiento real del {pct_crec:.1f}% con {int(unidades)} unidades emitidas. Se asigna bono según tabla.")

        total = bono_prod + bono_sini + bono_crec

        st.markdown("---")
        st.markdown(f"### Resultado para {agente.upper()}")
        for c in comentarios:
            st.markdown(f"- {c}")
        st.markdown(f"**➡ Total Bono: {format_currency(total)}**")

        if notas:
            st.markdown("---")
            st.markdown("### Notas")
            for n in notas:
                st.markdown(f"- {n}")

elif tipo == "Daños":
    input_prod_danios = st.text_input("Producción Daños PYME 2025 ($)", value="", placeholder="Ej. $500,000")
    prod_danios = parse_currency(input_prod_danios)

    siniestralidad_danios = st.number_input("Siniestralidad Daños (%)", min_value=0.0, max_value=100.0, step=0.1)

    if st.button("Calcular Bonos Daños"):
        comentarios = []

        st.markdown("### Datos Ingresados")
        st.markdown(f"- Agente: **{agente.upper()}**")
        st.markdown(f"- Producción Daños: **{format_currency(prod_danios)}**")
        st.markdown(f"- Siniestralidad Daños: **{siniestralidad_danios:.2f}%**")

        if siniestralidad_danios < 60:
            if prod_danios <= 350000:
                pct_danios = 0.01
            elif prod_danios <= 500000:
                pct_danios = 0.02
            else:
                pct_danios = 0.03
        else:
            pct_danios = 0.01

        bono_danios = prod_danios * pct_danios

        if siniestralidad_danios <= 30:
            pct_sini_danios = 0.03
        elif siniestralidad_danios <= 45:
            pct_sini_danios = 0.02
        elif siniestralidad_danios <= 55:
            pct_sini_danios = 0.01
        else:
            pct_sini_danios = 0

        bono_sini_danios = prod_danios * pct_sini_danios

        comentarios.append(f"Bono Producción Daños ({pct_danios*100:.0f}%): {format_currency(bono_danios)}")
        comentarios.append(f"Bono Siniestralidad Daños ({pct_sini_danios*100:.0f}%): {format_currency(bono_sini_danios)}")

        total_danios = bono_danios + bono_sini_danios

        st.markdown("---")
        st.markdown(f"### Resultado para {agente.upper()}")
        for c in comentarios:
            st.markdown(f"- {c}")
        st.markdown(f"**➡ Total Bono: {format_currency(total_danios)}**")
