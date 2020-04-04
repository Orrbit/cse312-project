# run.py
#!/usr/bin/env python
from biazza import app

globalLikes = 0 # Probably going to keep track of all the likes. But will probably be a dictionary

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=8000)