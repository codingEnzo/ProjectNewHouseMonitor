# -*- coding:utf-8 -*-
from fabric.api import run, env, parallel, cd, put
from fabric.decorators import hosts


env.roledefs = {
    'worker': [
        '10.30.1.64',
        '10.30.1.51',
        '10.30.1.65',
        '10.30.1.66',
        ]
}

env.warn_only = True
env.user = 'chiufung'
env.password = '12345678'


def set_root():
    env.user = 'root'
    env.password = 'gh001'


def set_prod_env():
    run('echo "DJANGO_SETTINGS_MODULE=fangadmin.settings.prod\nexport DJANGO_SETTINGS_MODULE" >> ~/.bash_profile')
    run('echo "DJANGO_SETTINGS_MODULE=fangadmin.settings.prod\nexport DJANGO_SETTINGS_MODULE" >> ~/.zsh_rc')


@parallel
def install_env():
    "运行root"
    run('mv /etc/localtime /etc/localtime.bak')
    run('ln -s /usr/share/zoneinfo/Asia/Shanghai /etc/localtime')
    run('yum makecache')
    run('yum install -y git zsh tmux')
    run('yum -y install epel-release')
    run('yum install -y python34')
    run('yum install -y python34-devel')
    run('yum install -y python34-pip')
    run('yum install -y python-devel')
    run('yum install -y zlib-devel')
    run('yum install -y openssl-devel')
    run('yum install libxslt-devel  libxslt libxml2 libxml2-devel -y')
    run('pip3 install ipython -i https://pypi.douban.com/simple/')
    run('pip3 install virtualenv -i https://pypi.douban.com/simple/')
    run('pip install supervisor')
    run('useradd chiufung')
    # 修改密码好方法
    run('echo -e "12345678\\n12345678" | passwd chiufung')


def install_zsh():
    run('sh -c "$(curl -fsSL https://raw.githubusercontent.com/robbyrussell/oh-my-zsh/master/tools/install.sh)"')


def test_ls():
    run('ls -al')


def install_project():
    run('mkdir -p ~/.config/pip/')
    put('conf/pip.conf', '~/.config/pip/')
    run('mkdir /home/chiufung/work')

    with cd('/home/chiufung/work'):
        run('rm -rf ProjectNewHouseMonitor')
        run('git clone http://10.30.4.20/ProjectNewHouse/ProjectNewHouseMonitor.git')

    with cd('/home/chiufung/work/ProjectNewHouseMonitor'):
        run('virtualenv .venv3 -p python3')


def install_s3_client():
    put('conf/.s3cfg', '~/')
    with cd('/home/chiufung/work/ProjectNewHouseMonitor'):
        run('.venv3/bin/pip3 install s3cmd airflow[3] -i https://pypi.douban.com/simple/')


@parallel
def update():
    with cd('/home/chiufung/work/ProjectNewHouseMonitor'):
        run('git fetch')
        run('git reset --hard origin/dev_airflow')
        run('git checkout dev_airflow')
        run('.venv3/bin/pip3 install -r requirements/common.txt')


def start():
    with cd('work/ProjectNewHouseMonitor'):
        run('supervisord -c conf/supervisord.conf')


@parallel
def start_all():
    with cd('work/ProjectNewHouseMonitor'):
        run('supervisorctl -c conf/supervisord.conf start all')


@parallel
def stop():
    with cd('work/ProjectNewHouseMonitor'):
        run('supervisorctl -c conf/supervisord.conf stop all')


@parallel
def restart():
    with cd('work/ProjectNewHouseMonitor'):
        run('supervisorctl -c conf/supervisord.conf stop all')
        run('supervisorctl -c conf/supervisord.conf restart celery_worker:*')


def reload():
    with cd('work/ProjectNewHouseMonitor'):
        run('supervisorctl -c conf/supervisord.conf reload')


def stop_wsgi():
    with cd('/home/chiufung/work/ProjectNewHouseMonitor/'):
        run('supervisorctl -c conf/supervisord.conf stop wsgi')
        run('supervisorctl -c conf/supervisord.conf stop APIlogWeb')


def start_wsgi():
    with cd('/home/chiufung/work/ProjectNewHouseMonitor/'):
        run('supervisorctl -c conf/supervisord.conf  start wsgi')


@hosts('root@10.30.1.16')
def install_pg_server():
    run('yum install -y https://download.postgresql.org/pub/repos/yum/9.6/redhat/rhel-7-x86_64/pgdg-centos96-9.6-3.noarch.rpm')
    run('yum install -y postgresql96')
    run('yum install -y postgresql96-server')
    run('/usr/pgsql-9.6/bin/postgresql96-setup initdb')
    run('systemctl enable postgresql-9.6')
    run('systemctl start postgresql-9.6')


def update_time():
    run('ntpdate cn.ntp.org.cn')


def restart_celery():
    "使用信号重启celery"
    run('pkill -HUP celery')


def kill_celery():
    "使用信号重启celery"
    run('pkill -9 celery')


def free():
    run('free -h')


def test():
    run('ps aux |grep log_celery')
