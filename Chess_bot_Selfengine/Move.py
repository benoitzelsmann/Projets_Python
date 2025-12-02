class Move:


    __slots__ = ('start', 'end', 'specificity', 'gives_check', 'attacking_piece_pos')


    def __init__(self, start, end, specificity, gives_check, attacking_piece_pos):
        self.start = start
        self.end = end
        self.specificity = specificity
        self.gives_check = gives_check
        self.attacking_piece_pos = attacking_piece_pos

    def __str__(self):
        res = str(type(self).__name__).upper() + '\n'
        for key in self.__slots__:
            res += f'{key} : {getattr(self, key)}\n'
        return res


