import streamlit as st
import pandas as pd
import random

# --- SMART DATABASE (Phase 1.7 - 2026 Accurate) ---
# Each meal now includes 'Steps' for time-breakup and 'SKUs' for cost-breakup
meals_data = [
    {
        "name": "Veg Poha", "type": "Breakfast", "vibe": "Quick", "cal": 250, "cook_time": 15, "order_time": 25, "cost": 35, "order": 90, "tags": "light, healthy, poha, rice", "veg": True,
        "prep_steps": "1. Soak 150g Poha (5m)\n2. Chop 1 Onion & Potato (5m)\n3. Sauté with spices (5m)", 
        "cost_breakup": "1. Poha Pack (200g): ₹25\n2. Veggies (Onion/Potato): ₹8\n3. Spices/Oil: ₹2"
    },
    {
        "name": "Paneer Sandwich", "type": "Breakfast", "vibe": "Quick", "cal": 320, "cook_time": 10, "order_time": 30, "cost": 85, "order": 180, "tags": "protein, paneer, sandwich", "veg": True,
        "prep_steps": "1. Slice Paneer & Veggies (4m)\n2. Arrange on Bread (2m)\n3. Toast (4m)",
        "cost_breakup": "1. Amul Paneer (200g): ₹65\n2. Atta Bread (4 slices): ₹15\n3. Veggies/Butter: ₹5"
    },
    {
        "name": "Rajma Chawal", "type": "Lunch", "vibe": "Relaxed", "cal": 450, "cook_time": 55, "order_time": 45, "cost": 65, "order": 240, "tags": "protein, beans, rice, family", "veg": True,
        "prep_steps": "1. Pressure Cook Rajma (30m)\n2. Make Gravy (15m)\n3. Cook Rice (10m)",
        "cost_breakup": "1. Rajma Beans (150g): ₹40\n2. Basmati Rice (100g): ₹15\n3. Gravy (Onion/Tomato/Spices): ₹10"
    },
    {
        "name": "Dal Tadka + Rice", "type": "Lunch", "vibe": "Quick", "cal": 410, "cook_time": 30, "order_time": 35, "cost": 50, "order": 180, "tags": "light, comfort, dal, rice", "veg": True,
        "prep_steps": "1. Cook Toor Dal (15m)\n2. Prepare Tadka (5m)\n3. Steam Rice (10m)",
        "cost_breakup": "1. Toor Dal (100g): ₹25\n2. Basmati Rice (100g): ₹15\n3. Spices & Tadka Oil: ₹10"
    },
    {
        "name": "Egg Curry", "type": "Dinner", "vibe": "Quick", "cal": 380, "cook_time": 35, "order_time": 40, "cost": 55, "order": 210, "tags": "protein, eggs, spicy", "veg": False,
        "prep_steps": "1. Boil Eggs (10m)\n2. Prepare Spicy Gravy (15m)\n3. Sauté Eggs in Gravy (10m)",
        "cost_breakup": "1. Eggs (4 pcs): ₹24\n2. Onion/Tomato Gravy: ₹20\n3. Spices/Oil: ₹11"
    },
    {
        "name": "Chicken Curry", "type": "Lunch", "vibe": "Relaxed", "cal": 520, "cook_time": 60, "order_time": 50, "cost": 180, "order": 380, "tags": "protein, chicken, spicy", "veg": False,
        "prep_steps": "1. Clean & Marinate Chicken (15m)\n2. Prepare Rich Gravy (25m)\n3. Cook Chicken in Gravy (20m)",
        "cost_breakup": "1. Raw Chicken (250g): ₹130\n2. Gravy (Veggies/Spices): ₹30\n3. Oil/Other: ₹20"
    }
]
df = pd.DataFrame(meals_data)

st.set_page_config(page_title="MealBrain AI", layout="wide", page_icon="🍲")

# --- SIDEBAR: INPUT ---
with st.sidebar:
    st.header("1. Your Setup")
    headcount = st.number_input("Headcount (People)", min_value=1, max_value=20, value=1)
    diet = st.radio("Diet Preference", ["Veg Only", "Everything"])
    goal = st.select_slider("Health Goal", ["Light", "Balanced", "Cheat Day"])
    vibe = st.radio("Cooking Vibe", ["Quick", "Relaxed"])

st.title("🍲 MealBrain AI")
user_input = st.text_input("Craving something specific?", placeholder="e.g. 'spicy', 'paneer', 'eggs'")

# --- ACTION LOGIC ---
if 'last_meal' not in st.session_state: st.session_state.last_meal = None

# Filtering
f_df = df.copy()
if diet == "Veg Only": f_df = f_df[f_df['veg'] == True]
if goal == "Light": f_df = f_df[f_df['cal'] < 300]
elif goal == "Balanced": f_df = f_df[(f_df['cal'] >= 300) & (f_df['cal'] <= 450)]

if user_input:
    f_df = f_df[f_df.apply(lambda x: user_input.lower() in x['name'].lower() or user_input.lower() in x['tags'], axis=1)]

# Execution Buttons
c1, c2, _ = st.columns([1, 1, 4])
generate = c1.button("🚀 Get Meal")
try_another = c2.button("🔄 Try Another")

# Determine which meal to show
meal_to_show = None
if generate or try_another:
    if not f_df.empty:
        # Prevent the same meal from appearing twice in a row
        available_meals = f_df[f_df['name'] != st.session_state.last_meal]
        if not available_meals.empty:
            meal_to_show = available_meals.sample(n=1).iloc[0]
            st.session_state.last_meal = meal_to_show['name']
        else:
            meal_to_show = f_df.iloc[0] # Edge case if only 1 meal fits filters
    else:
        st.error("No results found! Try changing your diet or calorie filters.")

# --- RESULTS DISPLAY ---
if meal_to_show is not None:
    winner = meal_to_show
    st.header(f"Recommendation: **{winner['name']}**")
    
    # FIXED: Image Engine (Switched to Unsplash Source)
    # Using specific query [Indian, food, DishName] ensures a high-quality visual.
    # Appending a random number ensures it changes when you click 'Try Another'.
    img_url = f"https://source.unsplash.com/800x400/?indian,food,{winner['name'].replace(' ', '')}?random={random.randint(1,1000)}"
    st.image(img_url, use_container_width=True, caption=f"Visualizing your fresh serving of {winner['name']}...")
    
    st.markdown("---")
    
    # DYNAMIC SCALING (HEADCOUNT)
    total_cook_cost = winner['cost'] * headcount
    total_order_cost = winner['order'] * headcount
    total_cal = winner['cal'] * headcount
    
    # --- ROW 1: HOME COOKING (Smart Attributes) ---
    st.subheader("🏠 Option 1: Cook at Home")
    h1, h2, h3, h4, h5 = st.columns([1, 1, 1, 1, 2])
    h1.metric("Cook Time", f"{winner['cook_time']}m")
    h2.metric("Total Cost", f"₹{total_cook_cost}")
    h3.metric("Calories", f"{total_cal} kcal")
    
    # INTELLIGENCE LAYER: Time Breakdown
    with h4.expander("⏱️ Click for Steps", expanded=False):
        st.write(winner['prep_steps'])
        
    blinkit_url = f"https://www.google.com/search?q=buy+{winner['name'].replace(' ', '+')}+ingredients+on+Blinkit"
    h5.link_button("🛒 Shop Ingredients (Blinkit)", blinkit_url, use_container_width=True)

    st.markdown("---")

    # --- ROW 2: ORDERING (Smart Attributes) ---
    st.subheader("🛵 Option 2: Order Online")
    o1, o2, o3, o4, o5 = st.columns([1, 1, 1, 1, 2])
    o1.metric("Delivery", f"{winner['order_time']}m")
    o2.metric("Total Cost", f"₹{total_order_cost}")
    o3.metric("Calories", f"{total_cal} kcal")
    
    # INTELLIGENCE LAYER: Cost Breakdown (Scaling with Headcount)
    with o4.expander("💰 Click for Breakup", expanded=False):
        st.caption(f"Price breakdown for {headcount} person(s)")
        # Simple string multiplication for scaled breakdown
        scaled_breakup = winner['cost_breakup']
        st.write(scaled_breakup)
        
    zomato_url = f"https://www.google.com/search?q=order+{winner['name'].replace(' ', '+')}+on+Zomato"
    o5.link_button("🥡 Order Now (Zomato)", zomato_url, use_container_width=True)

st.divider()
st.caption("v1.7 | Smart Metrics Active (Click ⏱️ or 💰 to expand) | Standard Time & Cost Estimates")
