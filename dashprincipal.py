import dash
import pandas as pd
import plotly.express as px
from dash import html, Input, Output, dcc
from dash import dash_table

from database import obtenerestudiantes


COLUMNAS_BASE = ["Nombre", "Edad", "Carrera", "nota1", "nota2", "nota3", "Promedio", "Desempeño"]


def obtener_datos_dashboard():
    dataf = obtenerestudiantes()

    if dataf.empty:
        return pd.DataFrame(columns=COLUMNAS_BASE)

    dataf["Edad"] = pd.to_numeric(dataf["Edad"], errors="coerce")
    dataf["Promedio"] = pd.to_numeric(dataf["Promedio"], errors="coerce")
    dataf = dataf.dropna(subset=["Edad", "Promedio", "Carrera", "Nombre", "Desempeño"])

    return dataf


def crear_figura_vacia(tipo="scatter", titulo="Sin datos disponibles"):
    if tipo == "histogram":
        fig = px.histogram(title=titulo)
    elif tipo == "bar":
        fig = px.bar(title=titulo)
    elif tipo == "pie":
        fig = px.pie(title=titulo)
    else:
        fig = px.scatter(title=titulo)

    return fig


def creartablero(server):
    def construir_layout():
        dataf = obtener_datos_dashboard()

        edad_min = int(dataf["Edad"].min()) if not dataf.empty else 0
        edad_max = int(dataf["Edad"].max()) if not dataf.empty else 0
        carreras = sorted(dataf["Carrera"].dropna().unique()) if not dataf.empty else []
        opciones_carrera = [{"label": "Todas", "value": "Todas"}] + [
            {"label": carrera, "value": carrera} for carrera in carreras
        ]

        return html.Div([
            html.H1("TABLERO AVANZADO", style={
                "textAlign": "center",
                "backgroundColor": "#41431B",
                "color": "#E3DBBB",
                "padding": "20px",
                "borderRadius": "20px"
            }),

            html.Div([
                html.Label("Seleccionar carrera"),
                dcc.Dropdown(
                    id="filtro_carrera",
                    options=opciones_carrera,
                    value="Todas",
                    clearable=False
                ),
                html.Br(),

                html.Label("Rango de edad"),
                dcc.RangeSlider(
                    id="slider_edad",
                    min=edad_min,
                    max=edad_max,
                    step=1,
                    value=[edad_min, edad_max],
                    tooltip={"placement": "bottom", "always_visible": True}
                ),
                html.Br(),

                html.Label("Rango promedio"),
                dcc.RangeSlider(
                    id="slider_promedio",
                    min=0,
                    max=5,
                    step=0.5,
                    value=[0, 5],
                    tooltip={"placement": "bottom", "always_visible": True}
                )
            ], style={"width": "80%", "margin": "auto", "color": "#41431B"}),

            html.Br(),

            html.Div(
                id="kpis",
                style={"display": "flex", "justifyContent": "space-around", "gap": "20px", "flexWrap": "wrap"}
            ),

            html.Br(),

            dcc.Loading(
                dash_table.DataTable(
                    id="tabla",
                    page_size=8,
                    filter_action="native",
                    sort_action="native",
                    row_selectable="multi",
                    selected_rows=[],
                    style_table={"overflowX": "auto"},
                    style_cell={"textAlign": "center"}
                ),
                type="circle"
            ),

            html.Br(),

            dcc.Input(
                id="busqueda",
                type="text",
                placeholder="Buscar Estudiante",
                style={"width": "300px", "padding": "10px"}
            ),

            html.Br(),
            html.Br(),

            dcc.Interval(id="intervalo", interval=10000, n_intervals=0),

            dcc.Loading(dcc.Graph(id="gra_detallado"), type="default"),

            html.Br(),

            html.Div([
                html.H3("Top 10 estudiantes por promedio", style={"color": "#41431B"}),
                dash_table.DataTable(
                    id="tabla_ranking",
                    page_size=10,
                    style_table={"overflowX": "auto"},
                    style_cell={"textAlign": "center"},
                    style_header={"backgroundColor": "#41431B", "color": "white", "fontWeight": "bold"}
                )
            ]),

            html.Br(),

            html.Div([
                html.H3(id="alerta_riesgo", style={"color": "#8B1E1E"}),
                dash_table.DataTable(
                    id="tabla_riesgo",
                    page_size=10,
                    style_table={"overflowX": "auto"},
                    style_cell={"textAlign": "center"},
                    
                    style_header={"backgroundColor": "#41431B", "color": "white", "fontWeight": "bold"}
                )
            ], style={
                "border": "2px solid #E5B1B1",
                "borderRadius": "16px",
                "padding": "18px",
                "backgroundColor": "#FFF7F7"
            }),

            html.Br(),

            dcc.Tabs([
                dcc.Tab(label="Histograma", children=[dcc.Graph(id="histograma")]),
                dcc.Tab(label="Dispersion", children=[dcc.Graph(id="dispersion")]),
                dcc.Tab(label="Desempeño", children=[dcc.Graph(id="pie")]),
                dcc.Tab(label="Promedio por Carrera", children=[dcc.Graph(id="barras")])
            ])
        ])

    appnotas = dash.Dash(
        __name__,
        server=server,
        url_base_pathname="/dashprincipal/",
        suppress_callback_exceptions=True
    )

    appnotas.layout = construir_layout

    @appnotas.callback(
        Output("tabla", "data"),
        Output("tabla", "columns"),
        Output("kpis", "children"),
        Output("histograma", "figure"),
        Output("dispersion", "figure"),
        Output("pie", "figure"),
        Output("barras", "figure"),
        Output("tabla_ranking", "data"),
        Output("tabla_ranking", "columns"),
        Output("tabla_riesgo", "data"),
        Output("tabla_riesgo", "columns"),
        Output("alerta_riesgo", "children"),
        Input("filtro_carrera", "value"),
        Input("slider_edad", "value"),
        Input("slider_promedio", "value"),
        Input("busqueda", "value"),
        Input("intervalo", "n_intervals")
    )
    def actualizar_comp(carrera, rangoedad, rangoprome, busqueda, n_intervals):
        dataf = obtener_datos_dashboard()

        if dataf.empty:
            columnas = [{"name": columna, "id": columna} for columna in COLUMNAS_BASE]
            columnas_tablas = [{"name": columna, "id": columna} for columna in ["Nombre", "Carrera", "Promedio"]]
            return (
                [],
                columnas,
                [
                    html.Div([html.H4("Promedio"), html.H2(0)], style={"backgroundColor": "#41431B", "color": "white", "padding": "15px", "borderRadius": "10px"}),
                    html.Div([html.H4("Total estudiantes"), html.H2(0)], style={"backgroundColor": "#41431B", "color": "white", "padding": "15px", "borderRadius": "10px"}),
                    html.Div([html.H4("Máximo"), html.H2(0)], style={"backgroundColor": "#41431B", "color": "white", "padding": "15px", "borderRadius": "10px"})
                ],
                crear_figura_vacia("histogram"),
                crear_figura_vacia("scatter"),
                crear_figura_vacia("pie"),
                crear_figura_vacia("bar"),
                [],
                columnas_tablas,
                [],
                columnas_tablas,
                "No hay estudiantes en riesgo"
            )

        filtro = dataf.copy()

        if carrera and carrera != "Todas":
            filtro = filtro[filtro["Carrera"] == carrera]

        filtro = filtro[
            (filtro["Edad"] >= rangoedad[0]) &
            (filtro["Edad"] <= rangoedad[1]) &
            (filtro["Promedio"] >= rangoprome[0]) &
            (filtro["Promedio"] <= rangoprome[1])
        ]

        if busqueda:
            filtro = filtro[filtro.apply(lambda fila: busqueda.lower() in str(fila).lower(), axis=1)]

        total = len(filtro)
        promedio = round(filtro["Promedio"].mean(), 2) if total else 0
        maximo = round(filtro["Promedio"].max(), 2) if total else 0

        kpis = [
            html.Div([html.H4("Promedio"), html.H2(promedio)], style={"backgroundColor": "#41431B", "color": "white", "padding": "15px", "borderRadius": "10px", "minWidth": "180px", "textAlign": "center"}),
            html.Div([html.H4("Total estudiantes"), html.H2(total)], style={"backgroundColor": "#41431B", "color": "white", "padding": "15px", "borderRadius": "10px", "minWidth": "180px", "textAlign": "center"}),
            html.Div([html.H4("Máximo"), html.H2(maximo)], style={"backgroundColor": "#41431B", "color": "white", "padding": "15px", "borderRadius": "10px", "minWidth": "180px", "textAlign": "center"})
        ]

        histo = px.histogram(filtro, x="Promedio", nbins=10, title="Distribución de Promedios") if total else crear_figura_vacia("histogram", "Sin datos para el histograma")
        dispersion = px.scatter(
            filtro,
            x="Edad",
            y="Promedio",
            color="Desempeño",
            trendline="ols",
            title="Edad vs Promedio"
        ) if total else crear_figura_vacia("scatter", "Sin datos para la dispersión")
        pie = px.pie(filtro, names="Desempeño", title="Distribución por Desempeño") if total else crear_figura_vacia("pie", "Sin datos para desempeño")

        promedios = dataf.groupby("Carrera")["Promedio"].mean().reset_index()
        barras = px.bar(
            promedios,
            x="Carrera",
            y="Promedio",
            color="Carrera",
            title="Promedio General por Carrera"
        ) if not promedios.empty else crear_figura_vacia("bar", "Sin datos por carrera")

        ranking = dataf.sort_values(["Promedio", "Nombre"], ascending=[False, True])[["Nombre", "Carrera", "Promedio"]].head(10)
        riesgo = dataf[dataf["Promedio"] < 3][["Nombre", "Carrera", "Promedio"]].sort_values(["Promedio", "Nombre"])
        mensaje_riesgo = f"Alerta: {len(riesgo)} estudiante(s) en riesgo academico" if not riesgo.empty else "No hay estudiantes en riesgo"

        return (
            filtro.to_dict("records"),
            [{"name": columna, "id": columna} for columna in filtro.columns],
            kpis,
            histo,
            dispersion,
            pie,
            barras,
            ranking.to_dict("records"),
            [{"name": columna, "id": columna} for columna in ranking.columns],
            riesgo.to_dict("records"),
            [{"name": columna, "id": columna} for columna in riesgo.columns],
            mensaje_riesgo
        )

    @appnotas.callback(
        Output("gra_detallado", "figure"),
        Input("tabla", "derived_virtual_data"),
        Input("tabla", "derived_virtual_selected_rows")
    )
    def actualizartab(rows, selected_rows):
        if not rows:
            return crear_figura_vacia("scatter", "Sin datos")

        dff = pd.DataFrame(rows)

        if selected_rows:
            dff = dff.iloc[selected_rows]

        return px.scatter(
            dff,
            x="Edad",
            y="Promedio",
            color="Desempeño",
            size="Promedio",
            title="Analisis detallado",
            trendline="ols"
        )

    return appnotas
