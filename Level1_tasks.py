import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Cognifyz - Level 1", layout="wide")
st.title("🍽️ Cognifyz Data Analysis — Level 1")

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

# ---------- Task 1: Top Cuisines ----------
st.header("Task 1: Top Cuisines")
df_c = df.dropna(subset=['Cuisines'])
cuisines = df_c['Cuisines'].str.split(', ').explode()
top3 = cuisines.value_counts().head(3)
total = len(df_c)

cols = st.columns(3)
for col, (c, n) in zip(cols, top3.items()):
    col.metric(label=c, value=f"{n} restaurants", delta=f"{n/total*100:.2f}%")

st.markdown("---")

# ---------- Task 2: City Analysis ----------
st.header("Task 2: City Analysis")
city_counts = df['City'].value_counts()
city_avg = df.groupby('City')['Aggregate rating'].mean().sort_values(ascending=False)

c1, c2 = st.columns(2)
c1.metric("City with most restaurants", city_counts.idxmax(), f"{city_counts.max()} restaurants")
c2.metric("City with highest avg rating", city_avg.idxmax(), f"{round(city_avg.iloc[0], 2)} ⭐")

top10_cities = city_counts.head(10)
fig2, ax2 = plt.subplots(figsize=(6, 3))
ax2.barh(top10_cities.index[::-1], top10_cities.values[::-1], color='#55A868')
ax2.set_xlabel('Number of Restaurants', fontsize=9)
ax2.set_title('Top 10 Cities by Restaurant Count', fontsize=10)
ax2.tick_params(labelsize=8)
ax2.spines['top'].set_visible(False)
ax2.spines['right'].set_visible(False)
st.pyplot(fig2, use_container_width=False)

st.markdown("---")

# ---------- Task 3: Price Range Distribution ----------
st.header("Task 3: Price Range Distribution")
counts = df['Price range'].value_counts().sort_index()
pct = (counts / len(df) * 100).round(2)

left, right = st.columns([1, 1])
with left:
    fig, ax = plt.subplots(figsize=(4, 3))
    bars = ax.bar(counts.index.astype(str), counts.values, color='#4C72B0', width=0.6)
    ax.set_xlabel('Price Range', fontsize=9)
    ax.set_ylabel('Restaurants', fontsize=9)
    ax.set_title('Price Range Distribution', fontsize=10)
    ax.tick_params(labelsize=8)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    for bar in bars:
        h = bar.get_height()
        ax.annotate(f'{h}', xy=(bar.get_x() + bar.get_width()/2, h),
                    xytext=(0, 3), textcoords="offset points", ha='center', fontsize=8)
    st.pyplot(fig, use_container_width=False)

with right:
    st.dataframe(
        pd.DataFrame({'Price Range': counts.index, 'Count': counts.values, 'Percentage (%)': pct.values}),
        hide_index=True, use_container_width=True
    )

st.markdown("---")

# ---------- Task 4: Online Delivery ----------
st.header("Task 4: Online Delivery")
delivery_pct = (df['Has Online delivery'].value_counts(normalize=True) * 100).round(2)
avg_rating_delivery = df.groupby('Has Online delivery')['Aggregate rating'].mean().round(2)

d1, d2 = st.columns(2)
d1.metric("Restaurants offering delivery", f"{delivery_pct.get('Yes', 0)}%")
d2.metric("Restaurants without delivery", f"{delivery_pct.get('No', 0)}%")

r1, r2 = st.columns(2)
r1.metric("Avg rating (with delivery)", avg_rating_delivery.get('Yes', 0))
r2.metric("Avg rating (without delivery)", avg_rating_delivery.get('No', 0))

left2, right2 = st.columns(2)
with left2:
    fig3, ax3 = plt.subplots(figsize=(4, 3))
    ax3.pie(delivery_pct.values, labels=delivery_pct.index, autopct='%1.1f%%',
            colors=['#C44E52', '#4C72B0'], startangle=90, textprops={'fontsize': 9})
    ax3.set_title('Online Delivery Availability', fontsize=10)
    st.pyplot(fig3, use_container_width=False)

with right2:
    fig4, ax4 = plt.subplots(figsize=(4, 3))
    ax4.bar(avg_rating_delivery.index, avg_rating_delivery.values, color=['#C44E52', '#4C72B0'], width=0.5)
    ax4.set_ylabel('Avg Rating', fontsize=9)
    ax4.set_title('Rating: Delivery vs No Delivery', fontsize=10)
    ax4.tick_params(labelsize=8)
    ax4.spines['top'].set_visible(False)
    ax4.spines['right'].set_visible(False)
    st.pyplot(fig4, use_container_width=False)