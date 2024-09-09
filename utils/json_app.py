from flask import jsonify
from utils.api_result import error_response
from werkzeug.exceptions import HTTPException, _aborter, default_exceptions

def JsonApp(app):
  def error_handling(error):
    error_message = error.description if isinstance(error, HTTPException) else _aborter.mapping[500].description
    error_code = error.code if isinstance(error, HTTPException) else 500
    return error_response(error_code, error_message)
  
  for code in default_exceptions.keys():
    app.register_error_handler(code, error_handling)
    
  return app