# Sonar Analyzer

<center>
<img src="assets/riachuelo_submarine.jpg" width="400px">
</center>

Sonar Analyzer is a tool developed by the Researchers of the Signal Processing Laboratory (LPS) from the Federal University of Rio de Janeiro, in order to make it easier to analyzer Sonar Signals and evaluate the machine learning models developed at the lab. This tool was created using [Streamlit](https://www.streamlit.io/), which is an open-source app framework for Machine Learning and Data Science teams.

# Running Locally
To run this application locally you must create a virtual environment, then install streamlit and run the following command:
```bash
$ pip install streamlit
$ streamlit run https://github.com/viniciusdsmello/SonarAnalyzer.git
``` 

# Running with Docker
To run this project using docker you need to first build the image:

```bash
$ docker build . -t sonar-analyzer
```

Then use docker compose to start the container:

```bash
docker-compose up
```
