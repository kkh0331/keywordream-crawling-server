from flask import jsonify

def success_response(code, message):
  result = {
    "success": True,
    "response" : message,
    "error" : None
  }
  response = jsonify(result)
  response.status_code = code
  return response

def error_response(code, message):
  result = {
    "success": False,
    "response" : None,
    "error" : message
  }
  response = jsonify(result)
  response.status_code = code
  return response