# from fabric.api import cd, env, local, run
from fabric import Connection, task
import invoke

# env.user = 'kitarez'
# env.hosts = ['kitarez.uber.space']
# code_dir = '~/kita-rezepte'

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


# # call with: `fab server_pull:my_branch`
# def server_pull(branch='master'):
#     with cd(code_dir):
#         run("git pull origin " + branch)


# # def install_requirements():
# #     run("pip3.6 install -r stationsplan/requirements.txt --user")


# def staticfiles():
#     with cd(code_dir):
#         run("python3.6 manage.py collectstatic --noinput")


# def migrate():
#     with cd(code_dir):
#         run("python3.6 manage.py migrate")


# # def restart_server():
# #     run("touch ~/stationsplan/stationsplan/uberspace_wsgi.py")


# # call with: `fab deploy:my_branch`
# def deploy(branch='master'):
#     server_pull(branch)
#     # install_requirements()
#     migrate()
#     staticfiles()
#     # copy_htaccess()
#     # restart_server()
