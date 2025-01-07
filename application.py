from app import application
import os

if __name__ == "__main__":
    debug_mode = os.getenv('FLASK_DEBUG', 'False').lower() in ['true', '1', 't']
    application.run(port=8088, debug=debug_mode)
