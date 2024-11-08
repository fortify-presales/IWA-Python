[![Fortify on Demand](https://github.com/fortify-presales/IWA-Python/actions/workflows/fod.yml/badge.svg)](https://github.com/fortify-presales/IWA-Python/actions/workflows/fod.yml) [![Debricked](https://github.com/fortify-presales/IWA-Python/actions/workflows/debricked.yml/badge.svg)](https://github.com/fortify-presales/IWA-Python/actions/workflows/debricked.yml)

# Fortify Demo App

This is a simple Python Flask web application that can be used for the demonstration of application
security testing tools - such as those provided by [Fortify by OpenText](https://www.microfocus.com/en-us/cyberres/application-security). 
It is a cut down "search" results/details page from a larger sample application [IWA-Java](https://github.com/fortify/IWA-Java) and is kept deliberately small for demos.

Pre-requisities
---------------

 - Windows or Linux machine with Python 3.12 or later
 - [Pip package manager](https://pypi.org/project/pip/)
 - Local Fortify Static Code Analyzer installation 
 - Local Docker installation
 - [Debricked CLI](https://docs.debricked.com/tools-and-integrations/cli/debricked-cli)
 - [Fortify CLI](https://github.com/fortify/fcli)

Run Application (locally)
-------------------------

You can the run the application locally using the following:

Windows:

```
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
.\run.bat
```

Linux/UNIX:

```
python3 -m venv .venv           
. .venv/bin/activate
pip install -r requirements.txt
./run.sh
```

The application should then be available at the URL `http://localhost:5000`. If it fails to start,
make sure you have no other applications running on port 5000. 

Run Application (as Docker container)
-------------------------------------

You also can build a Docker image for the application using the following:

```
docker build -t demoapp:latest .
```

Then run the container using a command similar to the following:

```
docker run -dp 8080:8000 demoapp:latest
```

The application will then be available at the URL `http://localhost:8080`. If it fails to start,
make sure you have no other applications running on port 8080.

Using the Application
---------------------

There are only a few features that are functional in this version of the app:

- you can navigate to the "Shop"
- you can type in some keywords in the Shop search box, e.g. "alphadex" to filter results
- you can click on any search result to navigate to a details page
- you can download a datasheet PDF from a details page
- you can subscribe to the newsletter by entering an email address in the input field of the footer
- you can login/logout (user credentials are: user1@localhost.com/password or admin@localhost.com/password)

These have been "enabled" because they all have potential security issues that can be found by Fortify.

Scan Application (with Fortify)
-------------------------------

To carry out a Fortify Static Code Analyzer local scan, run the following:

```
sourceanalyzer -b iwapy -clean
sourceanalyzer -b iwapy -python-path ".venv/Lib/site-packages/" -exclude ".venv" "app"
sourceanalyzer -b iwapy -scan
```

To carry out a Fortify ScanCentral SAST scan, run the following:

```
fcli ssc session login
scancentral package -o package.zip -bt none --python-virtual-env .venv -oss
fcli ssc sast-scan start --release "_YOURAPP_:_YOURREL_" -f package.zip --store curScan
fcli ssc sast-scan wait-for ::curScan::
fcli ssc action run appversion-summary --av "_YOURAPP_:_YOURREL_" -fs "Security Auditor View" -f summary.md
```

To carry out a Fortify on Demand scan, run the following:

```
fcli fod session login
scancentral package -o package.zip -bt none --python-virtual-env .venv -oss
fcli fod sast-scan start --release "_YOURAPP_:_YOURREL_" -f package.zip --store curScan
fcli fod sast-scan wait-for ::curScan::
fcli fod action run release-summary --rel "_YOURAPP_:_YOURREL_" -f summary.md
```

---

Kevin A. Lee (kadraman) - klee2@opentext.com
