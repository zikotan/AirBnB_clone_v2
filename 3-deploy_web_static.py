#!/usr/bin/python3
"""destribute an archive to a web server"""

from fabric.api import *
import os
import os.path
import datetime
env.hosts = ['34.239.248.211', '18.234.107.30']
env.user = 'ubuntu'


def do_pack():
    """compress + bundle local sweb files"""
    if not os.path.isdir('versions'):
        local('mkdir -p versions')
    time = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    packed = 'versions/web_static_' + time + '.tgz'
    local('tar -cvzf {} web_static'.format(packed))
    return (packed)


def do_deploy(archive_path):
    """deploy an archive from the archive_path"""
    if os.path.exists(archive_path) is False:
        return False

    file_name = os.path.splitext(os.path.split(archive_path)[1])[0]
    target = '/data/web_static/releases/' + file_name
    path = archive_path.split('/')[1]
    try:
        put(archive_path, "/tmp/")
        run('sudo mkdir -p ' + target)
        run('sudo tar -xzf /tmp/' + path + ' -C ' + target + '/')
        run('sudo rm /tmp/' + path)
        run('sudo mv ' + target + '/web_static/* ' + target + '/')
        run('sudo rm -rf ' + target + '/web_static')
        run('sudo rm -rf /data/web_static/current')
        run('sudo ln -s ' + target + '/ /data/web_static/current')
        print('deploy success')
        return True
    except Exception as e:
        print("Error:", e)
        return False


def deploy():
    """make and ship static"""
    path = do_pack()
    if path is None:
        return False
    return do_deploy(path)
