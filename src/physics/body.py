class Body:
    DYNAMIC_BODY = 0
    STATIC_BODY = 1
    KINEMATIC_BODY = 2

    def __init__(self, body_type=DYNAMIC_BODY):
        self.position = None
        self.shape = None
        self.world = None
        self.body_type = body_type

    def set_position(self, position):
        self.position = position

    def get_position(self):
        return self.position

