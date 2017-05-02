class A:
    def __init__(self, qw):
        self.qw = qw
    def get(self):
        return self.qw
    def set(self,qw):
        self.qw =qw
if __name__ == '__main__':
    a=A(1)
    b=a
    b.set(2)
    print(a.get())
