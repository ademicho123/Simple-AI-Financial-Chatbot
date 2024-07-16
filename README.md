# Financial Chatbot README

## Overview

This chatbot reads financial data from a CSV file and calculates year-over-year growth for key metrics. It responds to predefined financial queries using the processed data.

## Predefined Queries

The chatbot can respond to the following queries:

1. **Total Revenue for 2023:** 
   - *Query:* "What is the total revenue for 2023?"

2. **Net Income Change Over the Last Year:** 
   - *Query:* "How has net income changed over the last year?"

3. **Total Assets for 2023:** 
   - *Query:* "What are the total assets for 2023?"

4. **Cash Flow Change Over the Last Year:** 
   - *Query:* "How has cash flow from operating activities changed over the last year?"

5. **Revenue Growth Percentage from 2022 to 2023:** 
   - *Query:* "What is the revenue growth percentage from 2022 to 2023?"

## How It Works

1. **Data Processing:** 
    - Reads and processes the CSV file to calculate growth metrics.

2. **Query Handling:** 
    - Matches user queries to predefined questions and returns the corresponding financial data.

## Limitations

- **Predefined Queries Only:** 
    - Responds only to specific, predefined queries.

- **Data Dependency:** 
    - Requires a correctly formatted CSV file in the same directory.

- **Scope:** 
    - Limited to the companies and years present in the CSV file.

## Running the Chatbot

1. Ensure `financial_data.csv` is in the same directory.
2. Run the Flask app using:
    ```bash
    python app.py
