
import streamlit as st
import json
import random
import string
from pathlib import Path

# =========================
# BANK CLASS
# =========================

class Bank:

    database = "data.json"

    # Load data
    @classmethod
    def load_data(cls):
        if Path(cls.database).exists():
            with open(cls.database, "r") as file:
                return json.load(file)
        return []

    # Save data
    @classmethod
    def save_data(cls, data):
        with open(cls.database, "w") as file:
            json.dump(data, file, indent=4)

    # Generate account number
    @classmethod
    def generate_account_number(cls):
        chars = string.ascii_uppercase + string.digits
        return ''.join(random.choices(chars, k=10))

    # Find user
    @classmethod
    def find_user(cls, acc_num, pin):
        data = cls.load_data()

        for user in data:
            if user["account_number"] == acc_num and user["pin"] == pin:
                return user

        return None

    # Create account
    @classmethod
    def create_account(cls, name, age, email, pin):

        if age < 18:
            return "Age must be 18+"

        if len(str(pin)) != 4:
            return "PIN must be 4 digits"

        data = cls.load_data()

        user = {
            "name": name,
            "age": age,
            "email": email,
            "pin": pin,
            "account_number": cls.generate_account_number(),
            "balance": 0
        }

        data.append(user)
        cls.save_data(data)

        return user

    # Deposit money
    @classmethod
    def deposit_money(cls, acc_num, pin, amount):

        data = cls.load_data()

        for user in data:
            if user["account_number"] == acc_num and user["pin"] == pin:

                if amount <= 0:
                    return "Invalid amount"

                user["balance"] += amount
                cls.save_data(data)

                return user["balance"]

        return "Invalid account credentials"

    # Withdraw money
    @classmethod
    def withdraw_money(cls, acc_num, pin, amount):

        data = cls.load_data()

        for user in data:
            if user["account_number"] == acc_num and user["pin"] == pin:

                if amount <= 0:
                    return "Invalid amount"

                if amount > user["balance"]:
                    return "Insufficient balance"

                user["balance"] -= amount
                cls.save_data(data)

                return user["balance"]

        return "Invalid account credentials"

    # Delete account
    @classmethod
    def delete_account(cls, acc_num, pin):

        data = cls.load_data()

        for user in data:
            if user["account_number"] == acc_num and user["pin"] == pin:
                data.remove(user)
                cls.save_data(data)
                return "Account deleted successfully"

        return "Invalid credentials"


# =========================
# STREAMLIT UI
# =========================

st.title("🏦 Banking Management System")

menu = [
    "Create Account",
    "Deposit Money",
    "Withdraw Money",
    "Check Details",
    "Delete Account"
]

choice = st.sidebar.selectbox("Menu", menu)

# =========================
# CREATE ACCOUNT
# =========================

if choice == "Create Account":

    st.subheader("Create New Account")

    name = st.text_input("Enter Name")
    age = st.number_input("Enter Age", min_value=1, step=1)
    email = st.text_input("Enter Email")
    pin = st.text_input("Enter 4 Digit PIN", type="password")

    if st.button("Create Account"):

        result = Bank.create_account(
            name,
            age,
            email,
            pin
        )

        if isinstance(result, dict):
            st.success("Account Created Successfully")

            st.write("### Account Details")
            st.write(f"Name: {result['name']}")
            st.write(f"Account Number: {result['account_number']}")
            st.write(f"Balance: ₹{result['balance']}")

        else:
            st.error(result)

# =========================
# DEPOSIT MONEY
# =========================

elif choice == "Deposit Money":

    st.subheader("Deposit Money")

    acc_num = st.text_input("Account Number")
    pin = st.text_input("PIN", type="password")
    amount = st.number_input("Amount", min_value=1)

    if st.button("Deposit"):

        result = Bank.deposit_money(acc_num, pin, amount)

        if isinstance(result, (int, float)):
            st.success(f"Money Deposited Successfully")
            st.info(f"Updated Balance: ₹{result}")
        else:
            st.error(result)

# =========================
# WITHDRAW MONEY
# =========================

elif choice == "Withdraw Money":

    st.subheader("Withdraw Money")

    acc_num = st.text_input("Account Number")
    pin = st.text_input("PIN", type="password")
    amount = st.number_input("Amount", min_value=1)

    if st.button("Withdraw"):

        result = Bank.withdraw_money(acc_num, pin, amount)

        if isinstance(result, (int, float)):
            st.success("Withdrawal Successful")
            st.info(f"Remaining Balance: ₹{result}")
        else:
            st.error(result)

# =========================
# CHECK DETAILS
# =========================

elif choice == "Check Details":

    st.subheader("Account Details")

    acc_num = st.text_input("Account Number")
    pin = st.text_input("PIN", type="password")

    if st.button("Show Details"):

        user = Bank.find_user(acc_num, pin)

        if user:
            st.write("### User Information")
            st.write(f"Name: {user['name']}")
            st.write(f"Age: {user['age']}")
            st.write(f"Email: {user['email']}")
            st.write(f"Balance: ₹{user['balance']}")
        else:
            st.error("Invalid credentials")

# =========================
# DELETE ACCOUNT
# =========================

elif choice == "Delete Account":

    st.subheader("Delete Account")

    acc_num = st.text_input("Account Number")
    pin = st.text_input("PIN", type="password")

    if st.button("Delete Account"):

        result = Bank.delete_account(acc_num, pin)

        if "successfully" in result:
            st.success(result)
        else:
            st.error(result)


# id="q7w2n1"
# import streamlit as st
# import json
# import random
# import string
# from pathlib import Path

# # =========================================
# # PAGE CONFIG
# # =========================================

# st.set_page_config(
#     page_title="Smart Bank",
#     page_icon="🏦",
#     layout="wide"
# )

# # =========================================
# # CUSTOM CSS
# # =========================================

# st.markdown("""
# <style>

# .main {
#     background: linear-gradient(to right, #141e30, #243b55);
#     color: white;
# }

# h1, h2, h3 {
#     color: #00FFD1;
# }

# .stButton>button {
#     width: 100%;
#     background: linear-gradient(90deg, #00C9FF, #92FE9D);
#     color: black;
#     border-radius: 12px;
#     height: 3em;
#     font-size: 18px;
#     font-weight: bold;
#     border: none;
#     transition: 0.3s;
# }

# .stButton>button:hover {
#     transform: scale(1.03);
#     background: linear-gradient(90deg, #92FE9D, #00C9FF);
# }

# .stTextInput>div>div>input {
#     border-radius: 10px;
# }

# .stNumberInput>div>div>input {
#     border-radius: 10px;
# }

# .card {
#     padding: 25px;
#     border-radius: 20px;
#     background-color: rgba(255,255,255,0.08);
#     box-shadow: 0 8px 20px rgba(0,0,0,0.3);
#     margin-bottom: 20px;
# }

# .sidebar .sidebar-content {
#     background-color: #111827;
# }

# .metric-card {
#     background: rgba(255,255,255,0.08);
#     padding: 20px;
#     border-radius: 15px;
#     text-align: center;
# }

# </style>
# """, unsafe_allow_html=True)

# # =========================================
# # BANK CLASS
# # =========================================

# class Bank:

#     database = "data.json"

#     @classmethod
#     def load_data(cls):
#         if Path(cls.database).exists():
#             with open(cls.database, "r") as file:
#                 return json.load(file)
#         return []

#     @classmethod
#     def save_data(cls, data):
#         with open(cls.database, "w") as file:
#             json.dump(data, file, indent=4)

#     @classmethod
#     def generate_account_number(cls):
#         chars = string.ascii_uppercase + string.digits
#         return ''.join(random.choices(chars, k=10))

#     @classmethod
#     def find_user(cls, acc_num, pin):

#         data = cls.load_data()

#         for user in data:
#             if user["account_number"] == acc_num and user["pin"] == pin:
#                 return user

#         return None

#     @classmethod
#     def create_account(cls, name, age, email, pin):

#         if age < 18:
#             return "Age must be above 18"

#         if len(pin) != 4:
#             return "PIN must be exactly 4 digits"

#         data = cls.load_data()

#         user = {
#             "name": name,
#             "age": age,
#             "email": email,
#             "pin": pin,
#             "account_number": cls.generate_account_number(),
#             "balance": 0
#         }

#         data.append(user)
#         cls.save_data(data)

#         return user

#     @classmethod
#     def deposit_money(cls, acc_num, pin, amount):

#         data = cls.load_data()

#         for user in data:

#             if user["account_number"] == acc_num and user["pin"] == pin:

#                 user["balance"] += amount
#                 cls.save_data(data)

#                 return user["balance"]

#         return None

#     @classmethod
#     def withdraw_money(cls, acc_num, pin, amount):

#         data = cls.load_data()

#         for user in data:

#             if user["account_number"] == acc_num and user["pin"] == pin:

#                 if amount > user["balance"]:
#                     return "Insufficient Balance"

#                 user["balance"] -= amount
#                 cls.save_data(data)

#                 return user["balance"]

#         return None


# # =========================================
# # HEADER
# # =========================================

# st.markdown("""
# <div style='text-align:center;padding:20px'>
#     <h1>🏦 Smart Banking System</h1>
#     <p style='font-size:20px;color:#D1D5DB'>
#         Secure • Fast • Modern Banking Experience
#     </p>
# </div>
# """, unsafe_allow_html=True)

# # =========================================
# # SIDEBAR
# # =========================================

# st.sidebar.image(
#     "https://cdn-icons-png.flaticon.com/512/2830/2830284.png",
#     width=120
# )

# st.sidebar.title("Navigation")

# menu = [
#     "🏠 Home",
#     "🆕 Create Account",
#     "💰 Deposit",
#     "💸 Withdraw",
#     "📄 Account Details"
# ]

# choice = st.sidebar.radio("Go To", menu)

# # =========================================
# # HOME
# # =========================================

# if choice == "🏠 Home":

#     col1, col2, col3 = st.columns(3)

#     with col1:
#         st.markdown("""
#         <div class='metric-card'>
#             <h2>💳</h2>
#             <h3>Secure Banking</h3>
#             <p>Advanced account protection</p>
#         </div>
#         """, unsafe_allow_html=True)

#     with col2:
#         st.markdown("""
#         <div class='metric-card'>
#             <h2>⚡</h2>
#             <h3>Fast Transactions</h3>
#             <p>Instant deposits & withdrawals</p>
#         </div>
#         """, unsafe_allow_html=True)

#     with col3:
#         st.markdown("""
#         <div class='metric-card'>
#             <h2>🌐</h2>
#             <h3>Digital Banking</h3>
#             <p>Bank from anywhere</p>
#         </div>
#         """, unsafe_allow_html=True)

#     st.balloons()

# # =========================================
# # CREATE ACCOUNT
# # =========================================

# elif choice == "🆕 Create Account":

#     st.markdown("<div class='card'>", unsafe_allow_html=True)

#     st.subheader("Create New Account")

#     col1, col2 = st.columns(2)

#     with col1:
#         name = st.text_input("👤 Full Name")
#         age = st.number_input("🎂 Age", min_value=1)

#     with col2:
#         email = st.text_input("📧 Email")
#         pin = st.text_input("🔐 4 Digit PIN", type="password")

#     if st.button("Create Account"):

#         result = Bank.create_account(name, age, email, pin)

#         if isinstance(result, dict):

#             st.success("✅ Account Created Successfully")

#             st.info(f"""
#             Account Number: {result['account_number']}
#             """)

#             st.balloons()

#         else:
#             st.error(result)

#     st.markdown("</div>", unsafe_allow_html=True)

# # =========================================
# # DEPOSIT
# # =========================================

# elif choice == "💰 Deposit":

#     st.markdown("<div class='card'>", unsafe_allow_html=True)

#     st.subheader("Deposit Money")

#     acc_num = st.text_input("💳 Account Number")
#     pin = st.text_input("🔐 PIN", type="password")
#     amount = st.number_input("💵 Amount", min_value=1)

#     if st.button("Deposit Money"):

#         result = Bank.deposit_money(acc_num, pin, amount)

#         if result is not None:

#             st.success("✅ Money Deposited Successfully")

#             st.metric(
#                 label="Updated Balance",
#                 value=f"₹ {result}"
#             )

#         else:
#             st.error("Invalid Credentials")

#     st.markdown("</div>", unsafe_allow_html=True)

# # =========================================
# # WITHDRAW
# # =========================================

# elif choice == "💸 Withdraw":

#     st.markdown("<div class='card'>", unsafe_allow_html=True)

#     st.subheader("Withdraw Money")

#     acc_num = st.text_input("💳 Account Number")
#     pin = st.text_input("🔐 PIN", type="password")
#     amount = st.number_input("💵 Amount", min_value=1)

#     if st.button("Withdraw Money"):

#         result = Bank.withdraw_money(acc_num, pin, amount)

#         if isinstance(result, (int, float)):

#             st.success("✅ Withdrawal Successful")

#             st.metric(
#                 label="Remaining Balance",
#                 value=f"₹ {result}"
#             )

#         else:
#             st.error(result)

#     st.markdown("</div>", unsafe_allow_html=True)

# # =========================================
# # ACCOUNT DETAILS
# # =========================================

# elif choice == "📄 Account Details":

#     st.markdown("<div class='card'>", unsafe_allow_html=True)

#     st.subheader("User Details")

#     acc_num = st.text_input("💳 Account Number")
#     pin = st.text_input("🔐 PIN", type="password")

#     if st.button("Show Details"):

#         user = Bank.find_user(acc_num, pin)

#         if user:

#             col1, col2 = st.columns(2)

#             with col1:
#                 st.metric("👤 Name", user["name"])
#                 st.metric("🎂 Age", user["age"])

#             with col2:
#                 st.metric("💰 Balance", f"₹ {user['balance']}")
#                 st.metric("📧 Email", user["email"])

#             st.success("Account Loaded Successfully")

#         else:
#             st.error("Invalid Credentials")

#     st.markdown("</div>", unsafe_allow_html=True)

# # =========================================
# # FOOTER
# # =========================================

# st.markdown("""
# <hr>
# <center>
#     <h4 style='color:gray'>
#         Made with ❤️ using Streamlit
#     </h4>
# </center>
# """, unsafe_allow_html=True)

