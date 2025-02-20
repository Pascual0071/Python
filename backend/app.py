from flask import Flask, request, jsonify
import pandas as pd
import os

app = Flask(__name__)

ARCHIVO_EXCEL = "finanzas.xlsx"

def guardar_en_excel(datos, tipo):
    columnas = ["Mes", "Categoría", "Ingresos", "Gastos"]
    df_nuevo = pd.DataFrame(datos, columns=columnas)
    df_existente = pd.read_excel(ARCHIVO_EXCEL).fillna(0) if os.path.exists(ARCHIVO_EXCEL) else pd.DataFrame(columns=columnas)
    
    df_existente = df_existente[df_existente["Categoría"] != "Total"]
    df_existente = df_existente[df_existente["Categoría"] != "Balance General"]
    df_final = pd.concat([df_existente, df_nuevo], ignore_index=True)
    
    df_final = calcular_totales(df_final)
    df_final.to_excel(ARCHIVO_EXCEL, index=False)

def calcular_totales(df):
    df_totales = df.groupby("Mes")[["Ingresos", "Gastos"]].sum().reset_index()
    df_totales["Categoría"] = "Total"
    df_totales["Balance"] = df_totales["Ingresos"] - df_totales["Gastos"]
    
    balance_general = pd.DataFrame({
        "Mes": [""],
        "Categoría": ["Balance General"],
        "Ingresos": [df_totales["Ingresos"].sum()],
        "Gastos": [df_totales["Gastos"].sum()],
        "Balance": [df_totales["Balance"].sum()]
    })
    
    return pd.concat([df, df_totales, balance_general], ignore_index=True)

@app.route('/registrar', methods=['POST'])
def registrar():
    data = request.json
    mes = data.get("mes")
    categoria = data.get("categoria")
    cantidad = data.get("cantidad")
    tipo = data.get("tipo")  # "Ingresos" o "Gastos"

    if not mes or not categoria or cantidad is None or not tipo:
        return jsonify({"error": "Faltan datos"}), 400

    guardar_en_excel([[mes, categoria, cantidad if tipo == "Ingresos" else 0, cantidad if tipo == "Gastos" else 0]], tipo)
    return jsonify({"mensaje": "Datos guardados correctamente"})

@app.route('/ver', methods=['GET'])
def ver():
    if os.path.exists(ARCHIVO_EXCEL):
        df = pd.read_excel(ARCHIVO_EXCEL).fillna(0)
        return df.to_json(orient="records")
    return jsonify({"error": "No hay datos registrados"}), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
