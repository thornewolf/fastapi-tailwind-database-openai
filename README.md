# Application Template

## Setup

### Prerequisites

- https://github.com/casey/just
- https://python-poetry.org/
- https://www.npmjs.com/

### Setup

```bash
poetry install
npm i
```

Env variables:

`.env`

```bash
AUTH0_DOMAIN=...
AUTH0_CLIENT_ID=...
AUTH0_CLIENT_SECRET=...
DATABASE_URL=...
DATABASE_URL_PROD=...
OPENAI_API_KEY=...
REDDIT_USERNAME=...
REDDIT_PASSWORD=...
REDDIT_CLIENT_ID=...
REDDIT_CLIENT_SECRET=...
ENV=dev
```

## Database Management

Whenever you change the schema, run the following commands to migrate the databse. Be sure your env variables are set.

```bash
just revision $env # where $env is dev or prod
# THIS
just upgrade $env
# OR
just upgrade-all
```

## Launching the server and css env (needs two terminals)

```bash
just css
just post && just run
```

## Going to Production

```bash
just up
```

## References

- Server built with: https://fastapi.tiangolo.com/
- Databse management: https://alembic.sqlalchemy.org/en/latest/
- Hosting: https://railway.app/
- Authentication: https://auth0.com/ - https://auth0.com/docs/quickstart/webapp/python/interactive
- Templating: https://jinja.palletsprojects.com/en/3.1.x/
- Styling: https://tailwindcss.com/
- Package management: https://python-poetry.org/

## Misc Commands

```bash
poetry run alembic init alembic
poetry run python -m unittest
```

### Educational Resources

For providing CLI arguments to alembic: https://gist.github.com/twolfson/4bc5813b022178bd7034
