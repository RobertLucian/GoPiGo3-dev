# AltGPG3 - Alternative GoPiGo3 Library to the Official One [![Build Status](https://travis-ci.com/RobertLucian/AltGPG3.svg?token=zRic2qBaGDm1LBnLp8aP&branch=develop)](https://travis-ci.com/RobertLucian/AltGPG3)

<img src="https://i.imgur.com/EH8amg1.jpg" width="600">

This library represents an alternative to the [official one](https://github.com/DexterInd/GoPiGo3) of the [GoPiGo3 robot](https://www.dexterindustries.com/gopigo3/) that has quite a few advantages over the latter:

1. **Versioned Software**: On this one, CI/CD systems are used, which means you have at your hand a safe mechanism for version controlling your software and for updating it to a very specific version.
1. **Preview Packages**: Access to develop versions of the package. You can install packages from different branches of this repo. Check **Semantic Releasing** -> **Where Does This Get Pushed To** section.
1. **CLI Tool**: On this version you also have a CLI tool with which you can interface with your GoPiGo3 robot directly from your terminal line. How cool!
1. **Architecture**: A much better organized package directory-wise and semantic-wise.

Also, this library is a drop-in replacement for the official library, where the only downside with it is that it doesn't include all functionalities in it. Functionalities have been stripped down because the original architecture of the classes and whatnot on the official are generally bad. Slowly, I'll be adding features back in while trying to keep it as compatible as possible.

# CLI Tool

There's also a CLI tool that allows you to interface with the GoPiGo3 directly from the terminal line.

<img src="https://i.imgur.com/QKnDfib.gif">

# Installing It

The package can be either installed by:

1. By using PIP to install it from [packagecloud.io/twine/develop](https://packagecloud.io/twine/develop)

1. Or by going to the [releases page](https://github.com/RobertLucian/AltGPG3/releases) and download the latest `tar.gz` archive and then install it.

To install it with PIP, you can run the following command:
```
pip install altgpg3 --extra-index-url=https://packagecloud.io/twine/develop/pypi/simple
```
Or by adding this `--extra-index-url` to a pip configuration file (or to the bottom of a requirements file). There's a script that does that for you:
```
curl -s https://packagecloud.io/install/repositories/twine/develop/script.python.sh | bash
```


# Semantic Releasing

## Commiting Stuff

Each commit message and body can be customized by following a given set of patterns. What it's written in the commit message ends up in the release notes once a push to the `master` branch is done.

In order for a commit message/body to be taken into consideration by the semantic
system, the following patterns has to be used:

#### Message of the Commit

`@type(scope): message of the commit`.
Mind that *"@,(,),: "* (*even the space after the colon*) symbols are all required in order for the commit message to taken into consideration. The only part where you can write anything is where the message fits in (i.e. `message of the commit`).

#### Body of the Commit
```
Body of the commit that ends up in the release note.
Fixes #24, #23, #91
BREAKING CHANGE: Added something that changed the API completely.
```

The body of the commit, which is the **1st line** in the above paragraph *can be included or not*.

The **2nd part** of the body, which is the footer has to start with one of the following keywords: `close|fixes|closes`. These keywords are case-insensitive, so you can shift-type them or not, but you can't use them in the first part of the body, which is the commit message that ends up in the release. This footer is *used for automatically closing mentioned issues when a PR is merged*.

And the **3rd part** is again optional and it's required to be added *if to the code-base has been added a breaking change* - the required keyword for this is `BREAKING CHANGE: ` and it's case sensitive, so you have to type in caps.

## Considerations on Commit Messages

The `type` of the commit message can be any of the following:

* `feature` - for new features added.
* `fix`
* `docs` - whenever a change is brought to the docs.
* `refactor` - when code gets refactored.
* `test` - unit tests, functional tests, tests listed in the docs, whatever.
* `chore` - mindless stuff.

The `scope` of the commit message can literally be anything. It depends on what you're working on. Some that are being used frequently can be:
* `automation`
* `server`
* `cmdline`
* etc.

Also, the body message of the commit which can be composed of 3 sections (body message + footer + breaking change) can accept newlines between each section. Also, you can pair the following:
* Body Message + Footer + Breaking Change
* Body Message + Footer
* Body Message
* No body at all

## Where Does This Get Pushed To

Semantic release pushes the following:
1. Release log on the repository on GitHub.
2. Python installer as archive on the release page on GitHub.
3. Python installer as archive on packagecloud.

Also, on packagecloud, you have the option of installing packages from different branches. Say for instance there's a branch called `fix/gopigo3-commanding-wheel` and we do work on it - if we want to test it we can just `pip install altgpg3-fix-gopigo3-commanding-wheel` and there we have it. As a last example we can install from the `develop` branch by running `pip install altgpg3-develop`. Of course, since the package comes from packagecloud, you have to include the `extra-index-url` option.

The versioning on branches that are not the `master` branch is done by using the date and the build number.

## When Does It Get Released

A new version is released when a push is made to `master` branch.
