import streamlit as st
import pandas as pd
import plotly.express as px


st.set_page_config(layout="wide")


df = pd.read_csv("crime_cleaned.csv")


df["Victim Gender"] = df["Victim Gender"].replace({
    "M": "Male",
    "F": "Female",
    "X": "Unknown"
})



st.sidebar.title("Indian Crime Analytics (2020-2024)")


# City
cities = sorted(df["City"].dropna().unique())
cities.insert(0, "Entire India")

selected_city = st.sidebar.selectbox(
    "Select City",
    cities
)


# Crime
crimes = sorted(df["Crime Description"].dropna().unique())
crimes.insert(0, "All Crimes")

selected_crime = st.sidebar.selectbox(
    "Select Crime",
    crimes
)


# Gender
genders = ["Both", "Male", "Female", "Unknown"]

selected_gender = st.sidebar.selectbox(
    "Select Gender",
    genders
)



filtered_df = df.copy()

if selected_city != "Entire India":
    filtered_df = filtered_df[
        filtered_df["City"] == selected_city
    ]

if selected_crime != "All Crimes":
    filtered_df = filtered_df[
        filtered_df["Crime Description"] == selected_crime
    ]

if selected_gender != "Both":
    filtered_df = filtered_df[
        filtered_df["Victim Gender"] == selected_gender
    ]



map_data = (
    filtered_df
    .groupby("City")
    .agg(
        Crime_Count=("City", "size"),
        Latitude=("Latitude", "first"),
        Longitude=("Longitude", "first")
    )
    .reset_index()
)



fig = px.scatter_geo(
    map_data,
    lat="Latitude",
    lon="Longitude",

    # Bubble size
    size="Crime_Count",

    # Bubble color
    color="Crime_Count",

    # Hover
    hover_name="City",
    hover_data={
        "Crime_Count": True,
        "Latitude": False,
        "Longitude": False
    },

    # Color theme
    color_continuous_scale="Plasma",

    # Map projection
    projection="mercator",
    scope="asia"
)



fig.update_geos(

    # Center India
    center={
        "lat": 22.5,
        "lon": 79
    },

    # Tighter view of India
    lataxis_range=[6, 37],
    lonaxis_range=[67, 99],

    # Land
    showland=True,
    landcolor="#FAF6F6",

    # Ocean
    showocean=True,
    oceancolor="#403F41",

    # Country borders
    showcountries=True,
    countrycolor="#000000",
    countrywidth=1
)



fig.update_coloraxes(
    colorbar=dict(
        title="Crime Count",

        orientation="v",

        # Right side
        x=1.02,
        xanchor="left",

        # Center vertically
        y=0.5,
        yanchor="middle",

        # Height and thickness
        len=0.7,
        thickness=18
    )
)



fig.update_layout(

    width=1400,
    height=680,

    margin=dict(
        l=0,
        r=90,
        t=0,
        b=10
    )
)

st.plotly_chart(
    fig,
    use_container_width=True
)