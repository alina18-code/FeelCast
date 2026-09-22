from flask import Flask, render_template, request

app = Flask(__name__, template_folder="../templates")

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/search", methods=["GET", "POST"])
def search():
    city = request.values.get("city")
    print(f"location:{city}")
    return f"Search submitted for {city}"  


if __name__ == "__main__":
    app.run(debug=True)