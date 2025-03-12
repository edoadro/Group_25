import sys
sys.path.append("..") # Adds higher directory to python modules path.
from MovieAnalysis import MovieAnalysis
import streamlit as st
import matplotlib.pyplot as plt

# Initialize the MovieAnalysis instance
analysis = MovieAnalysis()

st.title("Movie Data Analysis")

# 1. Histogram for movie types
st.header("Movie Types Histogram")

# Create a number input to select N (the top N movie types)
N = st.number_input("Select value of N", min_value=1, max_value=100, value=10, step=1)
movie_types = analysis.movie_type(N)

# Plot the movie types as a bar chart
fig1, ax1 = plt.subplots()
movie_types.plot(kind="bar", ax=ax1)
ax1.set_xlabel("Movie Type")
ax1.set_ylabel("Count")
ax1.set_title(f"Top {N} Movie Types")
st.pyplot(fig1)

# 2. Histogram for actor count per movie
st.header("Actor Count Histogram")
actor_count_df = analysis.actor_count()



# Plot actor count histogram
fig2, ax2 = plt.subplots()
ax2.bar(actor_count_df["actor_count"], actor_count_df["movie_count"])
ax2.set_xlabel("Number of Actors per Movie")
ax2.set_ylabel("Number of Movies")
ax2.set_title("Distribution of Actor Counts per Movie")
st.pyplot(fig2)

# 3. Distribution of actor heights based on filters
st.header("Actor Height Distribution")

# Create a dropdown for gender selection
# 'All' plus all unique non-null genders from the dataset
unique_genders = analysis.character_data['Actor gender'].dropna().unique().tolist()
gender_options = ["All"] + unique_genders
selected_gender = st.selectbox("Select Gender", options=gender_options)

# Input fields for minimum and maximum height in meters
min_height = st.number_input("Minimum Height (m)", value=1.0, step=0.1)
max_height = st.number_input("Maximum Height (m)", value=2.2, step=0.1)

# Validate the input heights
if min_height > max_height:
    st.error("Minimum height must be less than maximum height.")
else:
    # Get the filtered DataFrame from the method (plot=False, as we will plot it later)
    actor_heights = analysis.actor_distributions(gender=selected_gender, min_height=min_height, max_height=max_height, plot=False)

    if actor_heights.empty:
        st.write("No data available for the selected parameters.")
    else:
        # Plot the height distribution histogram
        fig3, ax3 = plt.subplots()
        ax3.hist(actor_heights['Actor height'], bins=30, edgecolor='black')
        ax3.set_xlabel("Actor Height (m)")
        ax3.set_ylabel("Frequency")
        ax3.set_title(f"Height Distribution for {selected_gender} Actors")
        st.pyplot(fig3)