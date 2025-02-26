import streamlit as st
import pyecharts
from pyecharts.charts import Line, Bar, HeatMap, Liquid
from pyecharts import options as opts
from streamlit_echarts import st_pyecharts, st_echarts
import pandas as pd

meses = ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio', 'Julio', 'Agosto', 'Septiembre', 'Octubre',
         'Noviembre', 'Diciembre']
rename_dict = {str(i): mes for i, mes in zip(range(1,13), meses)}
rename_dict_int = {i: mes for i, mes in zip(range(1,13), meses)}


df_final = pd.read_csv("data/df_final.csv", index_col=0)
resumen_pivot_empleado= pd.read_csv("data/resumen_pivot_empleado.csv", index_col=[0,1,2])
resumen_pivot_empresa= pd.read_csv("data/resumen_pivot_empresa.csv", index_col=[0,1,2])


df_final['mes'] = df_final['mes'].map(rename_dict_int)
resumen_pivot_empleado.rename(columns=rename_dict, inplace=True)
resumen_pivot_empresa.rename(columns=rename_dict, inplace=True)

# df_final['anio'].unique().tolist()
anios_unicos = sorted(set(df_final['anio']))
empleados_unicos = sorted(set(df_final['empleado']))
empresas_unicos = sorted(set(resumen_pivot_empresa.index.get_level_values(1)))

st.set_page_config(page_title="Grupo Interact", layout="wide", initial_sidebar_state="collapsed")

def main():
    st.title("Análisis de horas Grupo Interact")
    st.sidebar.header("Filtros")
    with st.sidebar:
        input_type = st.sidebar.radio('Búsqueda por:', ["Empleado", "Empresa"], None)
        input_anio = st.selectbox("Selecciona el año:", anios_unicos, None)

        if input_type:
            if input_type == 'Empleado':
                input_empleados = st.selectbox("Selecciona el empleado:", empleados_unicos, None)
                if input_empleados:
                    input_empresas = None
            else:
                input_empresas = st.selectbox("Selecciona el empresa:", empresas_unicos, None)
                if input_empresas:
                    input_empleados = None

        input_mes = st.selectbox("Selecciona el mes:", meses, None, disabled=True)


    if input_type == "Empleado" and input_empleados != None:

        df_filtrado_empleado = resumen_pivot_empleado.copy()

        if input_anio:
            df_filtrado_empleado = df_filtrado_empleado[df_filtrado_empleado.index.get_level_values('anio') == input_anio]
        if input_empleados:
            df_filtrado_empleado = df_filtrado_empleado[df_filtrado_empleado.index.get_level_values('empleado') == input_empleados]

        df_filtrado_final = df_final.copy()
        df_final_resumen = df_filtrado_final.query('empleado == @input_empleados and anio == @input_anio')
        df_final_resumen = df_final_resumen.loc[:, df_final_resumen.columns != 'empleado']

        df_filtrado_empleado = df_filtrado_empleado.reset_index()
        df_filtrado_empleado = df_filtrado_empleado.drop(columns=['anio', 'empleado'])
        df_filtrado_empleado = df_filtrado_empleado.set_index('cliente')

        df_filtrado_chart = df_final_resumen[df_final_resumen['anio'] == input_anio]

        # Definir las series de datos para el gráfico
        x_axis = df_filtrado_chart['mes'].unique().tolist()  # Meses en el eje X
        horas_efectivas = df_filtrado_chart['horas_efectivas_trabajadas'].tolist()  # Horas efectivas
        horas_meta = df_filtrado_chart['horas_meta'].tolist()  # Horas meta

        # Configurar el gráfico
        chart_config = {
            "title": {
                "text": "Comparación de Horas Trabajadas",
                "subtext": f"Año {input_anio}",
                "left": "center",
                "top": "5%"
            },
            "tooltip": {
                "trigger": "axis"
            },
            "legend": {
                "data": ["Horas Efectivas", "Horas Meta"],
                "top": "15%"
            },
            "grid": {
                "top": "25%",
                "left": "10%",
                "right": "10%",
                "bottom": "10%"
            },
            "xAxis": {
                "type": "category",
                "data": x_axis
            },
            "yAxis": {
                "type": "value"
            },
            "series": [
                {
                    "name": "Horas Efectivas",
                    "type": "line",
                    "data": horas_efectivas
                    # "smooth": True
                },
                {
                    "name": "Horas Meta",
                    "type": "line",
                    "data": horas_meta
                    # "smooth": True
                }
            ]
        }

        # Mostrar el gráfico con streamlit-echarts
        st_echarts(chart_config, height="600px")

        # Mostrar resultados
        st.markdown(f"### {input_empleados}", unsafe_allow_html=True)
        st.dataframe(df_filtrado_empleado, use_container_width=True)



        st.dataframe(df_final_resumen, use_container_width=True)



    elif input_type == "Empresa" and input_empresas != None:
        st.markdown(f"### {input_empresas}", unsafe_allow_html=True)
        # st.dataframe(resumen_pivot_empresa)

        df_filtrado_empresas = resumen_pivot_empresa.copy()
        df_filtrado_empresas = df_filtrado_empresas.reset_index()
        df_filtrado_empresas = df_filtrado_empresas.query('cliente == @input_empresas and anio == @input_anio')

        st.dataframe(df_filtrado_empresas.loc[:, ~df_filtrado_empresas.columns.isin(['anio', 'cliente'])], use_container_width=True)

# options = {
#     "xAxis": {
#         "type": "category",
#         "data": ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"],
#     },
#     "yAxis": {"type": "value"},
#     "series": [
#         {
#             "data": [
#                 120,
#                 {"value": 200, "itemStyle": {"color": "#a90000"}},
#                 150,
#                 80,
#                 70,
#                 110,
#                 130,
#             ],
#             "type": "bar",
#         }
#     ],
# }
# st_echarts(
#     options=options,
#     height="400px",
# )

def mes_a_numero(mes):
    meses = ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio',
             'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre']
    return meses.index(mes)

if __name__ == "__main__":
    main()







