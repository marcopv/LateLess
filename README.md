<h1 align="center">
  <br>
  <a ><img src="https://upload.wikimedia.org/wikipedia/commons/thumb/4/49/Kb_Airports_World.svg/1024px-Kb_Airports_World.svg.png" alt="Logo" width="250"></a>
 <br> 
 <br>
    <b>
    USA Airlines Delay - LateLess 
    <b>
  <br>
</h1>

<h4 align="center"> 
<b> 
  A ML Delay Prediction App Made with Streamlit. Demo Avaliable at: <a>https://lateless.streamlit.app/</a>
<b>
</h4>

<!-- TABLE OF CONTENTS -->

  # Table of Contents
  <ol>
    <li><a href="#about-the-project">About The Project</a></li>
    <li><a href="#technology">Technology</a></li>
    <li><a href="#data">Data</a></li>
    <li><a href="#files">Files</a></li>
    <li><a href="#getting-started">Getting Started</a></li>
    <li><a href="#authors">Authors</a></li>
    <li><a href="#who-can-contribute-to-this-project?">Who can contribute to this project?</a></li>
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
The project was developed using python 3.8.10 with the following packages:

- Pandas
- Numpy
- Scikit-learn
- Pandas-profiling
- Joblib
- Streamlit

Technologies used are:

- Kubeflow
- Kubernetes
- Docker

 <p id=data>
 </p>

# Data
The data for the application is originated from [U.S. Department of Transportation's (DOT) Bureau of Transportation Statistics (BTS)](https://www.transtats.bts.gov/ONTIME/) and a simplified version is available on [Kaggle](https://www.kaggle.com/datasets/jimschacko/airlines-dataset-to-predict-a-delay): this version merged and removed some features to better represent the informations.
<br> 
The data contains 539383 BTS instances from different USA Airlines.
Since the data has been added to the `data/` directory, cloning this repository would suffice to obtain them.
<br>
Follows an example of how the dataset is organized:
<br>


|    |   id | Airline   |   Flight | AirportFrom   | AirportTo   |   DayOfWeek |   Time |   Length |   Delay |
|---:|-----:|:----------|---------:|:--------------|:------------|------------:|-------:|---------:|--------:|
|  0 |    1 | CO        |      269 | SFO           | IAH         |           3 |     15 |      205 |       1 |
|  1 |    2 | US        |     1558 | PHX           | CLT         |           3 |     15 |      222 |       1 |
|  2 |    3 | AA        |     2400 | LAX           | DFW         |           3 |     20 |      165 |       1 |
|  3 |    4 | AA        |     2466 | SFO           | DFW         |           3 |     20 |      195 |       1 |
|  4 |    5 | AS        |      108 | ANC           | SEA         |           3 |     30 |      202 |       0 |

 <p id=files>
 </p>

# Files
- dashboard-adminuser.yaml : YAML manifest to generate an user for k8s dashboard.
- DelayPrediction.yaml : YAML manifest for the depoyment of the K8s cluster.
- Kubeflow/flight_delay_prediction.ipynb : Jupyter Notebook used to generate the pipeline in kubeflow. It contains the main Machine Learning procedure including data preparation, training and validation.
- Kubeflow/katib-rsndom-forest-training.ipynb : Jupyter Notebook used for hyperparameters tuning with Katib on Random Forest Classifier.
- Kubeflow/requirements.txt : requirements for the Kubeflow environment to repeat the training.
- Kubeflow/Dataset : DataSet used for the training also avaliable on Kaggle.
- Streamlit/requirements.txt : Project Requirements for local run.
- Streamlit/info_page.py: Main Streamlit page.
- Streamlit/Dockerfile : Dockerfile used to build the docker container.
- Streamlit/data/ : directory containing the starting Dataset and a subset of it, used as example in the app.
- Streamlit/models/ : directory with Trained models used for inference in app.
- Streamlit/map/ : Map information to generate the folium airports map.
- Streamlit/pages/prediction_page.py : Second streamlit page used for prediction.
- Streamlit/style/ : directory with CSS styling information and backgound image.

 <p id=getting-started>
 </p>

# Getting Started
To run the app on your local machine first install the required python modules with:

```shell
  $ pip install -r requirements.txt
```

After that run the application with
```shell
  $ streamlit run info_page.py
```
Finally open your browser and connect to https://localhost:8501. You should be able to see the main page of the app now.

## Run on Docker
Start the Docker Engine and build the docker container given the Dockerfile in the main folder with the following command:
```shell
  $ docker build -t delay-prediction .
```
Note that with the `-t` argument we are assigning a tag or alias to the image that in this case is streamlit.

Run the docker image with:
```shell
  $ docker run -dp 8501:8501 --name delay-app delay-prediction
```
Here with the argument `-p` we are doing a port forwarding linking the port 8501 of the host to the container port used by streamlit. With `-d` we are running it in detached mode so we can use the current terminal to stop the container.

Now you can access the application at https://localhost:8501 on your browser.

Finally you can stop the container an remove it with
```shell
  $ docker stop delay-app
  $ docker rm delay-app
```

## Deploy Kubernetes 
Create an image for the streamlit application with the tag `delay-prediction`:

```shell
  $ docker build -t delay-prediction .
```
Deploy your application to Kubernetes with the command:
```shell
  $ kubectl apply -f DelayPrediction.yaml
```
It will start:
- A `Deployment`, comprising of just one replica of the pod having just one container in it, based off of the `delay-application` image from the previous step.
- A NodePort service, which will route traffic from port 30001 on the host to port 8501 inside the pods it routes to, allowing you to reach the delay prediction application via your browser.
It is possible to check the correctness of the process through the command:
```shell
  $ kubectl get deployments
```
The app is avaliable at https://localhost:30001

When done using the app the services can be stopped with:
```shell
  $ kubectl delete -f DelayPrediction.yaml
```

## Access Kubernetes Dashboard
Dashboard is a web-based Kubernetes user interface. You can use Dashboard to deploy containerized applications to a Kubernetes cluster, troubleshoot your containerized application, and manage the cluster resources.
To deploy it, run the following command:

```shell
$ kubectl apply -f https://raw.githubusercontent.com/kubernetes/dashboard/v2.7.0/aio/deploy/recommended.yaml
```

Currently, Dashboard only supports logging in with a Bearer Token. Creating a token requires an account.
<br>
We are gonna create a dummy account with administrative privilege. In a complex environment this could present a security threat but beaing our application local we are confident that this shouldn't be a problem. We already provided a `dashboard-adminuser.yaml` so run:

```shell
  $ kubectl apply -f dashboard-adminuser.yaml
```
Created the account, we are gonna generate a token with the following command:

```shell
  $ kubectl -n kubernetes-dashboard create token admin-user
```
Save the token (because you will need it next) and to start the dashboard run:

 ```shell
  $ kubectl proxy
```

Kubectl will make Dashboard available at http://localhost:8001/api/v1/namespaces/kubernetes-dashboard/services/https:kubernetes-dashboard:/proxy/.

From the dashboard it is possible to create the pod cluster with the + icon on the upper right section of the interface. Now it is possible create the cluster from input, copy-pasting the content of `DelayPrediction.yaml` or create it from file selecting the same file.

To cleanup the setup we built, first remove the admin account:

```shell
  $ kubectl -n kubernetes-dashboard delete serviceaccount admin-user
  $ kubectl -n kubernetes-dashboard delete clusterrolebinding admin-user
```

To remove the dashboard altogether do:

```shell
  $ kubectl delete -f https://raw.githubusercontent.com/kubernetes/dashboard/v2.7.0/aio/deploy/recommended.yaml
```

Now it is also possible to stop the application with the command stated before.


 <p id=authors>
 </p>
 
# Authors
- Marco Pastore: m.pastore55@studenti.unisa.it - matr. 0622701851
- Speranza Ranieri: s.ranieri4@studenti.unisa.it - matr. 0622701687


 <p id=who-can-contribute-to-this-project?>
 </p>

# Who can contribute to this project?
Since this is an assignment project, only the authors can contribute to this project. Despite this, you are still free to use and distribute the code contained in this repository for your own projects according to **GNU GPL v3**.

 <p id=license>
 </p>
 
# License
Distributed under the GNU License. See LICENSE.md for more information.
