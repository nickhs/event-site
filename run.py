from eventsite import app

app.run(host=app.config['HOST'], port=app.config['PORT'])
