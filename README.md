# Package all the things!

These tools are supposed to parse a YAML file with some
metadata about GNU Radio OOT and then automatically create a
`debian/` directory to create packages from the sources and then
feed this to a CI for creation of a binary package feed.

This project is still very much work in progress, but at least some
templates are starting to be OK.

Resulting packages will not be fully compliant with Debian policy, but these packages
are intended to be just easy-to-install low-hanging fruit to be provided to users to
shift to more binary packages away from almost only source-packages.
