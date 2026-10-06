from langchain.tools import tool
import plotly.express as px

# A tool for creating charts using Plotly Express
@tool
def create_chart(chart_type: str,labels: list[str],values: list[float],title: str):
    """Create a bar, line, or pie chart."""

    if chart_type == "bar":
        figure = px.bar(x=labels,y=values,title=title)

    elif chart_type == "line":
        figure = px.line(x=labels,y=values,title=title)

    elif chart_type == "pie":
        figure = px.pie(names=labels,values=values,title=title)

    elif chart_type == "scatter":
        figure = px.scatter(x=labels,y=values,title=title)

    else:
        return "Unsupported chart type."

    return figure