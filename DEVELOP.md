# Developing

This document is designed to walk you through working with the schemas
by taking a simple example that one might run into.

At the time of this commit the `checksum` field of the Data Object is
misnamed as it can be multiply valued. We'll go through 0 to pull
request of how you could offer this improvement.

## Using git

First, fork the repository using the github interface by clicking the
`Fork` button in the upper right of the repos landing page. This
creates a copy of the code you have complete control over so you can
work on your changes and publish them!

Then, navigate to the repo's page and use the URL to clone the repo
to your local machine!

```
git clone git clone https://github.com/YourGithubHandle/data-object-schemas.git
cd data-object-schemas
```

Now that you have the code, you could make a branch called "fix_checksum".

```
git checkout -b fix_checksum
```

Great, now we're all set up so that our change can be easily and quickly
reviewed!

## Installing requirements

With the code, install the necessary requirements to begin developing.
If you have virtualenv, it can make it easier to work with!

```
virtualenv env
source env/bin/activate
pip install -r python/requirements.txt -c python/constraints.txt
pip install -r python/dev-requirements.txt
```

This will create a workspace so we don't clobber your normal python
environment. Then, you'll install the libraries necessary to run
and modify the code in the requirements and dev requirements.

## Modifying the proto

We now need to find the `DataObject` message in `proto/data_objects.proto`
to make our modification. Any text editor will work!

Our offending line looks like:

```
  repeated Checksum checksum =  8;
```

There are some protobuf details we will skim over as we are mainly
using protobuf as a path to easily developed schemas. The line was
changed to.

```
  repeated Checksum checksums =  8;
```

The same change was also made to the DataBundle and Create* and
Update* requests, so that anywhere we are creating or reading a
Data Object or Bundle, one can provide all the checksums they
have.

## Generating OpenAPI Definitions

If everything went OK with installing the requirements you can
generate OpenAPI Definitions using `cwltool`. If you run this
from the root directory of the project it will process the
protobuf descriptions into a Swagger JSON named
`data_objects_service.swagger.json`.

You can modify this file further by hand and use it for your
purposes to generate servers and clients.

## Running the server

A simple test/server and client are provided for working with
these schemas from Python.

Some last minute modifications to the swagger make it so the
connexion and bravado libraries can use them.

```
sh tools/prepare_swagger.sh
```

Then in one terminal window start the app, which uses the
`connexion` library to connect OpenAPI endpoints and properly
named Python functions. All of the methods are written out
and match the `OperationId` in the swagger JSON.

```
python app.py
```

## Trying out the demo

A small demo which creates a dummy Data Object message, updates
it, then deletes it can be seen in `demo.py`. When running the
demo the first thing we notice is that the `Checksums` are not
properly being set!

We expected this, however, since we modified the schemas without
making modifications to the demo.

With a couple of modifications to the demo and app (add `s`)
we can see the demo storing checksums properly!

## Updating your repository

Now we can commit our changes back to the feature branch.

```
git add proto demo.py app.py swagger
git commit -m "Change repeated checksum message to be titled 'checksums'"
git push origin fix_checksum
```

This adds your code, commits the changes with a small message,
and updates your fork in github!

## Making a Pull Request

Now that your change works you can publish it to the community
using a Pull Request. This will attempt to merge your feature
branch with the master branch, which in our case is really
easy!

Github gives us a little box to describe our changes in to the world.
Don't be afraid of being descriptive, but in our case we wouldn't
have to say too much!

## Making review changes

If someone asks us to make changes (Add more documentation!) we
can do so by simply adding more commits and pushing them to
the same branch!

<hr />

Hope this helped you find a way to get started with the schemas!
We also use python style guidelines in our Python code (PEP8),
which you'll see by running `flake8 *.py` against any changes
you make to the code!
