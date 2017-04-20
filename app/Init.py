def list_of_cases(test_case):
    test_1=["Test1","P1","P2"]
    test_2=["Test2","P1","P2"]
    test_3=["Test3","P1","P2"]
    test_4=["Test4","P1","P2"]
    
    if test_case=="test1":
        return test_1
    
    elif test_case=="test2":
        return test_2
        
    elif test_case=="test3":
        return test_3
        
    elif test_case=="test4":
        return test_4
        
    else:
        print("You have entered an invalid test case.")
        main()

def test_run(test_case):
    test_details=list_of_cases(test_case)
    print(test_details[0],test_details[1],test_details[2])



def main():
    test_case=str(input("What test would you like to run? (Input as test1 - test2 etc.)"))
    test_run(test_case)
    
main()