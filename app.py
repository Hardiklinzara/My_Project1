import streamlit as st
import random

st.set_page_config(page_title="Smart E-Commerce", layout="wide")

# -----------------------------
# SESSION INIT
# -----------------------------
# -----------------------------
# SESSION STATE INIT (FIX)
# -----------------------------
if "role" not in st.session_state:
    st.session_state["role"] = None

if "username" not in st.session_state:
    st.session_state["username"] = ""

if "products" not in st.session_state:
    st.session_state["products"] = [
        {
            "id": 1,
            "name": "Running Shoes",
            "price": 1999,
            "image": "https://images.unsplash.com/photo-1542291026-7eec264c27ff"
        },
        {
            "id": 2,
            "name": "T-Shirt",
            "price": 799,
            "image": "https://images.unsplash.com/photo-1521572163474-6864f9cf17ab"
        },
        {
            "id": 3,
            "name": "Jeans",
            "price": 1499,
            "image": "https://images.unsplash.com/photo-1542272604-787c3835535d"
        }
    ]

if "cart" not in st.session_state:
    st.session_state["cart"] = {}
if "cart" not in st.session_state:
    st.session_state.cart = {}

# -----------------------------
# LOGIN
# -----------------------------
def login():
    st.title("🛒 Smart AI E-Commerce")

    st.subheader("Login")
    username = st.text_input("Enter Name")
    role = st.selectbox("Select Role", ["Customer", "Shop Owner"])

    if st.button("Login"):
        if username:
            st.session_state.role = role
            st.session_state.username = username
            st.rerun()
        else:
            st.warning("Enter your name")

# -----------------------------
# PERSONALIZED OFFERS
# -----------------------------
def get_discount():
    return random.choice([5, 10, 15, 20])

# -----------------------------
# CUSTOMER DASHBOARD
# -----------------------------
def customer_dashboard():
    st.title(f"Welcome {st.session_state['username']} 👋")

    # ---------------- SIDEBAR ----------------
    st.sidebar.header("🛒 Cart Summary")

    total = 0
    total_savings = 0
    item_count = sum(st.session_state["cart"].values())

    st.sidebar.write(f"Items: {item_count}")

    # ---------------- SEARCH ----------------
    search = st.text_input("🔍 Search Products")

    st.markdown("## 🔥 Personalized Offers For You")

    # ---------------- GRID ----------------
    cols = st.columns(3)

    for i, product in enumerate(st.session_state["products"]):

        if search and search.lower() not in product["name"].lower():
            continue

        # ---------------- DISCOUNT LOGIC ----------------
        discount = 5

        if product["price"] > 2000:
            discount += 10
        elif product["price"] > 1000:
            discount += 5

        if product["id"] in st.session_state["cart"]:
            discount += 5

        discount = min(discount, 25)
        final_price = int(product["price"] * (1 - discount / 100))
        saved = product["price"] - final_price

        # ---------------- CARD ----------------
        with cols[i % 3]:
            st.image(product["image"], use_container_width=True)

            st.markdown(f"### {product['name']}")

            st.markdown(
                f"""
                ~~₹{product['price']}~~  
                **₹{final_price} ({discount}% OFF)**  
                💸 You save ₹{saved}
                """
            )

            # TAGS (visual improvement)
            if product["price"] > 2000:
                st.caption("⭐ Bestseller")

            if product["id"] in st.session_state["cart"]:
                st.caption("🔥 Extra discount applied")

            if st.button("Add to Cart", key=f"add{i}"):
                if product["id"] in st.session_state["cart"]:
                    st.session_state["cart"][product["id"]] += 1
                else:
                    st.session_state["cart"][product["id"]] = 1
                st.rerun()

    st.divider()

    # ---------------- CART ----------------
    st.markdown("## 🧾 Cart Details")

    if not st.session_state["cart"]:
        st.info("Your cart is empty")
        return

    for pid, qty in st.session_state["cart"].items():
        product = next(p for p in st.session_state["products"] if p["id"] == pid)

        # same discount logic again for accurate total
        discount = 5
        if product["price"] > 2000:
            discount += 10
        elif product["price"] > 1000:
            discount += 5
        discount += 5
        discount = min(discount, 25)

        final_price = int(product["price"] * (1 - discount / 100))

        col1, col2, col3 = st.columns([4,1,1])

        with col1:
            st.write(f"{product['name']} (x{qty}) - ₹{final_price * qty}")

        with col2:
            if st.button("➕", key=f"inc{pid}"):
                st.session_state["cart"][pid] += 1
                st.rerun()

        with col3:
            if st.button("❌", key=f"dec{pid}"):
                st.session_state["cart"][pid] -= 1
                if st.session_state["cart"][pid] <= 0:
                    del st.session_state["cart"][pid]
                st.rerun()

        total += final_price * qty
        total_savings += (product["price"] - final_price) * qty

    st.subheader(f"Total: ₹{total}")
    st.success(f"🎉 You saved ₹{total_savings}")

    if st.button("Clear Cart"):
        st.session_state["cart"] = {}
        st.rerun()
# -----------------------------
# OWNER DASHBOARD
# -----------------------------
def owner_dashboard():
    st.title(f"Shop Owner Panel 👤 ({st.session_state.username})")

    st.header("➕ Add Product")

    name = st.text_input("Product Name")
    price = st.number_input("Price", min_value=0)
    image = st.text_input("Image URL")

    if st.button("Add Product"):
        if name and price and image:
            st.session_state.products.append({
                "id": len(st.session_state.products) + 1,
                "name": name,
                "price": price,
                "image": image
            })
            st.success("Product Added")
            st.rerun()
        else:
            st.warning("Fill all fields")

    st.divider()

    st.header("📦 Your Products")

    cols = st.columns(3)

    for i, product in enumerate(st.session_state.products):
        with cols[i % 3]:
            st.image(product["image"])
            st.write(f"{product['name']} - ₹{product['price']}")

            # 🔴 IMPORTANT: Delete button sirf owner ko dikhe
            if st.button("Delete", key=f"del{i}"):
                st.session_state.products.pop(i)
                st.rerun()


# ----------------------------- CUSTOMER DASHBOARD

   def customer_dashboard():
    st.title("Customer Dashboard 🛍️")

    st.header("Available Products")

    cols = st.columns(3)

    for i, product in enumerate(st.session_state.products):
        with cols[i % 3]:
            st.image(product["image"])
            st.write(f"{product['name']} - ₹{product['price']}")

            # ✅ Sirf view ya cart option
            if st.button("Add to Cart", key=f"cart{i}"):
                st.session_state.cart[product["id"]] = product
                st.success("Added to cart")



# -----------------------------
# MAIN
# -----------------------------
def main():
    if st.session_state.role is None:
        login()
    else:
        st.sidebar.title("Navigation")

        if st.sidebar.button("Logout"):
            st.session_state.role = None
            st.session_state.cart = {}
            st.rerun()

      
        if st.session_state.role == "Customer":
            customer_dashboard()

        elif st.session_state.role == "Owner":
            owner_dashboard()

        else:
            st.error("Invalid role detected")

main()
