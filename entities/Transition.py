class Transition:
    def __init__(self, id, source, target, notation, player = "0"):
        self.id = id
        self.source = source
        self.target = target
        self.notation = notation
        self.angle = 0
        self.x = 100
        self.y = 100
        self.type = None
        self.player = player

    def shared_to_file(self):
        return ("    <shared-transition name=\"{}\" urgent=\"false\"/>\n"
                .format(self.notation))

    def to_file(self):
        return (
            "    <transition angle=\"{}\" displayName=\"true\" id=\"{}\" infiniteServer=\"false\" name=\"{}\" "
            "nameOffsetX=\"-5.0\" nameOffsetY=\"35.0\" player=\"{}\" positionX=\"{}\" positionY=\"{}\" priority=\"0\" "
            "urgent=\"false\"/>\n"
            .format(self.angle, self.notation, self.notation, self.player, self.x, self.y))

    def info(self):
        print("ID: {}, Source: {}, Target: {},  Notation: {},  X Coord: {}, Y Coord: {}"
              .format(self.id, self.source, self.target, self.notation, self.x, self.y))


