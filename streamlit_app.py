import streamlit as st
import pandas as pd
import random

# --- STABILIZED DATABASE ---
meals_data = [
    {
        "name": "Veg Poha", "type": "Breakfast", "vibe": "Quick", "cal": 250, "cook_time": 15, "order_time": 25, "cost": 35, "order": 90, "tags": "light, healthy, poha, rice", "veg": True,
        "recipe_url": "https://www.youtube.com/results?search_query=how+to+make+veg+poha",
        "cost_breakup": "1. Poha (150g): ₹25\n2. Onion/Potato/Spices: ₹10"
    },
    {
        "name": "Paneer Sandwich", "type": "Breakfast", "vibe": "Quick", "cal": 320, "cook_time": 10, "order_time": 30, "cost": 85, "order": 180, "tags": "protein, paneer, sandwich", "veg": True,
        "recipe_url": "https://www.youtube.com/results?search_query=paneer+sandwich+recipe",
        "cost_breakup": "1. Paneer (200g): ₹65\n2. Bread & Butter: ₹20"
    },
    {
        "name": "Rajma Chawal", "type": "Lunch", "vibe": "Relaxed", "cal": 450, "cook_time": 55, "order_time": 45, "cost": 65, "order": 240, "tags": "protein, beans, rice, family", "veg": True,
        "recipe_url": "https://www.youtube.com/results?search_query=punjabi+rajma+chawal+recipe",
        "cost_breakup": "1. Rajma (150g): ₹40\n2. Rice (100g): ₹15\n3. Gravy: ₹10"
    },
    {
        "name": "Dal Tadka + Rice", "type": "Lunch", "vibe": "Quick", "cal": 410, "cook_time": 30, "order_time": 35, "cost": 50, "order": 180, "tags": "light, comfort, dal, rice", "veg": True,
        "recipe_url": "https://www.youtube.com/results?search_query=dal+tadka+rice+recipe",
        "cost_breakup": "1. Dal (100g): ₹25\n2. Rice: ₹15\n3. Tadka: ₹10"
    }
]
df = pd.DataFrame(meals_data)

st.set_page_config(page_title="MealBrain AI", layout="wide")

# --- SIDEBAR ---
with st.sidebar:
    st.header("1. Your Setup")
    headcount = st.number_input("Headcount (People)", min_value=1, value=3)
    diet = st.radio("Diet Preference", ["Veg Only", "Everything"])
    goal = st.select_slider("Health Goal", ["Light", "Balanced", "Cheat Day"])
    vibe = st.radio("Cooking Vibe", ["Quick", "Relaxed"])

st.title("🍲 MealBrain AI")

# --- SESSION STATE ---
if 'current_meal' not in st.session_state: st.session_state.current_meal = None

# --- FILTERING ---
f_df = df.copy()
if diet == "Veg Only": f_df = f_df[f_df['veg'] == True]
if goal == "Light": f_df = f_df[f_df['cal'] < 300]
elif goal == "Balanced": f_df = f_df[(f_df['cal'] >= 300) & (f_df['cal'] <= 450)]

# --- ACTION BUTTONS ---
c1, c2, _ = st.columns([1, 1, 4])
if c1.button("🚀 Get Meal") or c2.button("🔄 Suggest Another"):
    if not f_df.empty:
        st.session_state.current_meal = f_df.sample(n=1).iloc[0]

# --- MAIN DISPLAY ---
if st.session_state.current_meal is not None:
    m = st.session_state.current_meal
    st.header(f"Recommendation: {m['name']}")
    
    # NEW STABLE IMAGE ENGINE
    img_id = random.randint(1, 1000)
    img_url = f"https://images.weserv.nl/?url=https://loremflickr.com/800/400/indianfood,{m['name'].replace(' ', '')}&w=800&h=400&fit=cover&cache={img_id}"
    st.image(img_url, use_container_width=True)

    st.markdown("---")
    
    # Scaled Variables
    total_cook = m['cost'] * headcount
    total_order = m['order'] * headcount
    total_savings = total_order - total_cook
    total_cal = m['cal'] * headcount

    # --- ROW 1: COOK AT HOME ---
    st.subheader("🏠 Option 1: Cook at Home")
    h1, h2, h3, h4, h5 = st.columns([1, 1, 1, 1, 2])
    
    h1.metric("Cook Time", f"{m['cook_time']}m")
    h1.link_button("📺 Recipe", m['recipe_url'], use_container_width=True)
    
    with h2:
        st.metric("Total Cost", f"₹{total_cook}")
        with st.popover("💰 Breakup"):
            st.write(m['cost_breakup'])
            
    h3.metric("Calories", f"{total_cal}kcal")
    
    # RE-ESTABLISHED SAVINGS LOGIC
    h4.metric("Savings", f"₹{total_savings}", f"{int((total_savings/total_order)*100)}%")
    
    blinkit_url = f"https://www.google.com/search?q=buy+{m['name'].replace(' ', '+')}+ingredients+on+Blinkit"
    h5.link_button("🛒 Shop (Blinkit)", blinkit_url, use_container_width=True)

    st.divider()

    # --- ROW 2: ORDER ONLINE ---
    st.subheader("🛵 Option 2: Order Online")
    o1, o2, o3, o4, o5 = st.columns([1, 1, 1, 1, 2])
    
    o1.metric("Delivery", f"{m['order_time']}m")
    o2.metric("Total Cost", f"₹{total_order}")
    o3.metric("Calories", f"{total_cal}kcal")
    o4.metric("Status", "Instant")
    
    zomato_url = f"https://www.google.com/search?q=order+{m['name'].replace(' ', '+')}+on+Zomato"
    o5.link_button("🥡 Order (Zomato)", zomato_url, use_container_width=True)

st.divider()
st.caption("v1.9 | Image Fix | Savings Logic Re-integrated")
