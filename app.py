from flask import Flask, request, jsonify
import math

app = Flask(__name__)

# Root-finding methods
def bisection_method(func, a, b, tol=1e-6, max_iter=100):
    if func(a) * func(b) > 0:
        raise ValueError("The function values at the interval endpoints must have opposite signs.")
    iteration = 0 
    while (b - a) / 2 > tol and iteration < max_iter:
        c = (a + b) / 2  # Compute the midpoint
        if func(c) == 0:
            return c  # Found exact root
        elif func(c) * func(a) < 0:
            b = c  # Root lies in the left subinterval [a, c]
        else:
            a = c  # Root lies in the right subinterval [c, b]
        iteration += 1 
    return (a + b) / 2 

def newton_raphson_method(func, func_derivative, initial_guess, tol=1e-6, max_iter=100):
    x = initial_guess
    iteration = 0  
    while abs(func(x)) > tol and iteration < max_iter:
        x = x - func(x) / func_derivative(x)  
        iteration += 1  
    return x 

def secant_method(func, x0, x1, tol=1e-6, max_iter=100):
    x_k_minus_1 = x0
    x_k = x1

    for k in range(max_iter):
        f_k_minus_1 = func(x_k_minus_1)
        f_k = func(x_k)
        x_k_plus_1 = x_k - f_k * (x_k - x_k_minus_1) / (f_k - f_k_minus_1)
        if abs(x_k_plus_1 - x_k) < tol:
            return x_k_plus_1, k + 1  # Return the root and the number of iterations
        x_k_minus_1 = x_k
        x_k = x_k_plus_1

    raise ValueError("Secant method did not converge within the maximum number of iterations.")

@app.route('/compute_root', methods=['POST'])
def compute_root():
    try:
        data = request.json
        print(data)  # Log received data for debugging

        method = data.get('method')
        func_str = data.get('func_str')
        tol = data.get('tol', 1e-6)

        func = eval(f"lambda x: {func_str}")

        if method == "Bisection Method":
            a = data.get('a')
            b = data.get('b')
            result = bisection_method(func, a, b, tol)
        elif method == "Newton-Raphson Method":
            derivative_str = data.get('derivative_str')
            func_derivative = eval(f"lambda x: {derivative_str}")
            initial_guess = data.get('initial_guess')
            result = newton_raphson_method(func, func_derivative, initial_guess, tol)
        elif method == "Secant Method":
            x0 = data.get('x0')
            x1 = data.get('x1')
            result, iterations = secant_method(func, x0, x1, tol)
        else:
            return jsonify({'error': 'Invalid method'}), 400

        return jsonify({'root': result})

    except Exception as e:
        print(f"Error: {e}")  # Log the exception for debugging
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
