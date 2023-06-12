class A:
    def __init__(self, beta):
        self.B = beta
        pass
    
    def signature(self):
        print("ditmemayA")


class B:
    def __init__(self):
        self.A = A(self)

    def signature(self):
        print("ditmemayB")
    

beta = B()
beta.A.signature()
beta.A.B.signature()