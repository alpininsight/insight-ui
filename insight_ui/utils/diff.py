"""HTML diff generation utilities."""

file_template = """
<!DOCTYPE html">
<html>
    <head>
        <meta http-equiv="Content-Type" content="text/html; charset=%(charset)s" />
        <title></title>
        <style type="text/css">%(styles)s
        </style>
    </head>
    <body>
        %(table)s
    </body>
</html>"""

styles = """
    table.diff {font-family:Courier; border:medium; margin-bottom: 1.0rem;}
    .diff_header {background-color:#e0e0e0}
    td.diff_header {text-align:right}
    td {padding-left: 0.25rem; padding-right: 0.25rem}
    .diff_next {background-color:#c0c0c0}
    .diff_add {background-color:#aaffaa}
    .diff_chg {background-color:#ffff77}
    .diff_sub {background-color:#ffaaaa}"""
