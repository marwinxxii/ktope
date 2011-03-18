def buildCircuits(lines):
    #dict because we need to store numbers of circuits
    circuits={}
    i=1
    for line in lines:
        #using set to avoid duplicate elements
        circuit=set()
        for element in line.split(','):
            el=int(element)
            circuit.add(el)
        #circuits[i]=circuit
        circuits[i]=list(circuit)
        i+=1
    return circuits

def buildComplexMatrix(circuits,elements):
    print(elements)
    matrix={}
    for elem in elements:
        matrix[elem]=[]
        for c in circuits:
            if elem in circuits[c]:
                matrix[elem].append(1)
            else:
                matrix[elem].append(0)
    return matrix

def buildConnMatrix(circuits,elements):
    print(elements)
    matrix={}
    for elem in elements:
        matrix[elem]=[]
        for el in elements:
            s=0
            if el!=elem:
                for cir in circuits:
                    if elem in circuits[cir] and el in circuits[cir]:
                        s+=1
            matrix[elem].append(s)
    return matrix

lines=[
    '5,4,3,2',
    '4,8,3'
   ]
circuits=buildCircuits(lines)
print(circuits)
elements=set()
for i in circuits:
    for el in circuits[i]:
        elements.add(el)
elements=list(elements)
elements.sort()
matrix1=buildComplexMatrix(circuits,elements)
temp=list(matrix1.keys())
temp.sort()
print(matrix1)
matrix2=buildConnMatrix(circuits,elements)
print(matrix2)
