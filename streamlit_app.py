import streamlit as st
import pandas as pd

# --- VERIFIED DATABASE (v2.2) ---
meals_data = [
    {"name": "Veg Poha", "type": "Breakfast", "cal": 250, "cook_time": 15, "order_time": 25, "cost": 35, "order": 90, "veg": True, "recipe_url": "https://www.youtube.com/results?search_query=veg+poha+recipe", "breakup": "Poha: ₹20, Veggies: ₹15"},
    {"name": "Paneer Sandwich", "type": "Breakfast", "cal": 320, "cook_time": 10, "order_time": 30, "cost": 85, "order": 180, "veg": True, "recipe_url": "https://www.youtube.com/results?search_query=paneer+sandwich+recipe", "breakup": "Paneer: ₹65, Bread: ₹20"},
    {"name": "Rajma Chawal", "type": "Lunch", "cal": 450, "cook_time": 55, "order_time": 45, "cost": 65, "order": 240, "veg": True, "recipe_url": "https://www.youtube.com/results?search_query=rajma+chawal+recipe", "breakup": "Rajma: ₹40, Rice: ₹15, Gravy: ₹10"},
    {"name": "Dal Tadka + Rice", "type": "Lunch", "cal": 410, "cook_time": 30, "order_time": 35, "cost": 50, "order": 180, "veg": True, "recipe_url": "https://www.youtube.com/results?search_query=dal+tadka+recipe", "breakup": "Dal: ₹25, Rice: ₹15, Tadka: ₹10"},
    {"name": "Chicken Curry + Roti", "type": "Lunch", "cal": 520, "cook_time": 60, "order_time": 50, "cost": 180, "order": 380, "veg": False, "recipe_url": "https://www.youtube.com/results?search_query=chicken+curry+recipe", "breakup": "Chicken: ₹140, Gravy: ₹40"},
    {"name": "Masala Dosa", "type": "Breakfast", "cal": 350, "cook_time": 40, "order_time": 30, "cost": 45, "order": 150, "veg": True, "recipe_url": "https://www.youtube.com/results?search_query=masala+dosa+recipe", "breakup": "Batter: ₹25, Masala: ₹20"},
    {"name": "Egg Curry", "type": "Dinner", "cal": 380, "cook_time": 35, "order_time": 40, "cost": 55, "order": 210, "veg": False, "recipe_url": "https://www.youtube.com/results?search_query=egg+curry+recipe", "breakup": "Eggs: ₹24, Gravy: ₹31"},
    {"name": "Moong Dal Khichdi", "type": "Dinner", "cal": 310, "cook_time": 25, "order_time": 35, "cost": 30, "order": 150, "veg": True, "recipe_url": "https://www.youtube.com/results?search_query=khichdi+recipe", "breakup": "Dal: ₹15, Rice: ₹10, Ghee: ₹5"}
]
df = pd.DataFrame(meals_data)

st.set_page_config(page_title="MealBrain AI", layout="wide")

# --- SIDEBAR: DETAILED INPUTS ---
with st.sidebar:
    st.header("👥 Family Composition")
    adults = st.number_input("Number of Adults", min_value=1, value=2)
    kids = st.number_input("Number of Kids", min_value=0, value=1)
    
    st.header("🥗 Preferences")
    diet = st.radio("Diet", ["Veg Only", "Everything"])
    goal = st.select_slider("Portion/Health Goal", ["Light", "Balanced", "Heavy"])
    
    st.header("🏠 Pantry Mode")
    have_staples = st.checkbox("I have Rice/Atta/Oil", value=False)
    
    # Logic: Kids count as 0.6 of an adult for cost/calories
    effective_headcount = adults + (kids * 0.6)
    pantry_discount = 0.20 if have_staples else 0.0

# --- LOGIC ---
if 'meal' not in st.session_state: st.session_state.meal = None

# Filter logic
f_df = df.copy()
if diet == "Veg Only": f_df = f_df[f_df['veg'] == True]
if goal == "Light": f_df = f_df[f_df['cal'] < 350]
elif goal == "Heavy": f_df = f_df[f_df['cal'] > 450]

# --- MAIN INTERFACE ---
st.title("🍲 MealBrain AI")
c1, c2, _ = st.columns([1, 1, 4])
if c1.button("🚀 Get Meal") or c2.button("🔄 Suggest Another"):
    if not f_df.empty:
        st.session_state.meal = f_df.sample(n=1).iloc[0]

if st.session_state.meal is not None:
    m = st.session_state.meal
    st.subheader(f"Recommended Meal: {m['name']}")
    
    # Calculations
    unit_cook_cost = m['cost'] * (1 - pantry_discount)
    total_cook = int(unit_cook_cost * effective_headcount)
    total_order = int(m['order'] * effective_headcount)
    total_savings = total_order - total_cook
    total_cal = int(m['cal'] * effective_headcount)

    st.markdown("---")

    # --- OPTION 1: COOK ---
    st.markdown("### 🏠 Option 1: Cook at Home")
    h1, h2, h3, h4, h5 = st.columns([1, 1, 1, 1, 2])
    
    # Clickable Time Metric
    h1.metric("Cook Time", f"{m['cook_time']}m")
    h1.link_button("📺 Recipe Video", m['recipe_url'], use_container_width=True)
    
    # Clickable Cost Metric
    with h2:
        st.metric("Total Cost", f"₹{total_cook}")
        with st.popover("💰 Price Breakup"):
            st.write(f"For {adults} Adults & {kids} Kids:")
            st.write(m['breakup'])
            if have_staples: st.success("20% Pantry Discount Applied")

    h3.metric("Total Calories", f"{total_cal} kcal")
    
    # Savings Metric
    h4.metric("Net Savings", f"₹{total_savings}", f"{int((total_savings/total_order)*100)}% Saved")
    
    h5.link_button("🛒 Shop (Blinkit)", f"https://www.google.com/search?q=buy+{m['name'].replace(' ', '+')}+on+Blinkit", use_container_width=True)

    st.divider()

    # --- OPTION 2: ORDER ---
    st.markdown("### 🛵 Option 2: Order Online")
    o1, o2, o3, o4, o5 = st.columns([1, 1, 1, 1, 2])
    
    o1.metric("Delivery", f"{m['order_time']}m")
    o2.metric("Total Cost", f"₹{total_order}")
    o3.metric("Total Calories", f"{total_cal} kcal")
    o4.metric("Portion", goal)
    o5.link_button("🥡 Order (Zomato)", f"https://www.google.com/search?q=order+{m['name'].replace(' ', '+')}+on+Zomato", use_container_width=True)

else:
    st.info("Adjust your filters and click 'Get Meal' to begin.")

st.caption("v2.2 | No-Image Stability | Family-Type Logic | Dynamic Savings")
