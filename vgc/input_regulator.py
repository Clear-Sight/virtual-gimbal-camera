class InputRegulator:
    def __init__(self, pipeline):
        self.usr_msg = pipeline.recv_usr_msg()
        
