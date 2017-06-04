# Files

### docker-compose.yml

* `docker-compose.yml`: primary `docker-compose` configuration for all services. It is not usable alone though, because it does not provide any docker image source (`build` or `image`).
* `docker-compose.build.yml`: provides `build` keys for all built images. Can be used on CI server to build images.
* `docker-compose.image.yml`: provides `image` keys for all built images. Can be used on CI server to push images and on application server to pull and run images.
* `docker-compose.development.yml`: provides development configuration.

### docker-compose wrappers

* `dcb` (**d**ocker-**c**ompose-**b**uild): wrapper to use `docker-compose.yml` and  `docker-compose.build.yml`, e.g.:
    ```
    $ ./dcb build
    ```
* `dcbi` (**d**ocker-**c**ompose-**b**uild-**i**mage): wrapper to use `docker-compose.yml`,  `docker-compose.build.yml` and `docker-compose.image.yml`, e.g.:
  ```
  $ BRANCH=master ./dcbi push
  ```
  Note the `BRANCH` environment variable: it specifies docker tag onto which images are pushed
* `dci` (**d**ocker-**c**ompose-**i**mage): wrapper to use `docker-compose.yml`  and `docker-compose.image.yml`, e.g.:
  ```
  $ BRANCH=master ./dci pull
  ```
  Note the `BRANCH` environment variable: it specifies docker tag from which images are pulled
* `dcd` (**d**ocker-**c**ompose-**d**evelopment): wrapper to use `docker-compose.yml`  and `docker-compose.development.yml`, e.g.:
  ```
  $ BRANCH=master ./dcd up
  ```

# Development configuration

In this configuration:
 * Your `node_modules` are mounted from `frontend/skael/node_modules` so they are persistent between containers rebuilds and restarts
 * Your `virtualenv` is mounted from `backend/skael/virtualenv` so it is persistent between containers rebuilds and restarts
 * Angular app is ran with development server
 * Flask app is ran by flask debugger instead of uWSGI
 * Your code is mounted into container so code auto-reload just works

### Bootstrapping

Build docker images

```bash
$ ./dcb build
```

Pull `node_modules` and `virtualenv` from build images

```
$ CONTAINER=$(./dcb run -d --no-deps --rm nginx sleep infinity | grep nginx_run_) && sudo docker cp $CONTAINER:/skael/node_modules frontend/skael && docker stop $CONTAINER
$ CONTAINER=$(./dcb run -d --no-deps --rm api sleep infinity | grep api_run_) && sudo docker cp $CONTAINER:/virtualenv backend && docker stop $CONTAINER
```

Now you can start your app

```
$ ./dcd up
```

### Importing database dumps (overwriting current data)

```
$ ./db-import dump.psql
```

### Accessing the psql shell

```
$ ./dcd exec postgres psql -U postgres
```

### Adding new dependencies

Frontend:

```
[desktop] ~/Dev/skael> ./dcd exec nginx bash   
root@cc2d3466b75c:/skael# npm install --save react
```

Backend:

```
[desktop] ~/Dev/skael> ./dcd exec api bash   
root@1958b4f49cba:/skael# pip install aiohttp
root@1958b4f49cba:/skael# pip freeze > requirements.txt
```
