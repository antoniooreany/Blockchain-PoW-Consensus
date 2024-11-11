# #   Copyright (c) 2024, Anton Gorshkov
# #   All rights reserved.
# #   This code is for a pow and its unit tests.
# #   For any questions or concerns, please contact Anton Gorshkov at antoniooreany@gmail.com
#
# import logging
#
# class LoggerSingleton:
#     _instance = None
#
#     @staticmethod
#     def get_instance():
#         if LoggerSingleton._instance is None:
#             LoggerSingleton()
#         return LoggerSingleton._instance
#
#     def __init__(self):
#         if LoggerSingleton._instance is not None:
#             raise Exception("This class is a singleton!")
#         else:
#             self.logger = logging.getLogger(__name__)
#             LoggerSingleton._instance = self