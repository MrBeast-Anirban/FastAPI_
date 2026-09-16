from flask import Flask, render_template_string, request

app = Flask(__name__)

# Single-file HTML template combining styles, input form, and results display
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Single File Table Generator</title>
    <style>
        body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background-color: #f0f2f5; margin: 50px; display: flex; justify-content: center; }
        .app-container { background: white; padding: 30px; border-radius: 12px; box-shadow: 0 4px 12px rgba(0,0,0,0.1); width: 100%; max-width: 400px; }
        h2 { color: #1a73e8; margin-top: 0; }
        .input-group { display: flex; gap: 10px; margin-bottom: 20px; }
        input[type="number"] { flex: 1; padding: 10px; border: 1px solid #dadce0; border-radius: 6px; font-size: 16px; }
        button { padding: 10px 20px; background-color: #1a73e8; color: white; border: none; border-radius: 6px; cursor: pointer; font-size: 16px; font-weight: bold; }
        button:hover { background-color: #1557b0; }
        .result-list { list-style: none; padding: 0; margin: 0; border-top: 1px solid #e8eaed; }
        .result-item { padding: 12px 0; border-bottom: 1px solid #e8eaed; font-size: 18px; color: #3c4043; text-align: center; }
    </style>
</head>
<body>

<div class="app-container">
    <h2>Table Generator</h2>
    
    <form method="POST">
        <div class="input-group">
            <input type="number" name="number" placeholder="Enter number" value="{{ number or '' }}" required>
            <button type="submit">Print</button>
        </div>
    </form>

    {% if table %}
        <h3>Multiplication Table for {{ number }}</h3>
        <ul class="result-list">
            {% for row in table %}
                <li class="result-item">{{ row }}</li>
            {% endfor %}
        </ul>
    {% endif %}
</div>

</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def home():
    number = None
    table = []
    
    if request.method == "POST":
        user_input = request.form.get("number")
        
        # Check if input is a valid integer string
        if user_input and user_input.strip().lstrip('-').isdigit():
            number = int(user_input)
            # Generate table rows dynamically
            table = [f"{number} x {i} = {number * i}" for i in range(1, 11)]
            
    # Render everything using the inline string template
    return render_template_string(HTML_TEMPLATE, number=number, table=table)

if __name__ == "__main__":
    app.run(host = "0.0.0.0", debug=True)
