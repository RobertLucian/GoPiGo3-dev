# Semantic Releasing

## Commiting Stuff

Each commit message and body can be customized by following a given set of patterns. What it's written in the commit message ends up in the release notes once a push to the `master` branch is done.

In order for a commit message/body to be taken into consideration by the semantic
system, the following patterns has to be used:

* **Message of the commit**: `@type(scope): message of the commit`. Mind that *"@,(,),: "* (*even the space after the colon*) symbols are all required in order for the commit message to taken into consideration. The only part where you can write anything is where the message fits in (i.e. `message of the commit`).
* **Body of the commit**:
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

Also, on packagecloud, you have the option of installing packages from different branches. Say for instance there's a branch called `fix/gopigo3-commanding-wheel` and we do work on it - if we want to test it we can just `pip install gopigo3-fix-gopigo3-commanding-wheel` and there we have it. As a last example we can install from the `develop` branch by running `pip install gopigo3-develop`. Of course, since the package comes from packagecloud, you have to include the `extra-index-url` option.

The versioning on branches that are not the `master` branch is done by using the date and the build number.

## When Does It Get Released

A new version is released when a push is made to `master` branch.
