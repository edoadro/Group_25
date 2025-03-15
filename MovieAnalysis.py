import os
import tarfile
import urllib.request
import pandas as pd

import matplotlib.pyplot as plt
import ast


class MovieAnalysis:
    """
    This class is used to analyze the movie data. It will be used to analyze the data and provide the results to the user.
    """

    def __init__(self):
        download_link = 'http://www.cs.cmu.edu/~ark/personas/data/MovieSummaries.tar.gz'
        download_path = 'MovieSummaries.tar.gz'
        extract_path = 'Downloads/MovieSummaries'

        # Check if the directory is empty or doesn't exist
        if not os.path.exists(extract_path) or not os.listdir(extract_path):
            self._download_and_extract(download_link, download_path, extract_path)

        # Data and MetaData
        self.movie_summaries = self._load_data('Downloads/MovieSummaries/plot_summaries.txt',
                                               ['Wikipedia movie ID', 'Plot summary'])
        self.character_data = self._load_data('Downloads/MovieSummaries/character.metadata.tsv',
                                              ['Wikipedia movie ID', 'Freebase movie ID', 'Movie release date',
                                               'Character name', 'Actor date of birth', 'Actor gender', 'Actor height',
                                               'Actor ethnicity', 'Actor name', 'Actor age at movie release',
                                               'Freebase character/actor map ID', 'Freebase character ID',
                                               'Freebase actor ID'])
        self.movie_data = self._load_data('Downloads/MovieSummaries/movie.metadata.tsv',
                                          ['Wikipedia movie ID', 'Freebase movie ID', 'Movie name',
                                           'Movie release date', 'Movie box office revenue', 'Movie runtime',
                                           'Movie languages', 'Movie countries', 'Movie genres'])
        # Test Data
        self.tvtropes_clusters = self._load_data('Downloads/MovieSummaries/tvtropes.clusters.txt',
                                                 ['Character type', 'Freebase character/actor map ID'])
        self.name_clusters = self._load_data('Downloads/MovieSummaries/name.clusters.txt',
                                             ['Character name', 'Freebase character/actor map ID'])

    def _download_and_extract(self, download_link, download_path, extract_path):
        """Download and extract the tar.gz file."""
        print('Downloading the file')
        urllib.request.urlretrieve(download_link, download_path)
        print('Downloaded the file')

        if not os.path.exists(extract_path):
            os.makedirs(extract_path)

        with tarfile.open(download_path, 'r:gz') as tar:
            print('Extracting the file')
            tar.extractall(path=extract_path)
            print('Extracted the file')

        os.remove(download_path)

    def _load_data(self, file_path, column_names):
        """Load data from a file into a pandas DataFrame."""
        return pd.read_csv(file_path, sep='\t', header=None, names=column_names)

    def movie_type(self, N: int = 10):
        """
        This function is used to find the top 'N' most common movie types.
        It returns a DataFrame with the movie type and the number of movies of that type.
        """
        if not isinstance(N, int):
            raise ValueError("N must be an integer")

        movies = self.movie_data.copy()

        # Uses ast to convert the string to a dictionary then converts the dictionary to a list wth lambda func
        movies['Movie genres'] = movies['Movie genres'].apply(lambda x: list(ast.literal_eval(x).values()))

        # explodes splits the list into separate rows and then value counts the number of each genre
        genre_counts = movies.explode('Movie genres')['Movie genres'].value_counts()

        return genre_counts.head(N)

    def actor_count(self):
        """
        This function returns a pandas dataframe with a histogram of "number of actors" vs "movie counts".
        """

        character_data = self.character_data.copy()

        # group by movies ID to get actor count
        actors_per_movie = character_data.groupby('Freebase movie ID').agg(
            actor_count=('Freebase actor ID', 'count')).reset_index()

        # group by actor count to get movie count and sort by actor count
        movie_count = actors_per_movie.groupby('actor_count').agg(
            movie_count=('Freebase movie ID', 'count')).sort_values('actor_count', ascending=True).reset_index()

        return movie_count

    def actor_distributions(self, gender: str, max_height: float, min_height: float, plot: bool = False):
        """
        Analyzes the height distribution of actors based on gender and height range.

        Parameters:
        -----------
        gender : str
            The gender of the actors to include in the analysis.
            Accepts "All" or any distinct non-missing value in the dataset.
        max_height : float
            The upper limit for actor height in the analysis. The value should passed in meters (1.95).
        min_height : float
            The lower limit for actor height in the analysis. The value should passed in meters (1.95).
        plot : bool, optional (default=False)
            If True, generates a histogram of the height distribution using matplotlib.

        Returns:
        --------
        pd.DataFrame
            A DataFrame containing the filtered actor height data.

        Raises:
        -------
        TypeError
            If gender is not a string or if max_height/min_height are not numerical values.
        ValueError
            If min_height is greater than max_height.
        """

        # Copy the data
        character_data = self.character_data.copy()

        # Convert height to numeric (to handle missing or incorrect values)
        character_data['Actor height'] = pd.to_numeric(character_data['Actor height'], errors='coerce')

        # convert 180 and 510 to 1.8 and 1.78 these are the only two values that are not in meters
        character_data['Actor height'] = character_data['Actor height'].replace({180: 1.8, 510: 1.78})

        # Get unique gender values
        unique_genders = character_data['Actor gender'].dropna().unique().tolist()

        # Check argument types
        if not isinstance(gender, str):
            raise TypeError("'gender' must be a string.")
        if not isinstance(max_height, (int, float)):
            raise TypeError("'max_height' must be a numerical value.")
        if not isinstance(min_height, (int, float)):
            raise TypeError("'min_height' must be a numerical value.")
        if not isinstance(plot, bool):
            raise TypeError("'plot' must be a boolean (True/False).")

        # Check argument values
        if min_height > max_height:
            raise ValueError("'min_height' must be less than 'max_height'.")
        if gender not in unique_genders and gender != 'All':
            raise ValueError(f"'gender' must be either one of {unique_genders} or 'All'.")

        # Apply height range filter
        filtered_data = character_data[
            (character_data['Actor height'] >= min_height) & (character_data['Actor height'] <= max_height)
            ]

        # Apply gender filter
        if gender != 'All':
            filtered_data = filtered_data[filtered_data['Actor gender'] == gender]

        # If no data remains after filtering, return an empty DataFrame
        if filtered_data.empty:
            return pd.DataFrame(columns=['Actor gender', 'Actor height'])

        # Plot the histogram
        if plot:
            plt.hist(filtered_data['Actor height'], bins=30, edgecolor='black')
            plt.xlabel('Height (m)')
            plt.ylabel('Frequency')
            plt.title(f'Actor Height Distribution ({gender})')
            plt.show()

        return filtered_data[['Actor gender', 'Actor height']]

    def releases(self, genre: str = None):
        """
        Returns a DataFrame with the number of movie releases per year.
        If a genre is specified, it filters only movies of that type.

        Parameters:
        -----------
        genre : str, optional
            The genre to filter movies by. If None, all movies are included.

        Returns:
        --------
        pd.DataFrame
            A DataFrame with columns ['Year', 'Movie Count'] showing the number of movies released per year.
        """
        # Copy the data
        movies = self.movie_data.copy()

        # Convert release date to numeric (some might be missing or invalid)
        movies['Movie release date'] = pd.to_numeric(movies['Movie release date'], errors='coerce')

        # Drop rows where the year is NaN
        movies = movies.dropna(subset=['Movie release date'])

        # Convert year to integer
        movies['Year'] = movies['Movie release date'].astype(int)

        # Filter by genre if provided
        if genre:
            try:
                # Convert genre column from string dictionary to list of genres
                movies['Movie genres'] = movies['Movie genres'].apply(lambda x: list(ast.literal_eval(x).values()))

                # Keep only movies that contain the selected genre
                movies = movies[movies['Movie genres'].apply(lambda x: genre in x)]
            except Exception as e:
                raise ValueError(f"Error processing genre filtering: {e}")

        # Count movies per year
        releases_per_year = movies.groupby('Year').size().reset_index(name='Movie Count')

        return releases_per_year



if __name__ == '__main__':
    test = MovieAnalysis()

    print(test.actor_distributions(gender='All', max_height=2.2, min_height=1, plot=True))