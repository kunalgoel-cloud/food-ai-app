import streamlit as st
import pandas as pd
import random

# --- DATABASE ---
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

# --- SIDEBAR ---
with st.sidebar:
    st.title("⚙️ Setup")
    headcount = st.number_input("Headcount (People)", min_value=1, max_value=20, value=1)
    diet = st.radio("Diet Preference", ["Veg Only", "Everything"])
    goal = st.select_slider("Health Goal", ["Light", "Balanced", "Cheat Day"])
    vibe = st.radio("Vibe", ["Quick", "Relaxed"])

st.title("🍲 MealBrain AI")
user_input = st.text_input("Craving something specific?", placeholder="e.g. 'Spicy' or 'Dal'")

# --- FILTERING ---
f_df = df.copy()
if diet == "Veg Only": f_df = f_df[f_df['veg'] == True]
if goal == "Light": f_df = f_df[f_df['cal'] < 300]
elif goal == "Balanced": f_df = f_df[(f_df['cal'] >= 300) & (f_df['cal'] <= 450)]
if user_input: f_df = f_df[f_df.apply(lambda x: user_input.lower() in x['name'].lower() or user_input.lower() in x['tags'], axis=1)]

# --- BUTTONS ---
c_btn1, c_btn2, _ = st.columns([1, 1, 4])
get_meal = c_btn1.button("🚀 Get Meal")
suggest_next = c_btn2.button("🔄 Suggest Another")

if get_meal or suggest_next:
    if not f_df.empty:
        winner = f_df.sample(n=1).iloc[0]
        
        st.header(f"Recommendation: {winner['name']}")
        
        # FIXED IMAGE ENGINE
        # Uses Source Unsplash for better food-specific results
        img_url = f"https://source.unsplash.com/800x400/?indian,food,{winner['name'].replace(' ', '')}"
        st.image(img_url, use_column_width=True)

        st.markdown("---")
        
        # --- ROW 1: HOME COOKING ---
        st.subheader("🏠 Option: Cook at Home")
        h1, h2, h3, h4, h5 = st.columns([1, 1, 1, 1, 2])
        h1.metric("Time", f"{winner['cook_time']}m")
        h2.metric("Total Cost", f"₹{winner['cost'] * headcount}")
        h3.metric("Calories", f"{winner['cal'] * headcount}kcal")
        h4.metric("Effort", winner['vibe'])
        blinkit_url = f"https://www.google.com/search?q=buy+{winner['name'].replace(' ', '+')}+ingredients+on+Blinkit"
        h5.markdown(f"<br><a href='{blinkit_url}' target='_blank'><button style='width:100%; border-radius:5px; background-color:#FFD700; border:none; padding:10px;'>🛒 Shop Ingredients (Blinkit)</button></a>", unsafe_allow_index=True)

        st.markdown("---")

        # --- ROW 2: ORDERING ---
        st.subheader("🛵 Option: Order Online")
        o1, o2, o3, o4, o5 = st.columns([1, 1, 1, 1, 2])
        o1.metric("Delivery", f"{winner['order_time']}m")
        o2.metric("Total Cost", f"₹{winner['order'] * headcount}")
        o3.metric("Calories", f"{winner['cal'] * headcount}kcal")
        o4.metric("Source", "Restaurant")
        zomato_url = f"https://www.google.com/search?q=order+{winner['name'].replace(' ', '+')}+from+Zomato"
        o5.markdown(f"<br><a href='{zomato_url}' target='_blank'><button style='width:100%; border-radius:5px; background-color:#CB202D; color:white; border:none; padding:10px;'>🥡 Order Now (Zomato)</button></a>", unsafe_allow_index=True)

    else:
        st.error("No matches! Try changing your 'Vibe' or 'Health Goal'.")

st.caption("v1.4 | Standardized UI | Accurate Scaling")
