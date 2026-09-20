import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


# --------------------------------------------------
# PAGE CONFIGURATION
# --------------------------------------------------

st.set_page_config(
    page_title="Superstore Business Analytics",
    page_icon="📊",
    layout="wide"
)


# --------------------------------------------------
# LOAD DATA
# --------------------------------------------------

@st.cache_data
def load_data():
    df = pd.read_csv(
        "data/Sample - Superstore.csv",
        encoding="latin-1"
    )

    df["Order Date"] = pd.to_datetime(df["Order Date"])
    df["Ship Date"] = pd.to_datetime(df["Ship Date"])

    return df


data = load_data()


# --------------------------------------------------
# TITLE
# --------------------------------------------------

st.title("📊 Superstore Business Analytics Dashboard")
st.markdown(
    "Interactive analysis of sales, profit, products and customer segments."
)


# --------------------------------------------------
# SIDEBAR FILTERS
# --------------------------------------------------

st.sidebar.header("🔎 Filters")

category = st.sidebar.multiselect(
    "Category",
    options=sorted(data["Category"].unique()),
    default=sorted(data["Category"].unique())
)

segment = st.sidebar.multiselect(
    "Customer Segment",
    options=sorted(data["Segment"].unique()),
    default=sorted(data["Segment"].unique())
)

region = st.sidebar.multiselect(
    "Region",
    options=sorted(data["Region"].unique()),
    default=sorted(data["Region"].unique())
)


# --------------------------------------------------
# FILTER DATA
# --------------------------------------------------

filtered_data = data[
    (data["Category"].isin(category)) &
    (data["Segment"].isin(segment)) &
    (data["Region"].isin(region))
]


# --------------------------------------------------
# KPI CALCULATIONS
# --------------------------------------------------

total_sales = filtered_data["Sales"].sum()
total_profit = filtered_data["Profit"].sum()
total_orders = filtered_data["Order ID"].nunique()
total_customers = filtered_data["Customer ID"].nunique()


# --------------------------------------------------
# KPI CARDS
# --------------------------------------------------

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "💰 Total Sales",
    f"${total_sales:,.0f}"
)

col2.metric(
    "📈 Total Profit",
    f"${total_profit:,.0f}"
)

col3.metric(
    "🛒 Total Orders",
    f"{total_orders:,}"
)

col4.metric(
    "👥 Customers",
    f"{total_customers:,}"
)


st.divider()


# --------------------------------------------------
# MONTHLY SALES & PROFIT
# --------------------------------------------------

monthly = (
    filtered_data
    .groupby(filtered_data["Order Date"].dt.month)
    .agg(
        Sales=("Sales", "sum"),
        Profit=("Profit", "sum")
    )
    .reset_index()
)

monthly.rename(
    columns={"Order Date": "Month"},
    inplace=True
)


col1, col2 = st.columns(2)


with col1:

    fig_sales = px.line(
        monthly,
        x="Month",
        y="Sales",
        markers=True,
        title="Monthly Sales Analysis"
    )

    fig_sales.update_layout(
        xaxis_title="Month",
        yaxis_title="Sales"
    )

    st.plotly_chart(
        fig_sales,
        use_container_width=True
    )


with col2:

    fig_profit = px.line(
        monthly,
        x="Month",
        y="Profit",
        markers=True,
        title="Monthly Profit Analysis"
    )

    fig_profit.update_layout(
        xaxis_title="Month",
        yaxis_title="Profit"
    )

    st.plotly_chart(
        fig_profit,
        use_container_width=True
    )


# --------------------------------------------------
# CATEGORY ANALYSIS
# --------------------------------------------------

sales_category = (
    filtered_data
    .groupby("Category")["Sales"]
    .sum()
    .reset_index()
)

profit_category = (
    filtered_data
    .groupby("Category")["Profit"]
    .sum()
    .reset_index()
)


col1, col2 = st.columns(2)


with col1:

    fig_category_sales = px.pie(
        sales_category,
        values="Sales",
        names="Category",
        hole=0.4,
        title="Sales Analysis by Category"
    )

    st.plotly_chart(
        fig_category_sales,
        use_container_width=True
    )


with col2:

    fig_category_profit = px.pie(
        profit_category,
        values="Profit",
        names="Category",
        hole=0.4,
        title="Profit Analysis by Category"
    )

    st.plotly_chart(
        fig_category_profit,
        use_container_width=True
    )


# --------------------------------------------------
# SUB-CATEGORY ANALYSIS
# --------------------------------------------------

sales_subcategory = (
    filtered_data
    .groupby("Sub-Category")["Sales"]
    .sum()
    .reset_index()
    .sort_values("Sales", ascending=False)
)

profit_subcategory = (
    filtered_data
    .groupby("Sub-Category")["Profit"]
    .sum()
    .reset_index()
    .sort_values("Profit", ascending=False)
)


col1, col2 = st.columns(2)


with col1:

    fig_sub_sales = px.bar(
        sales_subcategory,
        x="Sub-Category",
        y="Sales",
        title="Sales by Sub-Category"
    )

    st.plotly_chart(
        fig_sub_sales,
        use_container_width=True
    )


with col2:

    fig_sub_profit = px.bar(
        profit_subcategory,
        x="Sub-Category",
        y="Profit",
        title="Profit by Sub-Category"
    )

    st.plotly_chart(
        fig_sub_profit,
        use_container_width=True
    )


# --------------------------------------------------
# CUSTOMER SEGMENT ANALYSIS
# --------------------------------------------------

segment_analysis = (
    filtered_data
    .groupby("Segment")
    .agg(
        Sales=("Sales", "sum"),
        Profit=("Profit", "sum")
    )
    .reset_index()
)


fig_segment = go.Figure()

fig_segment.add_trace(
    go.Bar(
        x=segment_analysis["Segment"],
        y=segment_analysis["Sales"],
        name="Sales"
    )
)

fig_segment.add_trace(
    go.Bar(
        x=segment_analysis["Segment"],
        y=segment_analysis["Profit"],
        name="Profit"
    )
)

fig_segment.update_layout(
    title="Sales and Profit by Customer Segment",
    xaxis_title="Customer Segment",
    yaxis_title="Amount",
    barmode="group"
)

st.plotly_chart(
    fig_segment,
    use_container_width=True
)


# --------------------------------------------------
# DATA TABLE
# --------------------------------------------------

with st.expander("📋 View Filtered Data"):

    st.dataframe(
        filtered_data,
        use_container_width=True
    )