import pandas as pd
import plotly.express as px
import os
import dash
from dash import html, Input, Output, dcc, dash_table

# Cargar datos
# ruta = os.path.join(os.path.dirname(__file__), "notas_limpio.xlsx")
# dataf = pd.read_excel(ruta)

#Ruta para cargar desde al base de datos
def creartablero(server):
    

# Iniciar app
appnotas = dash.Dash(__name__, server = server, url_base_pathname = "/dashprincipal")

appnotas.layout = html.Div([
    html.H1("Tablero Avanzado de Notas", 
            style={"textAlign":"center", "backgroundColor":"#506004", 
                   "color":"white", "padding":"20px", "borderRadius":"8px"}),
    
    # Filtros
    html.Div([
        html.Label("Seleccionar Carrera", style={"fontWeight":"bold"}),
        dcc.Dropdown(id="filtro_carrera",
            options=[{"label":ca, "value":ca} for ca in sorted(dataf["Carrera"].unique())],
            value=dataf["Carrera"].unique()[0],
            style={"width":"100%"}),
        
        html.Br(),
        
        html.Label("Rango de Edad", style={"fontWeight":"bold"}),
        dcc.RangeSlider(id="slider_edad",
            min=dataf["Edad"].min(),
            max=dataf["Edad"].max(),
            step=1,
            value=[dataf["Edad"].min(), dataf["Edad"].max()],
            tooltip={"placement":"bottom", "always_visible":True},
            marks={int(dataf["Edad"].min()): str(int(dataf["Edad"].min())),
                   int(dataf["Edad"].max()): str(int(dataf["Edad"].max()))}),
        
        html.Br(),
        
        html.Label("Rango Promedio", style={"fontWeight":"bold"}),
        dcc.RangeSlider(id="slider_promedio",
            min=0, max=5, step=0.5,
            value=[0,5],
            tooltip={"placement":"bottom", "always_visible":True},
            marks={0:"0.0", 2.5:"2.5", 5:"5.0"}),
    ], style={"width":"80%", "margin":"auto", "padding":"20px", 
              "backgroundColor":"#f9f9f9", "borderRadius":"10px"}),
    
    html.Br(),
    
    # KPIs
    html.Div(id="kpis", 
             style={"display":"flex", "justifyContent":"space-around", 
                    "width":"80%", "margin":"auto"}),
    
    html.Br(),
    
    # Tabla con loading
    html.Div([
        html.H3("Datos Filtrados", style={"textAlign":"center"}),
        dcc.Loading([
            dash_table.DataTable(id="tabla",
                page_size=10,
                filter_action="native",
                sort_action="native",
                row_selectable="multi",
                style_table={"overflowX":"auto"},
                style_cell={"textAlign":"center", "padding":"8px"},
                style_header={"backgroundColor":"#506004", "color":"white", "fontWeight":"bold"})
        ], type="circle")
    ], style={"width":"80%", "margin":"auto"}),
    
    html.Br(),
    
    # Gráfico detallado de selección
    html.Div([
        html.H3("Análisis Detallado (Selección de Tabla)", style={"textAlign":"center"}),
        dcc.Loading(dcc.Graph(id="gra_detallado"), type="default")
    ], style={"width":"80%", "margin":"auto"}),
    
    html.Br(),
    
    # Tabs de gráficos
    html.Div([
        html.H3("Gráficos Interactivos", style={"textAlign":"center"}),
        dcc.Tabs([
            dcc.Tab(label="Histograma Promedios", children=[dcc.Graph(id="histograma")]),
            dcc.Tab(label="Dispersión Edad-Promedio", children=[dcc.Graph(id="dispersion")]),
            dcc.Tab(label="Distribución Carrera", children=[dcc.Graph(id="pie")]),
            dcc.Tab(label="Barras Desempeño", children=[dcc.Graph(id="barras")])
        ])
    ], style={"width":"80%", "margin":"auto"})
])

# Callback principal - actualiza TODO
@appnotas.callback(
    [Output("kpis", "children"),
     Output("tabla", "data"),
     Output("tabla", "columns"),
     Output("histograma", "figure"),
     Output("dispersion", "figure"),
     Output("pie", "figure"),
     Output("barras", "figure")],
    [Input("filtro_carrera", "value"),
     Input("slider_edad", "value"),
     Input("slider_promedio", "value")]
)
def actualizar_dashboard(carrera, rango_edad, rango_promedio):
    # Aplicar filtros
    filtro = dataf[
        (dataf["Carrera"] == carrera) &
        (dataf["Edad"] >= rango_edad[0]) &
        (dataf["Edad"] <= rango_edad[1]) &
        (dataf["Promedio"] >= rango_promedio[0]) &
        (dataf["Promedio"] <= rango_promedio[1])
    ].copy()
    
    if len(filtro) == 0:
        # Datos vacíos - mostrar mensaje
        kpis = [html.Div("Sin datos con estos filtros", 
                        style={"textAlign":"center", "padding":"20px"})]
        tabla_data = []
        tabla_columns = [{"name": i, "id": i} for i in dataf.columns]
        fig_vacio = px.scatter(title="Sin datos - ajusta los filtros")
        return kpis, tabla_data, tabla_columns, fig_vacio, fig_vacio, fig_vacio, fig_vacio
    
    # KPIs calculados
    promedio = round(filtro["Promedio"].mean(), 2)
    total = len(filtro)
    maximo = round(filtro["Promedio"].max(), 2)
    minimo = round(filtro["Promedio"].min(), 2)
    
    kpis = [
        html.Div([
            html.H4("Promedio", style={"color":"#506004"}),
            html.H2(promedio, style={"color":"#506004"})
        ], style={"backgroundColor":"#F1E4BD", "padding":"20px", 
                 "borderRadius":"10px", "textAlign":"center", "width":"22%"}),
        
        html.Div([
            html.H4("Total Estudiantes", style={"color":"#506004"}),
            html.H2(total, style={"color":"#506004"})
        ], style={"backgroundColor":"#F1E4BD", "padding":"20px", 
                 "borderRadius":"10px", "textAlign":"center", "width":"22%"}),
        
        html.Div([
            html.H4("Máximo", style={"color":"#506004"}),
            html.H2(maximo, style={"color":"#506004"})
        ], style={"backgroundColor":"#F1E4BD", "padding":"20px", 
                 "borderRadius":"10px", "textAlign":"center", "width":"22%"}),
        
        html.Div([
            html.H4("Mínimo", style={"color":"#506004"}),
            html.H2(minimo, style={"color":"#506004"})
        ], style={"backgroundColor":"#F1E4BD", "padding":"20px", 
                 "borderRadius":"10px", "textAlign":"center", "width":"22%"})
    ]
    
    # Tabla
    tabla_data = filtro.round(2).to_dict("records")
    tabla_columns = [{"name": i, "id": i} for i in filtro.columns]
    
    # Gráficos optimizados
    fig_hist = px.histogram(filtro, x="Promedio", nbins=20,
                           title=f"Distribución Promedios - {carrera} ({len(filtro)} estudiantes)",
                           color_discrete_sequence=["#506004"])
    
    fig_disp = px.scatter(filtro, x="Edad", y="Promedio", 
                         color="Carrera", size="Promedio",
                         title="Edad vs Promedio",
                         color_discrete_sequence=["#506004"])
    
    fig_pie = px.pie(filtro, names="Carrera", values="Promedio",
                    title="Distribución Promedio por Carrera")
    
    desempeño = filtro.groupby("Carrera")["Promedio"].agg(["mean", "count"]).reset_index()
    desempeño.columns = ["Carrera", "Promedio", "Cantidad"]
    fig_barras = px.bar(desempeño, x="Carrera", y="Promedio",
                       title="Desempeño Promedio por Carrera",
                       color_discrete_sequence=["#506004"])
    
    return kpis, tabla_data, tabla_columns, fig_hist, fig_disp, fig_pie, fig_barras

# Callback gráfico detallado (selección tabla)
@appnotas.callback(
    Output("gra_detallado", "figure"),
    Input("tabla", "derived_virtual_data"),
    Input("tabla", "derived_virtual_selected_rows")
)
def actualizar_grafico_detallado(rows, selected_rows):
    if rows is None or len(rows) == 0:
        return px.scatter(title="Selecciona filas en la tabla")
    
    df = pd.DataFrame(rows)
    
    if selected_rows and len(selected_rows) > 0:
        df = df.iloc[selected_rows]
        titulo = f"Selección ({len(df)} filas)"
    else:
        titulo = "Todas las filas filtradas"
    
    if len(df) == 0:
        return px.scatter(title="Sin datos seleccionados")
    
    fig = px.scatter(df, x="Edad", y="Promedio", 
                    color="Carrera" if "Carrera" in df.columns else None,
                    size="Promedio", 
                    title=titulo,
                    trendline="ols",
                    color_discrete_sequence=["#506004"])
    
    fig.update_traces(marker=dict(line=dict(width=1, color="white")))
    
    return fig

#Ejecutar la app
if __name__ == '__main__':
    appnotas.run(debug=True)
