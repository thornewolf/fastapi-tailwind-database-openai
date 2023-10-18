# Personal Dictionary

## Setup

Env variables:

`.env`

```bash
AUTH0_DOMAIN=...
AUTH0_CLIENT_ID=...
AUTH0_CLIENT_SECRET=...
DATABASE_URL=...
DATABASE_URL_PROD=...
OPENAI_API_KEY=...
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

## Launching the server

```bash
just run
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
# template-oct-2023
