# Sonar Analyzer

<center>
<img src="assets/riachuelo_submarine.jpg" width="400px">
</center>

Sonar Analyzer is a tool developed by the Researchers of the Signal Processing Laboratory (LPS) from the Federal University of Rio de Janeiro, in order to make it easier to analyzer Sonar Signals and evaluate the machine learning models developed at the lab. This tool was created using [Streamlit](https://www.streamlit.io/), which is an open-source app framework for Machine Learning and Data Science teams.

# Running Locally
First you will need to clone this repository and, then enter to the cloned directory:
```bash
$ git clone https://github.com/viniciusdsmello/SonarAnalyzer.git
$ cd SonarAnalyzer/
```

To run this application locally you must create a virtual environment, then install the requirements by running the following commands:
```bash
$ pip install -r requirements.txt
$ streamlit run main.py
```

# Running with Docker
To run this project using docker you need to first build the image:

```bash
$ docker build . -t sonar-analyzer
```

Then use docker compose to start the container:

```bash
docker-compose up --build
```
