




Robot GPT
=========
.. raw:: html

   <p>
   <img src="https://github.com/Huell-Howitzer/robotgpt/actions/workflows/docker-image.yml/badge.svg?branch=main" alt="Docker Image CI" align="left">
   <img src="https://github.com/Huell-Howitzer/robotgpt/actions/workflows/Qodana.yml/badge.svg?branch=main" align="right">
   <br>
   </p>

Some text on the line below the images.


The purpose of this app is changing by the hour...

Currently, this project is a flask app that interacts with ChatGPT in a loop, providing feedback until a goal is met.

Installation
------------

1. Clone the repository:

Using ssh
   .. code-block:: bash

      git clone git@github.com:Huell-Howitzer/robotgpt.git

or:

using https
  .. code-block:: bash

      git clone https://github.com/Huell-Howitzer/robotgpt.git

2. Build the Docker image:

   .. code-block:: bash

      docker build -t robotgpt .

3. Run the Docker container:

   .. code-block:: bash

      docker run -p 5000:5000 robotgpt

Usage
-----

Access the application at `http://127.0.0.1:5000.


Contributing
------------

1. Fork the repository.

2. Create a new branch:

   .. code-block:: bash

      git checkout -b feature/new-feature

3. Make your changes and commit them:

   .. code-block:: bash

      git commit -m "Add new feature"

4. Push the changes to your forked repository:

   .. code-block:: bash

      git push origin feature/new-feature

5. Open a pull request in the original repository.

License
-------

This project is licensed under the MIT License. See the `LICENSE` file for details.

Contact
-------

If you have any questions or suggestions, feel free to contact me at rmhowell@protonmail.com.
