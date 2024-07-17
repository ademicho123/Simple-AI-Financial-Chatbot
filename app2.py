from flask import Flask, request, jsonify, render_template
import pandas as pd

app = Flask(__name__)

# Read the CSV file
df = pd.read_csv('financial_data.csv')

# Ensure columns are correctly named and strip any leading/trailing whitespace
df.columns = [col.strip() for col in df.columns]

# Convert data types
df['Total Revenue'] = pd.to_numeric(df['Total Revenue'])
df['Net Income'] = pd.to_numeric(df['Net Income'])
df['Total Assets'] = pd.to_numeric(df['Total Assets'])
df['Total Liabilities'] = pd.to_numeric(df['Total Liabilities'])
df['Cash Flow from Operating Activities'] = pd.to_numeric(df['Cash Flow from Operating Activities'])

# Calculate percentage changes for each metric
df = df.sort_values(by=['Company', 'Year'])

df['Revenue Growth (%)'] = df.groupby('Company')['Total Revenue'].apply(lambda x: x.pct_change() * 100).reset_index(drop=True)
df['Net Income Growth (%)'] = df.groupby('Company')['Net Income'].apply(lambda x: x.pct_change() * 100).reset_index(drop=True)
df['Total Assets Growth (%)'] = df.groupby('Company')['Total Assets'].apply(lambda x: x.pct_change() * 100).reset_index(drop=True)
df['Total Liabilities Growth (%)'] = df.groupby('Company')['Total Liabilities'].apply(lambda x: x.pct_change() * 100).reset_index(drop=True)
df['Cash Flow Growth (%)'] = df.groupby('Company')['Cash Flow from Operating Activities'].apply(lambda x: x.pct_change() * 100).reset_index(drop=True)

df = df.fillna(0)
df.loc[df['Year'] == 2021, ['Revenue Growth (%)', 'Net Income Growth (%)', 'Total Assets Growth (%)', 'Total Liabilities Growth (%)', 'Cash Flow Growth (%)']] = 0

total_revenue_2023 = df[df['Year'] == 2023][['Company', 'Total Revenue']]
net_income_change = df[df['Year'] == 2023][['Company', 'Net Income Growth (%)']]
total_assets_2023 = df[df['Year'] == 2023][['Company', 'Total Assets']]
cash_flow_change = df[df['Year'] == 2023][['Company', 'Cash Flow Growth (%)']]
revenue_growth_2022_2023 = df[df['Year'] == 2023][['Company', 'Revenue Growth (%)']]

def simple_chatbot(user_query):
    if user_query == "What is the total revenue for 2023?":
        responses = []
        for index, row in total_revenue_2023.iterrows():
            responses.append(f"{row['Company']}: ${row['Total Revenue']} million")
        return "The total revenue for 2023 is:\n" + "\n".join(responses)
    
    elif user_query == "How has net income changed over the last year?":
        responses = []
        for index, row in net_income_change.iterrows():
            change = "increased" if row['Net Income Growth (%)'] > 0 else "decreased"
            responses.append(f"{row['Company']}: Net income has {change} by {abs(row['Net Income Growth (%)']):.2f}%")
        return "Net income changes over the last year:\n" + "\n".join(responses)
    
    elif user_query == "What are the total assets for 2023?":
        responses = []
        for index, row in total_assets_2023.iterrows():
            responses.append(f"{row['Company']}: ${row['Total Assets']} million")
        return "The total assets for 2023 are:\n" + "\n".join(responses)
    
    elif user_query == "How has cash flow from operating activities changed over the last year?":
        responses = []
        for index, row in cash_flow_change.iterrows():
            change = "increased" if row['Cash Flow Growth (%)'] > 0 else "decreased"
            responses.append(f"{row['Company']}: Cash flow has {change} by {abs(row['Cash Flow Growth (%)']):.2f}%")
        return "Cash flow from operating activities changes over the last year:\n" + "\n".join(responses)
    
    elif user_query == "What is the revenue growth percentage from 2022 to 2023?":
        responses = []
        for index, row in revenue_growth_2022_2023.iterrows():
            responses.append(f"{row['Company']}: {row['Revenue Growth (%)']:.2f}%")
        return "Revenue growth percentage from 2022 to 2023:\n" + "\n".join(responses)
    
    else:
        return "Sorry, I can only provide information on predefined queries."

@app.route('/')  
def index():
    return render_template('chatbot.html')  # Render the HTML template (no folder needed)

@app.route('/chatbot', methods=['GET'])
def chatbot():
    user_query = request.args.get('query')
    response = simple_chatbot(user_query)
    return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True)
