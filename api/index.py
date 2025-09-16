import sys
import os
from debat_LLM.wsgi import application

def handler(event, context):
    return application(event, context)
