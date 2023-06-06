# dash
import dash_mantine_components as dmc


def insert_footer():
    text = dmc.Text(
        children=[
            'App v0.4.0. Developed and maintained by the ',
            dmc.Anchor('SDG Integration team', href='https://sdgintegration.undp.org', target='_blank'),
            ' at UNDP. Visit ',
            dmc.Anchor('Data Futures Platform', href='https://data.undp.org', target='_blank'),
            ' to learn more about our projects.',
        ],
        size='sm',
        color='gray',
    )
    footer = dmc.Footer(
        height='25px',
        fixed=True,
        children=dmc.Center(text),
        zIndex=-1,
    )
    return footer
