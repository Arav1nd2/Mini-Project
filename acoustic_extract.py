import docker
import tarfile
import shutil
import os
import pandas as pd


def read_csv(filename, op_type):
    _df = pd.read_csv(filename, sep=';')
    _df['filename'] = op_type + filename.split('/')[-1].split('.')[0]
    return _df
# start merging files


def merger(op_type):
    filenames = ['./Acoustic/output/{}/'.format(op_type) + f for f in os.listdir(
        './Acoustic/output/{}/'.format(op_type))]
    # print(filenames)
    # print(read_csv(filenames[0], op_type))
    df = pd.concat([read_csv(f, op_type) for f in filenames])
    return df


def acoustic_features():
    docker_client = docker.from_env()

    # Build an opensmile image

    docker_client.images.build(
        path="./Acoustic", tag="opensmile-v2.0.0", pull=True)

    container = docker_client.containers.run('opensmile-v2.0.0', detach=True)

    f = open('./Acoustic/acoustic.tar', 'wb')
    bits, stat = container.get_archive('/app/output/')

    for chunk in bits:
        f.write(chunk)
    f.close()

    container.remove(force=True)

    docker_client.images.remove(image="opensmile-v2.0.0", force=True)

    raw_data = tarfile.open('./Acoustic/acoustic.tar')
    raw_data.extractall('./Acoustic/')
    raw_data.close()

    os.remove('./Acoustic/acoustic.tar')
    d_df = merger('D')
    nd_df = merger('ND')

    op = pd.concat([d_df, nd_df])
    op.drop(['name'], axis=1, inplace=True)
    op.to_csv('./Acoustic.csv', sep=';')
    shutil.rmtree('./Acoustic/output')
    return op
