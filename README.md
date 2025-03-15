# Group_25
Group 25's repository for the Advanced Programming course at Nova SBE 2025

The group is composed by: 

Edoardo Beccari (67990@novasbe.pt) \
Bernardo Arcão (68204@novasbe.pt) \
Ricardo Ferreira (39175@novasbe.pt) \
Tancredi Di Grande (61700@novasbe.pt)


## Local LLM Integration (Phase 2)
In the third page of the Streamlit app, we implemented a Local LLM-based movie genre classification pipeline. This was achieved using Ollama with the lightweight Mistral model.

Features:
Displays a random movie title and its plot summary.
Shows the actual genres associated with the movie from the dataset.
Sends the movie summary to the local LLM (Mistral via Ollama) to predict its genres.
Compares the predicted genres with the actual genres to evaluate correctness.

Prerequisites:
To use this feature, you need to have Ollama installed locally with the desired model.

On the Powershell execute the following commands:

### Install Ollama (Windows):
winget install Ollama.Ollama
### Mac...
### Run Ollama locally:
ollama serve
### Pull the Mistral model (or any other supported model):
ollama pull mistral
### After all dependencies are installed and Ollama is running, start the Streamlit app:
streamlit run MovieApp.py


Note: You don't need to run this everytime, just one time only.
