import sys

# str
str1 = str()
str2 = "1"
str3 = "12"
 
print("Memoria de str1: " + str(sys.getsizeof(str1)) + " bytes " + str(type(str1)))
print("Memoria de str2: " + str(sys.getsizeof(str2)) + " bytes " + str(type(str2)))
print("Memoria de str3: " + str(sys.getsizeof(str3)) + " bytes " + str(type(str3)))

# int
int1 =0
int2 =1
int3 =2

print("Memoria de int1: " + str(sys.getsizeof(int1)) + " bytes " + str(type(int1)))
print("Memoria de int2: " + str(sys.getsizeof(int2)) + " bytes " + str(type(int2)))
print("Memoria de int3: " + str(sys.getsizeof(int3)) + " bytes " + str(type(int3)))

# float
float1 =0.0
float2 =1.01
float3 =2.0123

print("Memoria de float1: " + str(sys.getsizeof(float1)) + " bytes " + str(type(float1)))
print("Memoria de float2: " + str(sys.getsizeof(float2)) + " bytes " + str(type(float2)))
print("Memoria de float3: " + str(sys.getsizeof(float3)) + " bytes " + str(type(float3)))

# complex

complex1=complex()
complex2=complex(1j)
complex3=complex(2j)

print("Memoria de complex1: " +str(sys.getsizeof(complex1)) + " bytes " +str(type(complex1)))
print("Memoria de complex2: " +str(sys.getsizeof(complex2)) + " bytes " +str(type(complex2)))
print("Memoria de complex3: " +str(sys.getsizeof(complex3)) + " bytes " +str(type(complex3)))

# list

list1=[]
list2=[1]
list3=[1,2]

print("Memoria de list1: " +str(sys.getsizeof(list1)) + " bytes " +str(type(list1)))
print("Memoria de list2: " +str(sys.getsizeof(list2)) + " bytes " +str(type(list2)))
print("Memoria de list3: " +str(sys.getsizeof(list3)) + " bytes " +str(type(list3)))

# tuple

tuple1=()
tuple2=tuple("1")
tuple3=(1,2)

print("Memoria de tuple1: " +str(sys.getsizeof(tuple1)) + " bytes " +str(type(tuple1)))
print("Memoria de tuple2: " +str(sys.getsizeof(tuple2)) + " bytes " +str(type(tuple2)))
print("Memoria de tuple3: " +str(sys.getsizeof(tuple3)) + " bytes " +str(type(tuple3)))

# range

range1=range(0)
range2=range(1)
range3=range(10)

print("Memoria de range1: " +str(sys.getsizeof(range1)) + " bytes " +str(type(range1)))
print("Memoria de range2: " +str(sys.getsizeof(range2)) + " bytes " +str(type(range2)))
print("Memoria de range3: " +str(sys.getsizeof(range3)) + " bytes " +str(type(range3)))

# dict

dict1={}
dict2={"1":1}
dict3={"1":1,2:2}

print("Memoria de dict1: " +str(sys.getsizeof(dict1)) + " bytes " +str(type(dict1)))
print("Memoria de dict2: " +str(sys.getsizeof(dict2)) + " bytes " +str(type(dict2)))
print("Memoria de dict3: " +str(sys.getsizeof(dict3)) + " bytes " +str(type(dict3)))

# set

set1=set()
set2=set({1})
set3=set({1,2})

print("Memoria de set1: " +str(sys.getsizeof(set1)) + " bytes " +str(type(set1)))
print("Memoria de set2: " +str(sys.getsizeof(set2)) + " bytes " +str(type(set2)))
print("Memoria de set3: " +str(sys.getsizeof(set3)) + " bytes " +str(type(set3)))

# frozenset

frozenset1=frozenset()
frozenset2=frozenset({1})
frozenset3=frozenset({1,2})

print("Memoria de frozenset1: " +str(sys.getsizeof(frozenset1)) + " bytes " +str(type(frozenset1)))
print("Memoria de frozenset2: " +str(sys.getsizeof(frozenset2)) + " bytes " +str(type(frozenset2)))
print("Memoria de frozenset3: " +str(sys.getsizeof(frozenset3)) + " bytes " +str(type(frozenset3)))

# bool

true=True
false=False

print("Memoria de true: " +str(sys.getsizeof(true)) + " bytes " +str(type(true)))
print("Memoria de false: " +str(sys.getsizeof(false)) + " bytes " +str(type(false)))

# bytes

byte1=b""
byte2=b"1"
byte3=b"21"

print("Memoria de byte1: " +str(sys.getsizeof(byte1)) + " bytes " +str(type(byte1)))
print("Memoria de byte2: " +str(sys.getsizeof(byte2)) + " bytes " +str(type(byte2)))
print("Memoria de byte3: " +str(sys.getsizeof(byte3)) + " bytes " +str(type(byte3)))

# bytes

bytearray1=bytearray(0)
bytearray2=bytearray(1)
bytearray3=bytearray(2)

print("Memoria de bytearray1: " +str(sys.getsizeof(bytearray1)) + " bytes " +str(type(bytearray1)))
print("Memoria de bytearray2: " +str(sys.getsizeof(bytearray2)) + " bytes " +str(type(bytearray2)))
print("Memoria de bytearray3: " +str(sys.getsizeof(bytearray3)) + " bytes " +str(type(bytearray3)))

# memoryview

memoryview1=memoryview(bytes(0))
memoryview2=memoryview(bytes(1))
memoryview3=memoryview(bytes(2))

print("Memoria de memoryview1: " +str(sys.getsizeof(memoryview1)) + " bytes " +str(type(memoryview1)))
print("Memoria de memoryview2: " +str(sys.getsizeof(memoryview2)) + " bytes " +str(type(memoryview2)))
print("Memoria de memoryview3: " +str(sys.getsizeof(memoryview3)) + " bytes " +str(type(memoryview3)))