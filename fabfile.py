# from fabric.api import cd, env, local, run
from fabric import Connection, task
import invoke

host = 'kitarez'

def run(command):
    Connection(host).run(command)


@task
def test(ctx, verbosity='1'):
    invoke.run(f"python ./manage.py test rezepte -v {verbosity}")


@task
def makemigrations(ctx):
    invoke.run("python ./manage.py makemigrations rezepte")


@task
def migrate_local(ctx):
    invoke.run("python ./manage.py migrate rezepte")


@task
def serve(ctx):
    invoke.run("./manage.py runserver")


@task
def sass(ctx):
    invoke.run("sass rezepte/static/css/main.{scss,css}")
    invoke.run("sass rezepte/static/css/print.{scss,css}")


@task
def commit(ctx):
    invoke.run("git add -p && git commit")


@task
def push(ctx):
    invoke.run("git push")


@task
def prepare_deploy(ctx):
    test()
    commit()
    push()


code_dir = "~/kita-rezepte"
# call with: `fab server_pull:my_branch`
@task
def server_pull(ctx, branch='master'):
    run(f"cd {code_dir} && git pull origin {branch}")


@task
def install_requirements(ctx):
    run(f"cd {code_dir} && pip3.6 install -r requirements.txt --user")


@task
def staticfiles(ctx):
    run(f"python3.6 {code_dir}/kitarezepte/manage.py collectstatic --noinput")


@task
def migrate(ctx):
    run(f"python3.6 {code_dir}/kitarezepte/manage.py migrate")


# def restart_server():
#     run("touch ~/stationsplan/stationsplan/uberspace_wsgi.py")


# # call with: `fab deploy:my_branch`
# def deploy(branch='master'):
#     server_pull(branch)
#     # install_requirements()
#     migrate()
#     staticfiles()
#     # copy_htaccess()
#     # restart_server()
