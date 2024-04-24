Writing Documentation for ItsPrompt
===================================

This document describes how to write documentation for ItsPrompt.

Basics of ItsPrompt Documentation
---------------------------------

`ItsPrompt` uses `Sphinx` for documentation. The documentation is written in `reStructuredText` format. The source
can be found in the `docs/source` directory.

Creating Media Files using vhs
------------------------------

`ItsPrompt` uses `vhs <https://github.com/charmbracelet/vhs>`_ to record terminal sessions and create gif and image files
for the documentation. Before running any command, refer to the `vhs` documentation to understand how to install and use it.

If you simply want to update all the included media, you can run the following command:

.. code-block:: bash

    make vhs

The generated media files will be placed in the `docs/source/media` directory.

Adding Media Files to the Documentation
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

To add a new media file to the documentation, you need to create a new `.tape` file in the `docs/scripts/vhs` directory.

You can use the content from `tape.template` for a quick guide on how to create a new `.tape` file.
