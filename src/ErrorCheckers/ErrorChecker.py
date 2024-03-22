
class ErrorChecker:

    def __int__(self):
        pass

    def get_header(self):
        pass

    def get_error_detecting_code(self, msg_arr):
        pass

    def validate_error_detecting_code(self, msg_arr, old_code):
        return old_code.value == self.get_error_detecting_code(msg_arr).value
