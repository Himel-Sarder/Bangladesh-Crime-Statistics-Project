import streamlit as st
import pandas as pd
import plotly.express as px

# Load data
df = pd.read_csv("BDCrimes.csv")

df.columns = df.columns.str.strip()


st.markdown(
    """
    <h1 style="text-align: center; color: #e63946; font-size: 3em; font-family: 'Segoe UI', sans-serif; margin-bottom: 0.2em;">
        Bangladesh Crime Statistics Dashboard (2010 - 2019)
    </h1>
    <hr style="border: 1px solid #ccc; margin-bottom: 2em;">
    """,
    unsafe_allow_html=True
)


# Sidebar filters
year = st.sidebar.selectbox("Select Year", sorted(df["Year"].unique()))
selected_areas = st.sidebar.multiselect("Select Area(s)", df["Area"].unique(), default=df["Area"].unique())
color_by = st.sidebar.selectbox("Crime Type", [
    "Dacoity", "Robbery", "Murder", "Speedy Trial", "Riot",
    "Women & Child Repression", "Kidnapping", "Police Assault",
    "Burglary", "Theft", "Other Cases"
])

# Filter dataframe
filtered_df = df[(df["Year"] == year) & (df["Area"].isin(selected_areas))]

# Add total crimes column
filtered_df["Total Crimes"] = filtered_df[[
    "Dacoity", "Robbery", "Murder", "Speedy Trial", "Riot",
    "Women & Child Repression", "Kidnapping", "Police Assault",
    "Burglary", "Theft", "Other Cases"
]].sum(axis=1)

# Show data table
st.subheader(f"Crime Data for {year}")
st.dataframe(filtered_df.drop(columns=["Year", "lat", "lon"]))


color_scale = [
    [0, 'green'],     # low value → green
    [0.5, 'yellow'],  # mid value → yellow
    [1, 'red']        # high value → red
]

# Subheader before the map
st.subheader(f"{color_by} across Selected Areas in {year}")

# Scatter map with size and color
fig = px.scatter_mapbox(
    filtered_df,
    lat="lat",
    lon="lon",
    hover_name="Area",
    hover_data=["Total Crimes", color_by],
    color=color_by,
    color_continuous_scale=color_scale,
    size="Total Crimes",
    size_max=30,
    zoom=5,
    mapbox_style="carto-positron",
    # title=f"{color_by} across Selected Areas in {year}"
)

st.plotly_chart(fig)

# Pie chart of selected crime contribution
st.subheader(f"{color_by} Contribution by Area")
pie_fig = px.pie(
    filtered_df,
    names="Area",
    values=color_by,
    title=f"Distribution of {color_by} in {year}",
    color_discrete_sequence=px.colors.sequential.Reds
)
st.plotly_chart(pie_fig)

# Heatmap
st.subheader("Crime Type Distribution by Area")
heatmap_fig = px.imshow(
    filtered_df.set_index("Area")[[
        "Dacoity", "Robbery", "Murder", "Speedy Trial", "Riot",
        "Women & Child Repression", "Kidnapping", "Police Assault",
        "Burglary", "Theft", "Other Cases"
    ]],
    labels=dict(color="Crime Count"),
    color_continuous_scale=color_scale
)
st.plotly_chart(heatmap_fig)


# Bar Chart: Total Crimes by Area
st.subheader("Total Crimes by Area")
bar_fig = px.bar(
    filtered_df,
    x="Area",
    y="Total Crimes",
    color="Total Crimes",
    color_continuous_scale=color_scale,
    labels={"Total Crimes": "Total Crimes"}
)
st.plotly_chart(bar_fig)

# Stacked Bar Chart of Crime Types per Area
st.subheader("Crime Type Breakdown by Area")
crime_breakdown_fig = px.bar(
    filtered_df.melt(id_vars=["Area"], value_vars=[
        "Dacoity", "Robbery", "Murder", "Speedy Trial", "Riot",
        "Women & Child Repression", "Kidnapping", "Police Assault",
        "Burglary", "Theft", "Other Cases"
    ]),
    x="Area",
    y="value",
    color="variable",
    labels={"value": "Crime Count", "variable": "Crime Type"}
)
st.plotly_chart(crime_breakdown_fig)

# Treemap of Crime Composition
st.subheader("Treemap of Crime Composition by Area")
treemap_df = filtered_df.melt(id_vars=["Area"], value_vars=[
    "Dacoity", "Robbery", "Murder", "Speedy Trial", "Riot",
    "Women & Child Repression", "Kidnapping", "Police Assault",
    "Burglary", "Theft", "Other Cases"
], var_name="Crime Type", value_name="Count")

treemap_fig = px.treemap(
    treemap_df,
    path=["Area", "Crime Type"],
    values="Count",
)
st.plotly_chart(treemap_fig)

# Box Plot for selected crime type
st.subheader(f"Distribution of {color_by} Across Areas")
box_fig = px.box(
    filtered_df,
    y=color_by,
    points="all",
    labels={color_by: f"{color_by} Cases"}
)
st.plotly_chart(box_fig)

st.subheader(f"{color_by} Trend Over the Years")
crime_trend_df = df[df["Area"].isin(selected_areas)]
trend_fig = px.line(
    crime_trend_df,
    x="Year",
    y=color_by,
    color="Area",
    markers=True,
)
st.plotly_chart(trend_fig)

st.subheader(f"Distribution of {color_by} Across Areas")
violin_fig = px.violin(
    filtered_df,
    y=color_by,
    x="Area",
    box=True,
    points="all",
)
st.plotly_chart(violin_fig)


st.markdown(
    """
    <hr style="margin-top: 50px;"/>
    <div style="text-align: center; padding: 10px;">
        <small>
            Developed by <a href="https://www.linkedin.com/in/himel-sarder/" target="_blank">Himel Sarder</a> • Data Visualization with <a href="https://plotly.com/python/" target="_blank">Plotly</a> & <a href="https://streamlit.io" target="_blank">Streamlit</a> <br/>
        </small>
    </div>
    """,
    unsafe_allow_html=True
)
