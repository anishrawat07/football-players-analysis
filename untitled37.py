import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Initialize Streamlit app
st.set_page_config(layout="wide")

# Dashboard Title
st.title("Football Player Performance Dashboard")

def load_data(data_file):
  """Loads data from an uploaded file, handling potential errors.

  Args:
    data_file: The uploaded file object.

  Returns:
    A pandas DataFrame if successful, otherwise None.
  """

  try:
    df = pd.read_csv(data_file)
    # Check if 'league_id' column exists after loading
    if 'league_id' not in df.columns:
      st.error("Error: 'league_id' column not found in the CSV file.")
      return None
    return df
  except pd.errors.ParserError as e:
    st.error(f"Error parsing CSV: {e}")
    # Additional checks based on error message (if needed)
    return None
  except Exception as e:
    st.error(f"An unexpected error occurred: {e}")
    return None

# File uploader
uploaded_file = st.file_uploader("Upload your CSV file")

if uploaded_file is not None:
  df = load_data(uploaded_file)
  if df is None:
    st.stop()

  # Sidebar for filters
  st.sidebar.header("Filter Players")
  selected_league = st.sidebar.selectbox("Select League", df['league_id'].unique())
  selected_club = st.sidebar.selectbox("Select Club", df[df['league_id'] == selected_league]['club_team_id'].unique())
  selected_position = st.sidebar.selectbox("Select Position", df['club_position_oe'].unique())

  # Filter the dataframe
  filtered_df = df[(df['league_id'] == selected_league) &
                   (df['club_team_id'] == selected_club) &
                   (df['club_position_oe'] == selected_position)]

  # Display the filtered dataframe
  st.header(f"Player Statistics for {selected_club} in {selected_league}")
  st.write(filtered_df)

  # Dashboard title
  st.title("Football Player Performance Dashboard")

  # Player statistics
  st.subheader("Player Statistics")
  # Display selected player statistics (e.g., using st.write or other visualization components)

  # Visualizations
  st.subheader("Performance Visualizations")
  # Create and display charts (e.g., using st.bar_chart, st.line_chart, etc.)

  # Country-wise analysis
  st.subheader("Country-wise Analysis")
  country_data = df.groupby('nationality_id')[metrics].mean().reset_index()
  st.dataframe(country_data)

  fig, ax = plt.subplots(figsize=(12, 6))
  sns.barplot(x='nationality_id', y='overall_mmnorm', data=country_data, ax=ax)
  ax.set_title("Overall Performance by Country")
  st.pyplot(fig)

  # Individual Player Analysis
  st.subheader("Individual Player Analysis")
  selected_player = st.selectbox("Select Player", filtered_df.index)
  player_data = filtered_df.loc[selected_player]
  st.write(player_data)

  # Suggestions for Improvement
  st.subheader("Suggestions for Improvement")
  improvement_areas = ['weak_foot', 'skill_moves', 'international_reputation',
                        'attacking_crossing_mmnorm', 'mentality_vision_mmnorm']
  st.write(player_data[improvement_areas])

  # Conclusion
  st.markdown("""
  ### Conclusion
  This dashboard allows managers to gain insights into the performance of players across various metrics. The country-wise analysis helps in comparing players on a global scale, while the individual analysis aids in tracking and improving specific players' skills.
  """)
