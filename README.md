# jorah
Backend for autograder service

## Setup
Using Python Flask for our backend service. In order to maintain the correct python environment to run, setup a python virtual environment in the folder of the repository. I have been using pyenv with virtualenv, here is a good tutorial for that: https://medium.com/@adocquin/mastering-python-virtual-environments-with-pyenv-and-pyenv-virtualenv-c4e017c0b173

Once you have a virtual environment set up, use python version 3.11 or higher (I am using 3.11.7). In order to install the necessary dependencies, simply run:

`pip install -r requirements.txt`

This should install all the necessary libraries for you to connect to the MongoDB Atlas instance using Flask. In order to test that your connection is working properly, run:

`flask run -p 4000`

And you should see text come up that looks something like this:<img width="740" alt="Screenshot 2024-03-06 at 4 19 35 PM" src="https://github.com/The-DSA-Duckies/jorah/assets/62037622/d0a04a2a-24ad-4bc3-a9d3-be92af36f695">

If you follow the URL that's provided in the screenshot there, you should get to a page that has a single line of text that says "My First API !!"
That means that the Flask server is up and running successfully. To verify that you have connected to the MongoDB Atlas instance, look for the following text after navigating to the URL:<img width="739" alt="Screenshot 2024-03-06 at 4 21 15 PM" src="https://github.com/The-DSA-Duckies/jorah/assets/62037622/c3d4c5de-6ba6-447c-8435-db86e01508c3">

This won't work immediately because you won't have a `.env` folder in your project that contains the MongoDB username and password for the URI. Simply place the `.env` folder in the root of the project directory, and you should be able to successfully connect, and then start development using the MongoDB Atlas instance.

## Saving Dependencies
If your changes to the backend include a change to the dependencies that we are using (i.e you had to `pip install` something new), please save those dependencies in the `requirements.txt` file in the root of the project, and don't commit until we know that others can run the service with the new dependencies (create a PR for us to test it). In order to save your new dependencies in the file, run:

`pip freeze > requirements.txt`
