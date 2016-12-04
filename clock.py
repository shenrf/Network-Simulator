class Clock:
    """ 
        Current time
        
    """
    def __init__(self):
        self.current_time = 0.00
    
    def update_time(self, time):
        self.current_time = time
    
    def get_time(self):
        return self.current_time

clk=Clock()


