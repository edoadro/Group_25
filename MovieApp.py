import sys
sys.path.append("..")  # Adds higher directory to python modules path.
from MovieAnalysis import MovieAnalysis
import streamlit as st
import matplotlib.pyplot as plt
import ollama

# Initialize the MovieAnalysis instance
analysis = MovieAnalysis()

st.title("Movie Data Analysis - Group_25")
page = st.sidebar.selectbox("Choose a page", ["Main Analysis", "Chronological Info", "AI Classification"])

# Main Analysis Page
if page == "Main Analysis":
    st.markdown(
        "## Main Analysis\n"
        "This app provides an analysis of the [CMU movie corpus](https://www.cmu.edu/) movie dataset. "
        "[Dataset Link](http://www.cs.cmu.edu/~ark/personas/data/MovieSummaries.tar.gz)."
    )
    st.markdown("The dataset contains information about movies, characters, and actors. The analysis includes histograms for movie types, actor counts per movie, and actor heights.")

    # 1. Histogram for movie types
    st.subheader("Movie Types Histogram")
    N = st.number_input("Select value of N", min_value=1, max_value=100, value=10, step=1)
    movie_types = analysis.movie_type(N)

    fig1, ax1 = plt.subplots()
    movie_types.plot(kind="bar", ax=ax1)
    ax1.set_xlabel("Movie Type")
    ax1.set_ylabel("Count")
    ax1.set_title(f"Top {N} Movie Types")
    st.pyplot(fig1)

    # 2. Histogram for actor count per movie
    st.subheader("Actor Count Histogram")
    actor_count_df = analysis.actor_count()

    fig2, ax2 = plt.subplots()
    ax2.bar(actor_count_df["actor_count"], actor_count_df["movie_count"])
    ax2.set_xlabel("Number of Actors per Movie")
    ax2.set_ylabel("Number of Movies")
    ax2.set_title("Distribution of Actor Counts per Movie")
    st.pyplot(fig2)

    # 3. Distribution of actor heights based on filters
    st.subheader("Actor Height Distribution")
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
    st.header("Chronological Analysis of Movies")

    # 1. Movie Releases per Year
    st.subheader("Movie Releases Over Time")

    # Genre Selection
    available_genres = ['Drama', 'Comedy', 'Romance Film', 'Black-and-white', 'Action', 'Thriller', 'Short Film', 'World cinema', 'Crime Fiction', 'Indie']
    available_genres.sort()
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

    # 2. Actor Births Over Time
    st.subheader("Actor Births Distribution")

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

# AI Classification Page
elif page == "AI Classification":
    st.title("🤖 AI-Based Movie Genre Classification")

    # Button to shuffle a movie
    if st.button("🔀 Shuffle Movie"):
        movie = analysis.get_random_movie()

        # Display movie details
        st.subheader("📖 Movie Title & Summary")
        st.write(f"**Title:** {movie['title']}")
        st.write(f"**Summary:** {movie['summary']}")

        st.subheader("🎭 Actual Genres")
        st.write(", ".join(movie['genres']))

        # Prepare the LLM prompt
        prompt = f"""
        You are a movie classification AI. Given a movie summary, return only the genres that match the movie.
        Output only a comma-separated list of genres. Do not add extra words.

        Movie Summary:
        {movie['summary']}
        """

        # Call Ollama to classify the movie
        with st.spinner("Analyzing movie..."):
            try:
                response = ollama.chat(model="mistral", messages=[{"role": "user", "content": prompt}])
                predicted_genres = response['message']['content']
            except Exception as e:
                st.error(f"Error communicating with the LLM: {e}")
                predicted_genres = ""

        # Clean and process the LLM output
        predicted_genres_list = [genre.strip() for genre in predicted_genres.split(",") if genre.strip()]
        actual_genres_set = set(movie['genres'])
        llm_genres_set = set(predicted_genres_list)

        # Compare with actual genres
        is_match = llm_genres_set.issubset(actual_genres_set)

        # Display LLM Prediction
        st.subheader("🤖 LLM-Predicted Genres")
        st.write(", ".join(predicted_genres_list) if predicted_genres_list else "No genres identified.")

        # Show whether the genres match
        st.subheader("✅ Match Check")
        if is_match:
            st.success("The LLM's predicted genres match the database genres!")
        else:
            st.error("The LLM's predicted genres do NOT match the database genres!")


