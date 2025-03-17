# Group_25

Group 25's repository for the Advanced Programming course at Nova SBE 2025

The group is composed by:

[Edoardo Beccari] - (67990@novasbe.pt) \
[Bernardo Arcão] - (68204@novasbe.pt) \
[Ricardo Ferreira] - (39175@novasbe.pt) \
[Tancredi Di Grande] - (61700@novasbe.pt)

## Movie Data Analysis App

This project analyzes movie data using Python and Streamlit, leveraging the CMU Movie Corpus dataset. It provides visual insights into movie genres, actor distributions, and AI-powered genre classification.

---

## Installation Guide

Follow these steps to set up and run the project on your local machine.

### Install Ollama and download the LLM model

Make sure you install Ollama from the [official website](https://ollama.com/download/)

After installing Ollama, download the LLM model you want to use with the app.

```sh
ollama pull mistral
```

**N.B.:** By default the app uses `mistral` for genre classification. If you wish to use a different model you can specify it in the configuration file. [View config.json](config.json)

### Clone the Repository

Clone this repository to your local machine:

```sh
git clone https://github.com/edoadro/Group_25.git
cd Group_25
```

### Set Up a Virtual Environment

Creating a virtual environment ensures that dependencies do not interfere with other Python projects on your system.

```sh
python -m venv myvenv
source myvenv/bin/activate  # On macOS/Linux
myvenv\Scripts\activate     # On Windows
```

### Install Project Dependencies

```sh
pip install -r requirements.txt
```

### Run Ollama

Make sure to run Ollama

```sh
ollama serve # Start Ollama (must remain running)
```

**N.B.:** Keep the terminal window open to ensure Ollama remains active. The app will fail without Ollama runnig. Execute the following shell commands in a new window.

### Run the Streamlit App

```sh
streamlit run MovieApp.py
```

### Deactivate the Virtual Environment (when done)

#### **For Windows (Command Prompt or PowerShell)**

```sh
venv\Scripts\deactivate
```

#### **For macOS/Linux**

```sh
deactivate
```

## How the text classification of this project can help with the UN's SDGs

The Streamlit app developed in this project serves as an interactive tool for analyzing movie data from the CMU Movie Corpus dataset. It allows users to analyze the most common movie genres, actor participation in films, and the distribution of actor height and gender. Furthermore, it tracks movie release trends over time, enabling users to filter movies by genre and observe historical patterns. Another key feature is the ability to examine birth trends, either by year or by month, providing insights into demographic shifts in the film industry.

Beyond traditional data analysis, the app uses artificial intelligence to automate genre classification. It randomly selects a movie, displays its title and plot summary, and then compares its actual database genres with those predicted by a LLM from Ollama.
As a result, this text classification project could help the United Nations Sustainable Development Goals by fostering education, inclusivity, ethical storytelling, and environmental awareness, for example.

Starting with education, SDG 4 –  “Ensure inclusive and equitable quality education and promote lifelong learning opportunities for all” – this project can be used in film studies, communication and media literacy courses. Students may use the app to explore how gender and diversity representation floats in cinema or how different genres have evolved over time. Additionally, it is a real experiment that allows students to check how AI can classify films based on descriptions.

One of the app’s key functionalities is its ability to analyze actor demographics using height and gender distribution. This feature may be used to identify gender gaps in film casting, track the evolution of female representation in different movie genres or to compare diversity trends over decades, highlighting improvements or ongoing disparities. Therefore, the app can contribute to "Reduce inequality within and among countries", SDG 10.

Although cinema is primarily an entertainment industry, it can also be a powerful tool for shaping the audience’s minds, influencing policy discussions and raising awareness about important topics such as climate change.  Thus, the project may help SDG 13 - "Take urgent action to combat climate change and its impacts" – by enabling the easy identification of environmental documentaries or films that focus on sustainability and climate crisis narratives. Moreover, it can be useful to checking trends in climate related storytelling, analyzing if the industry is prioritizing sustainability topics.

To conclude, this project bridges data science, AI, and social impact by analyzing cinema trends and automating genre classification. It supports SDG 4 (Quality Education) by enhancing media literacy, SDG 10 (Reduced Inequalities) by highlighting representation gaps, and SDG 13 (Climate Action) by tracking sustainability themes in films. By aligning with multiple UN Sustainable Development Goals, this project shows that technology can be a powerful force for change, helping us build a more just, educated, and sustainable world.



