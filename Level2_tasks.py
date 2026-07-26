import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Cognifyz - Level 2", layout="wide")
st.title("🍽️ Cognifyz Data Analysis — Level 2")

st.markdown("""
    <style>
    .main { background-color: #F7F9FC; }
    div[data-testid="stMetric"] {
        background-color: #FFFFFF;
        border: 1px solid #E6E9EF;
        border-radius: 10px;
        padding: 15px 10px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.06);
    }
    div[data-testid="stMetricLabel"] { font-size: 14px; color: #5A6474; }
    div[data-testid="stMetricValue"] { font-size: 22px; color: #1F2A44; }
    h1 {
        background: linear-gradient(90deg, #4C72B0, #55A868);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 800;
    }
    h2 {
        color: #1F2A44;
        border-left: 5px solid #4C72B0;
        padding-left: 10px;
        margin-top: 25px;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown("---")

df = pd.read_csv('Dataset .csv')  # match your actual filename

# ---------- Task 1: Restaurant Ratings ----------
st.header("Task 1: Restaurant Ratings")

bins = [-0.1, 1, 2, 3, 4, 5]
labels = ['0-1', '1-2', '2-3', '3-4', '4-5']
df['rating_bin'] = pd.cut(df['Aggregate rating'], bins=bins, labels=labels)
rating_dist = df['rating_bin'].value_counts().sort_index()
most_common_range = rating_dist.idxmax()
avg_votes = df['Votes'].mean()

c1, c2 = st.columns(2)
c1.metric("Most common rating range", most_common_range)
c2.metric("Average votes per restaurant", f"{avg_votes:.2f}")

fig1, ax1 = plt.subplots(figsize=(7, 4.5))
ax1.bar(rating_dist.index.astype(str), rating_dist.values, color='#4C72B0', width=0.6)
ax1.set_xlabel('Rating Range', fontsize=12)
ax1.set_ylabel('Number of Restaurants', fontsize=12)
ax1.set_title('Distribution of Aggregate Ratings', fontsize=13)
ax1.tick_params(labelsize=11)
ax1.spines['top'].set_visible(False)
ax1.spines['right'].set_visible(False)
st.pyplot(fig1, use_container_width=False)

st.markdown("---")

# ---------- Task 2: Cuisine Combination ----------
st.header("Task 2: Cuisine Combination")

df_c = df.dropna(subset=['Cuisines'])
combo_counts = df_c['Cuisines'].value_counts().head(10)
combo_ratings = df_c.groupby('Cuisines')['Aggregate rating'].mean()
top_combo_ratings = combo_ratings.loc[combo_counts.index].round(2)

left, right = st.columns(2)
with left:
    fig2, ax2 = plt.subplots(figsize=(7, 5))
    ax2.barh(combo_counts.index[::-1], combo_counts.values[::-1], color='#55A868')
    ax2.set_xlabel('Number of Restaurants', fontsize=12)
    ax2.set_title('Top 10 Cuisine Combinations', fontsize=13)
    ax2.tick_params(labelsize=11)
    ax2.spines['top'].set_visible(False)
    ax2.spines['right'].set_visible(False)
    st.pyplot(fig2, use_container_width=False)

with right:
    st.dataframe(
        pd.DataFrame({
            'Cuisine Combination': combo_counts.index,
            'Restaurant Count': combo_counts.values,
            'Avg Rating': top_combo_ratings.values
        }),
        hide_index=True, use_container_width=True
    )

st.markdown("---")

# ---------- Task 3: Geographic Analysis ----------
st.header("Task 3: Geographic Analysis")

geo_df = df.dropna(subset=['Latitude', 'Longitude'])
geo_df = geo_df[(geo_df['Latitude'] != 0) & (geo_df['Longitude'] != 0)]
st.map(geo_df.rename(columns={'Latitude': 'lat', 'Longitude': 'lon'})[['lat', 'lon']])
st.caption("Each point represents a restaurant location. Clusters indicate high-density restaurant areas.")

st.markdown("---")

# ---------- Task 4: Restaurant Chains ----------
st.header("Task 4: Restaurant Chains")

chain_counts = df['Restaurant Name'].value_counts()
chains = chain_counts[chain_counts > 1]
top_chains = chains.head(10)
chain_ratings = df[df['Restaurant Name'].isin(top_chains.index)].groupby('Restaurant Name')['Aggregate rating'].mean().round(2)

c3, c4 = st.columns(2)
c3.metric("Total restaurant chains found", len(chains))
c4.metric("Largest chain", f"{top_chains.idxmax()} ({top_chains.max()} outlets)")

left2, right2 = st.columns(2)
with left2:
    fig3, ax3 = plt.subplots(figsize=(7, 5))
    ax3.barh(top_chains.index[::-1], top_chains.values[::-1], color='#C44E52')
    ax3.set_xlabel('Number of Outlets', fontsize=12)
    ax3.set_title('Top 10 Restaurant Chains', fontsize=13)
    ax3.tick_params(labelsize=11)
    ax3.spines['top'].set_visible(False)
    ax3.spines['right'].set_visible(False)
    st.pyplot(fig3, use_container_width=False)

with right2:
    st.dataframe(
        pd.DataFrame({
            'Chain': top_chains.index,
            'Outlets': top_chains.values,
            'Avg Rating': [chain_ratings[c] for c in top_chains.index]
        }),
        hide_index=True, use_container_width=True
    )