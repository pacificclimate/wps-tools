class NCInput:  # For testing 'get_filepaths'
    def __init__(self, url="", file=""):
        self.url = url
        self.file = file


class Response:  # For testing 'log_handler'
    def __init__(self):
        self.message = ""
        self.status_percentage = 0

    def update_status(self, message, status_percentage):
        self.message = message
        self.status_percentage = status_percentage
