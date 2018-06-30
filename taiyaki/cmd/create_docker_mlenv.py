import argparse
import os
import re
import stat
import jinja2


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
_env = jinja2.Environment(
    loader = jinja2.FileSystemLoader(os.path.join(BASE_DIR, 'templates'), encoding='utf-8')
)


def _get_path_by_tplname(tplname):
    sp = tplname.split('__')
    if len(sp) < 1:
        raise ValueError('invalid length')
    d = sp[:-1]
    f = sp[-1]
    if len(d) > 0:
        return os.path.join(*d), f
    else:
        return '.', f


def process(tpl_file, target_filename, filemode, **params):
    dirpath, filename = _get_path_by_tplname(tpl_file)
    os.makedirs(dirpath, exist_ok=True)
    filepath = os.path.join(dirpath, target_filename)
    with open(filepath, 'w') as f:
        f.write(_env.get_template(tpl_file).render(**params) + '\n')
    if filemode == 'executable':
        os.chmod(filepath, stat.S_IRUSR | stat.S_IRWXU | stat.S_IRWXG | stat.S_IROTH)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('datasetname')
    parser.add_argument('base_image_name')
    parser.add_argument('--docker-bin', default='tyk')
    parser.add_argument('--dockerd-hostname', default='localhost')
    parser.add_argument('--docker-working-dir', default='/dockerwork')
    parser.add_argument('--docker-volume-dir', default='/dockervolume')
    parser.add_argument('--volume-image-name', default=None)
    parser.add_argument('--app-image-name', default=None)
    parser.add_argument('--jupyter-port', default=18888)
    ns = parser.parse_args()

    # extract params
    volume_image_name = app_image_name = ns.app_image_name
    if app_image_name is None:
        rgx = re.search('^(\S+)-base$', ns.base_image_name)
        if rgx is None:
            raise ValueError('invalid base_image_name')
        app_image_name = '{}-application'.format(rgx.group(1))
    if volume_image_name is None:
        rgx = re.search('^(\S+)-base$', ns.base_image_name)
        if rgx is None:
            raise ValueError('invalid base_image_name')
        volume_image_name = '{}-volume'.format(rgx.group(1))

    # generate target files and directories
    process('utilcmd__tyk.tpl', ns.docker_bin, 'executable', hostname=ns.dockerd_hostname)
    process('env.sh.tpl', 'env.sh', None, docker_bin=ns.docker_bin)
    process('_dockerignore.tpl', '.dockerignore', None)
    process('utilcmd__build.sh.tpl', 'build.sh', 'executable', 
        docker_bin=ns.docker_bin,
        app_image_name=app_image_name
    )
    process('utilcmd__run_docker.tpl', 'run_docker', 'executable', 
        app_image_name=app_image_name,
        volume_image_name=volume_image_name,
        docker_bin=ns.docker_bin,
        jupyter_port=ns.jupyter_port
    )
    process('utilcmd__setup_datacontainer.sh.tpl', 'setup_datacontainer.sh', 'executable', 
        docker_bin=ns.docker_bin,
        volume_image_name=volume_image_name,
        docker_volume_dir=ns.docker_volume_dir
    )
    process('Dockerfile.tpl', 'Dockerfile', None, 
        base_image_name=ns.base_image_name,
        docker_working_dir=ns.docker_working_dir
    )


if __name__ == '__main__':
    main()
