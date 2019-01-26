### [chinese_text_vs_arabic_numerals](chinese_text_vs_arabic_numerals.py)
<br>中文和阿拉伯数字互相转化
```text
>>> from chinese_text_vs_arabic_numerals import *
>>> num = '01234567890.0123456'
>>> text = num2text(num)
>>> text
'一十二亿三千四百五十六万七千八百九十点零一二三四五六'
>>> text2num(text)
'1234567890.0123456'
```
### [generate_maze](generate_maze.py)
<br> 迷宫生成算法

refer to [generate_maze](generate_maze/README.md) to read more

### [grab_red_envelopes](grab_red_envelopes.py)
<br>微信抢红包算法
```text
>>> from grab_red_envelopes import *
>>> solve(100, 5)
[37.32, 1.41, 10.89, 12.75, 37.63]
```
### [leveling_chemical_equation](leveling_chemical_equation.py)
<br>化学方程式配平
```text
>>> from leveling_chemical_equation import *
>>> left, right = ('CH2OH(CHOH)4CHO', 'Ag(NH3)2OH'), ('CH2OH(CHOH)4COONH4', 'Ag', 'NH3', 'H2O')
>>> left_solve, right_solve = level(left, right)
>>> left_solve
array([1, 2])
>>> right_solve
array([1, 2, 3, 1])
>>> get_text(left, right, left_solve, right_solve)
'1CH2OH(CHOH)4CHO + 2Ag(NH3)2OH = 1CH2OH(CHOH)4COONH4 + 2Ag + 3NH3 + 1H2O'
```
### [magic_square](magic_square.py)
<br>求解幻方，有暴力破解求解和巧妙求解两种方案
```text
>>> from magic_square import *
>>> n = 3
>>> solve(list(range(1, n * n + 1)), n)
array([[2, 7, 6],
       [9, 5, 1],
       [4, 3, 8]])
```
### [sudoku](sudoku.py)
<br>数独生成和求解
```text
>>> from sudoku import *
>>> np.random.seed(0)
>>> answer, problem = generate_sudoku()
>>> answer
array([[8, 3, 2, 5, 9, 7, 4, 1, 6],
       [4, 7, 5, 1, 6, 8, 9, 2, 3],
       [6, 1, 9, 4, 2, 3, 5, 7, 8],
       [9, 4, 1, 3, 8, 6, 7, 5, 2],
       [7, 6, 8, 2, 5, 1, 3, 4, 9],
       [2, 5, 3, 9, 7, 4, 6, 8, 1],
       [3, 9, 7, 8, 1, 5, 2, 6, 4],
       [5, 8, 4, 6, 3, 2, 1, 9, 7],
       [1, 2, 6, 7, 4, 9, 8, 3, 5]])
>>> problem
array([[0, 3, 0, 0, 0, 0, 0, 1, 0],
       [0, 0, 5, 0, 6, 0, 9, 0, 3],
       [6, 1, 0, 0, 0, 0, 0, 0, 0],
       [0, 4, 1, 0, 8, 0, 7, 5, 0],
       [7, 0, 8, 0, 0, 1, 0, 4, 0],
       [2, 0, 3, 9, 0, 4, 6, 8, 0],
       [3, 0, 7, 8, 0, 5, 0, 6, 4],
       [5, 8, 4, 6, 3, 2, 0, 9, 0],
       [0, 2, 0, 7, 0, 0, 0, 3, 5]])
>>> solution = solve(problem)
>>> solution
array([[8, 3, 2, 4, 9, 7, 5, 1, 6],
       [4, 7, 5, 1, 6, 8, 9, 2, 3],
       [6, 1, 9, 2, 5, 3, 4, 7, 8],
       [9, 4, 1, 3, 8, 6, 7, 5, 2],
       [7, 6, 8, 5, 2, 1, 3, 4, 9],
       [2, 5, 3, 9, 7, 4, 6, 8, 1],
       [3, 9, 7, 8, 1, 5, 2, 6, 4],
       [5, 8, 4, 6, 3, 2, 1, 9, 7],
       [1, 2, 6, 7, 4, 9, 8, 3, 5]])
>>> check_solution(solution)
True
>>> np.all(answer == solution)
False
```
