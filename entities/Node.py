class Node:
    def __init__(self, id, notation, marking="0"):
        self.id = id
        self.notation = notation
        self.marking = marking
        self.transition_count = 0
        self.init_route = None
        self.final_route = None
        self.x = 100
        self.y = 200
        self.type = None

    def to_file(self):
        return (
            "    <place displayName=\"true\" id=\"{}\" initialMarking=\"{}\" invariant=\"&lt; inf\" name=\"{}\" nameOffsetX=\"-5.0\" nameOffsetY=\"35.0\" positionX=\"{}\" positionY=\"{}\"/>\n"
            .format(self.notation, self.marking, self.notation, self.x, self.y))

    def shared_to_file(self):
        return ("    <shared-place initialMarking=\"{}\" invariant=\"&lt; inf\" name=\"{}\"/>\n"
                .format(self.marking, self.notation))

    def info(self):
        print("ID: {}, Notation: {}, Transition count: {}, X Coord: {}, Y Coord: {}"
              .format(self.id, self.notation, self.transition_count, self.x, self.y))