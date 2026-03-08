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

st.set_page_config(page_title="MealBrain AI Planner", layout="wide")

# --- FIXED STATE PERSISTENCE ---
if 'plan' not in st.session_state:
    st.session_state.plan = {"Breakfast": None, "Lunch": None, "Dinner": None}

def update_meal(m_type, diet_pref, specific_name=None):
    f_df = df[df['type'] == m_type]
    if diet_pref == "Veg Only": 
        f_df = f_df[f_df['veg'] == True]
    
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
    if st.button("🚀 Regenerate Entire Day", use_container_width=True):
        for t in ["Breakfast", "Lunch", "Dinner"]: update_meal(t, diet)

# Init check
if st.session_state.plan["Breakfast"] is None:
    for t in ["Breakfast", "Lunch", "Dinner"]: update_meal(t, diet)

# --- MATH ---
p = st.session_state.plan
eff_hc = adults + (kids * 0.6)
total_cook = sum([p[t]['cost'] for t in p]) * eff_hc
total_order = sum([p[t]['order'] for t in p]) * eff_hc

st.title("🍲 MealBrain Daily Planner")
st.metric("Total Day Savings", f"₹{int(total_order - total_cook)}")

# --- INTEGRATED ROW FUNCTION v3.1 ---
def render_meal_row(m_type, headcount, scale=1.0, key_prefix="A"):
    m = p[m_type]
    opts = df[(df['type'] == m_type) & (df['veg'] if diet == "Veg Only" else True)]['name'].tolist()
    
    with st.container(border=True):
        # Increased columns to accommodate Shop/Order buttons per row
        c_label, c_sel, c_rnd, c_cal, c_cost, c_shop, c_order = st.columns([1, 2.5, 0.5, 1, 1, 1.2, 1.2])
        
        # 1. Row Label (Time of Day)
        c_label.markdown(f"**{m_type}**")
        
        # 2. Selection Dropdown
        with c_sel:
            new_sel = st.selectbox(f"Select {m_type}", opts, index=opts.index(m['name']) if m['name'] in opts else 0, key=f"sel_{key_prefix}_{m_type}", label_visibility="collapsed")
            if new_sel != m['name']:
                update_meal(m_type, diet, new_sel)
                st.rerun()
        
        # 3. Random Button (🎲) - Fixed Persistence
        if c_rnd.button("🎲", key=f"rnd_{key_prefix}_{m_type}", help="Randomize this meal"):
            update_meal(m_type, diet)
            st.rerun()

        # 4. Calories & Macros (Per Person)
        with c_cal:
            with st.popover(f"🔥 {int(m['cal'] * scale)}", use_container_width=True):
                st.markdown("**Macros (Per Person)**")
                st.write(f"Protein: {int(m['p']*scale)}g")
                st.write(f"Fat: {int(m['f']*scale)}g")
                st.write(f"Carbs: {int(m['c']*scale)}g")

        # 5. Cost & Breakup (Total for group)
        with c_cost:
            with st.popover(f"₹{int(m['cost'] * headcount * scale)}", use_container_width=True):
                st.markdown("**Cost Breakup**")
                st.write(m['breakup'])

        # 6. Shop on Blinkit (Individual Search)
        with c_shop:
            shop_url = f"https://www.google.com/search?q=buy+ingredients+for+{m['name'].replace(' ', '+')}+on+Blinkit"
            st.link_button("🛒 Blinkit", shop_url, use_container_width=True)

        # 7. Order on Zomato (Individual Order)
        with c_order:
            zomato_url = f"https://www.google.com/search?q=order+{m['name'].replace(' ', '+')}+on+Zomato"
            st.link_button("🥡 Zomato", zomato_url, use_container_width=True)

# --- DISPLAY ---
st.subheader("🏠 Home Cooking (Adults)")
for t in ["Breakfast", "Lunch", "Dinner"]:
    render_meal_row(t, adults, scale=1.0, key_prefix="adult")

if kids > 0:
    st.subheader("👶 Home Cooking (Kids - Scaled Portions)")
    for t in ["Breakfast", "Lunch", "Dinner"]:
        render_meal_row(t, kids, scale=0.6, key_prefix="kids")

st.divider()
st.markdown(f"### **Consolidated Zomato Bill (Whole Day): ₹{int(total_order)}**")
st.caption("v3.1 | Individual Row Actions | Time Labels | Per-Person Macros")
