from typing import TypeAlias
CellTriple: TypeAlias = tuple["Cell", "Cell", "Cell"]

class Player:
    __name: str
    __label: str

    def __init__(self, name: str, label: str):
        self.__name = name
        self.__label = label

    def __str__(self) -> str:
        return self.__label

    @property
    def name(self) -> str:
        return  self.__name


class Cell:
    __x: int
    __y: int
    __filled_by: Player | None = None

    def __init__(self, x: int = 0, y: int = 0):
        self.__x = x
        self.__y = y

    def __str__(self) -> str:
        return f"(x = {self.x}, y = {self.y})"

    def input(
        self,
        msg: str | None = "Enter X and Y via space: ",
        field_size: int = 3
    ) -> bool:
        input_data = input(msg) if msg is not None else input()
        input_data = input_data.split(" ")

        cleared_data: list[int] = []
        for input_item in input_data:
            if len(cleared_data) == 2:
                return False
            is_added: bool = False
            if input_item.isdigit():
                input_item = int(input_item)
                if 0 <= input_item < field_size:
                    cleared_data.append(input_item)
                    is_added = True
            if not is_added:
                return False

        if len(cleared_data) == 2:
            Cell(cleared_data[0], cleared_data[1])
            self.__x = cleared_data[0]
            self.__y = cleared_data[1]
            return True
        else:
            return False

    def input_looped(
        self,
        msg: str | None = "Enter X and Y via space: ",
        err_msg: str | None = "Error! Try again!",
        field_size: int = 3
    ) -> None:
        while True:
            is_cell_correct: bool = self.input(msg, field_size)
            if is_cell_correct:
                break
            elif err_msg is not None:
                print(err_msg)

    @property
    def x(self) -> int:
        return self.__x

    @property
    def y(self) -> int:
        return self.__y

    @property
    def filled_by(self) -> Player | None:
        return self.__filled_by
    @filled_by.setter
    def filled_by(self, player: Player | None) -> None:
        self.__filled_by = player


class Game:
    __field: tuple[CellTriple, CellTriple, CellTriple]
    __win_combinations: tuple[
        CellTriple, CellTriple, CellTriple,
        CellTriple, CellTriple, CellTriple,
        CellTriple, CellTriple
    ]
    __players: tuple[Player, Player]
    __active_player_id: int | None = None
    __filled_cells_count: int = 0

    __is_started: bool = False
    __is_win: bool = False
    __is_draw: bool = False

    def __init__(self):
        self.__init_field()
        self.__init_win_combinations()
        self.__init_players()

    def __str__(self) -> str:
        field_size: int = len(self.__field)
        sep_line: str = ''.join(['+-' for _ in range(field_size)]) + '+'
        result: list[str] = [sep_line]
        for i in range(field_size):
            # строка меток
            line = ['|']
            for cell in self.__field[i]:
                line.append(str(cell.filled_by) if cell.filled_by is not None else " ")
                line.append('|')
            result.append(''.join(line))
            # строка-разделитель
            result.append(sep_line)
        result.append(self.status)
        return '\n'.join(result)

    def __init_field(self) -> None:
        if not hasattr(self, '_Game__field'):
            self.__field = (
                (Cell(0,0), Cell(0,1), Cell(0,2)),
                (Cell(1,0), Cell(1,1), Cell(1,2)),
                (Cell(2,0), Cell(2,1), Cell(2,2))
            )

    def __init_win_combinations(self) -> None:
        if not hasattr(self, '_Game__win_combinations'):
            self.__win_combinations = (
                # столбцы
                (self.__field[0][0], self.__field[0][1], self.__field[0][2]),
                (self.__field[1][0], self.__field[1][1], self.__field[1][2]),
                (self.__field[2][0], self.__field[2][1], self.__field[2][2]),
                # строки
                (self.__field[0][0], self.__field[1][0], self.__field[2][0]),
                (self.__field[0][1], self.__field[1][1], self.__field[2][1]),
                (self.__field[0][2], self.__field[1][2], self.__field[2][2]),
                # диагонали
                (self.__field[0][0], self.__field[1][1], self.__field[2][2]),
                (self.__field[2][2], self.__field[1][1], self.__field[0][0]),
            )

    def __init_players(self) -> None:
        if not hasattr(self, '_Game__players'):
            self.__players = (
                Player("Cross", "x"),
                Player("Zero", "o")
            )

    def __switch_active_player(self) -> None:
        self.__active_player_id = (self.__active_player_id + 1) % len(self.__players)

    def __input_turn(self) -> Cell:
        entered_cell: Cell = Cell()
        chosen_cell: Cell
        while True:
            entered_cell.input_looped(field_size=len(self.__field))
            chosen_cell = self.__field[entered_cell.y][entered_cell.x]
            if chosen_cell.filled_by is None:
                return chosen_cell
            else:
                print(f"Cell {chosen_cell} is already filled! Try again!")

    def __update_statuses(self) -> None:
        self.__is_win = False
        self.__is_draw = False
        if self.__is_started:
            for combination in self.__win_combinations:
                if all(cell.filled_by == self.active_player for cell in combination):
                    self.__is_win = True
                    return
            if self.__filled_cells_count == len(self.__field) ** 2:
                self.__is_draw = True

    def __game_loop(self) -> None:
        while True:
            print(self)
            chosen_cell: Cell = self.__input_turn()
            chosen_cell.filled_by = self.active_player
            self.__filled_cells_count += 1
            self.__update_statuses()
            print()
            if self.__is_win or self.__is_draw:
                print(self, end='\n\n')
                break
            self.__switch_active_player()

    def start(self) -> None:
        self.__active_player_id = 0
        self.__is_started = True
        self.__game_loop()

    @property
    def active_player(self) -> Player | None:
        return self.__players[self.__active_player_id] if self.__active_player_id is not None else None

    @property
    def status(self) -> str:
        if self.__is_started:
            if self.__is_win:
                return f"{self.active_player.name} is winner!"
            elif self.__is_draw:
                return "Draw!"
            return f"{self.active_player.name}'s turn"
        return "Game isn't started"


if __name__ == "__main__":
    while True:
        game = Game()
        game.start()
        if input("Restart? (yes/no): ").lower() in ('y', 'yes'):
            print()
        else:
            break
