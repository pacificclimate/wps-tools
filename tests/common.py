class TestResponse:  # For testing 'log_handler'
    def __init__(self):
        self.message = ""
        self.status_percentage = 0

    def update_status(self, message, status_percentage):
        self.message = message
        self.status_percentage = status_percentage
