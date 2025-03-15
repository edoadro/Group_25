import sys
sys.path.append("..") # Adds higher directory to python modules path.
from MovieAnalysis import MovieAnalysis
import streamlit as st
import matplotlib.pyplot as plt

# Initialize the MovieAnalysis instance
analysis = MovieAnalysis()

st.title("Movie Data Analysis - Group_25")
page = st.sidebar.selectbox("Choose a page", ["Main Analysis", "Chronological Info"])


# Main Analysis Page
if page == "Main Analysis":
    # Existing main analysis page (do not modify)
    st.title("Movie Data Analysis - Group_25")
    st.markdown(
        "This app provides an analysis of the movie dataset. "
        "[Dataset Link](http://www.cs.cmu.edu/~ark/personas/data/MovieSummaries.tar.gz)."
    )
    st.markdown("The dataset contains information about movies, characters, and actors. The analysis includes histograms for movie types, actor counts per movie, and actor heights.")

    # 1. Histogram for movie types
    st.header("Movie Types Histogram")
    N = st.number_input("Select value of N", min_value=1, max_value=100, value=10, step=1)
    movie_types = analysis.movie_type(N)

    fig1, ax1 = plt.subplots()
    movie_types.plot(kind="bar", ax=ax1)
    ax1.set_xlabel("Movie Type")
    ax1.set_ylabel("Count")
    ax1.set_title(f"Top {N} Movie Types")
    st.pyplot(fig1)

    # 2. Histogram for actor count per movie
    st.header("Actor Count Histogram")
    actor_count_df = analysis.actor_count()

    fig2, ax2 = plt.subplots()
    ax2.bar(actor_count_df["actor_count"], actor_count_df["movie_count"])
    ax2.set_xlabel("Number of Actors per Movie")
    ax2.set_ylabel("Number of Movies")
    ax2.set_title("Distribution of Actor Counts per Movie")
    st.pyplot(fig2)

    # 3. Distribution of actor heights based on filters
    st.header("Actor Height Distribution")
    unique_genders = analysis.character_data['Actor gender'].dropna().unique().tolist()
    gender_options = ["All"] + unique_genders
    selected_gender = st.selectbox("Select Gender", options=gender_options)

    min_height = st.number_input("Minimum Height (m)", value=1.0, step=0.1)
    max_height = st.number_input("Maximum Height (m)", value=2.2, step=0.1)

    if min_height > max_height:
        st.error("Minimum height must be less than maximum height.")
    else:
        actor_heights = analysis.actor_distributions(gender=selected_gender, min_height=min_height, max_height=max_height, plot=False)

        if actor_heights.empty:
            st.write("No data available for the selected parameters.")
        else:
            fig3, ax3 = plt.subplots()
            ax3.hist(actor_heights['Actor height'], bins=30, edgecolor='black')
            ax3.set_xlabel("Actor Height (m)")
            ax3.set_ylabel("Frequency")
            ax3.set_title(f"Height Distribution for {selected_gender} Actors")
            st.pyplot(fig3)

# Chronological Info Page
elif page == "Chronological Info":
    st.title("Chronological Analysis of Movies")

    # 1. Movie Releases per Year
    st.header("Movie Releases Over Time")

    # Genre Selection
    available_genres = ["All", "Comedy", "Drama", "Action", "Thriller", "Horror", "Romance", "Sci-Fi", "Adventure", "Animation"]
    selected_genre = st.selectbox("Select Genre", available_genres)

    # Convert "All" to None for function call
    genre_filter = None if selected_genre == "All" else selected_genre

    # Get Data
    releases_df = analysis.releases(genre=genre_filter)

    # Plot the data
    if releases_df.empty:
        st.write("No data available for the selected genre.")
    else:
        fig4, ax4 = plt.subplots()
        ax4.bar(releases_df["Year"], releases_df["Movie Count"], color="royalblue")
        ax4.set_xlabel("Year")
        ax4.set_ylabel("Number of Movies Released")
        ax4.set_title(f"Movie Releases Over Time ({selected_genre})")
        st.pyplot(fig4)

        # 2️⃣ Actor Births Over Time
        st.header("Actor Births Distribution")

        # Dropdown to select Year ('Y') or Month ('M')
        selected_mode = st.selectbox("Choose Time Unit", ["Year", "Month"], key="time_unit_selector")

        # Convert selection to expected parameter
        mode_filter = 'Y' if selected_mode == "Year" else 'M'

        # Get Data
        ages_df = analysis.ages(mode=mode_filter)

        # Plot the data
        if ages_df.empty:
            st.write("No data available for the selected mode.")
        else:
            fig5, ax5 = plt.subplots()

            if mode_filter == 'Y':
                ax5.bar(ages_df["Year"], ages_df["Birth Count"], color="darkorange")
                ax5.set_xlabel("Year")
                ax5.set_ylabel("Number of Actor Births")
                ax5.set_title("Actor Births Per Year")
            else:
                ax5.bar(ages_df["Month"], ages_df["Birth Count"], color="green")
                ax5.set_xlabel("Month")
                ax5.set_ylabel("Number of Actor Births")
                ax5.set_title("Actor Births Per Month")
                ax5.set_xticks(range(1, 13))  # Ensure we show 1-12 for months

            st.pyplot(fig5)

    # 2. Actor Births Over Time
    st.header("Actor Births Distribution")

    # Dropdown to select Year ('Y') or Month ('M')
    selected_mode = st.selectbox("Choose Time Unit", ["Year", "Month"])

    # Convert selection to expected parameter
    mode_filter = 'Y' if selected_mode == "Year" else 'M'

    # Get Data
    ages_df = analysis.ages(mode=mode_filter)

    # Plot the data
    if ages_df.empty:
        st.write("No data available for the selected mode.")
    else:
        fig5, ax5 = plt.subplots()

        if mode_filter == 'Y':
            ax5.bar(ages_df["Year"], ages_df["Birth Count"], color="darkorange")
            ax5.set_xlabel("Year")
            ax5.set_ylabel("Number of Actor Births")
            ax5.set_title("Actor Births Per Year")
        else:
            ax5.bar(ages_df["Month"], ages_df["Birth Count"], color="green")
            ax5.set_xlabel("Month")
            ax5.set_ylabel("Number of Actor Births")
            ax5.set_title("Actor Births Per Month")
            ax5.set_xticks(range(1, 13))  # Ensure we show 1-12 for months

        st.pyplot(fig5)

