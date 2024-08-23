import plotly.graph_objs as go
from plotly.subplots import make_subplots
import polars as pl

def plot_quality_metrics_with_alerts(quality_metrics: pl.DataFrame, thresholds: dict):
    fig = make_subplots(
        rows=3, cols=2,
        subplot_titles=("Completeness", "Accuracy", "Timeliness", "Consistency", "Validity", "Uniqueness"),
        specs=[[{"type": "table"}, {"type": "table"}],
               [{"type": "table"}, {"type": "table"}],
               [{"type": "table"}, {"type": "table"}]],
    )

    alerts = []
    completeness_value = quality_metrics["Completeness"][0]
    completeness_df = pl.DataFrame({
        "Column": ["Completeness"],
        "Value": [completeness_value]
    })

    completeness_threshold = thresholds.get("Completeness", 1.0)
    if completeness_df["Value"].min() < completeness_threshold:
        alerts.append(f"Warning: Completeness below threshold {completeness_threshold}")

    completeness_table = go.Table(
        header=dict(values=["Column", "Value"], fill_color='paleturquoise', align='left'),
        cells=dict(values=[completeness_df["Column"].to_list(), completeness_df["Value"].to_list()],
                   fill_color='lavender', align='left')
    )

    accuracy_columns = [col for col in quality_metrics.columns if col.startswith("Accuracy_")]
    validity_columns = [col for col in quality_metrics.columns if col.startswith("Validity_")]
    uniqueness_columns = [col for col in quality_metrics.columns if col.startswith("Uniqueness_")]

    check_thresholds(quality_metrics, "Accuracy", accuracy_columns, thresholds, alerts)
    check_thresholds(quality_metrics, "Timeliness", ["Timeliness"], thresholds, alerts)
    check_thresholds(quality_metrics, "Consistency", ["Consistency"], thresholds, alerts)
    check_thresholds(quality_metrics, "Validity", validity_columns, thresholds, alerts)
    check_thresholds(quality_metrics, "Uniqueness", uniqueness_columns, thresholds, alerts)

    fig.add_trace(completeness_table, row=1, col=1)
    fig.add_trace(create_table(quality_metrics.select(accuracy_columns), "Accuracy"), row=1, col=2)
    fig.add_trace(create_table(quality_metrics.select("Timeliness"), "Timeliness"), row=2, col=1)
    fig.add_trace(create_table(quality_metrics.select("Consistency"), "Consistency"), row=2, col=2)
    fig.add_trace(create_table(quality_metrics.select(validity_columns), "Validity"), row=3, col=1)
    fig.add_trace(create_table(quality_metrics.select(uniqueness_columns), "Uniqueness"), row=3, col=2)

    if alerts:
        alert_text = "<br>".join(alerts)
        fig.update_layout(
            annotations=[go.layout.Annotation(
                text=alert_text,
                showarrow=False,
                xref="paper", yref="paper",
                x=0.5, y=1.0,
                font=dict(color="red", size=12),
                align="center"
            )]
        )

    fig.update_layout(height=900, showlegend=False, title_text="Data Quality Metrics Overview")
    fig.show()

def create_table(data: pl.DataFrame, metric_name: str):
    if data.shape[0] == 0:
        return go.Table(
            header=dict(values=[metric_name, "Value"], fill_color='paleturquoise', align='left'),
            cells=dict(values=[[], []], fill_color='lavender', align='left')
        )

    return go.Table(
        header=dict(values=[metric_name, "Value"], fill_color='paleturquoise', align='left'),
        cells=dict(values=[data.columns, data.row(0)], fill_color='lavender', align='left')
    )

def check_thresholds(df: pl.DataFrame, metric_name: str, columns: list, thresholds: dict, alerts: list):
    if columns:
        metric_threshold = thresholds.get(metric_name, 1.0)
        for column in columns:
            if df[column].min() < metric_threshold:
                alerts.append(f"Warning: {metric_name} ({column}) below threshold {metric_threshold}")
