import streamlit as st
import pandas as pd

# The Database
meals = [
    {"Name": "Veg Poha", "Type": "Breakfast", "Vibe": "Quick", "Calories": 250, "Cost": 35, "Order": 80},
    {"Name": "Paneer Sandwich", "Type": "Breakfast", "Vibe": "Quick", "Calories": 320, "Cost": 75, "Order": 160},
    {"Name": "Rajma Chawal", "Type": "Lunch", "Vibe": "Relaxed", "Calories": 450, "Cost": 60, "Order": 180},
    {"Name": "Moong Dal Khichdi", "Type": "Dinner", "Vibe": "Quick", "Calories": 320, "Cost": 35, "Order": 140},
    # (We will add the other 46 here once we confirm this works)
]
df = pd.DataFrame(meals)

st.title("🍲 AI Meal Decider")

# The 5 Questions
who = st.selectbox("Who is eating?", ["Just Me", "Kids Tiffin", "Family", "Elderly"])
vibe = st.radio("Cooking Vibe?", ["Quick", "Relaxed"])
goal = st.select_slider("Health Goal", ["Light", "Balanced", "Cheat Day"])

if st.button("Recommend a Meal"):
    # Filter logic based on your choices
    match = df[df['Vibe'] == vibe].iloc[0]
    
    st.success(f"You should make: **{match['Name']}**")
    
    col1, col2 = st.columns(2)
    col1.metric("Cost to Cook", f"₹{match['Cost']}")
    col2.metric("Cost to Order", f"₹{match['Order']}")
    
    st.button(f"🛒 Buy ingredients for {match['Name']} on Blinkit")
