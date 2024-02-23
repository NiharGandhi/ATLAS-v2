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
        self.analyze_traffic()
        current_signal = self.signal_order[self.current_signal_index]
        print(f"Green signal for {current_signal} side")
        # Logic to control signals...
        # After signal duration, move to the next signal in order
        self.current_signal_index = (
            self.current_signal_index + 1) % len(self.signal_order)
