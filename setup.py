from setuptools import setup, find_packages

setup(
        name="iforgot",
        version="0.3",
        description="A command line tool to help you remember",
        long_description="A command line tool to help you search for bash scripts",
        url="www.github.com/Renmusxd/iforgot",
        author="Sumner Hearth",
        author_email="sumnernh@gmail.com",
        license="MIT",
        classifiers=[
            # How mature is this project? Common values are
            #   3 - Alpha
            #   4 - Beta
            #   5 - Production/Stable
            'Development Status :: 3 - Alpha',

            # Indicate who your project is intended for
            'Intended Audience :: Developers',
            'Topic :: Software Development :: Build Tools',

            # Pick your license as you wish (should match "license" above)
            'License :: OSI Approved :: MIT License',

            # Specify the Python versions you support here. In particular, ensure
            # that you indicate whether you support Python 2, Python 3 or both.
            'Programming Language :: Python :: 2.6',
            'Programming Language :: Python :: 2.7',
            'Programming Language :: Python :: 3',
            'Programming Language :: Python :: 3.2',
            'Programming Language :: Python :: 3.3',
            'Programming Language :: Python :: 3.4',
            'Programming Language :: Python :: 3.5',
        ],
        keywords="forgot forget bash script",
        package_data={
            'rules': ['rules.txt'],
        },
        entry_points={
            'console_scripts': [
                'iforgot=iforgot:main',
            ],
        }
)