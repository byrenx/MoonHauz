import sys
import os
import logging

# Setup the import path
package_dir = "packages"
package_dir_path = os.path.abspath(
    os.path.join(os.path.dirname(__file__), '..', package_dir))

# Allow unzipped packages to be imported
# from packages folder
if not package_dir_path in sys.path:
    sys.path.insert(0, package_dir_path)

# Append zip archives to path for zipimport
for filename in os.listdir(package_dir_path):
    if filename.endswith((".zip", ".egg")):
        path = "%s/%s" % (package_dir_path, filename)
        if not path in sys.path:
            logging.debug('Adding zip package %s to path' % path)
            sys.path.insert(0, path)
