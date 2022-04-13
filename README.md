# Cryptum
Hello! This is **_Cryptum_**, my free and open-source project for a no-web-connection password manager. The reason why i chose to have a full offline password database manager is the need for a totally hidden database from any machine-external entity. Passwords and user data will never be stored in any third-party server
or cloud. All you need to safely store is just in your machine as locally crypted files, and accessible only by the program itself.

## Install and use

As this app is Python-based you need a properly installed Python interpreter (Python 3.7+).
[Here]("https://www.python.org/") how to install Python on your machine.
In order to have this app to work correctly, you need to install the following additional libraries:

`PySide6`
`cryptography`

**PySide6** is a Python framework required for generating UI.
It can be installed via _pip_ command from terminal console.

<pre><code>$ pip install PySide6
</code></pre>

For more details about use and installation read the [PySide6 Docs](https://pypi.org/project/PySide6/)

## Cryptography package
This program uses the cryptography libraries developed by **Python Cryptographic Authority**.
It is an efficient and simple-to-implement package to crypt strings.
It can be installed via _pip_ command from terminal.

<pre><code>$ pip install cryptography
</code></pre>

More info at https://github.com/pyca/cryptography

## Standalone Windows app
You can use a compiled version of **_Cryptum_** without any need for a python interpreter or external libraries. App features and UI are the same as the console version, but this is completely
indipendent app package provided with a comfortable **_.exe_ file format**. All necessary libraries are included
with no need of other external installation files.

Download the current version of standalone executable [Cryptum 0.1.0-alpha](https://drive.google.com/file/d/1brj76VXdvVvGpV5mGVc4xbFefzS6ZRhZ/view?usp=sharing)


## Changelog
### 0.1.0-alpha
Initial release, some basic functinality not working yet.
