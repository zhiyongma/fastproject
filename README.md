
---

**Chinese Documentation**: <a href="https://www.cnblogs.com/mazhiyong/" target="_blank">https://www.cnblogs.com/mazhiyong/</a>

**Source Code**: <a href="https://github.com/zhiyongma/fastproject" target="_blank">https://github.com/zhiyongma/fastproject</a>

---


## Requirements

Python 3.6+

You should install the requirments below first.

<div class="termy">

```console
$ pip install fastapi
$ pip install pymysql
$ pip install sqlalchemy
$ pip install pyjwt
$ pip install bcrypt
$ pip install passlib
$ pip install python-multipart
```

</div>

Then you should create your mysql database. Sample sql in the deploy directory.</br>
You can configure the database connection in config.py.

You will also need an ASGI server, for production such as <a href="http://www.uvicorn.org" class="external-link" target="_blank">Uvicorn</a> or <a href="https://gitlab.com/pgjones/hypercorn" class="external-link" target="_blank">Hypercorn</a>.

<div class="termy">

```console
$ pip install uvicorn
```

</div>

For production deployment, you should also install Gunicorn.
<div class="termy">

```console
$ pip install gunicorn
```

</div>


## Example

### Local Run
<div class="termy">

```console
$ uvicorn local:app --reload
```

</div>

### Server Run

Run the server with gunicorn.

<div class="termy">

```console
$ gunicorn  -c  /data/fastest/gunicorn.py -e FASTAPI_ENV=production  run:app
```

* `-c`: gunicorn config.
* `-e`: environment parameter.

</div>

Run the server with service. </br>
See the file gunicorn_fast.service in deploy directory. You should put it in /usr/lib/systemd/system for linux os. </br>
<div class="termy">

```console
$ systemctl start/stop/restart/enable gunicorn_fast.service
```

</div>


### Production config
* `-e`: `FASTAPI_ENV=production`.
* `mysql`:  configure file `config.py` .
* `gunicorn`:  configure file `gunicorn.py` .
* `service`:  configure file `gunicorn_fast.service` .

remarks: the `pidfile` in `gunicorn_fast.service` and `gunicorn.py` should point to the same one file.

### API test
##### `1、user register`
<p align="left">
  <a href="https://github.com/zhiyongma/fastproject"><img src="http://qiniu.image.xiaomafeixiang.com/register.png" alt="FastAPI"></a>
</p>

##### `2、user login`
<p align="left">
  <a href="https://github.com/zhiyongma/fastproject"><img src="http://qiniu.image.xiaomafeixiang.com/login.png" alt="FastAPI"></a>
</p>

##### `3、user info`
<p align="left">
  <a href="https://github.com/zhiyongma/fastproject"><img src="http://qiniu.image.xiaomafeixiang.com/users_me.png" alt="FastAPI"></a>
</p>


## License

This project is licensed under the terms of the MIT license.
