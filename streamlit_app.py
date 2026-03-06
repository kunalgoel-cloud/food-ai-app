import streamlit as st
import pandas as pd
import random

# --- REFINED DATABASE (v1.8) ---
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
    },
    {
        "name": "Egg Curry", "type": "Dinner", "vibe": "Quick", "cal": 380, "cook_time": 35, "order_time": 40, "cost": 55, "order": 210, "tags": "protein, eggs, spicy", "veg": False,
        "recipe_url": "https://www.youtube.com/results?search_query=dhabha+style+egg+curry",
        "cost_breakup": "1. Eggs (4): ₹24\n2. Gravy & Spices: ₹31"
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

# --- LOGIC ---
if 'meal' not in st.session_state: st.session_state.meal = None

f_df = df.copy()
if diet == "Veg Only": f_df = f_df[f_df['veg'] == True]
if goal == "Light": f_df = f_df[f_df['cal'] < 300]
elif goal == "Balanced": f_df = f_df[(f_df['cal'] >= 300) & (f_df['cal'] <= 450)]

c1, c2, _ = st.columns([1, 1, 4])
if c1.button("🚀 Get Meal") or c2.button("🔄 Suggest Another"):
    if not f_df.empty:
        st.session_state.meal = f_df.sample(n=1).iloc[0]

# --- RESULTS DISPLAY ---
if st.session_state.meal is not None:
    m = st.session_state.meal
    st.header(f"Recommendation: {m['name']}")
    
    # FIXED IMAGE: Using Unsplash Source with cache-busting randomizer
    img_seed = random.randint(1, 1000)
    st.image(f"https://source.unsplash.com/featured/800x400?indian,food,{m['name'].replace(' ', '')}&sig={img_seed}", use_container_width=True)

    st.markdown("---")
    
    # --- ROW 1: OPTION 1 (COOK AT HOME) ---
    st.subheader("🏠 Option 1: Cook at Home")
    h1, h2, h3, h4 = st.columns([1, 1, 1, 2])
    
    # Metric 1: Time as a Link
    h1.metric("Cook Time (Click for Video)", f"{m['cook_time']}m")
    h1.link_button("📺 Watch Recipe", m['recipe_url'], use_container_width=True)
    
    # Metric 2: Cost as a Popover (Clickable Breakdown)
    with h2:
        st.metric("Total Cost", f"₹{m['cost'] * headcount}")
        with st.popover("💰 View Breakup"):
            st.write(f"Breakdown for {headcount} person(s):")
            st.write(m['cost_breakup'])
            
    h3.metric("Calories", f"{m['cal'] * headcount} kcal")
    
    blinkit_url = f"https://www.google.com/search?q=buy+{m['name'].replace(' ', '+')}+ingredients+on+Blinkit"
    h4.link_button("🛒 Shop Ingredients (Blinkit)", blinkit_url, use_container_width=True)

    st.divider()

    # --- ROW 2: OPTION 2 (ORDER ONLINE) ---
    st.subheader("🛵 Option 2: Order Online")
    o1, o2, o3, o4 = st.columns([1, 1, 1, 2])
    
    o1.metric("Delivery", f"{m['order_time']}m")
    
    with o2:
        st.metric("Total Cost", f"₹{m['order'] * headcount}")
        with st.popover("💵 Why this price?"):
            st.write(f"Includes Restaurant Markup & Est. Delivery Fee for {headcount} portions.")
            
    o3.metric("Calories", f"{m['cal'] * headcount} kcal")
    
    zomato_url = f"https://www.google.com/search?q=order+{m['name'].replace(' ', '+')}+on+Zomato"
    o4.link_button("🥡 Order Now (Zomato)", zomato_url, use_container_width=True)

st.divider()
st.caption("v1.8 | Metric-Integrated Actions | Youtube Recipe Links")
