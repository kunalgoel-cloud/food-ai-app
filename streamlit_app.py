import streamlit as st
import pandas as pd

# --- REALISTIC DATABASE (Unique Times & Costs) ---
meals_data = [
    {"name": "Veg Poha", "type": "Breakfast", "vibe": "Quick", "cal": 250, "cook_time": 15, "order_time": 25, "cost": 35, "order": 90, "tags": "light, healthy, poha, rice", "veg": True},
    {"name": "Paneer Sandwich", "type": "Breakfast", "vibe": "Quick", "cal": 320, "cook_time": 10, "order_time": 30, "cost": 85, "order": 180, "tags": "protein, paneer, sandwich", "veg": True},
    {"name": "Rajma Chawal", "type": "Lunch", "vibe": "Relaxed", "cal": 450, "cook_time": 55, "order_time": 45, "cost": 65, "order": 240, "tags": "protein, beans, rice, family", "veg": True},
    {"name": "Dal Tadka + Rice", "type": "Lunch", "vibe": "Quick", "cal": 410, "cook_time": 30, "order_time": 35, "cost": 50, "order": 180, "tags": "light, comfort, dal, rice", "veg": True},
    {"name": "Egg Curry", "type": "Dinner", "vibe": "Quick", "cal": 380, "cook_time": 35, "order_time": 40, "cost": 55, "order": 210, "tags": "protein, eggs, spicy", "veg": False},
    {"name": "Moong Dal Khichdi", "type": "Dinner", "vibe": "Quick", "cal": 320, "cook_time": 25, "order_time": 35, "cost": 35, "order": 160, "tags": "light, comfort, dal", "veg": True},
    {"name": "Chicken Curry", "type": "Lunch", "vibe": "Relaxed", "cal": 520, "cook_time": 60, "order_time": 50, "cost": 180, "order": 380, "tags": "protein, chicken, spicy", "veg": False},
    {"name": "Aloo Paratha", "type": "Breakfast", "vibe": "Relaxed", "cal": 310, "cook_time": 25, "order_time": 35, "cost": 30, "order": 120, "tags": "filling, potato, wheat", "veg": True}
]
df = pd.DataFrame(meals_data)

st.set_page_config(page_title="MealBrain AI", layout="wide")

# --- SIDEBAR: INPUT FORM ---
with st.sidebar:
    st.title("⚙️ Personalize")
    headcount = st.number_input("Headcount (People)", min_value=1, max_value=10, value=1)
    diet = st.radio("Diet Preference", ["Veg Only", "Everything"])
    goal = st.select_slider("Health Goal", ["Light", "Balanced", "Cheat Day"])
    vibe = st.radio("Vibe", ["Quick", "Relaxed"])

st.title("🍲 MealBrain AI")
user_input = st.text_input("Craving something specific?", placeholder="e.g. 'Rice' or 'High Protein'")

# --- LOGIC: FILTER & SELECTION ---
f_df = df.copy()
if diet == "Veg Only": f_df = f_df[f_df['veg'] == True]
if goal == "Light": f_df = f_df[f_df['cal'] < 300]
elif goal == "Balanced": f_df = f_df[(f_df['cal'] >= 300) & (f_df['cal'] <= 450)]
if vibe == "Quick": f_df = f_df[f_df['cook_time'] <= 30]

if user_input:
    f_df = f_df[f_df.apply(lambda x: user_input.lower() in x['name'].lower() or user_input.lower() in x['tags'], axis=1)]

# --- ACTION BUTTONS ---
c1, c2, _ = st.columns([1, 1, 4])
get_meal = c1.button("🚀 Get Meal")
suggest_next = c2.button("🔄 Try Another")

if get_meal or suggest_next:
    if not f_df.empty:
        winner = f_df.sample(n=1).iloc[0]
        
        st.header(f"Today's Recommendation: {winner['name']}")
        
        # Display Static Food Image (Avoids the 'statue' bug)
        img_url = f"https://img.freepik.com/free-photo/delicious-indian-food-tray_23-2148723505.jpg" # High-quality generic fallback
        st.image(img_url, use_container_width=True, caption=f"Visualizing your {winner['name']}...")

        # --- OPTION 1: COOK AT HOME ---
        st.subheader("🏠 Option 1: Cook at Home")
        h1, h2, h3, h4, h5 = st.columns([1, 1, 1, 1, 2])
        h1.metric("Cook Time", f"{winner['cook_time']}m")
        h2.metric("Total Cost", f"₹{winner['cost'] * headcount}")
        h3.metric("Calories", f"{winner['cal'] * headcount}kcal")
        
        # Restoration of Savings Logic
        savings = (winner['order'] - winner['cost']) * headcount
        h4.metric("Your Savings", f"₹{savings}", f"{int((savings/(winner['order']*headcount))*100)}%")
        
        blinkit_url = f"https://www.google.com/search?q=buy+{winner['name'].replace(' ', '+')}+ingredients+on+Blinkit"
        h5.link_button("🛒 Shop on Blinkit", blinkit_url, use_container_width=True)

        st.divider()

        # --- OPTION 2: ORDER ONLINE ---
        st.subheader("🛵 Option 2: Order Online")
        o1, o2, o3, o4, o5 = st.columns([1, 1, 1, 1, 2])
        o1.metric("Delivery", f"{winner['order_time']}m")
        o2.metric("Total Cost", f"₹{winner['order'] * headcount}")
        o3.metric("Calories", f"{winner['cal'] * headcount}kcal")
        o4.metric("Status", "Ready-to-eat")
        
        zomato_url = f"https://www.google.com/search?q=order+{winner['name'].replace(' ', '+')}+on+Zomato"
        o5.link_button("🥡 Order on Zomato", zomato_url, use_container_width=True)

    else:
        st.error("No results! Try selecting 'Everything' or 'Cheat Day' to see more options.")

st.divider()
st.caption("v1.6 | Realistic Times | Savings Metric Restored")
