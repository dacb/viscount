from flask import Flask

app = Flask("viscount")
app.config.from_object('config')

from viscount import user, views, project, job, file, event, worker
