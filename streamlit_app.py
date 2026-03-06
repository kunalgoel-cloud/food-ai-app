import streamlit as st
import pandas as pd

# 1. THE EXPANDED DATABASE (Phase 1.2)
meals_data = [
    # BREAKFAST
    {"name": "Veg Poha", "type": "Breakfast", "vibe": "Quick", "cal": 250, "cook_time": 15, "order_time": 25, "cost": 35, "order": 90, "tags": "light, healthy, poha, rice, quick", "veg": True},
    {"name": "Paneer Sandwich", "type": "Breakfast", "vibe": "Quick", "cal": 320, "cook_time": 10, "order_time": 30, "cost": 85, "order": 180, "tags": "protein, paneer, sandwich, kids", "veg": True},
    {"name": "Aloo Paratha", "type": "Breakfast", "vibe": "Relaxed", "cal": 280, "cook_time": 30, "order_time": 35, "cost": 25, "order": 70, "tags": "filling, potato, wheat, family", "veg": True},
    {"name": "Moong Dal Chilla", "type": "Breakfast", "vibe": "Quick", "cal": 180, "cook_time": 20, "order_time": 30, "cost": 45, "order": 130, "tags": "protein, healthy, vegan, moong", "veg": True},
    {"name": "Egg Bhurji + Toast", "type": "Breakfast", "vibe": "Quick", "cal": 350, "cook_time": 12, "order_time": 25, "cost": 55, "order": 140, "tags": "protein, eggs, bread, quick", "veg": False},
    
    # LUNCH
    {"name": "Rajma Chawal", "type": "Lunch", "vibe": "Relaxed", "cal": 450, "cook_time": 45, "order_time": 40, "cost": 65, "order": 220, "tags": "protein, beans, rice, family, heavy", "veg": True},
    {"name": "Dal Tadka + Rice", "type": "Lunch", "vibe": "Quick", "cal": 410, "cook_time": 25, "order_time": 30, "cost": 50, "order": 180, "tags": "light, comfort, dal, rice", "veg": True},
    {"name": "Chicken Curry + Roti", "type": "Lunch", "vibe": "Relaxed", "cal": 520, "cook_time": 50, "order_time": 45, "cost": 160, "order": 350, "tags": "protein, chicken, spicy, heavy", "veg": False},
    {"name": "Bhindi Fry + 2 Roti", "type": "Lunch", "vibe": "Quick", "cal": 310, "cook_time": 20, "order_time": 35, "cost": 40, "order": 150, "tags": "fiber, veg, light, okra", "veg": True},
    {"name": "Paneer Butter Masala", "type": "Lunch", "vibe": "Relaxed", "cal": 580, "cook_time": 35, "order_time": 40, "cost": 120, "order": 320, "tags": "rich, paneer, tomato, party", "veg": True},
    
    # SNACKS & BEVERAGES
    {"name": "Roasted Makhana", "type": "Snack", "vibe": "Quick", "cal": 120, "cook_time": 5, "order_time": 15, "cost": 30, "order": 60, "tags": "light, healthy, crunchy, low-cal", "veg": True},
    {"name": "Masala Chai", "type": "Snack", "vibe": "Quick", "cal": 80, "cook_time": 7, "order_time": 20, "cost": 15, "order": 45, "tags": "beverage, tea, hot", "veg": True},
    {"name": "Sprouts Salad", "type": "Snack", "vibe": "Quick", "cal": 150, "cook_time": 10, "order_time": 20, "cost": 35, "order": 110, "tags": "protein, healthy, raw, vegan", "veg": True},
    {"name": "Cold Coffee", "type": "Snack", "vibe": "Quick", "cal": 220, "cook_time": 5, "order_time": 25, "cost": 40, "order": 160, "tags": "beverage, cold, caffeine, sweet", "veg": True},
    
    # DINNER
    {"name": "Moong Dal Khichdi", "type": "Dinner", "vibe": "Quick", "cal": 320, "cook_time": 25, "order_time": 35, "cost": 35, "order": 160, "tags": "light, comfort, sick-day, dal", "veg": True},
    {"name": "Palak Paneer", "type": "Dinner", "vibe": "Relaxed", "cal": 350, "cook_time": 30, "order_time": 40, "cost": 110, "order": 280, "tags": "iron, healthy, paneer, spinach", "veg": True},
    {"name": "Egg Curry", "type": "Dinner", "vibe": "Quick", "cal": 380, "cook_time": 25, "order_time": 35, "cost": 50, "order": 190, "tags": "protein, eggs, spicy", "veg": False},
    {"name": "Lauki Sabzi + Roti", "type": "Dinner", "vibe": "Quick", "cal": 260, "cook_time": 20, "order_time": 35, "cost": 30, "order": 140, "tags": "light, easy-digest, low-cal", "veg": True},
    {"name": "Veg Biryani", "type": "Dinner", "vibe": "Relaxed", "cal": 420, "cook_time": 40, "order_time": 45, "cost": 80, "order": 240, "tags": "rice, heavy, veg, party", "veg": True},
]
df = pd.DataFrame(meals_data)

# --- UI CONFIG ---
st.set_page_config(page_title="MealBrain AI", page_icon="🍲")

st.title("🍲 MealBrain AI")
st.caption("Intelligence Layer v1.2 | Live 2026 Price & Time Estimates")

# --- SIDEBAR INPUTS ---
with st.sidebar:
    st.header("1. Your Profile")
    who = st.selectbox("Who are we feeding?", ["Just Me", "Kids Tiffin", "Family", "Elderly"])
    diet = st.radio("Diet Preference?", ["Veg Only", "Everything"])
    
    st.header("2. Constraints")
    vibe = st.radio("Cooking Vibe?", ["Quick", "Relaxed"])
    goal = st.select_slider("Health Goal", ["Light", "Balanced", "Cheat Day"])

st.subheader("3. Any specific craving?")
user_input = st.text_input("e.g. 'spicy', 'paneer', 'eggs'", placeholder="Search ingredients or flavors...")

# --- RECOMMENDATION LOGIC ---
if st.button("Generate Smart Recommendation"):
    filtered_df = df.copy()

    # Apply Filters
    if diet == "Veg Only":
        filtered_df = filtered_df[filtered_df['veg'] == True]
    
    if goal == "Light":
        filtered_df = filtered_df[filtered_df['cal'] < 300]
    elif goal == "Balanced":
        filtered_df = filtered_df[(filtered_df['cal'] >= 300) & (filtered_df['cal'] <= 450)]

    if user_input:
        filtered_df['score'] = filtered_df.apply(
            lambda x: 10 if user_input.lower() in x['name'].lower() or user_input.lower() in x['tags'] else 0, axis=1
        )
    else:
        filtered_df['score'] = 0

    if not filtered_df.empty:
        # Sort so the highest score match is at the top
        winner = filtered_df.sort_values(by='score', ascending=False).iloc[0]
        
        # --- DISPLAY RESULTS ---
        st.markdown(f"## 🏆 Top Choice: **{winner['name']}**")
        
        # ROW 1: STATS
        st.divider()
        c1, c2, c3 = st.columns(3)
        c1.metric("🔥 Calories", f"{winner['cal']} kcal")
        c2.metric("⏱️ Cook Time", f"{winner['cook_time']} min")
        c3.metric("🚚 Delivery", f"{winner['order_time']} min")

        # ROW 2: MONEY
        st.divider()
        s1, s2, s3 = st.columns(3)
        s1.metric("💰 Home Cost", f"₹{winner['cost']}")
        s2.metric("🥡 App Price", f"₹{winner['order']}")
        savings = winner['order'] - winner['cost']
        s3.metric("📈 Savings", f"₹{savings}", f"{int((savings/winner['order'])*100)}%")

        # RECOMMENDATION CONTEXT
        st.info(f"💡 **Why this?** It's {winner['cal']} calories. Home-prep is {winner['cook_time']}m vs {winner['order_time']}m delivery. You save ₹{savings}!")

        # MONETIZATION BUTTONS
        st.markdown("### 🛒 Take Action")
        col_btn1, col_btn2 = st.columns(2)
        with col_btn1:
            st.button(f"🛒 Shop Ingredients (Blinkit)", use_container_width=True)
        with col_btn2:
            st.button(f"🥡 Order Ready-to-Eat (Zepto)", use_container_width=True)
            
    else:
        st.error("I couldn't find a match! Try choosing 'Balanced' or 'Everything'.")

st.divider()
st.caption("v1.2 Fixed | Standardized Interface")
