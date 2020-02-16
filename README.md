#### The deployment machine learning model as a web application

After working on a machine learning project, it is the most important step: deployment.
It is here the steps that I've followed in order to figure out how to do:

1. Creating simple machine learning model by following this tutorial: 

    https://medium.com/@randerson112358/python-decision-tree-classifier-example-d73bc3aeca6

    In this step, I've created a decision tree model in order to predict whether the weather is suitable for playing golf or not.

    Source code is mostly the same except for the visualization of the decision tree.

2. Implementing the API for model by following another great tutorial:

    https://towardsdatascience.com/building-prediction-apis-in-python-part-1-series-introduction-basic-example-fe89e12ffbd3

    In the tutorial, an API is created for machine learning model for Iris dataset. I've adapted it to my model.

3. Creating web app with Flask by following the tutorial:

    https://medium.com/free-code-camp/how-to-build-a-web-app-using-pythons-flask-and-google-app-engine-52b1bb82b221

    A weather web app is created with Flask in the tutorial. Again, I've adapted it to this project. But I've not deployed on the Google Cloud.

4. Deploying it on the Heroku:

    https://devcenter.heroku.com/articles/getting-started-with-python

**Some important points:**

* The error "Couldn't find that process type"
I've run the command: heroku ps:scale web=1 --app golfprediction. Maybe, needed some extra steps such as removing existing buildpacks.
You can look at the page: https://help.heroku.com/W23OAFGK/why-am-i-seeing-couldn-t-find-that-process-type-when-trying-to-scale-dynos

* Setting Procfile:
web:gunicorn app:app is standard Procfile. It means that there is a app.py file and a flask object is created in that file. 
Hence, I've need to set it in that way: web:gunicorn GolfPrediction_API:app

* requirements.txt
requirements.txt should contain all Python packages that are used. 
If there is missing one, you can see in the log viewer in the Heroku such as "ModuleNotFoundError: No module named 'joblib'" message.
