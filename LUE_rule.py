from utils import Point
from LUE_rule_utils import *

class LUERule:
    def __init__(self, dx, dy, max_rad, id_gen=None, is_horizontal=None):
        self.dx = dx
        self.dy = dy
        self.max_rad = max_rad
        self.is_horizontal = is_horizontal

        self.start_LUE_id = None
        self.end_LUE_id = None

        if id_gen is not None:
            self.start_LUE_id = id_gen.generate_id()
            self.end_LUE_id = id_gen.generate_id()

    def __str__(self):
        return "dx=" + str(self.dx) + ", dy=" + str(self.dy) + ", max_rad="\
               + str(self.max_rad) + "," + str(self.start_LUE_id)\
               + "-------->"+ str(self.end_LUE_id)

    def apply_to_binary_map(self, binary_map):
        # собираем все единицы в список и из каждой пытаемся
        # вырастить образец последовательсноти по этому правилу,
        # рассмотренные единицы удаляем из списка,
        # процесс завершаем, когда все единицы рассмотрены.
        min_len = 3
        found_seqs = []
        points_to_process = get_all_1_points(binary_map)
        while True:
            if len(points_to_process)<min_len:
                break
            point = points_to_process[-1]
            seq = try_qrow_seq_of_points_with_u(point, binary_map, Point(self.dx, self.dy), self.max_rad)
            remove_points_from_list(points_to_process, seq)
            if len(seq)>=min_len:
                found_seqs.append(seq)

        return remove_dubles(found_seqs)