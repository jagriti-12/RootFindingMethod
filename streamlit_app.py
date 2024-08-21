import streamlit as st
import requests
import math

# Streamlit app
def main():
    st.title("Root Finding Methods")

    method = st.selectbox("Choose the method", ["Bisection Method", "Newton-Raphson Method", "Secant Method"])

    func_str = st.text_input("Enter the function (in terms of x, e.g., 'x**2 - 4', 'math.sin(x)'):")

    if not func_str:
        st.error("Function input cannot be empty.")
        return

    tol = st.number_input("Enter the tolerance (tol):", value=1e-6, format="%.10f")

    data = {
        "method": method,
        "func_str": func_str,
        "tol": tol
    }

    if method == "Bisection Method":
        a = st.number_input("Enter the start of the interval (a):")
        b = st.number_input("Enter the end of the interval (b):")
        data.update({"a": a, "b": b})

    elif method == "Newton-Raphson Method":
        derivative_str = st.text_input("Enter the derivative of the function (in terms of x, e.g., '2*x', 'math.cos(x)'):")
        if not derivative_str:
            st.error("Derivative input cannot be empty.")
            return
        initial_guess = st.number_input("Enter the initial guess:")
        data.update({"derivative_str": derivative_str, "initial_guess": initial_guess})

    elif method == "Secant Method":
        x0 = st.number_input("Enter the first initial guess (x0):")
        x1 = st.number_input("Enter the second initial guess (x1):")
        data.update({"x0": x0, "x1": x1})

    if st.button("Compute Root"):
        try:
            response = requests.post('http://127.0.0.1:5000/compute_root', json=data)
            if response.status_code == 200:
                result = response.json()
                st.success(f"Root: {result['root']}")
            else:
                st.error(f"Error: {response.status_code}")
                st.write(response.text)
        except requests.exceptions.RequestException as e:
            st.error(f"Request failed: {e}")

if __name__ == "__main__":
    main()
