from setuptools import setup, find_packages

setup(
    name='fsp-thermal-model',
    version='0.1.0',
    author='Curiefuel',
    author_email='hello@curiefuel.com',
    description='Thermal system model for fission surface power — heat pipes, Stirling conversion, radiator sizing with uncertainty quantification',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/curiefuel/fsp-thermal-model',
    packages=find_packages(),
    python_requires='>=3.10',
    install_requires=['numpy>=1.24.0', 'scipy>=1.10.0', 'matplotlib>=3.7.0'],
)
