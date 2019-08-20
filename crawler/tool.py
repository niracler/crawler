import os
import uuid

import paramiko


def random_filename(filename):
    ext = os.path.splitext(filename)[1]
    new_filename = uuid.uuid4().hex + ext
    return new_filename


def sftp_upload(host, port, username, password, local, remote):
    sf = paramiko.Transport(host, port)
    sf.connect(username=username, password=password)
    sftp = paramiko.SFTPClient.from_transport(sf)
    try:
        if os.path.isdir(local):  # 判断本地参数是目录还是文件
            for f in os.listdir(local):  # 遍历本地目录
                sftp.put(os.path.join(local + f), os.path.join(remote + f))  # 上传目录中的文件
        else:
            sftp.put(local, remote)  # 上传文件
    except Exception as e:
        print('upload exception:', e)
    sf.close()
