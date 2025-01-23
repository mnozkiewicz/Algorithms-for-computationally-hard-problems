import pulp

def main(cat="Continuous") -> None:
    model = pulp.LpProblem("test", pulp.LpMinimize)

    x = pulp.LpVariable("x" , cat=cat)
    y = pulp.LpVariable("y" , cat=cat)

    model += x + y
    model += y >= x - 1
    model += y >= (-4)*x + 4
    model += y <= -0.5*x + 3

    print(model)

    model.solve()       
    print(pulp.LpStatus[model.status] ) 
    print(x.value(), y.value())

    
if __name__ == '__main__':
    main()