import os

basedir = os.path.abspath(os.path.dirname(__file__))


class config(object):
    """Base configuration"""


class ProductionConfig(config):
    """Production configuration"""


class DevelopmentConfig(config):
    """Development configuration"""


class TestingConfig(config):
    """Testing configuration"""
