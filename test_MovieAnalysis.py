import pytest
from MovieAnalysis import MovieAnalysis
import pytest
from MovieAnalysis import MovieAnalysis

@pytest.fixture
def setup_analysis():
    return MovieAnalysis()

# Test movie_type method

def test_movie_type_invalid_input(setup_analysis):
    with pytest.raises(ValueError):
        setup_analysis.movie_type(25.5)  # N should be an integer

# Test actor_distributions method

def test_actor_distributions_invalid_gender(setup_analysis):
    with pytest.raises(ValueError):
        setup_analysis.actor_distributions('InvalidGender', 200, 100)

def test_actor_distributions_invalid_height_range(setup_analysis):
    with pytest.raises(ValueError):
        setup_analysis.actor_distributions('M', 100, 200)  # min_height > max_height

def test_actor_distributions_invalid_types(setup_analysis):
    with pytest.raises(TypeError):
        setup_analysis.actor_distributions('M', 'tall', 150)  # Non-numeric height
    with pytest.raises(TypeError):
        setup_analysis.actor_distributions(123, 200, 100)  # Non-string gender
    with pytest.raises(TypeError):
        setup_analysis.actor_distributions('M', 200, 'short')  # Non-numeric height

if __name__ == "__main__":
    pytest.main(['-v'])