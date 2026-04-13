import os

if __name__ == "__main__":
    if os.environ.get("RENDER"):
        app.run(host="0.0.0.0", port=10000)
    else:
        app.run(debug=True)
