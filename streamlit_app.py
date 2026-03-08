import streamlit as st
import pandas as pd

# --- STANDARDIZED DATABASE ---
def get_database():
    base = [
        {"name": "Veg Poha", "type": "Breakfast", "cal": 250, "p": 8, "f": 5, "c": 42, "cook_time": 15, "cost": 35, "order": 90, "veg": True, "breakup": "Poha: ₹20, Veggies: ₹15"},
        {"name": "Paneer Sandwich", "type": "Breakfast", "cal": 320, "p": 15, "f": 12, "c": 35, "cook_time": 10, "cost": 85, "order": 180, "veg": True, "breakup": "Paneer: ₹65, Bread: ₹20"},
        {"name": "Egg Bhurji + Pav", "type": "Breakfast", "cal": 350, "p": 18, "f": 15, "c": 30, "cook_time": 15, "cost": 45, "order": 140, "veg": False, "breakup": "Eggs: ₹21, Pav: ₹15, Veg: ₹9"},
        {"name": "Chicken Curry", "type": "Lunch", "cal": 520, "p": 45, "f": 22, "c": 10, "cook_time": 60, "cost": 180, "order": 380, "veg": False, "breakup": "Chicken: ₹140, Gravy: ₹40"},
        {"name": "Rajma Chawal", "type": "Lunch", "cal": 450, "p": 18, "f": 8, "c": 65, "cook_time": 55, "cost": 65, "order": 240, "veg": True, "breakup": "Rajma: ₹40, Rice: ₹15, Gravy: ₹10"},
        {"name": "Moong Dal Khichdi", "type": "Dinner", "cal": 310, "p": 12, "f": 6, "c": 52, "cook_time": 25, "cost": 30, "order": 150, "veg": True, "breakup": "Dal: ₹15, Rice: ₹10, Ghee: ₹5"},
        {"name": "Mutton Rogan Josh", "type": "Dinner", "cal": 650, "p": 50, "f": 35, "c": 12, "cook_time": 90, "cost": 400, "order": 850, "veg": False, "breakup": "Mutton: ₹350, Gravy: ₹50"}
    ]
    full = []
    for m_type in ["Breakfast", "Lunch", "Dinner"]:
        cat = [m for m in base if m["type"] == m_type]
        for i in range(50):
            item = cat[i % len(cat)].copy()
            if i >= len(cat): item["name"] = f"{item['name']} Variant {i+1}"
            full.append(item)
    return pd.DataFrame(full)

df = get_database()

st.set_page_config(page_title="MealBrain Daily Planner", layout="wide")

# --- SESSION STATE ---
if 'plan' not in st.session_state:
    st.session_state.plan = {"Breakfast": None, "Lunch": None, "Dinner": None}

def set_meal(m_type, diet_pref, specific_name=None):
    f_df = df[df['type'] == m_type]
    if diet_pref == "Veg Only": f_df = f_df[f_df['veg'] == True]
    
    if specific_name:
        st.session_state.plan[m_type] = f_df[f_df['name'] == specific_name].iloc[0].to_dict()
    else:
        st.session_state.plan[m_type] = f_df.sample(n=1).iloc[0].to_dict()

# --- SIDEBAR ---
with st.sidebar:
    st.header("👥 Family Setup")
    adults = st.number_input("Adults", 1, 10, 2)
    kids = st.number_input("Kids", 0, 10, 1)
    diet = st.radio("Diet Preference", ["Everything", "Veg Only"])
    st.divider()
    show_macros = st.checkbox("Show Macros (Protein/Fat/Carbs)", value=True)
    if st.button("🚀 Generate Entire Day", use_container_width=True):
        for t in ["Breakfast", "Lunch", "Dinner"]: set_meal(t, diet)

# Initialize if empty
if st.session_state.plan["Breakfast"] is None:
    for t in ["Breakfast", "Lunch", "Dinner"]: set_meal(t, diet)

# --- HEADER & SAVINGS ---
st.title("🍲 MealBrain Daily Planner")
p = st.session_state.plan
eff_hc = adults + (kids * 0.6)
total_cook = sum([p[t]['cost'] for t in p]) * eff_hc
total_order = sum([p[t]['order'] for t in p]) * eff_hc
st.metric("Total Day Savings", f"₹{int(total_order - total_cook)}")

# --- INTERACTIVE CONTROLS (ALIGNED) ---
st.write("### 🛠️ Customize Your Plan")
for t in ["Breakfast", "Lunch", "Dinner"]:
    # Using specific column ratios for perfect alignment
    col_sel, col_btn, col_brk = st.columns([4, 1, 1])
    
    opts = df[(df['type'] == t) & (df['veg'] if diet == "Veg Only" else True)]['name'].tolist()
    curr = p[t]['name']
    
    with col_sel:
        new_sel = st.selectbox(f"Select {t}", opts, index=opts.index(curr) if curr in opts else 0, key=f"sel_{t}")
        if new_sel != curr:
            set_meal(t, diet, new_sel)
            st.rerun()
            
    with col_btn:
        st.write(" ") # Padding for alignment
        if st.button(f"🎲 Random", key=f"btn_{t}", use_container_width=True):
            set_meal(t, diet)
            st.rerun()
            
    with col_brk:
        st.write(" ") # Padding for alignment
        with st.popover("💰 Breakup", use_container_width=True):
            st.caption(f"Price for {t}")
            st.write(p[t]['breakup'])

st.divider()

# --- TABLES ---
def draw_table(title, headcount, is_kids=False):
    st.subheader(title)
    scale = 0.6 if is_kids else 1.0
    rows = []
    for t in ["Breakfast", "Lunch", "Dinner"]:
        m = p[t]
        row = {
            "Meal": t,
            "Dish": m['name'],
            "Time": f"{m['cook_time']}m",
            "Calories": f"{int(m['cal'] * scale)} kcal",
            "Cost": f"₹{int(m['cost'] * headcount * scale)}",
            "Recipe": f"https://www.youtube.com/results?search_query=how+to+make+{m['name'].replace(' ', '+')}"
        }
        if show_macros:
            row.update({
                "Protein": f"{int(m['p']*scale)}g",
                "Fat": f"{int(m['f']*scale)}g",
                "Carbs": f"{int(m['c']*scale)}g"
            })
        rows.append(row)
    st.table(pd.DataFrame(rows).set_index("Meal"))

draw_table("🏠 Option 1: Home Cooking (Adults)", adults)
draw_table("👶 Option 1: Home Cooking (Kids)", kids, is_kids=True)

st.divider()

# --- ORDER SECTION ---
st.subheader("🛵 Option 2: Order Online (Consolidated)")
o_rows = []
for t in ["Breakfast", "Lunch", "Dinner"]:
    m = p[t]
    o_rows.append({
        "Meal": t,
        "Zomato Item": m['name'],
        "Total Cal": f"{int(m['cal'] * eff_hc)} kcal",
        "Total Cost": f"₹{int(m['order'] * eff_hc)}"
    })
st.table(pd.DataFrame(o_rows).set_index("Meal"))

st.markdown(f"### **Total Zomato Bill: ₹{int(total_order)}**")
# Correct Zomato Deep Link logic
zomato_query = "+".join([p[t]['name'].replace(' ', '+') for t in p])
st.link_button("🥡 Order All on Zomato", f"https://www.google.com/search?q=order+{zomato_query}+on+Zomato", use_container_width=True)

st.caption("v2.9 | Fixed Grid Alignment | Macro Support | Dynamic YT Search")
