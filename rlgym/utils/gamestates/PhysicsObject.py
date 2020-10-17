

class PhysicsObject(object):
    def __init__(self, position=None, quaternion=None, linear_velocity=None, angular_velocity=None):
        self.position = position
        self.quaternion = quaternion
        self.linear_velocity = linear_velocity
        self.angular_velocity = angular_velocity

    def decode_car_data(self, car_data):
        self.position = car_data[:3]
        self.quaternion = car_data[3:7]
        self.linear_velocity = car_data[7:10]
        self.angular_velocity = car_data[10:]

    def decode_ball_data(self, ball_data):
        self.position = ball_data[:3]
        self.linear_velocity = ball_data[3:6]
        self.angular_velocity = ball_data[6:9]
        
    def serialize(self):
        repr = []

        if self.position is not None:
            for arg in self.position:
                repr.append(arg)
                
        if self.quaternion is not None:
            for arg in self.quaternion:
                repr.append(arg)
                
        if self.linear_velocity is not None:
            for arg in self.linear_velocity:
                repr.append(arg)
                
        if self.angular_velocity is not None:
            for arg in self.angular_velocity:
                repr.append(arg)

        return repr
        