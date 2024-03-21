# Flask Grocery Store

Flask Grocery Store is a web application that allows users to browse and manage grocery store inventory. It provides features such as searching for products, adding items to a cart, and managing inventory for admins.


Step 1: Install Dependencies
Make sure you have the necessary dependencies installed. The code requires the following packages:

flask: A web framework for Python
sqlite3: A module to interact with SQLite databases
jinja2: A templating engine for Python
matplotlib: A plotting library for Python
You can install these dependencies by running the following command:
    pip install flask sqlite3 jinja2 matplotlib

Step 2: Set Up the Database
The Database setup is handled by the database.py file. It is called in the app.py file.

Step 3: Run the Application
Once the dependencies are installed and the database is set up, you can run the Flask application. Use the following command to start the application:
    python app.py

After running the command, you should see output similar to the following:
    * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
This indicates that the Flask application is running locally on your machine.

Open a web browser and enter the following URL:
    http://localhost:5000/

This will take you to the home page of the application. From there, you can navigate to different sections of the application, such as the inventory, cart, search, and statistics.

Note: Make sure to replace localhost with the appropriate IP address if you're running the application on a remote server.

That's it! You have successfully set up and run the code. You can now use the web application to interact with the features provided by the code.