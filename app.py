# cereal — mini assignment 1
# load a csv, filter it, reset filters, two charts

import streamlit as st
import pandas as pd
import altair as alt
import plotly.express as px

st.set_page_config(page_title="Cereal Explorer", layout="wide")
st.title("Cereal nutrition explorer")
st.caption("80 cereals. I wanted to see which ones are high sugar vs high rating.")




# LOAD 
# panda turns csv into a table called "df"
# the csv has to be in the same folder as this file (double check)
df = pd.read_csv("cereal.csv")


# PEEK 
# just checking if it loaded before I filter anything
with st.expander("peek at the data"):
    st.write("rows:", df.shape[0], "cols:", df.shape[1])
    st.write("columns:", ", ".join(list(df.columns)))
    st.write("first 5 rows only")
    st.dataframe(df.head())

st.divider()


# SESSION STATE 
# these keys remember the widgets after a rerun
# reset uses them so the dropdown/slider/search actually go back
if "brand_choice" not in st.session_state:
    st.session_state.brand_choice = "All brands"
if "max_sugars" not in st.session_state:
    st.session_state.max_sugars = int(df["sugars"].max())
if "search_text" not in st.session_state:
    st.session_state.search_text = ""

if st.button("Reset filters"):
    st.session_state.brand_choice = "All brands"
    st.session_state.max_sugars = int(df["sugars"].max())
    st.session_state.search_text = ""
    st.rerun()


# FILTERS 
# dropdown + slider. options come from the csv so I dont type brands myself
st.subheader("Filter the cereals")

col1, col2 = st.columns(2)

with col1:
    brands = df["mfr"].unique().tolist()
    brands = sorted(brands)
    brand_options = ["All brands"] + brands
    st.selectbox("Filter by manufacturer", brand_options, key="brand_choice")

with col2:
    low_sugar = int(df["sugars"].min())
    high_sugar = int(df["sugars"].max())
    st.slider("Max sugars", low_sugar, high_sugar, key="max_sugars")


# SEARCH 
# type part of a name. case=False so Bran and bran both work
st.text_input("Search by cereal name", placeholder="e.g. bran", key="search_text")


# APPLY FILTERS 
# start from the full table and keep cutting rows
# each check is True/False for every row, then we keep the True ones
ok_sugar = df["sugars"] <= st.session_state.max_sugars
filtered = df[ok_sugar]

if st.session_state.brand_choice != "All brands":
    same_brand = filtered["mfr"] == st.session_state.brand_choice
    filtered = filtered[same_brand]

if st.session_state.search_text:
    name_hit = filtered["name"].str.contains(st.session_state.search_text, case=False, na=False)
    filtered = filtered[name_hit]


# SORT 
# starting order. you can still click a column header after
s1, s2 = st.columns(2)
with s1:
    sort_by = st.selectbox("Sort by", ["rating", "sugars", "calories", "name"])
with s2:
    ascending = st.checkbox("Ascending order", value=False)

filtered = filtered.sort_values(by=sort_by, ascending=ascending)


# METRICS 
# these use filtered so they change when the widgets change
st.divider()
m1, m2 = st.columns(2)
m1.metric("Cereals shown", len(filtered))

if len(filtered) > 0:
    avg_rating = round(filtered["rating"].mean(), 1)
else:
    avg_rating = 0
m2.metric("Average rating (shown)", avg_rating)


# CHARTS 
# both use filtered, not df
# altair bar = average rating per brand (grouped)
# plotly scatter = one cereal per dot

st.subheader("Charts")
c1, c2 = st.columns(2)

with c1:
    st.write("Average rating by manufacturer")
    if len(filtered) > 0:
        by_brand = filtered.groupby("mfr", as_index=False)["rating"].mean()
        bar = (
            alt.Chart(by_brand)
            .mark_bar()
            .encode(
                x=alt.X("mfr", title="Manufacturer"),
                y=alt.Y("rating", title="Average rating"),
                color=alt.Color("mfr", legend=None),
            )
            .properties(title="Average rating by manufacturer")
        )
        st.altair_chart(bar, use_container_width=True)
    else:
        st.write("no rows to chart")

with c2:
    st.write("Sugars vs rating")
    if len(filtered) > 0:
        scatter = px.scatter(
            filtered,
            x="sugars",
            y="rating",
            hover_name="name",
            title="Sugars vs rating",
        )
        st.plotly_chart(scatter, use_container_width=True)
    else:
        st.write("no rows to chart")

        
# TABLE 
# show filtered, not df


st.dataframe(filtered, hide_index=True, use_container_width=True)

