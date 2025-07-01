from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

contacts = []

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/contacts", methods=["GET", "POST", "DELETE"])
def manage_contacts():
    if request.method == "GET":
        return jsonify(contacts)
    elif request.method == "POST":
        data = request.json
        contacts.append(data)
        return jsonify({"message": "Contact added!"})
    elif request.method == "DELETE":
        name = request.json.get("name")
        global contacts
        contacts = [c for c in contacts if c["name"] != name]
        return jsonify({"message": "Contact deleted!"})

if __name__ == "__main__":
    app.run(debug=True)
