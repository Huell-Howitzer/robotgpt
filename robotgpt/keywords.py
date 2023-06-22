from robot.api.deco import keyword
from robotgpt import generator as gen

class RobotGPTKeywords:
    @keyword("Create And Test Transform")
    def create_and_test_transform(self, sample_text_filename, expected_output_filename, attempts_allowed=5,
                                  max_invalid_code_attempts=3):
        result = gen.create_and_test_transform(sample_text_filename, expected_output_filename,
                                               attempts_allowed, max_invalid_code_attempts)
        return result

    @keyword("chatWithAgent")
    def chat_with_agent(self, agent, message):
        result = gen.chat_with_agent(agent, message)
        return result

    @keyword("readFile")
    def read_file(self, filename):
        result = gen.read_file(filename)
        return result

    @keyword("writeToFile")
    def write_to_file(self, filename, content):
        gen.write_to_file(filename, content)

    @keyword("runUntrustedCode")
    def run_untrusted_code(self, code, local_vars):
        gen.run_untrusted_code(code, local_vars)

    @keyword("createDirectories")
    def create_directories(self):
        gen.create_directories()

    @keyword("calculateSimilarity")
    def similarity(self, a, b):
        result = gen.similarity(a, b)
        return result

