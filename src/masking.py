
class Masking:
    def __init__(self, matrix, size, reserved):
        self.matrix = matrix
        self.size = size 
        self.reserved = reserved
        
    def mask_condition(self, row, col, mask_pattern:int):
        match mask_pattern:
            case 0: return (row+col)%2 == 0
            case 1: return row%2 == 0
            case 2: return col%3 == 0
            case 3: return (row+col)%3 == 0
            case 4: return (row//2 + col//3)%2 == 0
            case 5: return (row*col)%2 + (row*col)%3 == 0
            case 6: return ((row*col)%2 + (row*col)%3)%2 == 0
            case 7: return ((row*col)%3 + (row+col)%2)%2 == 0
            case _: return False

    def apply_mask(self, mask_pattern:int):
        for r in range(self.size):
            for c in range(self.size):
                if not self.reserved[r, c]:
                    if self.mask_condition(r, c, mask_pattern):
                        self.matrix[r, c] ^=1
                        
    def calculate_total_penalty(self):
        def penalty_case_1():
            penalty = 0

            for row in self.matrix:
                current_color = row[0]
                current_streak = 1
                
                for c in range(1, self.size):
                    if row[c] == current_color:
                        current_streak += 1
                    else: 
                        if current_streak >= 5:
                            penalty += 3 + (current_streak - 5)
                        current_streak = 1
                        current_color = row[c]
                if current_streak >= 5:
                    penalty += 3 + (current_streak - 5)

            for c in range(self.size):
                current_color = self.matrix[0][c]
                current_streak = 1  
                
                for r in range(1, self.size):
                    if self.matrix[r][c] == current_color:
                        current_streak += 1
                    else: 
                        if current_streak >= 5:
                            penalty += 3 + (current_streak - 5)
                        current_streak = 1
                        current_color = self.matrix[r][c]
                
                if current_streak >= 5:
                    penalty += 3 + (current_streak - 5)

            return penalty

        def penalty_case_2():
            penalty = 0
            for r in range(self.size - 1):
                for c in range(self.size - 1):
                    if self.matrix[r][c] == self.matrix[r][c+1] == self.matrix[r+1][c] == self.matrix[r+1][c+1]:
                        penalty += 3
            return penalty

        def penalty_case_3():
            pattern1 = [1, 0, 1, 1, 1, 0, 1, 0, 0, 0, 0] 
            pattern2 = [0, 0, 0, 0, 1, 0, 1, 1, 1, 0, 1]

            penalty = 0

            def count_pattern_occurrences(sequence, pattern):
                count = 0
                for i in range(len(sequence) - len(pattern) + 1):
                    if all(sequence[i+j] == pattern[j] for j in range(len(pattern))):
                        count += 1
                return count

            for row in self.matrix:
                penalty += count_pattern_occurrences(row, pattern1) * 40
                penalty += count_pattern_occurrences(row, pattern2) * 40

            for c in range(self.size):
                column = [self.matrix[r][c] for r in range(self.size)]
                penalty += count_pattern_occurrences(column, pattern1) * 40
                penalty += count_pattern_occurrences(column, pattern2) * 40

            return penalty

        def penalty_case_4():
            total_modules = self.size * self.size
        
            dark_modules = 0
            for row in self.matrix:
                for cell in row:
                    if cell == 1:
                        dark_modules += 1
        
            percent_dark = (dark_modules / total_modules) * 100
        
            deviation = abs(percent_dark - 50)
            steps = int(deviation / 5)
        
            return steps * 10
        total_penalty = penalty_case_1() + penalty_case_2() + penalty_case_3() + penalty_case_4()
        return total_penalty
    def evaluate_mask(self):
        best_mask = 0
        lowest_penalty = float('inf')
        
        for mask in range(8):
            self.apply_mask(mask)
            
            penalty = self.calculate_total_penalty()
            
            if penalty < lowest_penalty:
                lowest_penalty = penalty
                best_mask = mask
                
            self.apply_mask(mask)

        return best_mask
