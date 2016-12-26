class Robot(object):
    """docstring for Robot."""

    def __init__(self, room_widget, sight_distance):
        self.sight_distance
        self.room_widget = room_widget
        self.robot_position = room_widget.robot[0]
        self.detected_room = []
        self.detect_room()

    def move_one(self):
        print("move_one")
        # poziva funkciju iz genetskog koji je idući potez najbolji i salje trenutnu mapu
        # updatea trenutnu mapu u room-u (mozda napraviti funkciju u room-u za to)

    def move_all(self):
        print("move_all")
        #poziva se move_one dok ne napravimo sve poteze

    def move_back(self):
        print("move_back")
        #TODO: robot se vrati poziciju natrag i vrati polje da je neocisceno 
        #(nesto pametno ako je prije vec bilo ocisceno????)

    def detect_room(self):
        print("detect_room")
        #TODO: napraviti funkciju u room koja vraca dio sobe koji je detektiran
        #paziti kako ce se vratiti tako da znamo spremati.
