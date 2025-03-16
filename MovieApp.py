import sys
from MovieAnalysis import MovieAnalysis
import streamlit as st
import matplotlib.pyplot as plt
import ollama
import json

# Load configuration
def load_config():
    with open("config.json", "r") as file:
        return json.load(file)

config = load_config()
MODEL_NAME = config["ollama"]["model"]  # Get model name for Ollama to run the AI model

def jaccard_similarity(set1, set2):
    """Compute Jaccard similarity between two sets"""
    intersection = set1.intersection(set2)
    union = set1.union(set2)
    return len(intersection) / len(union) if union else 0

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
    st.markdown(
        "The dataset contains information about movies, characters, and actors."
        "The analysis includes histograms for movie types, actor counts per movie, and actor heights."
    )

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
    st.header("🤖 AI-Based Movie Genre Classification")
    st.sidebar.markdown(f"**LLM Model in Use:** `{MODEL_NAME}` (it can be configured in `config.json`)")

    # Button to shuffle a movie
    if st.button("🔀 Shuffle Movie"):
        movie = analysis.get_random_movie()
        
        #box1
        with st.container(border=True):
            st.markdown(f"### 🎥🎬Chosen Movie: *{movie['title']}* 🎥🎬")
            st.expander("Movie Summary - 𝘤𝘭𝘪𝘤𝘬 𝘵𝘰 𝘦𝘹𝘱𝘢𝘯𝘥").write(movie['summary'])

        # box2
        with st.container(border=True):
            st.markdown("### 🎭 Actual Genres")
            st.write(", ".join(movie['genres']))

        # Prepare the LLM prompt
        prompt = f"""
        You are a movie classification AI. Given a movie summary, return only the genres that match the movie.
        Output only a comma-separated list of genres. Do not add extra words.

        Movie Summary:
        {movie['summary']}
        """


        # box3
        with st.container(border=True):
            st.markdown("### 🤖 LLM-Predicted Genres")
            
            # Call Ollama to classify the movie
            with st.spinner("Analyzing movie..."):
                try:
                    response = ollama.chat(model=MODEL_NAME, messages=[{"role": "user", "content": prompt}])
                    predicted_genres = response['message']['content']
                except Exception as e:
                    st.error(f"Error communicating with the LLM: {e}")
                    predicted_genres = ""

            # Clean and process the LLM output
            predicted_genres_list = [genre.strip() for genre in predicted_genres.split(",") if genre.strip()]
            actual_genres_set = [set(genre.lower().split()) for genre in movie['genres']]
            llm_genres_set = [set(genre.lower().split()) for genre in predicted_genres_list]
            st.write(", ".join(predicted_genres_list) if predicted_genres_list else "No genres identified.")

        # box4 evalation
        with st.container(border=True):
            st.markdown("### Evaluation of genre prediction")
            
            if not actual_genres_set:
                st.warning("⚠️ No actual genres available for comparison. Skipping evaluation. ☹️\nPlease shuffle another movie.")
            else:
                st.markdown("#### Jaccard Similarity based Evaluation")
                
                threshold = 0.5  # Define a similarity threshold
                markdown_table = "| Predicted Genre | Match Found? | Highest Jaccard Similarity |\n"
                markdown_table += "|----------------|-------------|----------------------------|\n"
                matches_count = 0

                # Evaluate each predicted genre
                for pred in llm_genres_set:
                    pred_str = " ".join(pred)
                    max_similarity = max(jaccard_similarity(pred, act) for act in actual_genres_set)
                    match_status = "✅ Yes" if max_similarity >= threshold else "❌ No"
                    markdown_table += f"| {pred_str} | {match_status} | {max_similarity:.2f} |\n"
                    matches_count += 1 if max_similarity >= threshold else 0

                success_rate = matches_count / len(llm_genres_set)

                # Evaluation results
                if success_rate >= 0.5:
                    st.success(f"✅ At least half of the model's predictions were correct ({matches_count} out of {len(llm_genres_set)})\n" + markdown_table)
                else:
                    st.error(f"❌ Less then half of the model's predictions were correct ({matches_count} out of {len(llm_genres_set)})\n" + markdown_table)
                
                
                st.markdown("#### 🤖 LLM-Based Prediction Comparison")
                
                evaluation_messages=[
                    {"role": "system", "content": "You are a movie expert. You are in charge to evaluate the perfomance of an AI model that predicts movie genres."},
                    {"role": "user", "content": "Compare the model predictions with the actual genres and explain if they match well:\n\n"
                                                f"Model Prediction: [{', '.join(predicted_genres_list)}]\n"
                                                f"Actual Genres: [{', '.join(movie['genres'])}]\n"
                                                f"The predictions are for the movie: {movie['title']}\n"
                                                "Be very concise and clear in your evaluation."}
                ]
                
                with st.spinner("AI model is thinking..."):
                    try:
                        response = ollama.chat(model=MODEL_NAME, messages=evaluation_messages)
                        st.markdown(response['message']['content'])
                    except Exception as e:
                        st.error(f"Error communicating with the LLM: {e}")

