import streamlit as st
import mysql.connector

conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="apoorv@sql090",
    database="shopping_cart"
)

cursor = conn.cursor(dictionary=True)

st.set_page_config(
    page_title="Shopping Cart",
    layout="centered"
)

st.title("Shopping Cart")

if "cart" not in st.session_state:
    st.session_state.cart = []

cursor.execute("SELECT * FROM products")
products = cursor.fetchall()

product_names = [product["product_name"] for product in products]

st.subheader("Add Product")

selected_product = st.selectbox(
    "Select Product",
    product_names
)

selected = next(
    product for product in products
    if product["product_name"] == selected_product
)

st.write(f"**Price: ₹{selected['price']:,.2f}**")

if st.button("Add to Cart"):
    st.session_state.cart.append(selected)
    st.success(f"{selected_product} added to cart!")

st.subheader("My Cart")

if len(st.session_state.cart) == 0:

    st.info("Your cart is empty.")

else:

    total = 0

    for i, item in enumerate(st.session_state.cart):

        col1, col2, col3 = st.columns([3, 2, 1])

        with col1:
            st.write(item["product_name"])

        with col2:
            st.write(f"₹{item['price']:,.2f}")

        with col3:
            if st.button("Remove", key=f"remove_{i}"):
                st.session_state.cart.pop(i)
                st.rerun()

        total += float(item["price"])

    st.divider()

    st.subheader(f"Total: ₹{total:,.2f}")