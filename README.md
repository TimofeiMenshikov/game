Это игра-лабиринт, в которой черные пиксели - стена, белые - проход. Игрок может перемещаться по заранее сгенерированному лабиринту. 

Как расчитывается взаимодействие объекта со стенкой:
лабиринт делится на квадратные блоки, каждый блок биективно отображается в ячейку списка, выполняющего функцию двумерного массива. ПО координатам центра объекта определяется блок, в котором находится объект и выполняется функция проверки пересечения объекта с 9 блоками (3x3, центральный блок - тот, в котором находится центр объекта) 
