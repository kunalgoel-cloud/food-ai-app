import streamlit as st
import pandas as pd

# --- FULL 50-DISH DATABASE (Standardized Keys) ---
meals_data = [
    # BREAKFAST (1-12)
    {"name": "Veg Poha", "type": "Breakfast", "cal": 250, "cook_time": 15, "order_time": 25, "cost": 35, "order": 90, "veg": True, "recipe_url": "https://www.youtube.com/results?search_query=veg+poha", "breakup": "Poha: ₹20, Veggies/Oil: ₹15"},
    {"name": "Paneer Sandwich", "type": "Breakfast", "cal": 320, "cook_time": 10, "order_time": 30, "cost": 85, "order": 180, "veg": True, "recipe_url": "https://www.youtube.com/results?search_query=paneer+sandwich", "breakup": "Paneer: ₹65, Bread/Butter: ₹20"},
    {"name": "Aloo Paratha", "type": "Breakfast", "cal": 310, "cook_time": 25, "order_time": 35, "cost": 30, "order": 120, "veg": True, "recipe_url": "https://www.youtube.com/results?search_query=aloo+paratha", "breakup": "Potato: ₹10, Atta: ₹15, Spices: ₹5"},
    {"name": "Idli Sambar", "type": "Breakfast", "cal": 210, "cook_time": 20, "order_time": 30, "cost": 30, "order": 110, "veg": True, "recipe_url": "https://www.youtube.com/results?search_query=idli+sambar", "breakup": "Batter: ₹15, Dal/Veg: ₹15"},
    {"name": "Masala Dosa", "type": "Breakfast", "cal": 380, "cook_time": 40, "order_time": 35, "cost": 45, "order": 160, "veg": True, "recipe_url": "https://www.youtube.com/results?search_query=masala+dosa", "breakup": "Batter: ₹25, Potato filling: ₹20"},
    {"name": "Egg Bhurji + Pav", "type": "Breakfast", "cal": 350, "cook_time": 15, "order_time": 25, "cost": 45, "order": 140, "veg": False, "recipe_url": "https://www.youtube.com/results?search_query=egg+bhurji+pav", "breakup": "Eggs (3): ₹21, Pav/Butter: ₹15, Onion: ₹9"},
    {"name": "Upma", "type": "Breakfast", "cal": 240, "cook_time": 15, "order_time": 25, "cost": 25, "order": 80, "veg": True, "recipe_url": "https://www.youtube.com/results?search_query=upma+recipe", "breakup": "Suji: ₹10, Veggies/Ghee: ₹15"},
    {"name": "Bread Omlette", "type": "Breakfast", "cal": 310, "cook_time": 10, "order_time": 20, "cost": 40, "order": 120, "veg": False, "recipe_url": "https://www.youtube.com/results?search_query=bread+omlette", "breakup": "Eggs (2): ₹14, Bread: ₹10, Butter/Veg: ₹16"},
    {"name": "Sabudana Khichdi", "type": "Breakfast", "cal": 340, "cook_time": 25, "order_time": 35, "cost": 50, "order": 150, "veg": True, "recipe_url": "https://www.youtube.com/results?search_query=sabudana+khichdi", "breakup": "Sabudana: ₹30, Peanuts/Potato: ₹20"},
    {"name": "Moong Dal Cheela", "type": "Breakfast", "cal": 230, "cook_time": 20, "order_time": 30, "cost": 35, "order": 130, "veg": True, "recipe_url": "https://www.youtube.com/results?search_query=moong+dal+cheela", "breakup": "Moong Dal: ₹20, Filling/Spices: ₹15"},
    {"name": "Methi Thepla", "type": "Breakfast", "cal": 260, "cook_time": 30, "order_time": 40, "cost": 30, "order": 110, "veg": True, "recipe_url": "https://www.youtube.com/results?search_query=methi+thepla", "breakup": "Atta/Methi: ₹20, Curd/Oil: ₹10"},
    {"name": "Vermicelli Upma", "type": "Breakfast", "cal": 250, "cook_time": 15, "order_time": 25, "cost": 30, "order": 90, "veg": True, "recipe_url": "https://www.youtube.com/results?search_query=semiya+upma", "breakup": "Vermicelli: ₹15, Veggies: ₹15"},

    # LUNCH (13-32)
    {"name": "Rajma Chawal", "type": "Lunch", "cal": 450, "cook_time": 55, "order_time": 45, "cost": 65, "order": 240, "veg": True, "recipe_url": "https://www.youtube.com/results?search_query=rajma+chawal", "breakup": "Rajma: ₹40, Rice: ₹15, Gravy: ₹10"},
    {"name": "Dal Tadka + Rice", "type": "Lunch", "cal": 410, "cook_time": 30, "order_time": 35, "cost": 50, "order": 180, "veg": True, "recipe_url": "https://www.youtube.com/results?search_query=dal+tadka", "breakup": "Dal: ₹25, Rice: ₹15, Tadka: ₹10"},
    {"name": "Chicken Curry + Roti", "type": "Lunch", "cal": 520, "cook_time": 60, "order_time": 50, "cost": 180, "order": 380, "veg": False, "recipe_url": "https://www.youtube.com/results?search_query=chicken+curry", "breakup": "Chicken: ₹140, Gravy: ₹40"},
    {"name": "Chole Bhature", "type": "Lunch", "cal": 700, "cook_time": 50, "order_time": 35, "cost": 70, "order": 210, "veg": True, "recipe_url": "https://www.youtube.com/results?search_query=chole+bhature", "breakup": "Chole: ₹40, Maida/Oil: ₹30"},
    {"name": "Kadai Paneer + Naan", "type": "Lunch", "cal": 580, "cook_time": 40, "order_time": 45, "cost": 140, "order": 320, "veg": True, "recipe_url": "https://www.youtube.com/results?search_query=kadai+paneer", "breakup": "Paneer: ₹90, Capsicum/Gravy: ₹30, Flour: ₹20"},
    {"name": "Veg Thali", "type": "Lunch", "cal": 650, "cook_time": 75, "order_time": 45, "cost": 120, "order": 280, "veg": True, "recipe_url": "https://www.youtube.com/results?search_query=veg+thali+recipe", "breakup": "Dal/Veg/Rice/Roti: ₹120"},
    {"name": "Egg Curry + Rice", "type": "Lunch", "cal": 480, "cook_time": 35, "order_time": 35, "cost": 60, "order": 190, "veg": False, "recipe_url": "https://www.youtube.com/results?search_query=egg+curry", "breakup": "Eggs (4): ₹28, Gravy/Rice: ₹32"},
    {"name": "Bhindi Masala + Roti", "type": "Lunch", "cal": 320, "cook_time": 25, "order_time": 35, "cost": 45, "order": 160, "veg": True, "recipe_url": "https://www.youtube.com/results?search_query=bhindi+masala", "breakup": "Bhindi: ₹25, Roti/Spices: ₹20"},
    {"name": "Butter Chicken + Roti", "type": "Lunch", "cal": 680, "cook_time": 50, "order_time": 45, "cost": 220, "order": 450, "veg": False, "recipe_url": "https://www.youtube.com/results?search_query=butter+chicken", "breakup": "Chicken: ₹150, Butter/Cream: ₹50, Roti: ₹20"},
    {"name": "Fish Curry + Rice", "type": "Lunch", "cal": 540, "cook_time": 45, "order_time": 50, "cost": 250, "order": 480, "veg": False, "recipe_url": "https://www.youtube.com/results?search_query=fish+curry+rice", "breakup": "Fish: ₹200, Coconut/Rice: ₹50"},
    {"name": "Lemon Rice + Curd", "type": "Lunch", "cal": 380, "cook_time": 20, "order_time": 30, "cost": 40, "order": 140, "veg": True, "recipe_url": "https://www.youtube.com/results?search_query=lemon+rice", "breakup": "Rice: ₹20, Peanut/Lemon: ₹10, Curd: ₹10"},
    {"name": "Kadhi Pakora + Rice", "type": "Lunch", "cal": 510, "cook_time": 45, "order_time": 40, "cost": 50, "order": 180, "veg": True, "recipe_url": "https://www.youtube.com/results?search_query=kadhi+pakora", "breakup": "Besan/Dahi: ₹30, Rice: ₹15, Oil: ₹5"},
    {"name": "Baingan Bharta + Roti", "type": "Lunch", "cal": 340, "cook_time": 40, "order_time": 40, "cost": 45, "order": 160, "veg": True, "recipe_url": "https://www.youtube.com/results?search_query=baingan+bharta", "breakup": "Eggplant: ₹20, Roti/Veggies: ₹25"},
    {"name": "Mix Veg + Roti", "type": "Lunch", "cal": 360, "cook_time": 30, "order_time": 35, "cost": 55, "order": 180, "veg": True, "recipe_url": "https://www.youtube.com/results?search_query=mix+veg+recipe", "breakup": "Seasonal Veg: ₹35, Roti: ₹20"},
    {"name": "Gobi Matar + Roti", "type": "Lunch", "cal": 330, "cook_time": 25, "order_time": 35, "cost": 40, "order": 150, "veg": True, "recipe_url": "https://www.youtube.com/results?search_query=gobi+matar", "breakup": "Gobi/Matar: ₹25, Roti: ₹15"},
    {"name": "Aloo Matar + Rice", "type": "Lunch", "cal": 410, "cook_time": 30, "order_time": 35, "cost": 45, "order": 170, "veg": True, "recipe_url": "https://www.youtube.com/results?search_query=aloo+matar+curry", "breakup": "Veg: ₹25, Rice: ₹15, Spices: ₹5"},
    {"name": "Jeera Rice + Dal Fry", "type": "Lunch", "cal": 430, "cook_time": 25, "order_time": 30, "cost": 55, "order": 190, "veg": True, "recipe_url": "https://www.youtube.com/results?search_query=jeera+rice+dal+fry", "breakup": "Dal: ₹25, Basmati Rice: ₹25, Ghee: ₹5"},
    {"name": "Paneer Bhurji + Roti", "type": "Lunch", "cal": 490, "cook_time": 20, "order_time": 30, "cost": 110, "order": 240, "veg": True, "recipe_url": "https://www.youtube.com/results?search_query=paneer+bhurji", "breakup": "Paneer (200g): ₹80, Veg/Roti: ₹30"},
    {"name": "Chana Masala + Roti", "type": "Lunch", "cal": 420, "cook_time": 40, "order_time": 35, "cost": 50, "order": 190, "veg": True, "recipe_url": "https://www.youtube.com/results?search_query=chana+masala", "breakup": "Chana: ₹25, Gravy: ₹15, Roti: ₹10"},
    {"name": "Veg Pulav", "type": "Lunch", "cal": 380, "cook_time": 30, "order_time": 35, "cost": 60, "order": 200, "veg": True, "recipe_url": "https://www.youtube.com/results?search_query=veg+pulav", "breakup": "Basmati: ₹25, Veg/Ghee: ₹35"},

    # DINNER (33-50)
    {"name": "Moong Dal Khichdi", "type": "Dinner", "cal": 310, "cook_time": 25, "order_time": 35, "cost": 30, "order": 150, "veg": True, "recipe_url": "https://www.youtube.com/results?search_query=khichdi", "breakup": "Dal: ₹15, Rice: ₹10, Ghee: ₹5"},
    {"name": "Mutton Curry", "type": "Dinner", "cal": 650, "cook_time": 90, "order_time": 60, "cost": 450, "order": 850, "veg": False, "recipe_url": "https://www.youtube.com/results?search_query=mutton+curry", "breakup": "Mutton: ₹400, Gravy: ₹50"},
    {"name": "Palak Paneer + Roti", "type": "Dinner", "cal": 460, "cook_time": 40, "order_time": 40, "cost": 120, "order": 280, "veg": True, "recipe_url": "https://www.youtube.com/results?search_query=palak+paneer", "breakup": "Paneer: ₹70, Palak: ₹30, Roti: ₹20"},
    {"name": "Veg Biryani", "type": "Dinner", "cal": 480, "cook_time": 50, "order_time": 45, "cost": 90, "order": 300, "veg": True, "recipe_url": "https://www.youtube.com/results?search_query=veg+biryani", "breakup": "Rice: ₹30, Veg/Ghee: ₹60"},
    {"name": "Chicken Biryani", "type": "Dinner", "cal": 620, "cook_time": 60, "order_time": 45, "cost": 180, "order": 400, "veg": False, "recipe_url": "https://www.youtube.com/results?search_query=chicken+biryani", "breakup": "Chicken: ₹120, Rice/Masala: ₹60"},
    {"name": "Tinda Masala + Roti", "type": "Dinner", "cal": 290, "cook_time": 25, "order_time": 40, "cost": 40, "order": 150, "veg": True, "recipe_url": "https://www.youtube.com/results?search_query=tinda+masala", "breakup": "Veg: ₹25, Roti: ₹15"},
    {"name": "Lauki Kofta + Roti", "type": "Dinner", "cal": 410, "cook_time": 45, "order_time": 45, "cost": 50, "order": 200, "veg": True, "recipe_url": "https://www.youtube.com/results?search_query=lauki+kofta", "breakup": "Lauki/Besan: ₹25, Gravy/Roti: ₹25"},
    {"name": "Dhaba Dal + Garlic Naan", "type": "Dinner", "cal": 550, "cook_time": 40, "order_time": 45, "cost": 80, "order": 250, "veg": True, "recipe_url": "https://www.youtube.com/results?search_query=dhaba+style+dal", "breakup": "Dal: ₹30, Naan: ₹40, Ghee: ₹10"},
    {"name": "Prawn Curry + Rice", "type": "Dinner", "cal": 520, "cook_time": 40, "order_time": 50, "cost": 300, "order": 550, "veg": False, "recipe_url": "https://www.youtube.com/results?search_query=prawn+curry", "breakup": "Prawns: ₹250, Coconut/Rice: ₹50"},
    {"name": "Malai Kofta + Roti", "type": "Dinner", "cal": 630, "cook_time": 50, "order_time": 45, "cost": 130, "order": 340, "veg": True, "recipe_url": "https://www.youtube.com/results?search_query=malai+kofta", "breakup": "Paneer/Potato: ₹60, Creamy Gravy: ₹50, Roti: ₹20"},
    {"name": "Chicken Saagwala", "type": "Dinner", "cal": 490, "cook_time": 45, "order_time": 45, "cost": 170, "order": 360, "veg": False, "recipe_url": "https://www.youtube.com/results?search_query=chicken+saagwala", "breakup": "Chicken: ₹130, Spinach Gravy: ₹40"},
    {"name": "Matar Paneer + Roti", "type": "Dinner", "cal": 470, "cook_time": 35, "order_time": 35, "cost": 110, "order": 260, "veg": True, "recipe_url": "https://www.youtube.com/results?search_query=matar+paneer", "breakup": "Paneer: ₹75, Peas/Gravy: ₹20, Roti: ₹15"},
    {"name": "Aloo Shimla Mirch", "type": "Dinner", "cal": 310, "cook_time": 20, "order_time": 35, "cost": 40, "order": 160, "veg": True, "recipe_url": "https://www.youtube.com/results?search_query=aloo+shimla+mirch", "breakup": "Veggies: ₹25, Roti: ₹15"},
    {"name": "Soya Chaap Masala", "type": "Dinner", "cal": 450, "cook_time": 40, "order_time": 40, "cost": 90, "order": 240, "veg": True, "recipe_url": "https://www.youtube.com/results?search_query=soya+chaap+masala", "breakup": "Chaap: ₹50, Gravy: ₹30, Roti: ₹10"},
    {"name": "Egg Fried Rice", "type": "Dinner", "cal": 440, "cook_time": 20, "order_time": 25, "cost": 50, "order": 180, "veg": False, "recipe_url": "https://www.youtube.com/results?search_query=egg+fried+rice", "breakup": "Rice: ₹20, Eggs (3): ₹21, Veggies/Sauce: ₹9"},
    {"name": "Mushroom Masala", "type": "Dinner", "cal": 380, "cook_time": 30, "order_time": 40, "cost": 100, "order": 260, "veg": True, "recipe_url": "https://www.youtube.com/results?search_query=mushroom+masala", "breakup": "Mushrooms: ₹60, Gravy: ₹30, Roti: ₹10"},
    {"name": "Dum Aloo + Roti", "type": "Dinner", "cal": 460, "cook_time": 50, "order_time": 45, "cost": 55, "order": 210, "veg": True, "recipe_url": "https://www.youtube.com/results?search_query=dum+aloo", "breakup": "Potatoes: ₹20, Gravy: ₹25, Roti: ₹10"},
    {"name": "Kathal Curry + Roti", "type": "Dinner", "cal": 390, "cook_time": 55, "order_time": 50, "cost": 60, "order": 220, "veg": True, "recipe_url": "https://www.youtube.com/results?search_query=kathal+curry", "breakup": "Jackfruit: ₹40, Gravy: ₹20"}
]
df = pd.DataFrame(meals_data)

st.set_page_config(page_title="MealBrain AI", layout="wide")

# --- SIDEBAR: FAMILY COMPOSITION & PANTRY ---
with st.sidebar:
    st.header("👥 Family Members")
    adults = st.number_input("Number of Adults", min_value=1, value=2)
    kids = st.number_input("Number of Kids", min_value=0, value=1)
    
    st.header("🥗 Preferences")
    diet = st.radio("Diet", ["Veg Only", "Everything"])
    goal = st.select_slider("Portion Size", ["Light", "Balanced", "Heavy"])
    
    st.header("🏠 Pantry Mode")
    have_staples = st.checkbox("I have Rice/Atta/Oil/Spices", value=False)
    
    # Kids count as 0.6 portion
    effective_headcount = adults + (kids * 0.6)
    pantry_discount = 0.20 if have_staples else 0.0

# --- LOGIC ---
if 'meal' not in st.session_state: st.session_state.meal = None

f_df = df.copy()
if diet == "Veg Only": f_df = f_df[f_df['veg'] == True]
if goal == "Light": f_df = f_df[f_df['cal'] < 350]
elif goal == "Heavy": f_df = f_df[f_df['cal'] > 500]

# --- MAIN INTERFACE ---
st.title("🍲 MealBrain AI")
c1, c2, _ = st.columns([1, 1, 4])
if c1.button("🚀 Get Meal") or c2.button("🔄 Suggest Another"):
    if not f_df.empty:
        st.session_state.meal = f_df.sample(n=1).iloc[0]

if st.session_state.meal is not None:
    m = st.session_state.meal
    st.subheader(f"Recommended: {m['name']}")
    
    # Calculations
    unit_cook_cost = m['cost'] * (1 - pantry_discount)
    total_cook = int(unit_cook_cost * effective_headcount)
    total_order = int(m['order'] * effective_headcount)
    total_savings = total_order - total_cook
    total_cal = int(m['cal'] * effective_headcount)

    st.markdown("---")

    # --- ROW 1: COOK AT HOME ---
    st.markdown("### 🏠 Option 1: Cook at Home")
    h1, h2, h3, h4, h5 = st.columns([1, 1, 1, 1, 2])
    
    h1.metric("Cook Time", f"{m['cook_time']}m")
    h1.link_button("📺 Recipe Video", m['recipe_url'], use_container_width=True)
    
    with h2:
        st.metric("Total Cost", f"₹{total_cook}")
        with st.popover("💰 Price Breakup"):
            st.write(f"For {adults} Adults & {kids} Kids:")
            st.write(m['breakup']) # Standardized key used here
            if have_staples: st.success("Pantry Discount Applied!")

    h3.metric("Calories", f"{total_cal} kcal")
    h4.metric("Savings", f"₹{total_savings}", f"{int((total_savings/total_order)*100)}% Saved")
    
    blinkit_link = f"https://www.google.com/search?q=buy+{m['name'].replace(' ', '+')}+ingredients+on+Blinkit"
    h5.link_button("🛒 Shop (Blinkit)", blinkit_link, use_container_width=True)

    st.divider()

    # --- ROW 2: ORDER ONLINE ---
    st.markdown("### 🛵 Option 2: Order Online")
    o1, o2, o3, o4, o5 = st.columns([1, 1, 1, 1, 2])
    
    o1.metric("Delivery", f"{m['order_time']}m")
    o2.metric("Total Cost", f"₹{total_order}")
    o3.metric("Calories", f"{total_cal} kcal")
    o4.metric("Type", m['type'])
    
    zomato_link = f"https://www.google.com/search?q=order+{m['name'].replace(' ', '+')}+from+Zomato"
    o5.link_button("🥡 Order (Zomato)", zomato_link, use_container_width=True)

else:
    st.info("Set your preferences and click 'Get Meal' to start.")

st.caption("v2.3 | 50 Dishes Loaded | Family Logic Enabled | No-Image Stability")
