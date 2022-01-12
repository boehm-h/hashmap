# Name: Hannah Boehm
# OSU Email: boehmha@oregonstate.edu
# Description: HashMap Implementation


# Import pre-written DynamicArray and LinkedList classes
from a7_include import *


def hash_function_1(key: str) -> int:
    """
    Sample Hash function #1 to be used with A5 HashMap implementation
    DO NOT CHANGE THIS FUNCTION IN ANY WAY
    """
    hash = 0
    for letter in key:
        hash += ord(letter)
    return hash


def hash_function_2(key: str) -> int:
    """
    Sample Hash function #2 to be used with A5 HashMap implementation
    DO NOT CHANGE THIS FUNCTION IN ANY WAY
    """
    hash, index = 0, 0
    index = 0
    for letter in key:
        hash += (index + 1) * ord(letter)
        index += 1
    return hash


class HashMap:
    def __init__(self, capacity: int, function) -> None:
        """
        Init new HashMap based on DA with SLL for collision resolution
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self.buckets = DynamicArray()
        for _ in range(capacity):
            self.buckets.append(LinkedList())
        self.capacity = capacity
        self.hash_function = function
        self.size = 0

    def __str__(self) -> str:
        """
        Return content of hash map t in human-readable form
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        out = ''
        for i in range(self.buckets.length()):
            list = self.buckets.get_at_index(i)
            out += str(i) + ': ' + str(list) + '\n'
        return out

    def clear(self) -> None:
        """
        Clears the contents of the hash map. Does not change the underlying
        hash table capacity.
        """
        for i in range(self.capacity):             # iterates through every bucket in the dynamic array,
            self.buckets[i] = LinkedList()         # and initializes a new linked list for each

        self.size = 0                              # adjust value of self.size

    def get(self, key: str) -> object:
        """
        Returns the value associated with the given key. If the key is not in the hash map,
        the method returns None.
        """
        hash = self.hash_function(key)             # compute index using hash function
        index = hash % self.capacity               # use modulo to ensure index exists

        bucket = self.buckets[index]               # get individual bucket at this index (in dynamic array)

        if bucket.contains(key) is None:           # use contains() method for linked list to check if key exists
            return None                            # if so, return value. if not, return None
        else:
            return bucket.contains(key).value

    def put(self, key: str, value: object) -> None:
        """
        Updates the key / value pair in the hash map. If a given key already exists,
        its associated value will be replaced with the new value. If a given key does
        not exist, a key / value pair will be added.
        """
        hash = self.hash_function(key)             # compute index using hash function
        index = hash % self.capacity               # use modulo to ensure index exists

        bucket = self.buckets[index]               # get individual bucket at this index (in dynamic array)

        if bucket.contains(key) is not None:       # use contains() method for the linked list to check if key exists
            if bucket.contains(key) == value:      # if the value matches the given value, end here
                return
            else:
                bucket.remove(key)                 # otherwise, remove the existing key/value pair
                bucket.insert(key, value)          # add the updated key/value pair

        else:                                      # if the key does not yet exist
            bucket.insert(key, value)              # use insert() method for linked list to insert given key/value pair
            self.size += 1                         # increment size

    def remove(self, key: str) -> None:
        """
        Removes given key and its associated value from the hash map. If given key is not
        in the hash map, the method does nothing.
        """
        for i in range(self.capacity):               # iterate through the underlying dynamic array
            bucket = self.buckets[i]                 # get individual bucket at each index (in dynamic array)
            if bucket.contains(key) is not None:     # if the bucket contains the given key
                bucket.remove(key)                   # remove the key/value pair
                self.size -= 1                       # decrement size

    def contains_key(self, key: str) -> bool:
        """
        Returns True if the given key is in the hash map, otherwise it returns False.
        An empty hash map does not contain any keys.
        """
        for i in range(self.capacity):               # iterate through the underlying dynamic array
            bucket = self.buckets[i]                 # get individual bucket at each index (in dynamic array)
            if bucket.contains(key) is not None:     # if bucket contains given key, return True. else, return False
                return True

        return False

    def empty_buckets(self) -> int:
        """
        Returns the number of empty buckets in the hash table.
        """
        count = 0                              # initialize count to zero

        for i in range(self.capacity):         # check each bucket in the underlying dynamic array
            bucket = self.buckets[i]           # if the length of a linked list is zero, the bucket is empty
            if bucket.length() == 0:
                count += 1                     # increment count

        return count

    def table_load(self) -> float:
        """
        Returns the current hash table load factor.
        """
        load_factor = self.size / self.capacity    # 𝝺 (load factor) = n (number of elements) / m (number of buckets)
        return load_factor

    def resize_table(self, new_capacity: int) -> None:
        """
        Changes the capacity of the hash table. All existing key / value pairs will remain
        in the new hash map, and all hash table links will be rehashed. If new_capacity is
        less than 1, this method will do nothing.
        """
        if new_capacity < 1:
            return

        new_hash_table = HashMap(new_capacity, self.hash_function)   # initialize new hash table with the new capacity
                                                                     # and the same hash function
        for i in range(self.capacity):
            bucket = self.buckets[i]                                 # iterate through every node in every bucket
            for node in bucket:                                      # if the node.key is not None, use put() method
                if node.key is not None:                             # to insert key/value pair into new hash table
                    new_hash_table.put(node.key, node.value)

        self.buckets = new_hash_table.buckets                    # assign the new dynamic array to the current hash map
        self.capacity = new_capacity                             # update the current hash map's capacity

    def get_keys(self) -> DynamicArray:
        """
        Returns a DynamicArray that contains all keys stored in your hash map.
        The order of the keys in the DA does not matter.
        """
        keys_array = DynamicArray()                # initialize new dynamic array for the keys

        for i in range(self.capacity):             # iterate through every node in every bucket
            bucket = self.buckets[i]               # add all existing keys to keys_array
            for node in bucket:
                keys_array.append(node.key)

        return keys_array


# BASIC TESTING

if __name__ == "__main__":

    print("\nPDF - table_load example 1")
    print("--------------------------")
    m = HashMap(100, hash_function_1)
    print(m.table_load())
    m.put('key1', 10)
    print(m.table_load())
    m.put('key2', 20)
    print(m.table_load())
    m.put('key1', 30)
    print(m.table_load())

    print("\nPDF - table_load example 2")
    print("--------------------------")
    m = HashMap(50, hash_function_1)
    for i in range(50):
        m.put('key' + str(i), i * 100)
        if i % 10 == 0:
            print(m.table_load(), m.size, m.capacity)

    print("\nPDF - put example 1")
    print("-------------------")
    m = HashMap(50, hash_function_1)
    for i in range(150):
        m.put('str' + str(i), i * 100)
        if i % 25 == 24:
            print(m.empty_buckets(), m.table_load(), m.size, m.capacity)

    print("\nPDF - put example 2")
    print("-------------------")
    m = HashMap(40, hash_function_2)
    for i in range(50):
        m.put('str' + str(i // 3), i * 100)
        if i % 10 == 9:
            print(m.empty_buckets(), m.table_load(), m.size, m.capacity)
