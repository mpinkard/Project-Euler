class HT(object):

    def __init__(self, length=4):
        self.__array__ = [None] * length

    def getItem(self, key):
        length = len(self.__array__)
        index = hash(key) % length
        bucket = self.__array__[index]
        if bucket:
            for k, v in bucket:
                if k == key:
                    return v
        raise KeyError('No element with key: ' + key)


    def __getitem__(self, key):
        return self.getItem(key)


    def addItem(self, key, value):
        length = len(self.__array__)
        index = hash(key) % length
        bucket = self.__array__[index]
        if not bucket:
            self.__array__[index] = [(key, value)]
        else:
            for i in range(len(bucket)):
                if bucket[i][0] == key:
                    bucket[i] = (key, value)
                    break
            else:
                bucket.append((key, value))
        if self.isFull():
            self.double()


    def __setitem__(self, key, value):
        self.addItem(key, value)

    def removeItem(self, key):
        index = hash(key) % len(self.__array__)
        bucket = self.__array__[index]
        if bucket:
            for i in range(len(bucket)):
                if bucket[i][0] == key:
                    del bucket[i]

    def __contains__(self, key):
        index = hash(key) % len(self.__array__)
        bucket = self.__array__[index]
        if not bucket:
            return False
        else:
            for k, _ in bucket:
                if k == key:
                    return True
        return False

    def __iter__(self):
        for bucket in self.__array__:
            if bucket:
                for item in bucket:
                    yield item

    def isFull(self):
        """Two conditions:
            1) If more than half of the indexes are filled OR
            2) If one index has more than length/2 items
        """
        count_full_indices = len(list([i for i in self.__array__ if i is not None]))
        table_length = len(self.__array__)
        if count_full_indices > table_length/2:
            return True
        for bucket in self.__array__:
            if bucket and len(bucket) > table_length / 2:
                return True
        return False

    def double(self):
        new_table = HT(length = len(self.__array__)*2)
        # Re-hash all of the items in the table
        for bucket in self.__array__:
            if bucket:
                for k, v in bucket:
                    new_table[k] = v
        
        self.__array__ = new_table.__array__
