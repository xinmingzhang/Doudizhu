how to check a list is a pair chain?

sorry for my English, I want to check a list formate is like [2,2,3,3,4,4],[15,15,16,16,17,17,18,18,19,19] or not.
I can check the sigle chain,like [8,9,10,11,12,13], I just def a function, like

    def check_chain(my_list):

        if my_list == [my_list[0] + x for x in range(len(my_list))]:
            return True
        else:
            return False

    if __name__ == '__main__':
        a = [2,3,4,5,6,7,8,9]
        print(check_chain(a))

it works, so, how to def a function to check pair chain? or trio chain?
    
