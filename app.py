from flask import Flask, render_template, request

app = Flask(__name__)

# Simulated user database with usernames, passwords, and bank balances
users = {
    "ponmuthu": {"password": "123456789", "balance": 5050},
}

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/sql_injection', methods=['POST'])
def sql_injection():
    username = request.form.get('username')
    password = request.form.get('password')
    
    # Simulated SQL query
    simulated_query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'"
    
    # Log and provide background info
    log_message = f"Simulated SQL Query: {simulated_query}"
    action_message = ""
    background_info = ""

    # Check for SQL injection patterns
    if any(sql_injection_pattern in password for sql_injection_pattern in ["' OR '1'='1 --", "' OR 1=1 --", "1=1", "' OR 'x'='x", "--", "OR 1=1", "1=1 --"]):
        # Simulate SQL Injection success (bypasses login)
        bank_balance = users["ponmuthu"]["balance"]
        action_message = f"SQL Injection Successful: You have bypassed the login! Your bank balance is ${bank_balance}."
        background_info = "SQL injection detected. The query was modified and bypassed the authentication."
        result = {
            "success": True,
            "message": action_message,
            "log": log_message,
            "background": background_info
        }
    elif username in users and users[username]["password"] == password:
        # Successful login for valid user (normal authentication)
        bank_balance = users[username]["balance"]
        action_message = f"Login Successful! Your bank balance is ${bank_balance}."
        background_info = "Normal login attempt. Database query executed successfully."
        result = {
            "success": True,
            "message": action_message,
            "log": log_message,
            "background": background_info
        }
    else:
        result = {
            "success": False,
            "message": "Invalid username or password.",
            "log": log_message,
            "background": "Invalid login attempt. Database query failed."
        }

    return render_template('result.html', result=result)

if __name__ == '__main__':
    app.run(debug=True)
