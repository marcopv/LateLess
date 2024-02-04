<h1 align="center">
  <br>
  <a ><img src="https://upload.wikimedia.org/wikipedia/commons/thumb/4/49/Kb_Airports_World.svg/1024px-Kb_Airports_World.svg.png" alt="Logo" width="250"></a>
 <br> 
 <br>
    <b>
    USA Airlines Delay - Group 14 
    <b>
  <br>
</h1>

<h4 align="center"> 
<b> 
  A ML Delay Prediction App Made with Streamlit.
<b>
</h4>

<!-- TABLE OF CONTENTS -->

  # Table of Contents
  <ol>
    <li><a href="#about-the-project">About The Project</a></li>
    <li><a href="#technology">Technology</a></li>
    <li><a href="#data">Data</a></li>
    <li><a href="#keyfeatures">Key Features</a></li>
    <li><a href="#authors">Authors</a></li>
    <li><a href="#license">License</a></li>
  </ol>

 <p id=about-the-project>
 </p>
 
# About The Project
Flight delay plays an important role in both profits and loss of the airlines. An accurate estimation of flight delay is critical for airlines because the results can be applied to increase customer satisfaction and incomes of airline agencies. <br>
 So, the aim of the application is to allow the prediction of a specific US flight delay through the use of Machine Learning techniques.

 <p id=technology>
 </p>
 
# Technology

Technologies used are:
- Streamlit
- Kubeflow
- Kubernetes
- Docker

 <p id=data>
 </p>

# Data
The data for the application is originated from [U.S. Department of Transportation's (DOT) Bureau of Transportation Statistics (BTS)](https://www.transtats.bts.gov/ONTIME/) and a simplified version is available on [Kaggle](https://www.kaggle.com/datasets/jimschacko/airlines-dataset-to-predict-a-delay). This version merged and removed some features to better represent the information.
<br> 
The dataset used contains 539383 BTS instances from different USA Airlines.

A sample of the DataSet can be found below:
<style>
  th, tr:nth-child(Even){
    background-color: #fefefe!important;
    color: black!important
  }
  tr:nth-child(Odd){
    background-color: #f6f8fa!important;
    color: black!important
  }
</style>

|    |   id | Airline   |   Flight | AirportFrom   | AirportTo   |   DayOfWeek |   Time |   Length |   Delay |
|---:|-----:|:----------|---------:|:--------------|:------------|------------:|-------:|---------:|--------:|
|  0 |    1 | CO        |      269 | SFO           | IAH         |           3 |     15 |      205 |       1 |
|  1 |    2 | US        |     1558 | PHX           | CLT         |           3 |     15 |      222 |       1 |
|  2 |    3 | AA        |     2400 | LAX           | DFW         |           3 |     20 |      165 |       1 |
|  3 |    4 | AA        |     2466 | SFO           | DFW         |           3 |     20 |      195 |       1 |
|  4 |    5 | AS        |      108 | ANC           | SEA         |           3 |     30 |      202 |       0 |

 <p id=keyfeatures>
 </p>

# Key Features
The application consist of two pages:
- The info page where a brief description of the application and methodologies used to create ad app is present
- The prediction page where it is possible to insert data to make a prediction, view USA airports on the map and click them to show te flight in a specific day.
 
 <p id=authors>
 </p>
 
# Authors
- Marco Pastore: m.pastore55@studenti.unisa.it
- Speranza Ranieri: s.ranieri4@studenti.unisa.it

 <p id=license>
 </p>
 
# License
Distributed under the **GNU GPL v3** license.