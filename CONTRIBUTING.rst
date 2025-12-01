.. highlight:: shell

============
Contributing
============

Contributions are welcome, and they are greatly appreciated! Every
little bit helps, and credit will always be given.

You can contribute in many ways:

Types of Contributions
----------------------

Report Bugs
~~~~~~~~~~~

Report bugs at https://github.com/multiformats/py-multibase/issues.

If you are reporting a bug, please include:

* Your operating system name and version.
* Any details about your local setup that might be helpful in troubleshooting.
* Detailed steps to reproduce the bug.

Fix Bugs
~~~~~~~~

Look through the GitHub issues for bugs. Anything tagged with "bug"
and "help wanted" is open to whoever wants to implement it.

Implement Features
~~~~~~~~~~~~~~~~~~

Look through the GitHub issues for features. Anything tagged with "enhancement"
and "help wanted" is open to whoever wants to implement it.

Write Documentation
~~~~~~~~~~~~~~~~~~~

py-multibase could always use more documentation, whether as part of the
official py-multibase docs, in docstrings, or even on the web in blog posts,
articles, and such.

Submit Feedback
~~~~~~~~~~~~~~~

The best way to send feedback is to file an issue at https://github.com/multiformats/py-multibase/issues.

If you are proposing a feature:

* Explain in detail how it would work.
* Keep the scope as narrow as possible, to make it easier to implement.
* Remember that this is a volunteer-driven project, and that contributions
  are welcome :)

Get Started!
------------

Ready to contribute? Here's how to set up `multibase` for local development.

1. Fork the `py-multibase` repo on GitHub.
2. Clone your fork locally::

    $ git clone git@github.com:your_name_here/py-multibase.git

3. Install your local copy into a virtualenv. Create and activate a virtual environment::

    $ python -m venv venv
    $ source venv/bin/activate  # On Windows: venv\Scripts\activate
    $ pip install -e ".[dev]"

4. Install pre-commit hooks (optional but recommended)::

    $ pre-commit install

   This will set up git hooks to automatically run linting and formatting checks
   before each commit.

5. Create a branch for local development::

    $ git checkout -b name-of-your-bugfix-or-feature

   Now you can make your changes locally.

6. When you're done making changes, check that your changes pass linting and the
   tests, including testing other Python versions with tox::

    $ make lint
    $ make test
    $ tox

   Or run pre-commit manually on all files::

    $ pre-commit run --all-files

   If you installed pre-commit hooks (step 4), they will run automatically on commit.

Development Workflow Commands
-------------------------------

The project provides several ``make`` targets to help with development:

* ``make fix`` - Automatically fix formatting and linting issues using ruff.
  Use this when you want to auto-fix code style issues.

* ``make lint`` - Run all pre-commit hooks on all files to check for code quality
  issues. This includes YAML/TOML validation, trailing whitespace checks, pyupgrade,
  ruff linting and formatting, and mypy type checking.

* ``make typecheck`` - Run mypy type checking only. Use this when you want to
  quickly check for type errors without running all other checks.

* ``make test`` - Run the test suite with pytest using the default Python version.
  For testing across multiple Python versions, use ``tox`` instead.

* ``make pr`` - Run a complete pre-PR check: clean build artifacts, fix formatting,
  run linting, type checking, and tests. This is the recommended command to run
  before submitting a pull request.

* ``make coverage`` - Run tests with coverage reporting and open the HTML report
  in your browser.

For a full list of available commands, run ``make help``.

7. Commit your changes and push your branch to GitHub::

    $ git add .
    $ git commit -m "Your detailed description of your changes."
    $ git push -u origin name-of-your-bugfix-or-feature

8. Submit a pull request through the GitHub website.

Pull Request Guidelines
-----------------------

Before you submit a pull request, check that it meets these guidelines:

1. The pull request should include tests.
2. If the pull request adds functionality, the docs should be updated. Put
   your new functionality into a function with a docstring, and add the
   feature to the list in README.rst.
3. The pull request should work for Python 3.10, 3.11, 3.12, 3.13, and 3.14. Check
   https://github.com/multiformats/py-multibase/actions
   and make sure that the tests pass for all supported Python versions.

Tips
----

To run a subset of tests::

$ pytest tests/test_multibase.py


Deploying
---------

A reminder for the maintainers on how to deploy.
Make sure all your changes are committed (including an entry in HISTORY.rst).
Then run::

$ bump-my-version bump patch # possible: major / minor / patch
$ git push
$ git push --tags

GitHub Actions will then deploy to PyPI if tests pass.
