from genetic import Genetic

class Robot(object):
    """docstring for Robot."""

    def __init__(self, room_widget, sight_distance = 6):
        self.sight_distance = sight_distance
        self.room_widget = room_widget
        self.full_room = [[None]*len(i) for i in self.room_widget.room]
        #self.detected_room = [[] for i in self.room_widget.room]
        #self.detected_room = []
        #self.detect_room()

    def move_one(self):
        print("move_one")
        self.detect_room()
        gen = Genetic(self.detected_room, self.robot_position, 4, 5, 0.2, 0.8, 10)
        print("Slijedeci potez")
        next_move = gen.next_move()[0][1]
        print(next_move)
        self.room_widget.do_move(next_move)

        # poziva funkciju iz genetskog koji je idući potez najbolji i salje trenutnu mapu
        # updatea trenutnu mapu u room-u (mozda napraviti funkciju u room-u za to)

    def move_all(self):
        print("move_all")
        #poziva se move_one dok ne napravimo sve poteze

    def move_back(self):
        print("move_back")
        #TODO: robot se vrati poziciju natrag i vrati polje da je neocisceno
        #(nesto pametno ako je prije vec bilo ocisceno????)

    def extract_detected_only(self):
        self.detected_room = []
        for i, row in zip(range(len(self.full_room)), self.full_room):
            if(next((True for item in row if item is not None), False)):
                self.detected_room.append([symbol for symbol in row if symbol is not None])

        print(self.detected_room)

    def detect_room(self):
        print("detect_room")
        self.robot_position = self.room_widget.robot[-1]
        sensors_input = self.room_widget.detect_room(self.sight_distance)
        for start in sensors_input:
            for j, symbol in zip(range(start[1], len(sensors_input[start])+1), sensors_input[start]):
                if(symbol == 'R'):
                    symbol = 'o'
                self.full_room[start[0]][j] = symbol

        self.extract_detected_only()

        #TODO: pukusaj pametnijeg, nije bas proslo treba malo bolje razmisliti
        """for start in sensors_input:
            while(len(self.detected_room) <= start[0]):
                self.detected_room.append([])
            for j, symbol in zip(range(start[1], len(sensors_input[start])+1), sensors_input[start]):
                print(start)
                if(symbol == 'R'):
                    symbol = 'o'
                if(len(self.detected_room[start[0]]) <= j):
                    self.detected_room[start[0]].append(symbol)

                elif(self.detected_room[start[0]][j] != symbol):
                    print("Doslo je do greske, spremljeno je" + self.detected_room[start[0]][j]
                            + "u memoriji robota, a procitano je " + symbol + " iz mape")"""

        #print(self.detected_room)
        #print(len(self.detected_room))
