#Sudoku Solver
#48     91     4  3 52 9  8   1 5 3 85   7    7  81 4  2           5  9    3    2  
import pandas as pd
import numpy as np

#str = input("please input your sudoku array, right to left, top to bottom with a space representing a blank space on the board \n")
str = " 7219 4 6369 7        8 972  3  1 945 69   8 9  82   5 31  87  29   3 5    6 982  "
endArr = []
tempArr = []
counter = 0
for char in str:
    if counter % 9 == 0:
        endArr.append(tempArr)
        tempArr = []
    tempArr.append(char)
    counter+=1



def checkRow(row, num): # returns true if num is not in row
    for spot in endArr[row]:
        if spot == f'{num}':
            return False
    return True

def checkCol(col, num): # returns true if num is not in col
    for i in range(len(endArr)):
        if endArr[i][col] == f'{num}':
            return False
    
    return True

def checkBox(row, col, num):
    if row < 3:
        if col < 3:
            for i in range(3):
                for j in range(3):
                    if endArr[i][j] == f'{num}':
                        return False
        elif col < 6:
            for i in range(3):
                for j in range(3,6):
                    if endArr[i][j] == f'{num}':
                        return False
        else: 
            for i in range(3):
                for j in range(6,9):
                    if endArr[i][j] == f'{num}':
                        return False
    elif row < 6:
        if col < 3:
            for i in range(3, 6):
                for j in range(3):
                    if endArr[i][j] == f'{num}':
                        return False
        elif col < 6:
            for i in range(3, 6):
                for j in range(3,6):
                    if endArr[i][j] == f'{num}':
                        return False
        else: 
            for i in range(3, 6):
                for j in range(6,9):
                    if endArr[i][j] == f'{num}':
                        return False
    
    else:
        if col < 3:
            for i in range(6, 9):
                for j in range(3):
                    if endArr[i][j] == f'{num}':
                        return False
        elif col < 6:
            for i in range(6, 9):
                for j in range(3,6):
                    if endArr[i][j] == f'{num}':
                        return False
        else: 
            for i in range(6, 9):
                for j in range(6,9):
                    if endArr[i][j] == f'{num}':
                        return False
    return True

def buildPossibleSolutionsArr():
    posArr = []
    temp = []
    for row, arr in enumerate(endArr):
        for col, spot in enumerate(arr):
            temp = []
            if spot == " ":
                for i in range(1,10):
                    if((checkRow(row, i) == True) and (checkCol(col, i) == True) and (checkBox(row, col, i) == True)):
                        temp.append(i)
            posArr.append(temp)
    return posArr


def restrictPossibleSolutionsArr(arrCurrent):
    posArr = arrCurrent
    finalRowArr = []
    finalArr = []
    colPoss = []
    rowPoss = []
    rowChange = False
    addRow = []
    for spot, arrSpot in enumerate(posArr):
        rowIndex = spot//9
        colIndex = spot%9
        #colPoss = createColPoss(spot)
        rowPoss = createRowPoss(spot)
        if len(arrSpot) == 2:
            spot1 = arrSpot[0]
            spot2 = arrSpot[1]
            for o, r in enumerate(rowPoss):
                if len(r) == 2:
                    if r[0] == spot1 and r[1] == spot2 and o!= colIndex:
                        if rowChange == False:
                            addRow = eliminateFromArr(rowPoss, r[0], r[1], colIndex, o)
                            rowChange = True
        if spot%9 == 8:
            if rowChange == True:
                rowChange = False
                finalRowArr.append(addRow)
                addRow = []
            else:
                finalRowArr.append(rowPoss)
    colChange = False
    addCol = []
    for spot, arrSpot in enumerate(finalRowArr):
        rowIndex = spot//9
        colIndex = spot%9
        colPoss = createColPoss(spot)
        if len(arrSpot) == 2:
            spot1 = arrSpot[0]
            spot2 = arrSpot[1]
            for o, r in enumerate(colPoss):
                if len(r) == 2:
                    if r[0] == spot1 and r[1] == spot2 and o!= rowIndex:
                        if colChange == False:
                            addCol = eliminateFromArr(colPoss, r[0], r[1], rowIndex, o)
                            colChange = True
        if spot%9 == 8:
            if colChange == True:
                colChange = False
                finalArr.append(addCol)
                addCol = []
            else:
                finalArr.append(colPoss)

        return finalArr



def eliminateFromArr(arr, num1, num2, keep1, keep2):
    final = []
    for i, element in enumerate(arr):
        if i == keep1 or i == keep2:
            final.append(element)
        else:
            temp = []
            for e in element:
                if e == num1:
                    continue
                elif e == num2:
                    continue
                else:
                    temp.append(e)
            final.append(temp)
    return final

def createRowPoss(index):
    start_index = []
    if index < 9:
        start_index = 0
    else:
        start_index = (index//9)*9
    return newArr[start_index:start_index+9]

def createColPoss(index):
    super_col_arr = []
    for i, val in enumerate(newArr):
        if index%9 == i%9:
            super_col_arr.append(val)
    return super_col_arr



endArr.remove([])
newArr = buildPossibleSolutionsArr()
print(newArr)
print(len(newArr))
print("\n\n\n\n\n\n")
count = 40

print(endArr)
print("\n\n\n\n\n\n")


def solve():
    indices = []

    colArrs = []
    rowArrs = []
    boxArrs = []
    tempRow = []
    tempCol = []
    tempBox = []
    countah = 0

    #for element in newArr:
    #    if (countah % 9 == 0) and (countah != 0):
    #        rowArrs.append(tempRow)
    #        tempRow = []
    #    tempRow.append(element)
    #    countah+=1
    
    #for index, arr in enumerate(newArr):
    #    for i in range(9):
    #        if index % i == 0:
    go = True
    for index, arr in enumerate(newArr):
        if go == True:
            if len(arr) == 0:
                continue
            elif len(arr) == 1:
                del endArr[index//9][index%9]
                endArr[index//9].insert(index%9, f'{arr[0]}')
                indices.append(index)
                go = False
            else:
                if index < 9:
                    start_index = 0
                else:
                    start_index = (index//9)*9
                super_row_arr = newArr[start_index:start_index+9]
                #print("row arr")
                #print(super_row_arr)
                super_col_arr = []
                for i, val in enumerate(newArr):
                    if index%9 == i%9:
                        super_col_arr.append(val)
                #print("col arr")
                #print(super_col_arr)
                count_row = []
                count_col = []
                for i in range(1, 10):
                    count_rows = 0
                    count_cols = 0
                    for r in super_row_arr:
                        for row_val in r:
                            if row_val == i:
                                count_rows+=1
                    for c in super_col_arr:
                        for col_val in c:
                            if col_val == i:
                                count_cols+=1
                    count_row.append(count_rows)
                    count_col.append(count_cols)
                #print("col count")
                #print(count_col)
                #print("row count")
                #print(count_row)
                for number, val in enumerate(count_row):
                    if val == 1:
                        for spot_number, spot in enumerate(super_row_arr):
                            for place in spot:
                                if place == number+1:
                                    del endArr[index//9][spot_number]
                                    endArr[index//9].insert(spot_number, f'{number+1}')
                                    indices.append(index//9+spot_number)
                                    #print("row found number "+f'{(number+1)}'+" at "+f'{(index//9+1)}'+" , "+f'{(spot_number+1)}'+" also index is "+f'{(spot_number)}')
                                    go = False
                                    
                    elif count_col[number] == 1:
                        for spot_number, spot in enumerate(super_col_arr):
                            for place in spot:
                                if place == number+1:
                                    del endArr[spot_number][index%9]
                                    endArr[spot_number].insert(index%9, f'{number+1}')
                                    indices.append(index)
                                    #print("col found number "+f'{(number+1)}'+" at "+f'{(spot_number+1)}'+" , "+f'{(index%9+1)}'+" also index is "+f'{(index%9)}')
                                    go = False
                                    

        
        for remIndex in indices:
            del newArr[remIndex]
            newArr.insert(remIndex, [])


while count > 0:
    count -= 1
    solve()
    newArr = buildPossibleSolutionsArr()
    newArr = restrictPossibleSolutionsArr(newArr)

print(endArr)
print("\n\n\n\n\n\n")
print(newArr)
                