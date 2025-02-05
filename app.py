from flask import Flask, render_template, request
import mysql.connector
import pickle

app = Flask(__name__, template_folder="templates", static_folder="static")

# Load ML model safely
try:
    vectorizer, model = pickle.load(open("model/model.pkl", "rb"))
except Exception as e:
    print(f"Error loading ML model: {e}")
    vectorizer, model = None, None

# Connect to MySQL with error handling
try:
    db = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Gowtham@2203",
        database="epharma"
    )
    cursor = db.cursor()
except mysql.connector.Error as err:
    print(f"Error: {err}")
    db, cursor = None, None

@app.route("/", methods=["GET", "POST"])
def index():
    error_message = None
    medicine_name = "No data available"
    gender = ""
    age = ""
    symptoms = ""

    if request.method == "POST":
        gender = request.form.get("Gender", "").strip()
        age_input = request.form.get("age", "").strip()
        symptoms = request.form.get("symptoms", "").strip()

        print(f"DEBUG: Received Age Input: '{age_input}'")  # Debugging Line

        # Force conversion to integer
        try:
            age = int(age_input)
            if age <= 0:
                error_message = "Please enter a valid positive age."
        except ValueError:
            error_message = "Please enter a valid numeric age."

        print(f"DEBUG: Processed Age: {age}, Error: {error_message}")  # Debugging Line

        if error_message:
            return render_template("index.html", error=error_message, gender=gender, age=age_input, symptoms=symptoms)

        # ML model prediction
        if vectorizer and model:
            try:
                symptom_vectorized = vectorizer.transform([symptoms])
                predicted_medicine = model.predict(symptom_vectorized)[0]
                medicine_name = predicted_medicine
            except Exception as e:
                print(f"Model prediction error: {e}")

        # Database query
        if cursor:
            try:
                cursor.execute("SELECT medicine FROM medicines WHERE symptom=%s", (symptoms,))
                result = cursor.fetchone()
                if result:
                    medicine_name = result[0]
            except mysql.connector.Error as e:
                print(f"Database error: {e}")

        return render_template("results.html", gender=gender, age=age, symptoms=symptoms, medicine=medicine_name)

    return render_template("index.html", error=error_message, gender=gender, age=age, symptoms=symptoms)

# First Aid Routes
@app.route("/cpr")
def cpr():
    return render_template("first_aid/cpr.html")

@app.route("/snake_bites")
def snake_bites():
    return render_template("first_aid/snake_bites.html")

@app.route("/fire_accidents")
def fire_accidents():
    return render_template("first_aid/fire_accidents.html")

@app.route("/electric_shocks")
def electric_shocks():
    return render_template("first_aid/electric_shocks.html")

if __name__ == "__main__":
    app.run(debug=True)
