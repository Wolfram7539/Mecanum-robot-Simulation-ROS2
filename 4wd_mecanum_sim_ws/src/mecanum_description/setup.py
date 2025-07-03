import os
from glob import glob
from setuptools import find_packages, setup

package_name = 'mecanum_description'

def package_files(directory, data_files):
    data_files += [
        (
            os.path.join('share', package_name, root),
            [os.path.join(root, f) for f in files]
        )
        for root, _, files in os.walk(directory) if files
    ]
    return data_files

data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml'])
    ]
deta_files = package_files('meshes', data_files)
data_files = package_files('urdf', data_files)
data_files = package_files('worlds', data_files)
setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=data_files,
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='wolfram',
    maintainer_email='wolfram@todo.todo',
    description='TODO: Package description',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
        ],
    },
)
