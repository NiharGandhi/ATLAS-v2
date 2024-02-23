class TrafficHub:
    def __init__(self):
        self.side_data = {'north': [], 'south': [], 'east': [], 'west': []}
        self.signal_order = ['north', 'south', 'east', 'west']
        self.current_signal_index = 0
        self.signal_duration = 10  # in seconds

    def receive_data(self, side, vehicle_data):
        self.side_data[side] = vehicle_data

    def analyze_traffic(self):
        total_vehicles = sum(len(vehicles)
                             for vehicles in self.side_data.values())
        if total_vehicles > 20:
            # Adjust signal order based on traffic conditions
            self.signal_order = ['south', 'north', 'west', 'east']

    def control_signals(self):
        for side, data in self.side_data.items():
            # Calculate traffic density based on the number of vehicles and their clearance time
            traffic_density = len(data) * 2  # Assuming each vehicle takes 2 seconds to clear the signal

            # Adjust signal timing based on traffic density
            if traffic_density > 30:
                signal_duration = 30  # Maximum signal duration is 30 seconds
            else:
                signal_duration = traffic_density

            # Update signal status for the side
            self.signal_timings[side] = signal_duration

