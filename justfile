# List all available commands
default:
    just --list

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
    poetry run python app/tools/publish_posts.py

# Publish to Railway
up: post
    just db-sync-and-upgrade prod
    railway up

# Run the app locally
run:
    poetry run uvicorn app.main:app --reload

# Create an alembic revision. (Follow with `just upgrade`)
db-revision env="dev" message="default message":
    poetry run alembic -x env={{env}} revision -m "{{message}}" --autogenerate
    
# Upgrade the database to the latest revision
db-upgrade env="dev":
    poetry run alembic -x env={{env}} upgrade head

# Set the alebic known schema to what is present in the database
db-stamp env="dev":
    poetry run alembic -x env={{env}} stamp head

# Sync, calculate diffs in current schema, then upgrade
db-sync-and-upgrade env="dev":
    just db-stamp {{env}}
    just db-revision {{env}} "automatic revision" 
    just db-upgrade {{env}}


# Delete previous revisions
db-wipe-versions:
     rm -r alembic/versions/*
