# CAS API Example

This is an example of how to use the **CAS API** to build a web app that does
image recognition. **CAS** or **Cloud Analytic Services** is the central
engine of the [SAS Viya](http://www.sas.com/en_us/software/viya.html)
framework.

## Requirements

This example must run on the CAS controller node because of the way
we load images into CAS.

This example was built using [Flask](http://flask.pocoo.org/), a Python
web app framework. It also depends on the [SAS SWAT](https://github.com/sassoftware/python-swat)
package which is a Python interface to CAS. This app was built using
Python 3.6.5.

You can use any Python package and environment managers to make sure that
you have Python 3, Flask, and CAS installed. See the [SWAT](https://sassoftware.github.io/python-swat/install.html)
page to see instructions on installing CAS. An example would be to
use `pip` and `virtualenv` to create an isolated Python 3 environment,
and install Flask and CAS with `pip`.

# Getting Started

There are a couple of configuration statements in the `routes.py` file.

The app is configured to listen on `APP_IP` and `APP_PORT`.

`AUTHINFO` is the path to the `authinfo` file that is used to authenticate
the CAS package with CAS. See the [SWAT docs](https://sassoftware.github.io/python-swat/getting-started.html#authentication)
for details on authenticating with CAS using the `authinfo` file.

The `UPLOAD_FOLDER` is where we save images when we upload them to the app.
It is also where we tell CAS to load the images from. In **SAS Viya
3.3**, you must load images into CAS from an an absolute path. So 
the `UPLOAD_FOLDER` but be an absolute path. Also, the path needs to be
accessible by the user running the app as well as the user used to authenticate
with CAS in the `authinfo` file.

The app uses an `astore` that has already been created and is
already in memory. The configuration variable `ASTORE` represents the name
of the `astore` to score the images with, and `ASTORE_LIB` points to the
`caslib` the `astore` is living in.

`astore`s or analytic stores are the way SAS Viya represents the state
of analytical models such as the CNN that would be used to score an image.
See the [SAS Deep Learning Programming Guide](http://support.sas.com/documentation/prod-p/vdmml/index_deep_learn_guide.html)
to see how to build a CNN image recognition model and `astore`.

With those configuration variables set, the app is ready to run. Run it
with `python routes.py`. Visit the app at the by going to the right hostname/IP/port
that was set in the configuration variables. For example, if the app is
listening on all IPs (`APP_IP='0.0.0.0'`) and port 7050 (`APP_PORT=7050`)
then the app will be running at http://*hostname-where-app-is-running*:7050/

Drag and drop an image to score it. **Note:** the CAS image processing
pipeline in the app simply loads the image to CAS and scores it. It
does not resize the image to match the CNN `astore` model, so either upload
images that match the expected size of the CNN `astore` model, or add some
image processing to resize the image before scoring it. See the **SAS Viya**
image processing [documentation](http://go.documentation.sas.com/?cdcId=pgmsascdc&cdcVersion=9.4_3.3&docsetId=casactml&docsetTarget=casactml_image_table.htm&locale=en)
for more details.