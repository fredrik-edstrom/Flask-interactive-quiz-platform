"""
Imports are sorted in order by three categories (alphabetically if possible)
with an empty line between them:
1) Imports from standard library
2) Imports from third party libraries
3) Imports from custom defined modules

See example below.
"""

from datetime import datetime, timedelta
from os import urandom

from flask import Flask, redirect, render_template

from .models.company import Company
from .shared.custom_class import SomeCustomDefinedClass
