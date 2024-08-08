# Investment Scorecard App

The Investment Scorecard App is an educational tool designed to help seed investors evaluate potential investments across three key factors: Team, Product, and Market. Users can customize the weights of these factors, rate each subfactor, and add comments to generate a comprehensive investment score. The app also allows exporting the evaluation to PDF and CSV formats.

## Features

- **Customizable Weights**: Adjust the weights of the scoring factors to match your priorities.
- **Detailed Subfactor Evaluation**: Rate each subfactor on a scale of 1 to 5 and provide comments.
- **Score Summary**: View the overall investment score and a radar chart visualization.
- **Export Options**: Download the scorecard as a PDF or CSV file for easy sharing and record-keeping.

## Scoring Factors and Subfactors

### Team
- **Ability**: Team's capability to execute the business plan.
- **Speed**: Team's pace of execution and decision-making.
- **X-factor**: Unique qualities that massively set the team apart.

### Product
- **Value**: Product's ability to solve a significant problem.
- **Defensibility**: Product's competitive advantage and barriers to entry.
- **Scalability**: Product's potential for growth and expansion.

### Market
- **Size**: Total addressable market size.
- **Growth**: Market's growth rate and potential.
- **Dynamics**: Competitive landscape and market trends.

## Usage

1. **Install Dependencies**:
    ```bash
    pip install streamlit plotly streamlit-extras reportlab
    ```

2. **Run the App**:
    ```bash
    streamlit run app.py
    ```

3. **Evaluate Factors**:
    - Navigate to the app in your browser.
    - Adjust weights if needed using the sidebar.
    - Rate each subfactor and add comments.
    - View the overall score and radar chart visualization.

4. **Export Data**:
    - Download the scorecard as a PDF or CSV file from the sidebar.

## Customization

- **Adjust Weights**: Use the sidebar to input new weights for each scoring factor. Click "Update & Normalize Weights" to apply the changes.
- **Equal Weights**: Click "Set to Equal Weights" in the sidebar to distribute weights equally among the factors.

## Export Options

- **Download PDF**: Generates a detailed PDF report of the scorecard.
- **Download CSV**: Exports the scorecard data in CSV format.

## Disclaimer

This app is an educational tool. Do not rely on it for actual investment decisions.


---

Enjoy using the Investment Scorecard App!
