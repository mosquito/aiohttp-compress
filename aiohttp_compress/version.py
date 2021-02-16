author_info = (("Dmitry Orlov", "me@mosquito.su"),)

package_info = (
    "This module is the simplest way to enable compression support "
    "for aiohttp server applications globally."
)
package_license = "Apache Software License"

team_email = "me@mosquito.su"

version_info = (0, 2, 0)

__author__ = ", ".join("{} <{}>".format(*info) for info in author_info)
__version__ = ".".join(map(str, version_info))
