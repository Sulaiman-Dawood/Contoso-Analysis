"""Contoso FY2025 financial results dashboard."""

import calendar
from dataclasses import dataclass
from html import escape
from pathlib import Path

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st


BASE_DIRECTORY = Path(__file__).resolve().parent
DATA_DIRECTORY = BASE_DIRECTORY / "data"
LOGO_PATH = BASE_DIRECTORY / "images" / "contoso_logo.png"

PAGE_TITLE = "Contoso Financial Results FY25"
PRIMARY_GREEN = "#24b41f"
PRIMARY_BLUE = "#1f77b4"
ACCENT_BLUE = "#4463FF"
ACCENT_RED = "#ff4b4b"
DATAFRAME_ROW_HEIGHT = 35
DATAFRAME_CHROME_HEIGHT = 3

APP_STYLES = """
<style>
div[data-testid="stMetric"] {
    border: 1px solid rgba(49, 51, 63, 0.2);
    border-radius: 16px;
    padding: 1rem;
}

.block-container {
    padding-top: clamp(4rem, 12vw, 12rem);
    padding-right: clamp(1rem, 4vw, 5rem);
    padding-left: clamp(1rem, 4vw, 5rem);
}

.responsive-spacer--hero {
    height: 220px;
}

.responsive-spacer--section {
    height: 50px;
}

.responsive-spacer--large {
    height: 4.25rem;
}

.responsive-spacer--trends-to-age,
.responsive-spacer--age-to-channel,
.responsive-spacer--channel-to-store {
    height: 4.25rem;
}

.responsive-spacer--cohort-to-retention {
    height: 4.25rem;
}

.responsive-spacer--retention-to-conclusion {
    height: 50px;
}

.responsive-spacer--xxlarge {
    height: 8rem;
}

div[data-testid="stPlotlyChart"],
div[data-testid="stDataFrame"] {
    max-width: 100%;
}

.responsive-copy--mobile {
    display: none;
}

.responsive-copy--body {
    margin-bottom: 1rem;
    line-height: 1.6;
}

.responsive-copy--caption {
    margin-bottom: 1rem;
    font-size: 0.875rem;
    line-height: 1.45;
    opacity: 0.7;
}

.responsive-copy--mobile summary {
    cursor: pointer;
    list-style: none;
}

.responsive-copy--mobile summary::-webkit-details-marker {
    display: none;
}

.responsive-copy__read-more {
    margin-left: 0.35rem;
    font-weight: 600;
}

.responsive-copy__full-text,
.responsive-copy__show-less {
    display: none;
}

.responsive-copy__full-text {
    line-height: inherit;
}

.st-key-revenue-customer-charts-mobile,
.st-key-age-chart-mobile,
.st-key-channel-orders-mobile,
.st-key-cohort-analysis-mobile,
.st-key-retention-chart-mobile {
    display: none;
}

.responsive-copy__show-less {
    margin-top: 0.5rem;
    font-weight: 600;
}

.responsive-copy--mobile[open] .responsive-copy__short-text,
.responsive-copy--mobile[open] .responsive-copy__read-more {
    display: none;
}

.responsive-copy--mobile[open] .responsive-copy__full-text,
.responsive-copy--mobile[open] .responsive-copy__show-less {
    display: block;
}

@media (max-width: 768px) {
    .block-container {
        padding-top: 2rem;
        padding-right: 1rem;
        padding-left: 1rem;
    }

    .responsive-spacer--hero {
        height: 1rem;
    }

    .responsive-spacer--section,
    .responsive-spacer--large,
    .responsive-spacer--xxlarge {
        height: 0.75rem;
    }

    .responsive-spacer--trends-to-age,
    .responsive-spacer--age-to-channel,
    .responsive-spacer--channel-to-store,
    .responsive-spacer--cohort-to-retention,
    .responsive-spacer--retention-to-conclusion {
        display: none;
        height: 0;
    }

    div[data-testid="stHorizontalBlock"] {
        flex-wrap: wrap;
        gap: 1rem;
    }

    .st-key-revenue-customer-charts-desktop,
    .st-key-age-chart-desktop,
    .st-key-channel-orders-desktop,
    .st-key-cohort-analysis-desktop,
    .st-key-retention-chart-desktop {
        display: none !important;
    }

    .st-key-revenue-customer-charts-mobile,
    .st-key-age-chart-mobile,
    .st-key-channel-orders-mobile,
    .st-key-cohort-analysis-mobile,
    .st-key-retention-chart-mobile {
        display: block !important;
    }

    .st-key-revenue-customer-charts-mobile
        div[data-testid="stVerticalBlock"],
    .st-key-age-chart-mobile
        div[data-testid="stVerticalBlock"],
    .st-key-channel-orders-mobile
        div[data-testid="stVerticalBlock"],
    .st-key-cohort-analysis-mobile
        div[data-testid="stVerticalBlock"],
    .st-key-retention-chart-mobile
        div[data-testid="stVerticalBlock"] {
        gap: 0 !important;
    }

    div[data-testid="stColumn"] {
        flex: 1 1 100% !important;
        width: 100% !important;
        min-width: 100% !important;
    }

    div[data-testid="stColumn"]:has(div[data-testid="stImage"]) {
        display: none;
    }

    .st-key-store-performance-container
        div[data-testid="stColumn"]:has(div[data-testid="stDataFrame"]) {
        order: 2;
    }

    .st-key-store-performance-container
        div[data-testid="stColumn"]:has(h2) {
        order: 1;
    }

    div[data-testid="stMetric"] {
        padding: 0.75rem;
    }

    div[data-testid="stMetricLabel"] p {
        font-size: 0.75rem !important;
    }

    div[data-testid="stMetricValue"] {
        font-size: 1.35rem !important;
    }

    div[data-testid="stPlotlyChart"] {
        height: 320px !important;
        min-height: 320px !important;
    }

    div[data-testid="stPlotlyChart"] > div,
    div[data-testid="stPlotlyChart"] .js-plotly-plot,
    div[data-testid="stPlotlyChart"] .plot-container,
    div[data-testid="stPlotlyChart"] .svg-container {
        height: 100% !important;
        min-height: 0 !important;
    }

    div[data-testid="stPlotlyChart"] text {
        font-size: 11px !important;
    }

    h1 {
        font-size: 1.7rem !important;
        line-height: 1.2 !important;
    }

    h2 {
        font-size: 1.3rem !important;
        line-height: 1.25 !important;
    }

    h3 {
        font-size: 1.05rem !important;
    }

    p,
    li,
    .responsive-copy--body {
        font-size: 0.875rem;
        line-height: 1.45;
    }

    .responsive-copy--desktop {
        display: none;
    }

    .responsive-copy--mobile {
        display: block;
    }

    .responsive-copy--caption {
        margin-bottom: 0.75rem;
        font-size: 0.8rem;
        line-height: 1.4;
    }
}
</style>
"""


@dataclass(frozen=True)
class DashboardData:
    """Data frames required by the dashboard."""

    monthly_results: pd.DataFrame
    age_groups: pd.DataFrame
    sales_channels: pd.DataFrame
    store_revenue: pd.DataFrame
    top_brands: pd.DataFrame
    top_categories: pd.DataFrame
    top_products: pd.DataFrame
    monthly_customers: pd.DataFrame
    customer_cohorts: pd.DataFrame
    retention_cohorts: pd.DataFrame


@dataclass(frozen=True)
class DashboardCharts:
    """Plotly figures displayed by the dashboard."""

    revenue_trend: go.Figure
    customer_trend: go.Figure
    age_distribution: go.Figure
    channel_distribution: go.Figure
    customer_cohorts: go.Figure
    retention: go.Figure


def configure_page() -> None:
    """Configure Streamlit before rendering any page content."""
    st.set_page_config(
        page_title=PAGE_TITLE,
        page_icon=":material/trending_up:",
        layout="wide",
    )
    st.markdown(APP_STYLES, unsafe_allow_html=True)


def render_responsive_spacer(size: str) -> None:
    """Render vertical space that contracts on mobile screens."""
    supported_sizes = {
        "hero",
        "section",
        "large",
        "xxlarge",
        "trends-to-age",
        "age-to-channel",
        "channel-to-store",
        "cohort-to-retention",
        "retention-to-conclusion",
    }
    if size not in supported_sizes:
        raise ValueError(f"Unsupported responsive spacer size: {size}")
    st.markdown(
        f'<div class="responsive-spacer--{size}" aria-hidden="true"></div>',
        unsafe_allow_html=True,
    )


def render_responsive_copy(
    desktop_text: str,
    mobile_text: str,
    *,
    variant: str = "caption",
) -> None:
    """Render full desktop copy and a shorter mobile alternative."""
    if variant not in {"body", "caption"}:
        raise ValueError(f"Unsupported responsive copy variant: {variant}")

    st.markdown(
        f'<div class="responsive-copy responsive-copy--{variant} '
        f'responsive-copy--desktop">{escape(desktop_text)}</div>'
        f'<details class="responsive-copy responsive-copy--{variant} '
        f'responsive-copy--mobile">'
        f'<summary><span class="responsive-copy__short-text">'
        f'{escape(mobile_text)}</span>'
        f'<span class="responsive-copy__read-more">Read more</span>'
        f'<span class="responsive-copy__full-text">'
        f'{escape(desktop_text)}</span>'
        f'<span class="responsive-copy__show-less">Show less</span></summary>'
        f'</details>',
        unsafe_allow_html=True,
    )


@st.cache_data(show_spinner=False)
def load_dashboard_data() -> DashboardData:
    """Load and prepare all dashboard data from local CSV files."""
    monthly_results = pd.read_csv(DATA_DIRECTORY / "fy2025_monthly_kpis.csv")
    monthly_results["month_name"] = monthly_results["order_month"].map(
        dict(enumerate(calendar.month_abbr))
    )

    return DashboardData(
        monthly_results=monthly_results,
        age_groups=pd.read_csv(DATA_DIRECTORY / "fy2025_customer_age_groups.csv"),
        sales_channels=pd.read_csv(
            DATA_DIRECTORY / "fy2025_sales_channel_orders.csv"
        ),
        store_revenue=pd.read_csv(DATA_DIRECTORY / "fy2025_store_revenue.csv"),
        top_brands=pd.read_csv(DATA_DIRECTORY / "fy2025_top_brands.csv"),
        top_categories=pd.read_csv(DATA_DIRECTORY / "fy2025_top_categories.csv"),
        top_products=pd.read_csv(DATA_DIRECTORY / "fy2025_top_products.csv"),
        monthly_customers=pd.read_csv(
            DATA_DIRECTORY / "fy2025_regional_monthly_customers.csv"
        ),
        customer_cohorts=pd.read_csv(DATA_DIRECTORY / "customer_cohort_activity.csv"),
        retention_cohorts=pd.read_csv(
            DATA_DIRECTORY / "customer_cohort_retention.csv"
        ),
    )


def format_compact_metric(value: float) -> str:
    """Format a dashboard metric using its existing compact display style."""
    if value >= 1_000_000_000:
        return f"${value / 1_000_000_000:.1f}B"
    if value >= 1_000_000:
        return f"${value / 1_000_000:.1f}M"
    if value >= 1_000:
        return f"${value / 1_000:.1f}K"
    return f"${value:,.2f}"


def build_trend_chart(
    data: pd.DataFrame,
    *,
    y_column: str,
    title: str,
    y_axis_title: str,
    color: str,
) -> go.Figure:
    """Create a consistently styled monthly trend chart."""
    figure = px.line(
        data,
        x="month_name",
        y=y_column,
        title=title,
        markers=True,
        color_discrete_sequence=[color],
        labels={"month_name": "Month", y_column: y_axis_title},
    )
    figure.update_layout(xaxis_title="Month", yaxis_title=y_axis_title)
    return figure


def build_age_distribution_chart(age_groups: pd.DataFrame) -> go.Figure:
    """Create the customer age-group distribution chart."""
    figure = px.bar(
        age_groups,
        x="Age_Group",
        y="Customer_Count",
        color_discrete_sequence=[ACCENT_RED],
        labels={"Age_Group": "Age Group", "Customer_Count": "Total Customers"},
        custom_data=["Percentage_of_Customers"],
    )
    figure.update_layout(
        title="",
        xaxis_title="Age Group",
        yaxis_title="Total Customers",
        autosize=True,
        height=500,
    )
    figure.update_traces(
        hovertemplate=(
            "<b>%{x}</b><br>"
            "Customers: %{y:,}<br>"
            "Percentage: %{customdata[0]:.1f}%"
            "<extra></extra>"
        )
    )
    return figure


def build_channel_distribution_chart(sales_channels: pd.DataFrame) -> go.Figure:
    """Create the online versus in-store orders chart."""
    figure = px.pie(
        sales_channels,
        names="channel",
        values="total_orders",
        hole=0.6,
        title="",
        color="channel",
        color_discrete_sequence=["#7ac8ff", "#04a3f8"],
    )
    figure.update_traces(
        textposition="inside",
        textinfo="percent",
        hovertemplate=(
            "<b>%{label}</b><br>"
            "Orders: %{value:,.0f}<br>"
            "Share: %{percent}"
            "<extra></extra>"
        ),
    )
    figure.update_layout(
        legend_title_text="",
        legend={
            "orientation": "h",
            "x": 0.5,
            "xanchor": "center",
            "y": 1.1,
            "yanchor": "bottom",
        },
    )
    return figure


def build_customer_cohort_chart(customer_cohorts: pd.DataFrame) -> go.Figure:
    """Create the stacked customer cohort chart."""
    figure = px.bar(
        customer_cohorts,
        x="purchase_year",
        y="number_of_customers",
        color="cohort_year",
        barmode="stack",
        custom_data=["cohort_year"],
        labels={
            "purchase_year": "Purchase Year",
            "number_of_customers": "Customers",
            "cohort_year": "Cohort Year",
        },
        color_discrete_sequence=px.colors.sequential.Blues[2:],
    )
    figure.update_traces(
        hovertemplate=(
            "<b>Purchase Year:</b> %{x}<br>"
            "<b>Cohort:</b> %{customdata[0]}<br>"
            "<b>Customers:</b> %{y:,}"
            "<extra></extra>"
        )
    )
    figure.update_layout(
        template="plotly_white",
        xaxis_title="Purchase Year",
        yaxis_title="Number of Customers",
        legend_title="Cohort",
    )
    return figure


def build_retention_chart(retention_cohorts: pd.DataFrame) -> go.Figure:
    """Create the combined retention and churn chart."""
    figure = go.Figure()
    figure.add_bar(
        x=retention_cohorts["cohort_year"],
        y=retention_cohorts["churned_customers"],
        name="Churned Customers",
        marker_color=ACCENT_RED,
        hovertemplate=(
            "<b>Year:</b> %{x}<br>"
            "<b>Churned:</b> %{y:,}"
            "<extra></extra>"
        ),
    )
    figure.add_bar(
        x=retention_cohorts["cohort_year"],
        y=retention_cohorts["retained_customers"],
        name="Retained Customers",
        marker_color=ACCENT_BLUE,
        hovertemplate=(
            "<b>Year:</b> %{x}<br>"
            "<b>Retained:</b> %{y:,}"
            "<extra></extra>"
        ),
    )
    figure.add_scatter(
        x=retention_cohorts["cohort_year"],
        y=retention_cohorts["retention_rate"],
        name="Retention Rate",
        mode="lines+markers",
        line={"color": "#54A24B", "width": 3},
        marker={"size": 8},
        yaxis="y2",
        hovertemplate=(
            "<b>Year:</b> %{x}<br>"
            "<b>Retention Rate:</b> %{y:.1f}%"
            "<extra></extra>"
        ),
    )
    figure.update_layout(
        template="plotly_white",
        barmode="stack",
        xaxis_title="Cohort Year",
        yaxis_title="Customers",
        legend_title="Metric",
        legend={
            "orientation": "h",
            "x": 0.5,
            "xanchor": "center",
            "y": 1.12,
            "yanchor": "bottom",
        },
        yaxis2={
            "title": "Retention Rate (%)",
            "overlaying": "y",
            "side": "right",
        },
    )
    return figure


def build_charts(data: DashboardData) -> DashboardCharts:
    """Build every chart used by the dashboard."""
    return DashboardCharts(
        revenue_trend=build_trend_chart(
            data.monthly_results,
            y_column="total_revenue",
            title="Total Revenue Over Time",
            y_axis_title="Total Revenue",
            color=PRIMARY_GREEN,
        ),
        customer_trend=build_trend_chart(
            data.monthly_results,
            y_column="total_customers",
            title="Total Customers Over Time",
            y_axis_title="Total Customers",
            color=PRIMARY_BLUE,
        ),
        age_distribution=build_age_distribution_chart(data.age_groups),
        channel_distribution=build_channel_distribution_chart(data.sales_channels),
        customer_cohorts=build_customer_cohort_chart(data.customer_cohorts),
        retention=build_retention_chart(data.retention_cohorts),
    )


def create_mobile_chart(figure: go.Figure) -> go.Figure:
    """Create a compact chart copy with a native mobile height."""
    mobile_figure = go.Figure(figure)
    mobile_figure.update_layout(height=320)
    return mobile_figure


def create_mobile_retention_chart(figure: go.Figure) -> go.Figure:
    """Create a mobile retention chart with a single-row legend."""
    mobile_figure = create_mobile_chart(figure)
    mobile_legend_names = ("Churned", "Retained", "Retention %")
    for trace, legend_name in zip(
        mobile_figure.data,
        mobile_legend_names,
        strict=True,
    ):
        trace.name = legend_name

    mobile_figure.update_layout(
        legend={
            "orientation": "h",
            "x": 0.5,
            "xanchor": "center",
            "y": 1.05,
            "yanchor": "bottom",
            "font": {"size": 10},
            "title": {"text": ""},
        },
        margin={"t": 75},
    )
    return mobile_figure


def render_hero() -> None:
    """Render the dashboard introduction and desktop logo."""
    introduction, logo = st.columns([1, 1], gap="large")
    with introduction:
        st.title("The Contoso Retail Company Dashboard")
        render_responsive_copy(
            "The Contoso Retail Company Dashboard provides a comprehensive "
            "overview of the company's performance across key business areas, "
            "including revenue, profitability, customers, products, sales "
            "channels, and regional performance. The dashboard enables "
            "stakeholders to monitor key performance indicators (KPIs), identify "
            "trends, and gain actionable insights to support data-driven "
            "decision-making for FY2025.",
            "A concise view of Contoso's FY2025 revenue, customers, products, and "
            "regional performance.",
            variant="body",
        )
    with logo:
        st.image(LOGO_PATH, width="stretch")


def render_kpis(monthly_results: pd.DataFrame) -> None:
    """Render the primary financial and customer metrics."""
    render_responsive_spacer("xxlarge")
    st.header("Key Performance Indicators (KPIs)")
    render_responsive_copy(
        "FY2025 generated 30.8M in revenue while serving 15.5K customers who "
        "placed 15.7K orders. The average revenue per customer of 2.0K suggests "
        "solid customer value and provides a baseline for evaluating customer "
        "acquisition, retention, and revenue growth trends.",
        "FY2025 delivered $30.8M from 15.5K customers and 15.7K orders.",
    )

    total_revenue = monthly_results["total_revenue"].sum()
    total_customers = monthly_results["total_customers"].sum()
    total_orders = monthly_results["total_orders"].sum()
    metric_columns = st.columns(4, gap="large")
    metric_columns[0].metric("Total Revenue", format_compact_metric(total_revenue))
    metric_columns[1].metric(
        "Total Customers", format_compact_metric(total_customers)
    )
    metric_columns[2].metric("Total Orders", format_compact_metric(total_orders))
    metric_columns[3].metric(
        "Average Revenue per Customer",
        format_compact_metric(total_revenue / total_customers),
    )


def render_trend_sections(charts: DashboardCharts) -> None:
    """Render revenue, customer, age, and channel trend sections."""
    render_responsive_spacer("hero")
    st.header("Revenue & Customer Trends")
    render_responsive_copy(
        "Revenue and customer growth followed similar trends throughout FY2025, "
        "recovering after a mid-year slowdown and reaching their highest levels "
        "in December, reflecting strong year-end performance.",
        "Revenue and customers recovered after mid-year and peaked in December.",
    )
    with st.container(key="revenue-customer-charts-desktop"):
        revenue_column, customer_column = st.columns(2, gap="large")
        with revenue_column:
            st.plotly_chart(charts.revenue_trend, width="stretch")
        with customer_column:
            st.plotly_chart(charts.customer_trend, width="stretch")

    with st.container(key="revenue-customer-charts-mobile"):
        st.plotly_chart(
            create_mobile_chart(charts.revenue_trend),
            width="stretch",
        )
        st.plotly_chart(
            create_mobile_chart(charts.customer_trend),
            width="stretch",
        )

    render_responsive_spacer("trends-to-age")
    st.header("Customer Distribution by Age Group")
    render_responsive_copy(
        "Customers aged over 60 make up the largest segment, followed by the "
        "46–60 and 31–45 age groups. In contrast, customers aged 18–30 represent "
        "the smallest proportion of the customer base, suggesting a stronger "
        "presence of older customers.",
        "Customers over 60 are the largest segment; ages 18–30 are the smallest.",
    )
    with st.container(key="age-chart-desktop"):
        _, age_chart_column, _ = st.columns([2, 5, 2])
        with age_chart_column:
            st.plotly_chart(charts.age_distribution, width="stretch")

    with st.container(key="age-chart-mobile"):
        st.plotly_chart(
            create_mobile_chart(charts.age_distribution),
            width="stretch",
        )

    render_responsive_spacer("age-to-channel")
    with st.container(key="channel-orders-desktop"):
        channel_summary, channel_chart = st.columns([3, 4])
        with channel_summary:
            st.header("Online vs. In-Store Orders")
            render_responsive_copy(
                "Online orders represent the majority of transactions (54.6%), "
                "while in-store purchases contribute 45.4%. This balanced split "
                "highlights a healthy omnichannel strategy with a slight "
                "preference for online shopping.",
                "Online orders lead slightly at 54.6%, versus 45.4% in-store.",
            )
        with channel_chart:
            st.plotly_chart(charts.channel_distribution, width="stretch")

    with st.container(key="channel-orders-mobile"):
        st.header("Online vs. In-Store Orders")
        render_responsive_copy(
            "Online orders represent the majority of transactions (54.6%), "
            "while in-store purchases contribute 45.4%. This balanced split "
            "highlights a healthy omnichannel strategy with a slight preference "
            "for online shopping.",
            "Online orders lead slightly at 54.6%, versus 45.4% in-store.",
        )
        st.plotly_chart(
            create_mobile_chart(charts.channel_distribution),
            width="stretch",
        )


def render_regional_performance(data: DashboardData) -> None:
    """Render store revenue and regional customer tables."""
    render_responsive_spacer("channel-to-store")
    with st.container(key="store-performance-container"):
        store_table, store_summary = st.columns([4, 3], gap="large")
        with store_summary:
            st.header("Store Revenue Performance")
            render_responsive_copy(
                "Store performance varies significantly across regions. Canadian "
                "stores generate the highest revenues, with the Northwest "
                "Territories store leading at approximately 692K, demonstrating "
                "Canada's strong contribution to overall sales. Germany and the "
                "United States also feature several high-performing stores, while "
                "French stores consistently record the lowest revenues, with the "
                "highest-performing French store generating only about 83K. This "
                "disparity highlights potential opportunities to improve market "
                "performance and customer engagement in France.",
                "Canada leads store revenue, while France presents the clearest "
                "improvement opportunity.",
            )
        with store_table:
            st.dataframe(
                data.store_revenue,
                column_config={
                    "net_revenue": st.column_config.ProgressColumn(
                        "Total Revenue",
                        min_value=0,
                        max_value=data.store_revenue["net_revenue"].max(),
                        format="$%.0f",
                        color="green",
                    )
                },
                hide_index=True,
                width="stretch",
            )

    render_responsive_spacer("large")
    st.header("Regional Customer Trends")
    render_responsive_copy(
        "North America remains the dominant customer market throughout FY2025, "
        "followed by Europe, while Australia contributes a smaller but consistent "
        "share. Customer volumes recover steadily after the April decline, with "
        "all regions reaching their highest levels by year-end.",
        "North America leads customer volume; every region peaks near year-end.",
    )
    st.dataframe(
        data.monthly_customers,
        column_config={
            "month": "Month",
            "total_customers": "Total Customers",
            "north_american_customers": "North America Customers",
            "european_customers": "European Customers",
            "australian_customers": "Australian Customers",
        },
        hide_index=True,
        width="stretch",
        height=(
            (len(data.monthly_customers) + 1) * DATAFRAME_ROW_HEIGHT
            + DATAFRAME_CHROME_HEIGHT
        ),
        row_height=DATAFRAME_ROW_HEIGHT,
    )


def render_ranked_table(
    data: pd.DataFrame,
    *,
    heading: str,
    label_column: str,
    share_precision: int,
) -> None:
    """Render a ranked sales table with consistent column configuration."""
    st.markdown(f"**{heading}**")
    st.dataframe(
        data,
        column_config={
            label_column: label_column,
            "total_orders": st.column_config.ProgressColumn(
                "Total Orders",
                min_value=0,
                max_value=int(data["total_orders"].max()),
                format="%d",
            ),
            "percentage_of_total": st.column_config.NumberColumn(
                "Share (%)",
                format=f"%.{share_precision}f%%",
            ),
        },
        hide_index=True,
        width="stretch",
    )


def render_product_performance(data: DashboardData) -> None:
    """Render the brand, category, and product ranking tables."""
    render_responsive_spacer("large")
    st.header("Top of the Top: Brands, Categories, and Products")
    render_responsive_copy(
        "Contoso is the leading brand by total orders, while Cell Phones and "
        "Computers represent the highest-performing product categories. The "
        "top-selling products are primarily DVD players and portable media "
        "devices, highlighting a strong concentration of demand within the "
        "consumer electronics segment.",
        "Contoso leads orders, with Cell Phones and Computers as top categories.",
    )
    brand_and_category_tables, product_table = st.columns([1, 1], gap="large")
    with brand_and_category_tables:
        render_ranked_table(
            data.top_brands,
            heading="Top Selling Brands",
            label_column="Brand",
            share_precision=1,
        )
        render_ranked_table(
            data.top_categories,
            heading="Top Selling Categories",
            label_column="Category",
            share_precision=1,
        )
    with product_table:
        render_responsive_spacer("section")
        render_ranked_table(
            data.top_products,
            heading="Top Selling Products",
            label_column="Product",
            share_precision=2,
        )


def render_cohort_analysis(charts: DashboardCharts) -> None:
    """Render customer cohort and retention analysis."""
    render_responsive_spacer("large")
    with st.container(key="cohort-analysis-desktop"):
        cohort_summary, cohort_chart = st.columns([4, 5], gap="large")
        with cohort_summary:
            st.header("Customer Cohort Analysis")
            render_responsive_copy(
                "The 2023 cohort is the strongest contributor to overall customer "
                "activity, while customers acquired in previous years continue to "
                "make purchases alongside newer cohorts. This pattern suggests "
                "healthy customer retention and a balanced mix of new customer "
                "acquisition and repeat business across FY2021–FY2025.",
                "The 2023 cohort contributes the most activity, supported by "
                "repeat customers from earlier cohorts.",
            )
        with cohort_chart:
            st.plotly_chart(charts.customer_cohorts, width="stretch")

    with st.container(key="cohort-analysis-mobile"):
        st.header("Customer Cohort Analysis")
        render_responsive_copy(
            "The 2023 cohort is the strongest contributor to overall customer "
            "activity, while customers acquired in previous years continue to "
            "make purchases alongside newer cohorts. This pattern suggests "
            "healthy customer retention and a balanced mix of new customer "
            "acquisition and repeat business across FY2021–FY2025.",
            "The 2023 cohort contributes the most activity, supported by repeat "
            "customers from earlier cohorts.",
        )
        st.plotly_chart(
            create_mobile_chart(charts.customer_cohorts),
            width="stretch",
        )

    render_responsive_spacer("cohort-to-retention")
    st.header("Customer Retention & Churn")
    render_responsive_copy(
        "Although churn consistently exceeds retention across all cohorts, "
        "retention rates have improved significantly in recent years, peaking "
        "with the 2023 cohort and remaining strong through 2025. This trend "
        "suggests that customer retention strategies have become more effective "
        "over time.",
        "Retention has improved in recent cohorts, though churn remains higher.",
    )
    with st.container(key="retention-chart-desktop"):
        st.plotly_chart(charts.retention, width="stretch")

    with st.container(key="retention-chart-mobile"):
        st.plotly_chart(
            create_mobile_retention_chart(charts.retention),
            width="stretch",
        )


def render_footer() -> None:
    """Render the conclusion, project details, and contact links."""
    render_responsive_spacer("retention-to-conclusion")
    st.header("Conclusion")
    render_responsive_copy(
        "Contoso Retail delivered strong financial performance throughout FY2025, "
        "generating $30.8M in revenue from over 15.5K customers and 15.7K orders. "
        "After a noticeable slowdown during the first half of the year, both "
        "revenue and customer acquisition recovered steadily, reaching their "
        "highest levels in December. Customer demand is primarily driven by North "
        "America, while Canada contributes the highest-performing stores, "
        "highlighting the region's strategic importance. Product sales are "
        "concentrated within the consumer electronics segment, with Contoso-branded "
        "products and Cell Phones leading overall demand. Customer cohort analysis "
        "indicates that recent acquisition cohorts remain actively engaged, and "
        "retention rates have improved in recent years despite churn continuing to "
        "exceed retained customers. Overall, the business demonstrates healthy "
        "revenue growth, stable customer acquisition, and improving customer "
        "loyalty, while opportunities remain to strengthen retention efforts and "
        "improve the performance of lower-performing markets, particularly France.",
        "Contoso delivered $30.8M in FY2025 with strong year-end growth and "
        "improving retention. France and customer churn remain the main areas for "
        "improvement.",
        variant="body",
    )

    render_responsive_spacer("section")
    st.header("Project Information")
    st.write("**Dataset**: Microsoft Contoso Retail Dataset")
    st.write("- SQL Server")
    st.write("- Python")
    st.write("- Streamlit")
    st.write("- Plotly")
    st.write("- Pandas")

    render_responsive_spacer("section")
    st.header("Thank You")
    st.write(
        "Thank you for exploring the Contoso Retail Company Dashboard. "
        "If you'd like to learn more about my work, feel free to visit:"
    )
    st.link_button("LinkedIn", "https://linkedin.com/in/5ulaiman")
    st.link_button("GitHub", "https://github.com/sulaiman-dawood")
    st.link_button("Email", "mailto:sulaiman9553@gmail.com")


def main() -> None:
    """Run the Contoso dashboard application."""
    configure_page()
    dashboard_data = load_dashboard_data()
    dashboard_charts = build_charts(dashboard_data)

    render_hero()
    render_kpis(dashboard_data.monthly_results)
    render_trend_sections(dashboard_charts)
    render_regional_performance(dashboard_data)
    render_product_performance(dashboard_data)
    render_cohort_analysis(dashboard_charts)
    render_footer()


if __name__ == "__main__":
    main()
