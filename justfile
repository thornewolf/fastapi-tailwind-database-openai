# List all available commands
default:
    just --list

setup:
    git remote add upstream https://github.com/thornewolf/template-oct-2023
    git pull upstream main

test:
    poetry run coverage run -m unittest discover
    poetry run coverage report

# Commit to Github
commit message="Update without message": post
    git add -A; git commit -m "{{message}}"; git push

# Build CSS
css:
    npm run tailwind-build

# Convert Markdown to Jinja
post:
    poetry run python project/tools/publish_posts.py

# Publish to Railway
up: post
    railway up

# Run the app locally
run:
    poetry run uvicorn project.main:app --reload

# Create an alembic revision. (Follow with `just upgrade`)
revision message="default message" env="dev":
    poetry run alembic -x env={{env}} revision -m "{{message}}" --autogenerate
    
# Upgrade the database to the latest revision
upgrade env="dev":
    poetry run alembic -x env={{env}} upgrade head

stamp env="dev":
    poetry run alembic -x env={{env}} stamp head

# Upgrade all databases to the latest revision
upgrade-all:
    just upgrade dev
    just upgrade prod

# Delete previous revisions
wipe-versions:
     rm -r alembic/versions/*
