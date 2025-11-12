# iRental - [A Short Description of Your Project]
(e.g., "A Flask app to predict rental prices using a machine learning model.")

This application allows users to register, upload CSV data, and get price predictions.

---

## 1. Prerequisites

* Python 3.8+
* PostgreSQL

---

## 2. Setup and Installation

1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/iamtatendakagande/irental.git](https://github.com/iamtatendakagande/irental.git)
    cd irental
    ```

2.  **Create and activate a virtual environment:**
    (On Mac/Linux)
    ```bash
    python3 -m venv .venv
    source .venv/bin/activate
    ```
    (On Windows)
    ```bash
    py -3 -m venv .venv
    .venv\Scripts\activate
    ```

3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Configure Environment Variables:**
    Copy the example `.env.example` file to a new `.env` file.
    ```bash
    cp .env.example .env
    ```
    Now, open the `.env` file and add your database URL.

    **Example `.env` file:**
    ```
    FLASK_APP=irent.py
    DATABASE_URL='postgresql://tkagande:@127.0.0.1/irental'
    ```

5.  **Set up the Database:**
    (Make sure your PostgreSQL server is running and you have created the empty database)
    ```bash
    # e.g., createdb irental
    
    flask db upgrade
    ```
    *(Note: `flask db init` is only run once. `flask db migrate` is for when you change models. A new user only needs to `upgrade`.)*

---

## 3. Running the Application
    With your environment variables set and the database upgraded, run the app:

    ```bash
    flask run
    ```

## 4. How to Use the App
    Navigate to http://127.0.0.1:5000/register to create a new user account.
    Log in with your new account.

    Go to the "Suburbs" page (/suburbs) to upload the required suburb data. (You can find an example CSV in /data_templates/suburbs.csv).
    To get a prediction, go to the "Predict" page (/predict).
    Download the prediction template , fill it out, and upload it to get your results.

## 5. The ML Model
    Option A The model can be re-trained [Keras/Scikit-Learn] model. The file is found is machine/model/HarareRentNeuralNetworkModel.py and will saved as machine/pickled/HarareRentNeuralNetworkModel.keras.

    Option B: This project is already trained and the file is machine/pickled/HarareRentNeuralNetworkModel.keras.