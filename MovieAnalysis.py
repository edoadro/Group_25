import os
import tarfile
import urllib.request
import pandas as pd
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
        
        # Uses ast to convert the string to a dictionary
        movies = self.movie_data.copy()
        movies['Movie genres'] = movies['Movie genres'].apply(lambda x: list(ast.literal_eval(x).values()))
        genre_counts = movies.explode('Movie genres')['Movie genres'].value_counts()
        
        return genre_counts.head(N)
    
    def actor_count(self):
        """
        comments
        """
        pass
    
    def actor_distributions(self, gender: str, max_height: float, min_height: float, plot: bool = False):
        """
        comments
        """
        pass
    
    
        
if __name__ == '__main__':       
    test = MovieAnalysis()
    
    print(test.movie_type(25.5))
    