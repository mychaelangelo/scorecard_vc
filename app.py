import streamlit as st
import plotly.graph_objects as go
from streamlit_extras.colored_header import colored_header
import io
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import csv

# Define a class to represent a subfactor within a scoring factor
class SubFactor:
    def __init__(self, name, score=3, comment=""):
        self.name = name
        self.score = score
        self.comment = comment

# Define a class to represent a scoring factor with subfactors
class ScoringFactor:
    def __init__(self, name, subfactors, weight=1):
        self.name = name
        self.weight = weight
        # Create subfactors using dictionary comprehension
        self.subfactors = {sf: SubFactor(sf) for sf in subfactors}

    # Update the score of a specific subfactor
    def update_score(self, subfactor, score):
        self.subfactors[subfactor].score = score

    # Update the comment of a specific subfactor
    def update_comment(self, subfactor, comment):
        self.subfactors[subfactor].comment = comment

    # Calculate the average score of all subfactors
    def get_average_score(self):
        return sum(sf.score for sf in self.subfactors.values()) / len(self.subfactors)

    # Calculate the weighted score of the factor
    def get_weighted_score(self):
        return self.get_average_score() * self.weight

# Define a class to manage the overall investment scorecard
class InvestmentScorecard:
    def __init__(self):
        # Define the scoring factors and their subfactors
        self.factors = [
            ScoringFactor("Team", ["Ability", "Speed", "X-factor"], weight=0.5),
            ScoringFactor("Product", ["Value", "Defensibility", "Scalability"], weight=0.3),
            ScoringFactor("Market", ["Size", "Growth", "Dynamics"], weight=0.2)
        ]
        # Normalize initial weights to ensure they sum to 1
        self._normalize_weights()

    # Update the weights of the scoring factors
    def update_weights(self, new_weights):
        # Validate the number of weights
        if len(new_weights) != len(self.factors):
            raise ValueError("Number of weights must match number of factors")
        
        # Validate that weights are non-negative
        if any(w < 0 for w in new_weights):
            raise ValueError("Weights cannot be negative")
        
        total_weight = sum(new_weights)
        # Validate that total weight is not zero
        if total_weight == 0:
            raise ValueError("Total weight cannot be zero")
        
        # Update weights and normalize them
        for factor, weight in zip(self.factors, new_weights):
            factor.weight = weight / total_weight

    # Normalize factor weights to sum to 1
    def _normalize_weights(self):
        weights = [factor.weight for factor in self.factors]
        self.update_weights(weights)

    # Calculate the total score of the scorecard
    def get_total_score(self):
        return sum(factor.get_weighted_score() for factor in self.factors)

    # Return the maximum possible score (always 5 with normalized weights)
    def get_max_possible_score(self):
        return 5 

# Define the main Streamlit application class
class InvestmentScorecardApp:
    def __init__(self):
        # Initialize scorecard in session state if it doesn't exist
        if 'scorecard' not in st.session_state:
            st.session_state.scorecard = InvestmentScorecard()
        self.scorecard = st.session_state.scorecard

        # Flag to track if weights have been updated
        if 'weights_updated' not in st.session_state:
            st.session_state.weights_updated = False

        # Define score descriptions for display
        self.score_descriptions = {
            1: ("Poor", "😟"),
            2: ("Fair", "😐"),
            3: ("Average", "🙂"),
            4: ("Good", "😊"),
            5: ("Excellent", "🌟")
        }
        # Define descriptions for each subfactor
        self.subfactor_descriptions = {
            "Ability": "Team's capability to execute the business plan",
            "Speed": "Team's pace of execution and decision-making",
            "X-factor": "Unique qualities that massively set the team apart",
            "Value": "Product's ability to solve a significant problem",
            "Defensibility": "Product's competitive advantage and barriers to entry",
            "Scalability": "Product's potential for growth and expansion",
            "Size": "Total addressable market size",
            "Growth": "Market's growth rate and potential",
            "Dynamics": "Competitive landscape and market trends"
        }

    # Run the Streamlit application
    def run(self):
        st.set_page_config(layout="wide", page_title="Investment Scorecard")
        
        # Display sidebar content
        self._display_sidebar()
        
        st.title("Investment Scorecard")

        # Create two columns for layout
        col1, col2 = st.columns([2, 1])

        with col1:
            # Display scoring factors and subfactors
            self._display_factors()

        with col2:
            # Display score summary and visualization
            self._display_summary()
            self._display_visualization()

    # Display sidebar elements (About, Customization, Export)
    def _display_sidebar(self):
        with st.sidebar:
            # Custom CSS for styling
            st.markdown("""
            <style>
            .big-font {
                font-size:24px !important;
                font-weight: bold;
                color: #4682B4; 
            }
            .about-section {
                background-color: #F5F5F5;  
                padding: 10px;
                border-radius: 5px;
                margin-bottom: 10px;
                border: 1px solid #E0E0E0;  
            }
            .about-section h1 {
                color: #4682B4;  
                font-size: 20px;
            }
            .creator-info {
                font-style: italic;
                color: #708090;  
            }
            </style>
            """, unsafe_allow_html=True)

            st.markdown('<p class="big-font">Investment Scorecard</p>', unsafe_allow_html=True)
            
            # About section
            with st.expander("About the App", expanded=False):
                st.markdown("""
                <div class="about-section">
                <h1>About the App</h1>
                <p><strong>This is an educational tool.</strong></p>
                <p><strong>Do not rely on it for investment decisions.</strong></p>
                <p>The Investment Scorecard App helps seed investors evaluate potential 
                investments across key factors: Team, Product, and Market. 
                Customize the weights or leave the defaults.
                Rate each subfactor and add comments to 
                generate a comprehensive investment score.
                You can download a PDF or export to CSV.</p>
                <hr>
                <p class="creator-info">Created by <a href="https://michaeltefula.com/">Michael Tefula</a></p>
                </div>
                """, unsafe_allow_html=True)
            
            st.markdown("---")
            # Customization section
            self._display_customization()
            st.markdown("---")
            # Export options section
            self._display_export_options()

    # Display scoring factors and their subfactors for user input
    def _display_factors(self):
        colored_header("Scoring Factors", description="Rate each subfactor and add comments")
        for i, factor in enumerate(self.scorecard.factors):
            st.subheader(f"{factor.name}")
            
            with st.expander(f"Evaluate {factor.name} Sub-factors", expanded=True):
                for j, (subfactor_name, subfactor) in enumerate(factor.subfactors.items()):
                    col1, col2 = st.columns([1, 2])
                    with col1:
                        # Display score selection for each subfactor
                        score = st.selectbox(
                            f"{subfactor_name}",
                            options=[1, 2, 3, 4, 5],
                            format_func=lambda x: f"{x} - {self.score_descriptions[x][0]} {self.score_descriptions[x][1]}",
                            index=subfactor.score - 1,
                            key=f"select_{i}_{j}"
                        )
                        factor.update_score(subfactor_name, score)
                    with col2:
                        # Display comment area for each subfactor
                        comment = st.text_area(
                            f"Comment on {subfactor_name}",
                            value=subfactor.comment,
                            max_chars=280,
                            height=200,
                            key=f"comment_{i}_{j}",
                            placeholder=self.subfactor_descriptions[subfactor_name]
                        )
                        factor.update_comment(subfactor_name, comment)
                    st.markdown("---")
            
            st.write(f"Average Score: {factor.get_average_score():.2f}")
            st.write(f"Weight: {factor.weight:.2f}")
            st.markdown("---")

    # Display the overall score summary
    def _display_summary(self):
        colored_header("Score Summary", description="Overall investment score")
        total_score = self.scorecard.get_total_score()
        max_score = self.scorecard.get_max_possible_score()
        percentage = (total_score / max_score) * 100

        col1, col2 = st.columns(2)
        with col1:
            st.metric("Total Score", f"{total_score:.2f}")
        with col2:
            st.metric("Max Possible", f"{max_score:.2f}")

        st.progress(percentage / 100)

        overall_rating = round(total_score)
        description, emoji = self.score_descriptions[overall_rating]
        st.info(f"Overall Rating: {overall_rating} - {description} {emoji}")

    # Display customization options for factor weights
    def _display_customization(self):
        st.sidebar.header("Customize Scorecard")
        st.sidebar.write("Adjust weights")
        
        weights = []
        for i, factor in enumerate(self.scorecard.factors):
            # Input fields for adjusting weights
            weight = st.sidebar.number_input(
                f"{factor.name} Weight",
                min_value=0.0,
                value=factor.weight,
                step=0.1,
                format="%.2f",
                key=f"weight_input_{i}"
            )
            weights.append(weight)
        
        total_weight = sum(weights)
        st.sidebar.write(f"Total weight: {total_weight:.2f}")
        
        # Button to update and normalize weights
        if st.sidebar.button("Update & Normalize Weights"):
            try:
                self.scorecard.update_weights(weights)
                st.session_state.weights_updated = True
            except ValueError as e:
                st.sidebar.error(str(e))
            st.rerun()

        # Display success message after updating weights
        if st.session_state.weights_updated:
            st.sidebar.success("Weights updated successfully!")
            st.session_state.weights_updated = False

        # Button to set all weights equally
        if st.sidebar.button("Set to Equal Weights"):
            equal_weight = 1.0 / len(self.scorecard.factors)
            self.scorecard.update_weights([equal_weight] * len(self.scorecard.factors))
            st.session_state.weights_updated = True
            st.rerun()

    # Display a radar chart visualization of the scores
    def _display_visualization(self):
        colored_header("Score Visualization", description="Radar chart of factor scores")
        
        categories = [factor.name for factor in self.scorecard.factors]
        scores = [factor.get_average_score() for factor in self.scorecard.factors]
        weights = [factor.weight for factor in self.scorecard.factors]

        # Create the radar chart using Plotly
        fig = go.Figure(data=go.Scatterpolar(
            r=scores,
            theta=categories,
            fill='toself',
            name='Scores'
        ))

        fig.add_trace(go.Scatterpolar(
            r=[w * 5 for w in weights], 
            theta=categories,
            fill='toself',
            name='Weights'
        ))

        fig.update_layout(
            polar=dict(
                radialaxis=dict(visible=True, range=[0, 5])
            ),
            showlegend=True,
            height=400,
            margin=dict(l=50, r=50, t=50, b=50)
        )

        st.plotly_chart(fig, use_container_width=True)

    # Display export options for downloading PDF and CSV
    def _display_export_options(self):
        st.sidebar.header("Export Options")
        st.sidebar.write("Download your scorecard")
        
        pdf = self._generate_pdf()
        # Download button for PDF report
        st.sidebar.download_button(
            label="Download PDF",
            data=pdf,
            file_name="investment_scorecard.pdf",
            mime="application/pdf"
        )

        csv = self._generate_csv()
        # Download button for CSV data
        st.sidebar.download_button(
            label="Download CSV",
            data=csv,
            file_name="investment_scorecard.csv",
            mime="text/csv"
        )

    # Generate a PDF report of the scorecard
    def _generate_pdf(self):
        buffer = io.BytesIO()
        c = canvas.Canvas(buffer, pagesize=letter)
        width, height = letter

        # Helper function to draw wrapped text
        def draw_wrapped_text(text, x, y, width, font_name, font_size):
            c.setFont(font_name, font_size)
            words = text.split()
            lines = []
            current_line = []
            for word in words:
                if c.stringWidth(' '.join(current_line + [word])) < width:
                    current_line.append(word)
                else:
                    lines.append(' '.join(current_line))
                    current_line = [word]
            lines.append(' '.join(current_line))
            
            for line in lines:
                c.drawString(x, y, line)
                y -= font_size + 2
            return y

        # PDF content generation (title, factors, scores, comments, summary)
        y = height - 50
        y = draw_wrapped_text("Investment Scorecard Report", 50, y, width - 100, "Helvetica-Bold", 16)
        y -= 20

        for factor in self.scorecard.factors:
            y = draw_wrapped_text(f"{factor.name}", 50, y, width - 100, "Helvetica-Bold", 14)
            y -= 10
            for subfactor_name, subfactor in factor.subfactors.items():
                y = draw_wrapped_text(f"{subfactor_name}: Score {subfactor.score}", 70, y, width - 140, "Helvetica", 12)
                y -= 5
                y = draw_wrapped_text(f"Comment: {subfactor.comment}", 90, y, width - 180, "Helvetica", 12)
                y -= 10
            y = draw_wrapped_text(f"Average Score: {factor.get_average_score():.2f}, Weight: {factor.weight:.2f}", 50, y, width - 100, "Helvetica", 12)
            y -= 20
            
            # Start a new page if content exceeds current page
            if y < 50: 
                c.showPage()
                y = height - 50

        total_score = self.scorecard.get_total_score()
        max_score = self.scorecard.get_max_possible_score()
        percentage = (total_score / max_score) * 100
        
        y = draw_wrapped_text("Summary", 50, y, width - 100, "Helvetica-Bold", 14)
        y -= 10
        y = draw_wrapped_text(f"Total Score: {total_score:.2f} / {max_score:.2f}", 50, y, width - 100, "Helvetica", 12)
        y -= 5
        y = draw_wrapped_text(f"Percentage of Max Score: {percentage:.2f}%", 50, y, width - 100, "Helvetica", 12)

        c.save()
        buffer.seek(0)
        return buffer

    # Generate CSV data of the scorecard
    def _generate_csv(self):
        output = io.StringIO()
        writer = csv.writer(output)
        
        writer.writerow(["Factor", "Subfactor", "Score", "Comment", "Weight"])
        for factor in self.scorecard.factors:
            for subfactor_name, subfactor in factor.subfactors.items():
                writer.writerow([factor.name, subfactor_name, subfactor.score, subfactor.comment, factor.weight])
        
        total_score = self.scorecard.get_total_score()
        max_score = self.scorecard.get_max_possible_score()
        percentage = (total_score / max_score) * 100
        
        writer.writerow([])
        writer.writerow(["Total Score", total_score])
        writer.writerow(["Max Possible Score", max_score])
        writer.writerow(["Percentage of Max Score", f"{percentage:.2f}%"])
        
        return output.getvalue()

# Entry point for running the Streamlit application
if __name__ == "__main__":
    app = InvestmentScorecardApp()
    app.run()
