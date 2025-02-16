import streamlit as st
import pyecharts
from pyecharts.charts import Line, Bar, HeatMap, Liquid
from pyecharts import options as opts
from streamlit_echarts import st_pyecharts, st_echarts
import pandas as pd

st.title("Prueba 2.0")

options = {
    "xAxis": {
        "type": "category",
        "data": ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"],
    },
    "yAxis": {"type": "value"},
    "series": [
        {
            "data": [
                120,
                {"value": 200, "itemStyle": {"color": "#a90000"}},
                150,
                80,
                70,
                110,
                130,
            ],
            "type": "bar",
        }
    ],
}
st_echarts(
    options=options,
    height="400px",
)
print(pyecharts.__version__)