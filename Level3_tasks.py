import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Cognifyz - Level 3", layout="wide")
st.title("🍽️ Cognifyz Data Analysis — Level 3")

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

# ---------- Task 1: Restaurant Reviews ----------
st.header("Task 1: Restaurant Reviews")
st.warning(
    "⚠️ This dataset does not contain a review-text column, so keyword analysis and "
    "review-length vs. rating comparison cannot be performed. If you have a separate "
    "reviews file with text, load it here to complete this task."
)

st.markdown("---")

# ---------- Task 2: Votes Analysis ----------
st.header("Task 2: Votes Analysis")

highest_votes = df.loc[df['Votes'].idxmax()]
lowest_votes = df.loc[df['Votes'].idxmin()]
correlation = df['Votes'].corr(df['Aggregate rating'])

c1, c2, c3 = st.columns(3)
c1.metric("Highest votes", highest_votes['Restaurant Name'], f"{int(highest_votes['Votes'])} votes")
c2.metric("Lowest votes", lowest_votes['Restaurant Name'], f"{int(lowest_votes['Votes'])} votes")
c3.metric("Votes–Rating correlation", f"{correlation:.2f}")

fig1, ax1 = plt.subplots(figsize=(7, 4.5))
ax1.scatter(df['Votes'], df['Aggregate rating'], alpha=0.3, color='#4C72B0', s=15)
ax1.set_xlabel('Votes', fontsize=12)
ax1.set_ylabel('Aggregate Rating', fontsize=12)
ax1.set_title('Votes vs. Rating', fontsize=13)
ax1.tick_params(labelsize=11)
ax1.spines['top'].set_visible(False)
ax1.spines['right'].set_visible(False)
st.pyplot(fig1, use_container_width=False)
st.caption(f"Correlation coefficient of {correlation:.2f} indicates a "
           f"{'weak' if abs(correlation) < 0.3 else 'moderate' if abs(correlation) < 0.7 else 'strong'} "
           f"{'positive' if correlation > 0 else 'negative'} relationship between votes and rating.")

st.markdown("---")

# ---------- Task 3: Price Range vs. Online Delivery and Table Booking ----------
st.header("Task 3: Price Range vs. Online Delivery and Table Booking")

delivery_by_price = df.groupby('Price range')['Has Online delivery'].apply(
    lambda x: (x == 'Yes').mean() * 100).round(2)
booking_by_price = df.groupby('Price range')['Has Table booking'].apply(
    lambda x: (x == 'Yes').mean() * 100).round(2)

left, right = st.columns(2)
with left:
    fig2, ax2 = plt.subplots(figsize=(6, 4.5))
    ax2.bar(delivery_by_price.index.astype(str), delivery_by_price.values, color='#55A868', width=0.5)
    ax2.set_xlabel('Price Range', fontsize=12)
    ax2.set_ylabel('% Offering Online Delivery', fontsize=12)
    ax2.set_title('Online Delivery by Price Range', fontsize=13)
    ax2.tick_params(labelsize=11)
    ax2.spines['top'].set_visible(False)
    ax2.spines['right'].set_visible(False)
    st.pyplot(fig2, use_container_width=False)

with right:
    fig3, ax3 = plt.subplots(figsize=(6, 4.5))
    ax3.bar(booking_by_price.index.astype(str), booking_by_price.values, color='#C44E52', width=0.5)
    ax3.set_xlabel('Price Range', fontsize=12)
    ax3.set_ylabel('% Offering Table Booking', fontsize=12)
    ax3.set_title('Table Booking by Price Range', fontsize=13)
    ax3.tick_params(labelsize=11)
    ax3.spines['top'].set_visible(False)
    ax3.spines['right'].set_visible(False)
    st.pyplot(fig3, use_container_width=False)

st.dataframe(
    pd.DataFrame({
        'Price Range': delivery_by_price.index,
        '% Online Delivery': delivery_by_price.values,
        '% Table Booking': booking_by_price.values
    }),
    hide_index=True, use_container_width=True
)

higher_price_more_services = booking_by_price.iloc[-1] > booking_by_price.iloc[0]
st.info(
    f"Higher-priced restaurants are "
    f"{'more' if higher_price_more_services else 'less'} likely to offer table booking "
    f"(Price range 4: {booking_by_price.iloc[-1]}% vs Price range 1: {booking_by_price.iloc[0]}%)."
)