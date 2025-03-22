import tkinter as tk
from tkinter import ttk, messagebox
import locale

locale.setlocale(locale.LC_ALL, '')

def format_currency(event, entry):
    value = entry.get().replace(',', '').replace('$', '')
    if value:
        try:
            formatted = locale.format_string("%d", int(value), grouping=True)
            entry.delete(0, tk.END)
            entry.insert(0, f"${formatted}")
        except ValueError:
            pass

def parse_currency(value):
    return int(value.replace('$', '').replace(',', '') or 0)

def parse_integer(value):
    return int(value.replace('$', '').replace(',', '') or 0)

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

root = tk.Tk()
root.title("Simulador de Bonos CHUBB")
frame = tk.Frame(root)
frame.pack(padx=20, pady=20)

tk.Label(frame, text="Simulador de Bonos", font=("Helvetica", 18, "bold")).grid(row=0, column=0, columnspan=3)
tk.Label(frame, text="CHUBB 2025", font=("Helvetica", 14)).grid(row=1, column=0, columnspan=3)

tk.Label(frame, text="Nombre del Agente:").grid(row=2, column=0, sticky="e")
entry_nombre = tk.Entry(frame)
entry_nombre.grid(row=2, column=1)

tk.Label(frame, text="Tipo:").grid(row=3, column=0, sticky="e")
combo_tipo = ttk.Combobox(frame, values=["Autos", "Daños"])
combo_tipo.grid(row=3, column=1)
combo_tipo.set("Autos")

entry_prod_2024 = tk.Entry(frame)
entry_prod_2025 = tk.Entry(frame)
entry_siniestro = tk.Entry(frame)
entry_unidades = tk.Entry(frame)
entry_prod_danios = tk.Entry(frame)
entry_sini_danios = tk.Entry(frame)

label_prod_2024 = tk.Label(frame, text="Producción 2024:")
label_prod_2025 = tk.Label(frame, text="Producción 2025:")
label_siniestro = tk.Label(frame, text="Siniestralidad (%):")
label_unidades = tk.Label(frame, text="Número de Unidades Emitidas:")
label_prod_danios = tk.Label(frame, text="Producción 2025 Daños:")
label_sini_danios = tk.Label(frame, text="Siniestralidad Daños (%):")

resultado_text = tk.Text(frame, height=20, width=85)
resultado_text.grid(row=9, column=0, columnspan=3, pady=10)

def actualizar_campos():
    tipo = combo_tipo.get()
    if tipo == "Autos":
        label_prod_2024.grid(row=4, column=0, sticky="e")
        entry_prod_2024.grid(row=4, column=1)
        label_prod_2025.grid(row=5, column=0, sticky="e")
        entry_prod_2025.grid(row=5, column=1)
        label_siniestro.grid(row=6, column=0, sticky="e")
        entry_siniestro.grid(row=6, column=1)
        label_unidades.grid(row=7, column=0, sticky="e")
        entry_unidades.grid(row=7, column=1)
        label_prod_danios.grid_forget()
        entry_prod_danios.grid_forget()
        label_sini_danios.grid_forget()
        entry_sini_danios.grid_forget()
    else:
        label_prod_2024.grid_forget()
        entry_prod_2024.grid_forget()
        label_prod_2025.grid_forget()
        entry_prod_2025.grid_forget()
        label_siniestro.grid_forget()
        entry_siniestro.grid_forget()
        label_unidades.grid_forget()
        entry_unidades.grid_forget()
        label_prod_danios.grid(row=4, column=0, sticky="e")
        entry_prod_danios.grid(row=4, column=1)
        label_sini_danios.grid(row=5, column=0, sticky="e")
        entry_sini_danios.grid(row=5, column=1)

combo_tipo.bind("<<ComboboxSelected>>", lambda e: actualizar_campos())
for entry in [entry_prod_2024, entry_prod_2025, entry_prod_danios]:
    entry.bind("<KeyRelease>", lambda e, ent=entry: format_currency(e, ent))

def calcular_bonos():
    nombre = entry_nombre.get().strip()
    tipo = combo_tipo.get()
    resultado_text.delete(1.0, tk.END)
    comentarios = []

    if tipo == "Autos":
        try:
            p2024 = parse_currency(entry_prod_2024.get())
            p2025 = parse_currency(entry_prod_2025.get())
            sin = float(entry_siniestro.get())
            unidades = parse_integer(entry_unidades.get())
        except:
            messagebox.showerror("Error", "Datos inválidos en Autos")
            return

        resultado_text.insert(tk.END, f"Agente: {nombre}\nTipo: Autos\nProducción 2024: ${p2024:,.2f}\nProducción 2025: ${p2025:,.2f}\nSiniestralidad: {sin:.1f}%\nUnidades Emitidas: {unidades}\n\n")

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
            comentarios.append("⚠ Siniestralidad ≥60%, se aplica tabla de producción ajustada.")

        bono_prod = p2025 * pct_prod
        comentarios.append(f"Bono Producción ({pct_prod*100:.0f}%): ${bono_prod:,.2f} {'✔' if bono_prod>0 else '❌'}")

        pct_sini = 0.04 if sin <= 30 else 0.03 if sin <= 45 else 0.02 if sin <= 50 else 0.01 if sin <= 55 else 0
        bono_sini = p2025 * pct_sini
        motivo_sini = "✔ Aplica por siniestralidad aceptable." if pct_sini > 0 else "❌ No aplica por siniestralidad >55%."
        comentarios.append(f"Bono Siniestralidad ({pct_sini*100:.0f}%): ${bono_sini:,.2f} {'✔' if bono_sini>0 else '❌'} - {motivo_sini}")

        if p2024 == 0:
            bono_crec = p2025 * 0.04
            comentarios.append(f"✔ Agente nuevo sin producción previa, aplica bono crecimiento 4% sobre producción 2025. Total: ${bono_crec:,.2f}")
        else:
            crec = p2025 - p2024
            pct_crec = (crec / p2024) * 100
            bono_crec_pct = calcular_bono_crecimiento(pct_crec, unidades)
            bono_crec = crec * bono_crec_pct
            comentarios.append(f"Bono Crecimiento ({bono_crec_pct*100:.0f}%): ${bono_crec:,.2f} {'✔' if bono_crec>0 else '❌'}")
            comentarios.append(f"✔ Crecimiento real del {pct_crec:.1f}% con {unidades} unidades emitidas. Se asigna bono según tabla.")

        total = bono_prod + bono_sini + bono_crec
        for c in comentarios:
            resultado_text.insert(tk.END, c + "\n")
        resultado_text.insert(tk.END, f"\n➡ Total Bono: ${total:,.2f}\n")
        resultado_text.insert(tk.END, "\n*Nota: El bono por crecimiento se calcula sobre el crecimiento real (producción 2025 - 2024), no sobre el total 2025.")

btn_calcular = tk.Button(frame, text="Calcular Bonos", command=calcular_bonos)
btn_calcular.grid(row=8, column=1, pady=10)

actualizar_campos()
root.mainloop()

