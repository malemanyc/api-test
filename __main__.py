from api.app import app

if __name__ == '__main__':
    # run application 
    app.run(host='0.0.0.0', port=80, debug=True)
