# dash
import dash_mantine_components as dmc
from dash import html


def create_table(docs: list[dict]):
    fields = docs[0].keys()
    header = [html.Tr([html.Th(field) for field in fields])]
    rows = [html.Tr([html.Td(doc.get(field)) for field in fields]) for doc in docs]
    table = [html.Thead(header), html.Tbody(rows)]
    return table


def insert_table_leaderboard():
    table = dmc.Table(
        id='leaderboard',
        striped=True,
        highlightOnHover=True,
        withBorder=True,
        withColumnBorders=True,
    )
    return table
