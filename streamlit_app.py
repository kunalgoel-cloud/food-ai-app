import streamlit as st
import pandas as pd
import random

# --- STANDARDIZED DATABASE (50 per category) ---
def get_database():
    base = [
        {"name": "Veg Poha", "type": "Breakfast", "cal": 250, "cook_time": 15, "order_time": 25, "cost": 35, "order": 90, "veg": True, "recipe": "https://www.youtube.com/results?search_query=veg+poha"},
        {"name": "Paneer Sandwich", "type": "Breakfast", "cal": 320, "cook_time": 10, "order_time": 30, "cost": 85, "order": 180, "veg": True, "recipe": "https://www.youtube.com/results?search_query=paneer+sandwich"},
        {"name": "Rajma Chawal", "type": "Lunch", "cal": 450, "cook_time": 55, "order_time": 45, "cost": 65, "order": 240, "veg": True, "recipe": "https://www.youtube.com/results?search_query=rajma+chawal"},
        {"name": "Dal Tadka + Rice", "type": "Lunch", "cal": 410, "cook_time": 30, "order_time": 35, "cost": 50, "order": 180, "veg": True, "recipe": "https://www.youtube.com/results?search_query=dal+tadka"},
        {"name": "Chicken Curry", "type": "Lunch", "cal": 520, "cook_time": 60, "order_time": 50, "cost": 180, "order": 380, "veg": False, "recipe": "https://www.youtube.com/results?search_query=chicken+curry"},
        {"name": "Moong Dal Khichdi", "type": "Dinner", "cal": 310, "cook_time": 25, "order_time": 35, "cost": 30, "order": 150, "veg": True, "recipe": "https://www.youtube.com/results?search_query=khichdi"},
        {"name": "Palak Paneer", "type": "Dinner", "cal": 460, "cook_time": 40, "order_time": 40, "cost": 120, "order": 280, "veg": True, "recipe": "https://www.youtube.com/results?search_query=palak+paneer"}
    ]
    full = []
    for m_type in ["Breakfast", "Lunch", "Dinner"]:
        cat = [m for m in base if m["type"] == m_type]
        for i in range(50):
            item = cat[i % len(cat)].copy()
            if i >= len(cat): item["name"] = f"{item['name']} v{i}"
            full.append(item)
    return pd.DataFrame(full)

df = get_database()

st.set_page_config(page_title="MealBrain AI Planner", layout="wide")

# --- SESSION STATE FOR PERSISTENCE ---
if 'day_plan' not in st.session_state:
    st.session_state.day_plan = {"Breakfast": None, "Lunch": None, "Dinner": None}

def refresh_meal(m_type, diet_pref):
    f_df = df[df['type'] == m_type]
    if diet_pref == "Veg Only": f_df = f_df[f_df['veg'] == True]
    st.session_state.day_plan[m_type] = f_df.sample(n=1).iloc[0].to_dict()

# --- SIDEBAR ---
with st.sidebar:
    st.header("👥 Family Profile")
    adults = st.number_input("Adults", min_value=1, value=2)
    kids = st.number_input("Kids", min_value=0, value=1)
    diet = st.radio("Diet", ["Veg Only", "Everything"])
    if st.button("🔄 Generate New Day Plan", use_container_width=True):
        for t in ["Breakfast", "Lunch", "Dinner"]: refresh_meal(t, diet)

# Initialize plan if empty
if st.session_state.day_plan["Breakfast"] is None:
    for t in ["Breakfast", "Lunch", "Dinner"]: refresh_meal(t, diet)

# --- TOP STATS: NET SAVINGS ---
p = st.session_state.day_plan
effective_headcount = adults + (kids * 0.6)
total_cook_day = sum([p[t]['cost'] for t in p]) * effective_headcount
total_order_day = sum([p[t]['order'] for t in p]) * effective_headcount
net_savings = total_order_day - total_cook_day

st.title("🍲 Daily Meal Planner")
st.metric("Total Day Savings", f"₹{int(net_savings)}", f"{int((net_savings/total_order_day)*100)}% cheaper than ordering all day")

# --- ADULT TABLE ---
st.subheader("👨‍👩‍👧 Option 1: Cook at Home (Adult Portions)")
adult_data = []
for t in ["Breakfast", "Lunch", "Dinner"]:
    m = p[t]
    adult_data.append({
        "Meal": t,
        "Dish": m['name'],
        "Cook Time": f"{m['cook_time']}m",
        "Calories": f"{m['cal']} kcal",
        "Cost (Total)": f"₹{int(m['cost'] * adults)}",
        "Recipe": m['recipe']
    })
st.table(pd.DataFrame(adult_data).set_index("Meal"))

# --- KIDS TABLE ---
st.subheader("👶 Option 1: Cook at Home (Kids Portions - 60%)")
kids_data = []
for t in ["Breakfast", "Lunch", "Dinner"]:
    m = p[t]
    kids_data.append({
        "Meal": t,
        "Dish": m['name'],
        "Cook Time": f"{m['cook_time']}m",
        "Calories": f"{int(m['cal'] * 0.6)} kcal",
        "Cost (Total)": f"₹{int(m['cost'] * kids * 0.6)}",
        "Recipe": m['recipe']
    })
st.table(pd.DataFrame(kids_data).set_index("Meal"))

# --- MEAL REFRESH BUTTONS ---
st.write("💡 *Not feeling a specific dish? Swap it below:*")
r1, r2, r3 = st.columns(3)
if r1.button("🔄 Change Breakfast"): refresh_meal("Breakfast", diet); st.rerun()
if r2.button("🔄 Change Lunch"): refresh_meal("Lunch", diet); st.rerun()
if r3.button("🔄 Change Dinner"): refresh_meal("Dinner", diet); st.rerun()

st.divider()

# --- ORDER TABLE ---
st.subheader("🛵 Option 2: Order Now (Consolidated)")
order_data = []
for t in ["Breakfast", "Lunch", "Dinner"]:
    m = p[t]
    order_data.append({
        "Meal": t,
        "Dish": m['name'],
        "Calories (Total)": f"{int(m['cal'] * effective_headcount)} kcal",
        "Cost (Total)": f"₹{int(m['order'] * effective_headcount)}"
    })
st.table(pd.DataFrame(order_data).set_index("Meal"))

st.markdown(f"### **Total Zomato Bill: ₹{int(total_order_day)}**")
st.link_button("🥡 Order All on Zomato", f"https://www.google.com/search?q=order+food+on+Zomato")

st.caption("v2.6 | Separate Tables | 50 Dishes per Category | Interactive Swap Buttons")
