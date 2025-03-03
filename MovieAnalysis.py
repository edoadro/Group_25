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
        extract_path = 'Downloads'

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
        
        # explodes splits the list into separate rows and then value counts counts the number of each genre
        genre_counts = movies.explode('Movie genres')['Movie genres'].value_counts()
        
        
        return genre_counts.head(N)
    
    def actor_count(self):
        """
        This function returns a pandas dataframe with a histogram of "number of actors" vs "movie counts".
        """
        
        character_data = self.character_data.copy()
        
        # group by movies ID to get actor count
        actors_per_movie = character_data.groupby('Freebase movie ID').agg(actor_count = ('Freebase actor ID', 'count')).reset_index()

        # group by actor count to get movie count and sort by actor count
        movie_count = actors_per_movie.groupby('actor_count').agg(movie_count = ('Freebase movie ID', 'count')).sort_values('actor_count', ascending=True).reset_index()
    
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
        The upper limit for actor height in the analysis.
    min_height : float
        The lower limit for actor height in the analysis.
    plot : bool, optional (default=False)
        If True, generates a histogram of the height distribution using matplotlib.
        
    Example:
    --------  
    self.actor_distributions(gender = 'M', max_height = 200, min_height = 150, plot = True)
    will return a plot of the height distribution for male actors with heights between 150 and 200 cm.

    Returns:
    --------
    pd.DataFrame
        A DataFrame containing summary statistics of the height distribution.

    Raises:
    -------
    TypeError
        If `gender` is not a string or if `max_height`/`min_height` are not numerical values.
    ValueError
        If `min_height` is greater than `max_height`.
        """
        
        # Copy the data and get unique gender values
        character_data = self.character_data.copy()
        unique_genders = character_data['Actor gender'].dropna().unique().tolist()
        
        # check arguments types 
        if not isinstance(gender, str):
            raise TypeError("'gender' must be a string.")
        if not isinstance(max_height, (int, float)):
            raise TypeError("'max_height' must be a numerical value.")
        if not isinstance(min_height, (int, float)):   
            raise TypeError("'min_height' must be a numerical value.")
        if not isinstance(plot, bool):
            raise TypeError("'plot' must be a boolean (True/False).")
        
        #check arguments values
        if min_height > max_height:
            raise ValueError("'min_height' must be less than 'max_height'.")
        if not (gender in unique_genders or gender == 'All'):
            raise ValueError(f"'gender' must be either one of the non values in the dataframe or 'All'.")
        
        # filter the data based on parameters values
        # height range
        character_data = character_data[(character_data['Actor height'] >= min_height) & (character_data['Actor height'] <= max_height)]  
        
        # gender
        if not gender == 'All':
            character_data = character_data[character_data['Actor gender'] == gender]
        
        # plot the histogram
        if plot:
            character_data['Actor height'].plot(kind='hist', bins=100)
            plt.show()
        
        
if __name__ == '__main__':       
    test = MovieAnalysis()
    
    print(test.actor_distributions(gender = 'M', max_height = 300, min_height = 100, plot = True))
    