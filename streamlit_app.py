import streamlit as st
import pandas as pd

# --- DATABASE ENGINE (Standardized for 50 per category) ---
def get_database():
    # Adult/Standard Pool
    adult_base = [
        {"name": "Masala Dosa", "type": "Breakfast", "cal": 380, "cook_time": 40, "cost": 45, "order": 160, "recipe": "https://youtu.be/1"},
        {"name": "Paneer Paratha", "type": "Breakfast", "cal": 350, "cook_time": 25, "cost": 40, "order": 140, "recipe": "https://youtu.be/2"},
        {"name": "Chicken Curry", "type": "Lunch", "cal": 520, "cook_time": 60, "cost": 180, "order": 380, "recipe": "https://youtu.be/3"},
        {"name": "Rajma Chawal", "type": "Lunch", "cal": 450, "cook_time": 55, "cost": 65, "order": 240, "recipe": "https://youtu.be/4"},
        {"name": "Palak Paneer", "type": "Dinner", "cal": 460, "cook_time": 40, "cost": 120, "order": 280, "recipe": "https://youtu.be/5"},
        {"name": "Mutton Rogan Josh", "type": "Dinner", "cal": 650, "cook_time": 90, "cost": 400, "order": 800, "recipe": "https://youtu.be/6"}
    ]
    # Kids' Specific Pool (Milder, Healthy, Fun)
    kids_base = [
        {"name": "Cheese Corn Poha", "type": "Breakfast", "cal": 220, "cook_time": 15, "cost": 40, "order": 120, "recipe": "https://youtu.be/7"},
        {"name": "Mini Idli Fry", "type": "Breakfast", "cal": 180, "cook_time": 20, "cost": 30, "order": 100, "recipe": "https://youtu.be/8"},
        {"name": "Paneer Makhani (Mild)", "type": "Lunch", "cal": 400, "cook_time": 35, "cost": 100, "order": 260, "recipe": "https://youtu.be/9"},
        {"name": "Egg Fried Rice (No Spice)", "type": "Lunch", "cal": 380, "cook_time": 20, "cost": 50, "order": 180, "recipe": "https://youtu.be/10"},
        {"name": "Moong Dal Khichdi", "type": "Dinner", "cal": 280, "cook_time": 25, "cost": 30, "order": 140, "recipe": "https://youtu.be/11"},
        {"name": "Veg Pasta in Red Sauce", "type": "Dinner", "cal": 350, "cook_time": 20, "cost": 60, "order": 220, "recipe": "https://youtu.be/12"}
    ]
    
    full_data = []
    for m_type in ["Breakfast", "Lunch", "Dinner"]:
        # Populate Adult Pool (50)
        a_cat = [m for m in adult_base if m["type"] == m_type]
        for i in range(50):
            item = a_cat[i % len(a_cat)].copy()
            if i >= len(a_cat): item["name"] = f"{item['name']} Variant {i}"
            item["target"] = "Adult"
            full_data.append(item)
        
        # Populate Kids Pool (50)
        k_cat = [m for m in kids_base if m["type"] == m_type]
        for i in range(50):
            item = k_cat[i % len(k_cat)].copy()
            if i >= len(k_cat): item["name"] = f"{item['name']} Fun-Size {i}"
            item["target"] = "Kids"
            full_data.append(item)
            
    return pd.DataFrame(full_data)

df = get_database()

st.set_page_config(page_title="MealBrain AI Planner v2.7", layout="wide")

# --- SESSION STATE ---
if 'selections' not in st.session_state:
    st.session_state.selections = {
        "Adult": {"Breakfast": df[(df['type']=='Breakfast') & (df['target']=='Adult')].iloc[0].to_dict(),
                  "Lunch": df[(df['type']=='Lunch') & (df['target']=='Adult')].iloc[0].to_dict(),
                  "Dinner": df[(df['type']=='Dinner') & (df['target']=='Adult')].iloc[0].to_dict()},
        "Kids": {"Breakfast": df[(df['type']=='Breakfast') & (df['target']=='Kids')].iloc[0].to_dict(),
                 "Lunch": df[(df['type']=='Lunch') & (df['target']=='Kids')].iloc[0].to_dict(),
                 "Dinner": df[(df['type']=='Dinner') & (df['target']=='Kids')].iloc[0].to_dict()}
    }

# --- SIDEBAR ---
with st.sidebar:
    st.header("👥 Family Profile")
    adult_count = st.number_input("Adults", min_value=1, value=2)
    kids_count = st.number_input("Kids", min_value=0, value=1)
    st.info("Kids portion sizes are set to 60% of adult nutritional values.")

# --- TOP STATS ---
total_cook = sum([st.session_state.selections["Adult"][t]['cost'] * adult_count for t in ["Breakfast", "Lunch", "Dinner"]]) + \
             sum([st.session_state.selections["Kids"][t]['cost'] * kids_count * 0.6 for t in ["Breakfast", "Lunch", "Dinner"]])
total_order = sum([st.session_state.selections["Adult"][t]['order'] * adult_count for t in ["Breakfast", "Lunch", "Dinner"]]) + \
              sum([st.session_state.selections["Kids"][t]['order'] * kids_count for t in ["Breakfast", "Lunch", "Dinner"]])

st.title("🍲 MealBrain AI Custom Planner")
st.metric("Family Day Savings", f"₹{int(total_order - total_cook)}", f"{int(((total_order-total_cook)/total_order)*100)}% Cheaper")

# --- UTILITY: RENDER TABLE WITH MANUAL SELECTION ---
def render_section(title, target_key, headcount, scale=1.0):
    st.subheader(title)
    rows = []
    for t in ["Breakfast", "Lunch", "Dinner"]:
        # 1. Manual Selector & Swap Row
        col1, col2 = st.columns([3, 1])
        
        # Get list of 50 dishes for this category
        options = df[(df['type'] == t) & (df['target'] == target_key)]['name'].tolist()
        current_name = st.session_state.selections[target_key][t]['name']
        
        # Dropdown Search/Select
        new_selection = col1.selectbox(f"Select {t} Dish ({target_key})", options, 
                                       index=options.index(current_name) if current_name in options else 0,
                                       key=f"select_{target_key}_{t}")
        
        # Update state if manual selection changes
        if new_selection != current_name:
            st.session_state.selections[target_key][t] = df[df['name'] == new_selection].iloc[0].to_dict()
            st.rerun()

        # Random Swap Button
        if col2.button(f"🔄 Random {t}", key=f"rnd_{target_key}_{t}"):
            st.session_state.selections[target_key][t] = df[(df['type'] == t) & (df['target'] == target_key)].sample(n=1).iloc[0].to_dict()
            st.rerun()

        # 2. Data for Table
        m = st.session_state.selections[target_key][t]
        rows.append({
            "Meal": t,
            "Dish Name": m['name'],
            "Cook Time": f"{m['cook_time']}m",
            "Calories": f"{int(m['cal'] * scale)} kcal",
            "Cost": f"₹{int(m['cost'] * headcount * scale)}",
            "YouTube": m['recipe']
        })
    
    st.table(pd.DataFrame(rows).set_index("Meal"))

# DISPLAY TABLES
render_section("👨‍👩‍👧 Option 1: Cook at Home (Adults)", "Adult", adult_count)
render_section("👶 Option 1: Cook at Home (Kids)", "Kids", kids_count, scale=0.6)

st.divider()

# --- CONSOLIDATED ORDER TABLE ---
st.subheader("🛵 Option 2: Order Now (Consolidated Bill)")
order_rows = []
for t in ["Breakfast", "Lunch", "Dinner"]:
    a_m = st.session_state.selections["Adult"][t]
    k_m = st.session_state.selections["Kids"][t]
    order_rows.append({
        "Meal": t,
        "Adult Dish": a_m['name'],
        "Kids Dish": k_m['name'],
        "Total Cost": f"₹{int((a_m['order']*adult_count) + (k_m['order']*kids_count))}"
    })
st.table(pd.DataFrame(order_rows).set_index("Meal"))
st.markdown(f"### **Total Day Bill: ₹{int(total_order)}**")

st.caption("v2.7 | Kids-Specific Menu | Manual Dropdown Search | Independent Meal Swaps")
