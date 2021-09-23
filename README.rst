SIRENA
===============

🧰 About - Usage
-----------------

Python 3 library developed at SMHI.

- Read data (primarily sealevel data (eg. RH2000) from the database Wiski
- Read station information from the database SAMSA
- Use Statmodels to calculate statistics
- Visualize in bokeh plot

"Local settings" must be copied from your internal network.

🤔 How to contribute
---------------------

Please follow
`PEP8 <https://www.python.org/dev/peps/pep-0008/>`_ style guidelines and
limit lines of code to 80 characters whenever possible and when it doesn't
hurt readability. Sirena follows
`Google Style Docstrings <http://sphinxcontrib-napoleon.readthedocs.io/en/latest/example_google.html>`_
for all code API documentation.

Having said that, the current code does require some modification and restructuring.

**Fork this repository**

.. code-block:: bash

    # Fork using GitHub command line or trhough website
    $ gh repo fork JohannesSMHI/sirena

**Follow the steps below**

.. code-block:: bash

    # Clone your fork
    $ git clone your-fork-url && cd sirena

    # Create a branch with your feature
    $ git checkout -b my-feature

    # Make the commit with your changes
    $ git commit -m 'feat: My new feature'

    # Send the code to your remote branch
    $ git push origin my-feature

After your pull request is merged, you can delete your branch
