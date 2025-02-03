from flask import Flask, render_template, request
import mysql.connector
import pickle

app = Flask(__name__, template_folder="templates", static_folder="static")

# Load ML model
vectorizer, model = pickle.load(open("model/model.pkl", "rb"))

# Connect to MySQL
db = mysql.connector.connect(host="localhost", user="root", password="Gowtham@2203", database="epharma")
cursor = db.cursor()

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        name = request.form["name"]
        age = request.form["age"]

        symptoms = request.form["symptoms"]

        symptom_vectorized = vectorizer.transform([symptoms])
        predicted_medicine = model.predict(symptom_vectorized)[0]

        cursor.execute("SELECT medicine FROM medicines WHERE symptom=%s", (symptoms,))
        result = cursor.fetchone()
        medicine_name = result[0] if result else predicted_medicine

        return render_template("results.html", name=name, age=age, symptoms=symptoms, medicine=medicine_name)


    return render_template("index.html")

# Fix First Aid Routes to Correct Folder
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
'''from flask import Flask, render_template

app = Flask(__name__, template_folder="templates")

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/result", methods=["POST"])
def result():
    # Example variables (replace with actual logic)
    name = "John Doe"
    age = 30
    symptoms = "Headache"
    medicine_name = "Paracetamol"

    return render_template("result.html", name=name, age=age, symptoms=symptoms, medicine=medicine_name)

if __name__ == "__main__":
    app.run(debug=True)'''


