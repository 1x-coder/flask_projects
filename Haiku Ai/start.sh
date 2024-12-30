# For development use (simple logging, etc):
python3 app.py
# For production use: 
# gunicorn server:app -w 1 --log-file -