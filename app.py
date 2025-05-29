from flask import Flask, render_template, request, jsonify
import subprocess

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/run", methods=["POST"])
def run_code():
    data = request.json
    code = data.get("code", "")
    user_input = data.get("input", "")

    try:
        result = subprocess.run(
            ["python3", "-c", code],
            input=user_input.encode(),
            capture_output=True,
            timeout=5
        )
        output = result.stdout.decode()
        error = result.stderr.decode()
        return jsonify({"output": output, "error": error})
    except subprocess.TimeoutExpired:
        return jsonify({"error": "Code execution timed out."})

if __name__ == "__main__":
    app.run(debug=True)
