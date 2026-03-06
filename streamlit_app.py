import streamlit as st
import pandas as pd
import random

# --- EXPANDED DATABASE ---
meals_data = [
    {"name": "Veg Poha", "type": "Breakfast", "vibe": "Quick", "cal": 250, "cook_time": 15, "order_time": 25, "cost": 35, "order": 90, "tags": "light, healthy, poha, rice", "veg": True},
    {"name": "Paneer Sandwich", "type": "Breakfast", "vibe": "Quick", "cal": 320, "cook_time": 10, "order_time": 30, "cost": 85, "order": 180, "tags": "protein, paneer, sandwich", "veg": True},
    {"name": "Rajma Chawal", "type": "Lunch", "vibe": "Relaxed", "cal": 450, "cook_time": 45, "order_time": 40, "cost": 65, "order": 220, "tags": "protein, beans, rice, family", "veg": True},
    {"name": "Dal Tadka + Rice", "type": "Lunch", "vibe": "Quick", "cal": 410, "cook_time": 25, "order_time": 30, "cost": 50, "order": 180, "tags": "light, comfort, dal, rice", "veg": True},
    {"name": "Egg Curry", "type": "Dinner", "vibe": "Quick", "cal": 380, "cook_time": 25, "order_time": 35, "cost": 55, "order": 190, "tags": "protein, eggs, spicy", "veg": False},
    {"name": "Moong Dal Khichdi", "type": "Dinner", "vibe": "Quick", "cal": 320, "cook_time": 25, "order_time": 35, "cost": 35, "order": 160, "tags": "light, comfort, dal", "veg": True},
    {"name": "Chicken Curry", "type": "Lunch", "vibe": "Relaxed", "cal": 520, "cook_time": 50, "order_time": 45, "cost": 160, "order": 350, "tags": "protein, chicken, spicy", "veg": False}
]
df = pd.DataFrame(meals_data)

st.set_page_config(page_title="MealBrain AI", layout="wide")

# --- SESSION STATE FOR "SUGGEST ANOTHER" ---
if 'meal_index' not in st.session_state:
    st.session_state.meal_index = 0

# --- SIDEBAR INPUTS ---
with st.sidebar:
    st.title("⚙️ Parameters")
    headcount = st.number_input("Headcount (People)", min_value=1, max_value=20, value=1)
    diet = st.radio("Diet Preference", ["Veg Only", "Everything"])
    goal = st.select_slider("Health Goal", ["Light", "Balanced", "Cheat Day"])
    vibe = st.radio("Vibe", ["Quick", "Relaxed"])

st.title("🍲 MealBrain AI")
user_input = st.text_input("Craving something? (e.g. 'Paneer', 'Spicy')", placeholder="Search...")

# --- FILTERING LOGIC ---
filtered_df = df.copy()
if diet == "Veg Only":
    filtered_df = filtered_df[filtered_df['veg'] == True]
if goal == "Light":
    filtered_df = filtered_df[filtered_df['cal'] < 300]
elif goal == "Balanced":
    filtered_df = filtered_df[(filtered_df['cal'] >= 300) & (filtered_df['cal'] <= 450)]

if user_input:
    filtered_df = filtered_df[filtered_df.apply(lambda x: user_input.lower() in x['name'].lower() or user_input.lower() in x['tags'], axis=1)]

# --- EXECUTION ---
col_btns = st.columns([1, 1, 4])
generate = col_btns[0].button("🚀 Get Meal")
suggest_next = col_btns[1].button("🔄 Suggest Another")

if generate or suggest_next:
    if not filtered_df.empty:
        # Pick a random meal from the filtered list for variety
        winner = filtered_df.sample(n=1).iloc[0]
        
        # Scaling Calculations
        total_cook_cost = winner['cost'] * headcount
        total_order_cost = winner['order'] * headcount
        total_cal = winner['cal'] * headcount
        
        st.markdown(f"## Recommendation: {winner['name']}")
        
        # Visual Component
        st.image(f"https://loremflickr.com/800/400/indian,food,{winner['name'].replace(' ', ',')}", 
                 caption=f"Typical {winner['name']} serving", use_container_width=True)

        # --- OPTION A: COOK AT HOME ---
        st.subheader("🏠 Option A: Cook at Home")
        a1, a2, a3, a4 = st.columns(4)
        a1.metric("Time", f"{winner['cook_time']} min")
        a2.metric("Total Cost", f"₹{total_cook_cost}")
        a3.metric("Calories", f"{total_cal} kcal")
        blinkit_url = f"https://www.google.com/search?q=buy+{winner['name'].replace(' ', '+')}+ingredients+on+Blinkit"
        a4.markdown(f"[🛒 Shop Ingredients (Blinkit)]({blinkit_url})")

        st.divider()

        # --- OPTION B: ORDER ONLINE ---
        st.subheader("🛵 Option B: Order Online")
        b1, b2, b3, b4 = st.columns(4)
        b1.metric("Delivery", f"{winner['order_time']} min")
        b2.metric("Total Cost", f"₹{total_order_cost}")
        b3.metric("Calories", f"{total_cal} kcal")
        zomato_url = f"https://www.google.com/search?q=order+{winner['name'].replace(' ', '+')}+from+Zomato"
        b4.markdown(f"[🥡 Order Now (Zomato)]({zomato_url})")

    else:
        st.error("No matches found for these filters. Try relaxing your constraints!")

st.caption("Version 1.3 | Dynamic Headcount & Deep Linking Active")
