from flask import Flask, render_template, request, redirect, url_for
import csv
import torch

app = Flask(__name__)

from FoodWastageAnalyzer import Analyzer
analyzer = Analyzer()

# Route for the home page
@app.route('/')
def home():
    # Read the CSV file
    items = []
    with open('Database.csv', mode='r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            items.append(row)
    
    # Pass the items to the template
    return render_template('index.html', items=items)

@app.route('/AddNewItem', methods=['GET', 'POST'])
def add_item():
    if request.method == 'POST':
        # Get form data
        name = request.form['name']
        description = request.form['description']
        sales = request.form['sales']
        stock_remaining = request.form['stock_remaining']
        avg_consumption_rate = request.form['avg_consumption_rate']
        price = request.form['price']
        avc = request.form['avc']
        category = request.form['category']
        
        # Save the new item to the CSV file
        with open('Database.csv', mode='a', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=['Name', 'Description', 'Sales', 'Stock Remaining', 'Avg_consumption Rate', 'Price', 'AVC', 'Category'])
            writer.writerow({
                'Name': name,
                'Description': description,
                'Sales': sales,
                'Stock Remaining': stock_remaining,
                'Avg_consumption Rate': avg_consumption_rate,
                'Price': price,
                'AVC': avc,
                'Category': category
            })
        
        # Redirect back to the home page
        return redirect(url_for('home'))
    
    # If it's a GET request, render the Add Item form
    return render_template('AddNewItem.html')

@app.route('/analyze')
def analyze():
    # Capture the query parameters and convert them to appropriate types
    name = request.args.get('name')
    description = request.args.get('description')
    sales = int(request.args.get('sales'))  # Convert to float
    stock = float(request.args.get('stock'))  # Convert to int
    consumption = float(request.args.get('consumption'))  # Convert to float
    price = float(request.args.get('price'))  # Convert to float
    avc = float(request.args.get('avc'))  # Convert to float
    category = request.args.get('category')

    # Prepare data for analysis
    data = [sales, stock, consumption, price, avc]

    # Get the analysis result from the Analyzer
    analysis = analyzer.AnalyzeItem(data)

    # Extract analysis details from the returned dictionary
    action = analysis.get("Action")
    adjusted_price = analysis.get("AdjustedPrice")
    greta_action = analysis.get("GretaAction")
    stephen_action = analysis.get("StephenAction")

    # Render the template and pass the captured data along with analysis results
    return render_template('analyze.html', 
                           name=name, 
                           description=description, 
                           sales=sales, 
                           stock=stock, 
                           consumption=consumption, 
                           price=price, 
                           avc=avc,
                           category=category,
                           action=action,
                           adjusted_price=adjusted_price,
                           greta_action=greta_action,
                           stephen_action=stephen_action)

if __name__ == '__main__':
    app.run(debug=True)