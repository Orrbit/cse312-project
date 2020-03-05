# run.py
#!/usr/bin/env python
from biazza import app

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=8000)