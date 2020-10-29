class Node:
    def __init__(self, id, notation, marking):
        self.id = id
        self.notation = notation
        self.marking = marking
        self.transition_count = None
        self.x = 100
        self.y = 100
        self.type = None

    def to_file(self):
        return (
            "    <place displayName=\"true\" id=\"{}\" initialMarking=\"{}\" invariant=\"&lt; inf\" name=\"{}\" nameOffsetX=\"-5.0\" nameOffsetY=\"35.0\" positionX=\"{}\" positionY=\"{}\"/>\n"
            .format(self.notation, self.marking, self.notation, self.x, self.y))

    def shared_to_file(self):
        return ("    <shared-place initialMarking=\"0\" invariant=\"&lt; inf\" name=\"{}\"/>"
                .format(self.notation))

    def info(self):
        print("ID: {}, Notation: {}, Transition count: {}, X Coord: {}, Y Coord: {}"
              .format(self.id, self.notation, self.transition_count, self.x, self.y))